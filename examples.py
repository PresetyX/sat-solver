"""Example Usage of SAT Solver

Demonstrates various use cases and features of the SAT solver.
"""

from sat_solver import SATSolver, parse_dimacs, cnf_to_dimacs
from cnf_parser import CNFParser, CNFGenerator, CNFTransformer
from visualizer import SATVisualizer


def example_basic():
    """Basic SAT solver usage."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Define a simple CNF formula: (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)
    cnf = [[1, 2], [-1, 3], [-2, -3]]
    
    # Create solver and solve
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    
    # Display results
    SATVisualizer.print_result(sat, assignment, cnf)
    SATVisualizer.print_statistics(solver.get_statistics())


def example_unsatisfiable():
    """Example with unsatisfiable formula."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Unsatisfiable Formula")
    print("="*60)
    
    # Contradiction: (x1) ∧ (¬x1)
    cnf = [[1], [-1]]
    
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    
    SATVisualizer.print_result(sat, assignment, cnf)


def example_3sat():
    """Example with random 3-SAT instance."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Random 3-SAT Instance")
    print("="*60)
    
    # Generate random 3-SAT with 10 variables
    cnf = CNFGenerator.generate_3sat(10, ratio=4.2, seed=42)
    
    print(f"Generated 3-SAT formula:")
    print(f"Variables: 10")
    print(f"Clauses: {len(cnf)}")
    print(f"Clause-to-variable ratio: 4.2")
    
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    
    if sat:
        print("\n✓ SATISFIABLE")
        print(f"\nAssignment found with {len(assignment)} variables")
    else:
        print("\n✗ UNSATISFIABLE")
    
    SATVisualizer.print_statistics(solver.get_statistics())


def example_pigeon_hole():
    """Example with pigeon hole principle."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Pigeon Hole Principle")
    print("="*60)
    
    # 4 pigeons, 3 holes - impossible!
    n = 3
    cnf = CNFGenerator.generate_pigeon_hole(n)
    
    print(f"Pigeon Hole Problem:")
    print(f"Pigeons: {n+1}")
    print(f"Holes: {n}")
    print(f"Clauses generated: {len(cnf)}")
    print(f"\nThis should be UNSATISFIABLE (you can't fit {n+1} pigeons into {n} holes)")
    
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    
    SATVisualizer.print_result(sat, assignment, cnf)
    SATVisualizer.print_statistics(solver.get_statistics())


def example_dimacs():
    """Example with DIMACS format."""
    print("\n" + "="*60)
    print("EXAMPLE 5: DIMACS Format")
    print("="*60)
    
    # DIMACS format input
    dimacs_input = """c Example CNF formula in DIMACS format
    p cnf 4 4
    1 2 -3 0
    -1 3 0
    2 -3 4 0
    -2 -4 0
    """
    
    print("DIMACS Input:")
    print(dimacs_input)
    
    # Parse DIMACS
    cnf = parse_dimacs(dimacs_input)
    
    print("Parsed CNF:")
    print(CNFParser.to_readable(cnf))
    
    # Solve
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    
    SATVisualizer.print_result(sat, assignment, cnf)
    
    # Convert back to DIMACS
    if sat and assignment:
        print("\nDIMACS Output:")
        print(cnf_to_dimacs(cnf))


def example_real_world():
    """Example with real-world application."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Real-World Application - Sudoku Cell Constraint")
    print("="*60)
    
    # Simplified Sudoku constraint: a 2x2 grid where each cell has value 1 or 2
    # and each row/column must have both values
    
    # Variables: x_ij_v means cell (i,j) has value v
    # x_11_1 = 1, x_11_2 = 2, x_12_1 = 3, x_12_2 = 4, etc.
    
    cnf = []
    
    # Each cell must have at least one value
    cnf.append([1, 2])  # Cell (1,1)
    cnf.append([3, 4])  # Cell (1,2)
    cnf.append([5, 6])  # Cell (2,1)
    cnf.append([7, 8])  # Cell (2,2)
    
    # Each cell can't have both values
    cnf.append([-1, -2])
    cnf.append([-3, -4])
    cnf.append([-5, -6])
    cnf.append([-7, -8])
    
    # Row 1 must have both values
    cnf.append([1, 3])  # At least one cell has value 1
    cnf.append([2, 4])  # At least one cell has value 2
    
    # Row 2 must have both values
    cnf.append([5, 7])  # At least one cell has value 1
    cnf.append([6, 8])  # At least one cell has value 2
    
    # Column 1 must have both values
    cnf.append([1, 5])  # At least one cell has value 1
    cnf.append([2, 6])  # At least one cell has value 2
    
    # Column 2 must have both values
    cnf.append([3, 7])  # At least one cell has value 1
    cnf.append([4, 8])  # At least one cell has value 2
    
    print("2x2 Sudoku-like constraint:")
    print("- Each cell must have exactly one value (1 or 2)")
    print("- Each row must contain both values")
    print("- Each column must contain both values")
    
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    
    SATVisualizer.print_result(sat, assignment, cnf)
    
    if sat and assignment:
        print("\nDecoded Solution:")
        grid = [[0, 0], [0, 0]]
        
        # Decode assignment
        if assignment.get(1, False): grid[0][0] = 1
        elif assignment.get(2, False): grid[0][0] = 2
        
        if assignment.get(3, False): grid[0][1] = 1
        elif assignment.get(4, False): grid[0][1] = 2
        
        if assignment.get(5, False): grid[1][0] = 1
        elif assignment.get(6, False): grid[1][0] = 2
        
        if assignment.get(7, False): grid[1][1] = 1
        elif assignment.get(8, False): grid[1][1] = 2
        
        print("\n  ┌───┬───┐")
        print(f"  │ {grid[0][0]} │ {grid[0][1]} │")
        print("  ├───┼───┤")
        print(f"  │ {grid[1][0]} │ {grid[1][1]} │")
        print("  └───┴───┘")


def example_statistics():
    """Example analyzing solver statistics."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Solver Statistics Analysis")
    print("="*60)
    
    # Test multiple formulas of increasing difficulty
    test_cases = [
        ("Easy", [[1, 2], [-1, 3]]),
        ("Medium", CNFGenerator.generate_3sat(8, ratio=3.0, seed=42)),
        ("Hard", CNFGenerator.generate_3sat(12, ratio=4.3, seed=42)),
    ]
    
    print("\nComparing solver performance on different difficulties:\n")
    
    for name, cnf in test_cases:
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        stats = solver.get_statistics()
        
        print(f"{name:10s} | Vars: {stats['variables']:3d} | Clauses: {stats['clauses']:3d} | "
              f"Decisions: {stats['total_decisions']:4d} | Backtracks: {stats['backtracks']:3d} | "
              f"Result: {'SAT' if sat else 'UNSAT'}")


def main():
    """Run all examples."""
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + " "*15 + "SAT SOLVER EXAMPLES" + " "*24 + "#")
    print("#" + " "*58 + "#")
    print("#"*60)
    
    examples = [
        ("Basic Usage", example_basic),
        ("Unsatisfiable Formula", example_unsatisfiable),
        ("Random 3-SAT", example_3sat),
        ("Pigeon Hole Principle", example_pigeon_hole),
        ("DIMACS Format", example_dimacs),
        ("Real-World Application", example_real_world),
        ("Statistics Analysis", example_statistics),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
    
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + " "*18 + "EXAMPLES COMPLETE" + " "*23 + "#")
    print("#" + " "*58 + "#")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
