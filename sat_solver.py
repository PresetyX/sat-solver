"""SAT Solver using DPLL Algorithm

This module implements a complete Boolean Satisfiability (SAT) solver using
the Davis-Putnam-Logemann-Loveland (DPLL) algorithm with unit propagation
and pure literal elimination.
"""

from typing import List, Set, Dict, Optional, Tuple
from copy import deepcopy


class SATSolver:
    """Complete SAT Solver implementation using DPLL algorithm.
    
    The solver works with CNF (Conjunctive Normal Form) formulas represented as
    a list of clauses, where each clause is a list of literals (integers).
    Positive integers represent variables, negative integers represent negations.
    
    Example:
        CNF formula: (x1 OR NOT x2) AND (x2 OR x3) AND (NOT x1 OR NOT x3)
        Representation: [[1, -2], [2, 3], [-1, -3]]
    """
    
    def __init__(self, cnf: List[List[int]]):
        """Initialize the SAT Solver.
        
        Args:
            cnf: CNF formula as list of clauses (list of lists of integers)
        """
        self.original_cnf = cnf
        self.assignment: Dict[int, bool] = {}
        self.decisions: List[Tuple[int, bool, str]] = []  # (var, value, reason)
        
    def solve(self) -> Tuple[bool, Optional[Dict[int, bool]]]:
        """Solve the SAT problem.
        
        Returns:
            Tuple of (satisfiable: bool, assignment: Optional[Dict[int, bool]])
            If satisfiable, returns True and the satisfying assignment.
            If unsatisfiable, returns False and None.
        """
        result = self._dpll(deepcopy(self.original_cnf), {})
        
        if result:
            return True, self.assignment
        else:
            return False, None
    
    def _dpll(self, cnf: List[List[int]], assignment: Dict[int, bool]) -> bool:
        """DPLL algorithm implementation.
        
        Args:
            cnf: Current CNF formula
            assignment: Current variable assignment
            
        Returns:
            True if satisfiable, False otherwise
        """
        # Base case: empty formula is satisfiable
        if not cnf:
            self.assignment = assignment.copy()
            return True
        
        # Base case: empty clause means unsatisfiable
        if [] in cnf:
            return False
        
        # Unit propagation
        cnf, assignment = self._unit_propagation(cnf, assignment)
        
        if cnf is None:  # Conflict detected
            return False
        
        if not cnf:  # Formula satisfied
            self.assignment = assignment.copy()
            return True
        
        # Pure literal elimination
        cnf, assignment = self._pure_literal_elimination(cnf, assignment)
        
        if not cnf:  # Formula satisfied
            self.assignment = assignment.copy()
            return True
        
        # Choose a variable to branch on (first unassigned variable)
        var = self._choose_variable(cnf, assignment)
        
        if var is None:  # No variables left
            self.assignment = assignment.copy()
            return True
        
        # Try assigning True
        new_assignment = assignment.copy()
        new_assignment[var] = True
        new_cnf = self._simplify(cnf, var, True)
        
        self.decisions.append((var, True, "branch"))
        if self._dpll(new_cnf, new_assignment):
            return True
        
        # Backtrack: try assigning False
        new_assignment = assignment.copy()
        new_assignment[var] = False
        new_cnf = self._simplify(cnf, var, False)
        
        self.decisions.append((var, False, "backtrack"))
        if self._dpll(new_cnf, new_assignment):
            return True
        
        return False
    
    def _unit_propagation(self, cnf: List[List[int]], assignment: Dict[int, bool]) -> Tuple[Optional[List[List[int]]], Dict[int, bool]]:
        """Perform unit propagation.
        
        Unit propagation: if a clause has only one literal, that literal must be true.
        
        Args:
            cnf: Current CNF formula
            assignment: Current assignment
            
        Returns:
            Tuple of (simplified CNF, updated assignment) or (None, assignment) if conflict
        """
        changed = True
        
        while changed:
            changed = False
            
            for clause in cnf:
                if len(clause) == 1:  # Unit clause found
                    literal = clause[0]
                    var = abs(literal)
                    value = literal > 0
                    
                    # Check for conflict
                    if var in assignment and assignment[var] != value:
                        return None, assignment
                    
                    if var not in assignment:
                        assignment[var] = value
                        self.decisions.append((var, value, "unit_propagation"))
                        cnf = self._simplify(cnf, var, value)
                        changed = True
                        break
        
        return cnf, assignment
    
    def _pure_literal_elimination(self, cnf: List[List[int]], assignment: Dict[int, bool]) -> Tuple[List[List[int]], Dict[int, bool]]:
        """Eliminate pure literals.
        
        Pure literal: a variable that appears only in positive or only in negative form.
        
        Args:
            cnf: Current CNF formula
            assignment: Current assignment
            
        Returns:
            Tuple of (simplified CNF, updated assignment)
        """
        # Find all literals
        positive_vars = set()
        negative_vars = set()
        
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    positive_vars.add(literal)
                else:
                    negative_vars.add(-literal)
        
        # Find pure literals
        pure_positive = positive_vars - negative_vars
        pure_negative = negative_vars - positive_vars
        
        # Assign pure literals
        for var in pure_positive:
            if var not in assignment:
                assignment[var] = True
                self.decisions.append((var, True, "pure_literal"))
                cnf = self._simplify(cnf, var, True)
        
        for var in pure_negative:
            if var not in assignment:
                assignment[var] = False
                self.decisions.append((var, False, "pure_literal"))
                cnf = self._simplify(cnf, var, False)
        
        return cnf, assignment
    
    def _simplify(self, cnf: List[List[int]], var: int, value: bool) -> List[List[int]]:
        """Simplify CNF formula given a variable assignment.
        
        Args:
            cnf: Current CNF formula
            var: Variable to assign
            value: Value to assign (True/False)
            
        Returns:
            Simplified CNF formula
        """
        literal = var if value else -var
        new_cnf = []
        
        for clause in cnf:
            # If clause contains the literal, the clause is satisfied
            if literal in clause:
                continue
            
            # Remove negation of the literal from clause
            new_clause = [lit for lit in clause if lit != -literal]
            new_cnf.append(new_clause)
        
        return new_cnf
    
    def _choose_variable(self, cnf: List[List[int]], assignment: Dict[int, bool]) -> Optional[int]:
        """Choose next variable to assign.
        
        Uses a simple heuristic: pick the first unassigned variable.
        
        Args:
            cnf: Current CNF formula
            assignment: Current assignment
            
        Returns:
            Variable number or None if all assigned
        """
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if var not in assignment:
                    return var
        return None
    
    def get_statistics(self) -> Dict[str, int]:
        """Get solver statistics.
        
        Returns:
            Dictionary with solver statistics
        """
        unit_props = sum(1 for _, _, reason in self.decisions if reason == "unit_propagation")
        pure_lits = sum(1 for _, _, reason in self.decisions if reason == "pure_literal")
        branches = sum(1 for _, _, reason in self.decisions if reason == "branch")
        backtracks = sum(1 for _, _, reason in self.decisions if reason == "backtrack")
        
        return {
            "total_decisions": len(self.decisions),
            "unit_propagations": unit_props,
            "pure_literals": pure_lits,
            "branches": branches,
            "backtracks": backtracks,
            "clauses": len(self.original_cnf),
            "variables": len(self.assignment) if self.assignment else 0
        }


