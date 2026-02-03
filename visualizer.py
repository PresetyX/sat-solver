"""SAT Solver Result Visualizer

Visualizes SAT solver results, assignment graphs, and decision trees.
"""

from typing import List, Dict, Optional
import sys


class SATVisualizer:
    """Visualizer for SAT solver results."""
    
    @staticmethod
    def print_result(satisfiable: bool, assignment: Optional[Dict[int, bool]], cnf: List[List[int]]):
        """Print formatted SAT result.
        
        Args:
            satisfiable: Whether formula is satisfiable
            assignment: Variable assignment (if satisfiable)
            cnf: Original CNF formula
        """
        from cnf_parser import CNFParser
        
        print("\n" + "="*60)
        print("SAT SOLVER RESULT")
        print("="*60)
        
        print(f"\nFormula: {CNFParser.to_readable(cnf)}")
        print(f"Clauses: {len(cnf)}")
        
        if satisfiable:
            print("\n✓ SATISFIABLE")
            print("\nSatisfying Assignment:")
            
            if assignment:
                sorted_vars = sorted(assignment.keys())
                for var in sorted_vars:
                    value = assignment[var]
                    symbol = "✓" if value else "✗"
                    print(f"  x{var} = {value} {symbol}")
                
                # Verify assignment
                print("\nVerification:")
                SATVisualizer._verify_assignment(cnf, assignment)
        else:
            print("\n✗ UNSATISFIABLE")
            print("\nNo satisfying assignment exists.")
        
        print("\n" + "="*60)
    
    @staticmethod
    def _verify_assignment(cnf: List[List[int]], assignment: Dict[int, bool]):
        """Verify that assignment satisfies the formula.
        
        Args:
            cnf: CNF formula
            assignment: Variable assignment
        """
        all_satisfied = True
        
        for i, clause in enumerate(cnf):
            clause_satisfied = False
            satisfied_by = []
            
            for literal in clause:
                var = abs(literal)
                expected_value = literal > 0
                
                if var in assignment and assignment[var] == expected_value:
                    clause_satisfied = True
                    satisfied_by.append(f"x{var}={assignment[var]}")
            
            status = "✓" if clause_satisfied else "✗"
            
            if clause_satisfied:
                print(f"  Clause {i+1}: {status} (satisfied by {', '.join(satisfied_by)})")
            else:
                print(f"  Clause {i+1}: {status} NOT SATISFIED")
                all_satisfied = False
        
        if all_satisfied:
            print("\n  ✓ All clauses satisfied!")
        else:
            print("\n  ✗ Some clauses not satisfied (assignment may be incomplete)")
    
    @staticmethod
    def print_statistics(stats: Dict[str, int]):
        """Print solver statistics.
        
        Args:
            stats: Statistics dictionary from solver
        """
        print("\n" + "="*60)
        print("SOLVER STATISTICS")
        print("="*60)
        
        print(f"\nVariables: {stats.get('variables', 0)}")
        print(f"Clauses: {stats.get('clauses', 0)}")
        print(f"\nTotal Decisions: {stats.get('total_decisions', 0)}")
        print(f"  • Unit Propagations: {stats.get('unit_propagations', 0)}")
        print(f"  • Pure Literals: {stats.get('pure_literals', 0)}")
        print(f"  • Branches: {stats.get('branches', 0)}")
        print(f"  • Backtracks: {stats.get('backtracks', 0)}")
        
        print("\n" + "="*60)
    
    @staticmethod
    def create_assignment_table(assignment: Dict[int, bool]) -> str:
        """Create ASCII table of variable assignments.
        
        Args:
            assignment: Variable assignment
            
        Returns:
            ASCII table string
        """
        if not assignment:
            return "No assignment"
        
        sorted_vars = sorted(assignment.keys())
        
        # Calculate table dimensions
        vars_per_row = 10
        rows = [sorted_vars[i:i+vars_per_row] for i in range(0, len(sorted_vars), vars_per_row)]
        
        table = "\n┌" + "─"*59 + "┐\n"
        table += "│" + " "*18 + "VARIABLE ASSIGNMENT" + " "*22 + "│\n"
        table += "├" + "─"*59 + "┤\n"
        
        for row in rows:
            # Variable numbers
            var_line = "│ "
            for var in row:
                var_line += f"x{var:2d} "
            var_line += " "*(57 - len(var_line) + 1) + "│\n"
            table += var_line
            
            # Values
            val_line = "│ "
            for var in row:
                value = "T" if assignment[var] else "F"
                val_line += f" {value}  "
            val_line += " "*(57 - len(val_line) + 1) + "│\n"
            table += val_line
            
            if row != rows[-1]:
                table += "├" + "─"*59 + "┤\n"
        
        table += "└" + "─"*59 + "┘\n"
        
        return table
    
    @staticmethod
    def export_to_file(filename: str, cnf: List[List[int]], satisfiable: bool, assignment: Optional[Dict[int, bool]], stats: Dict[str, int]):
        """Export results to file.
        
        Args:
            filename: Output filename
            cnf: CNF formula
            satisfiable: Whether satisfiable
            assignment: Variable assignment
            stats: Solver statistics
        """
        from cnf_parser import CNFParser
        
        with open(filename, 'w') as f:
            f.write("SAT SOLVER RESULT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Formula: {CNFParser.to_readable(cnf)}\n")
            f.write(f"Clauses: {len(cnf)}\n\n")
            
            if satisfiable:
                f.write("Result: SATISFIABLE\n\n")
                
                if assignment:
                    f.write("Assignment:\n")
                    for var in sorted(assignment.keys()):
                        f.write(f"  x{var} = {assignment[var]}\n")
            else:
                f.write("Result: UNSATISFIABLE\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("STATISTICS\n")
            f.write("=" * 60 + "\n\n")
            
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
        
        print(f"\nResults exported to: {filename}")


class ProgressBar:
    """Simple progress bar for batch processing."""
    
    def __init__(self, total: int, width: int = 50):
        """Initialize progress bar.
        
        Args:
            total: Total number of items
            width: Width of progress bar in characters
        """
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, amount: int = 1):
        """Update progress.
        
        Args:
            amount: Amount to increment
        """
        self.current += amount
        self._draw()
    
    def _draw(self):
        """Draw progress bar."""
        progress = self.current / self.total
        filled = int(self.width * progress)
        bar = "█" * filled + "░" * (self.width - filled)
        percent = progress * 100
        
        sys.stdout.write(f"\r[{}] {percent:.1f}% ({self.current}/{self.total})")
        sys.stdout.flush()
        
        if self.current >= self.total:
            sys.stdout.write("\n")
    
    def reset(self):
        """Reset progress bar."""
        self.current = 0


if __name__ == "__main__":
    from sat_solver import SATSolver
    
    print("SAT Visualizer Demo\n")
    
    # Example: Satisfiable formula
    cnf = [[1, 2], [-1, 3], [-2, -3]]
    
    solver = SATSolver(cnf)
    sat, assignment = solver.solve()
    stats = solver.get_statistics()
    
    SATVisualizer.print_result(sat, assignment, cnf)
    SATVisualizer.print_statistics(stats)
    
    if assignment:
        print(SATVisualizer.create_assignment_table(assignment))