def parse_dimacs(dimacs_string: str) -> List[List[int]]:
    """Parse DIMACS CNF format.
    
    DIMACS format example:
        c This is a comment
        p cnf 3 2
        1 -2 0
        2 3 0
    
    Args:
        dimacs_string: String in DIMACS CNF format
        
    Returns:
        CNF formula as list of clauses
    """
    cnf = []
    
    for line in dimacs_string.strip().split('\n'):
        line = line.strip()
        
        # Skip comments and problem line
        if line.startswith('c') or line.startswith('p') or not line:
            continue
        
        # Parse clause
        literals = [int(x) for x in line.split()]
        
        # Remove trailing 0
        if literals and literals[-1] == 0:
            literals = literals[:-1]
        
        if literals:
            cnf.append(literals)
    
    return cnf


def cnf_to_dimacs(cnf: List[List[int]]) -> str:
    """Convert CNF formula to DIMACS format.
    
    Args:
        cnf: CNF formula as list of clauses
        
    Returns:
        String in DIMACS CNF format
    """
    if not cnf:
        return "p cnf 0 0\n"
    
    # Find number of variables
    variables = set()
    for clause in cnf:
        for literal in clause:
            variables.add(abs(literal))
    
    num_vars = max(variables) if variables else 0
    num_clauses = len(cnf)
    
    dimacs = f"p cnf {num_vars} {num_clauses}\n"
    
    for clause in cnf:
        dimacs += " ".join(str(lit) for lit in clause) + " 0\n"
    
    return dimacs


if __name__ == "__main__":
    # Example usage
    print("SAT Solver - DPLL Algorithm\n")
    
    # Example 1: Satisfiable formula
    # (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3)
    cnf1 = [[1, 2], [-1, 3], [-2, -3]]
    
    print("Example 1: (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)")
    solver1 = SATSolver(cnf1)
    sat, assignment = solver1.solve()
    
    if sat:
        print("✓ SATISFIABLE")
        print(f"Assignment: {assignment}")
    else:
        print("✗ UNSATISFIABLE")
    
    print(f"Statistics: {solver1.get_statistics()}\n")
    
    # Example 2: Unsatisfiable formula
    # (x1) AND (NOT x1)
    cnf2 = [[1], [-1]]
    
    print("Example 2: (x1) ∧ (¬x1)")
    solver2 = SATSolver(cnf2)
    sat, assignment = solver2.solve()
    
    if sat:
        print("✓ SATISFIABLE")
        print(f"Assignment: {assignment}")
    else:
        print("✗ UNSATISFIABLE")
    
    print(f"Statistics: {solver2.get_statistics()}")
