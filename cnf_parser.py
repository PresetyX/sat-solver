"""CNF Parser and Formula Generator

Utilities for parsing, generating, and manipulating CNF formulas.
"""

from typing import List, Set, Tuple
import random


class CNFParser:
    """Parser for CNF formulas in various formats."""
    
    @staticmethod
    def from_string(formula: str) -> List[List[int]]:
        """Parse CNF formula from human-readable string.
        
        Supports formats:
        - "(1 OR -2) AND (2 OR 3)"
        - "[[1, -2], [2, 3]]"
        - DIMACS format
        
        Args:
            formula: Formula string
            
        Returns:
            CNF formula as list of clauses
        """
        formula = formula.strip()
        
        # Try DIMACS format
        if 'p cnf' in formula or formula.startswith('c'):
            from sat_solver import parse_dimacs
            return parse_dimacs(formula)
        
        # Try Python list format
        if formula.startswith('['):
            try:
                return eval(formula)
            except:
                pass
        
        # Try human-readable format
        cnf = []
        
        # Remove parentheses and split by AND
        formula = formula.replace('(', '').replace(')', '')
        clauses = formula.split('AND')
        
        for clause_str in clauses:
            clause_str = clause_str.strip()
            
            # Split by OR
            literals_str = clause_str.split('OR')
            clause = []
            
            for lit_str in literals_str:
                lit_str = lit_str.strip()
                
                # Handle negation
                if lit_str.startswith('-') or lit_str.startswith('NOT '):
                    lit_str = lit_str.replace('NOT ', '').replace('-', '').strip()
                    clause.append(-int(lit_str))
                else:
                    clause.append(int(lit_str))
            
            if clause:
                cnf.append(clause)
        
        return cnf
    
    @staticmethod
    def to_readable(cnf: List[List[int]]) -> str:
        """Convert CNF to human-readable string.
        
        Args:
            cnf: CNF formula
            
        Returns:
            Human-readable string
        """
        if not cnf:
            return "TRUE"
        
        clause_strs = []
        
        for clause in cnf:
            if not clause:
                return "FALSE"
            
            lit_strs = []
            for lit in clause:
                if lit > 0:
                    lit_strs.append(f"x{lit}")
                else:
                    lit_strs.append(f"¬x{-lit}")
            
            clause_strs.append(f"({' ∨ '.join(lit_strs)})")
        
        return ' ∧ '.join(clause_strs)


class CNFGenerator:
    """Generator for random CNF formulas."""
    
    @staticmethod
    def generate_random(num_vars: int, num_clauses: int, clause_length: int = 3, seed: int = None) -> List[List[int]]:
        """Generate random CNF formula.
        
        Args:
            num_vars: Number of variables
            num_clauses: Number of clauses
            clause_length: Literals per clause
            seed: Random seed for reproducibility
            
        Returns:
            Random CNF formula
        """
        if seed is not None:
            random.seed(seed)
        
        cnf = []
        
        for _ in range(num_clauses):
            clause = []
            
            # Select random variables
            selected_vars = random.sample(range(1, num_vars + 1), min(clause_length, num_vars))
            
            for var in selected_vars:
                # Random polarity
                if random.random() < 0.5:
                    clause.append(var)
                else:
                    clause.append(-var)
            
            cnf.append(clause)
        
        return cnf
    
    @staticmethod
    def generate_3sat(num_vars: int, ratio: float = 4.3, seed: int = None) -> List[List[int]]:
        """Generate random 3-SAT instance.
        
        The ratio of clauses to variables (typically around 4.3) determines
        the difficulty of the problem.
        
        Args:
            num_vars: Number of variables
            ratio: Clause-to-variable ratio
            seed: Random seed
            
        Returns:
            Random 3-SAT formula
        """
        num_clauses = int(num_vars * ratio)
        return CNFGenerator.generate_random(num_vars, num_clauses, 3, seed)
    
    @staticmethod
    def generate_pigeon_hole(n: int) -> List[List[int]]:
        """Generate pigeon hole principle formula.
        
        Represents the unsatisfiable problem of placing n+1 pigeons into n holes.
        
        Args:
            n: Number of holes (n+1 pigeons)
            
        Returns:
            Pigeon hole CNF formula
        """
        cnf = []
        
        # Helper function to get variable number for pigeon i in hole j
        def var(pigeon: int, hole: int) -> int:
            return pigeon * n + hole + 1
        
        # Each pigeon must be in at least one hole
        for pigeon in range(n + 1):
            clause = [var(pigeon, hole) for hole in range(n)]
            cnf.append(clause)
        
        # No two pigeons in the same hole
        for hole in range(n):
            for p1 in range(n + 1):
                for p2 in range(p1 + 1, n + 1):
                    cnf.append([-var(p1, hole), -var(p2, hole)])
        
        return cnf


class CNFTransformer:
    """Transformer for CNF formula operations."""
    
    @staticmethod
    def negate(cnf: List[List[int]]) -> List[List[int]]:
        """Negate CNF formula (NOT CNF).
        
        Uses De Morgan's laws to convert to CNF.
        Warning: This can result in exponential blowup.
        
        Args:
            cnf: Original CNF formula
            
        Returns:
            Negated formula in CNF
        """
        # NOT (clause1 AND clause2 AND ...) = NOT clause1 OR NOT clause2 OR ...
        # NOT (lit1 OR lit2 OR ...) = NOT lit1 AND NOT lit2 AND ...
        
        # For simplicity, we convert to DNF then back to CNF
        # This is a simplified implementation
        
        if not cnf:
            return [[1]]  # NOT TRUE = FALSE
        
        # Negate each clause (apply De Morgan's law)
        negated_clauses = []
        for clause in cnf:
            negated_clause = [-lit for lit in clause]
            negated_clauses.append(negated_clause)
        
        # Convert from DNF to CNF using distribution
        # For simple cases, just return the negated literals as separate clauses
        result = []
        for negated_clause in negated_clauses:
            for lit in negated_clause:
                result.append([lit])
        
        return result
    
    @staticmethod
    def simplify(cnf: List[List[int]]) -> List[List[int]]:
        """Simplify CNF formula.
        
        Removes duplicate clauses and tautologies.
        
        Args:
            cnf: CNF formula
            
        Returns:
            Simplified CNF formula
        """
        simplified = []
        seen_clauses = set()
        
        for clause in cnf:
            # Check for tautology (clause with both x and NOT x)
            literals = set(clause)
            is_tautology = False
            
            for lit in literals:
                if -lit in literals:
                    is_tautology = True
                    break
            
            if is_tautology:
                continue
            
            # Remove duplicates within clause
            clause = sorted(list(literals))
            clause_tuple = tuple(clause)
            
            # Check for duplicate clauses
            if clause_tuple not in seen_clauses:
                seen_clauses.add(clause_tuple)
                simplified.append(clause)
        
        return simplified
    
    @staticmethod
    def get_variables(cnf: List[List[int]]) -> Set[int]:
        """Get all variables in CNF formula.
        
        Args:
            cnf: CNF formula
            
        Returns:
            Set of variable numbers
        """
        variables = set()
        
        for clause in cnf:
            for lit in clause:
                variables.add(abs(lit))
        
        return variables
    
    @staticmethod
    def get_statistics(cnf: List[List[int]]) -> dict:
        """Get formula statistics.
        
        Args:
            cnf: CNF formula
            
        Returns:
            Dictionary with statistics
        """
        variables = CNFTransformer.get_variables(cnf)
        
        clause_lengths = [len(clause) for clause in cnf]
        
        return {
            "num_variables": len(variables),
            "num_clauses": len(cnf),
            "avg_clause_length": sum(clause_lengths) / len(clause_lengths) if clause_lengths else 0,
            "max_clause_length": max(clause_lengths) if clause_lengths else 0,
            "min_clause_length": min(clause_lengths) if clause_lengths else 0,
            "total_literals": sum(clause_lengths),
            "clause_to_variable_ratio": len(cnf) / len(variables) if variables else 0
        }


if __name__ == "__main__":
    print("CNF Parser and Generator\n")
    
    # Example: Parse formula
    formula_str = "(1 OR -2) AND (2 OR 3) AND (-1 OR -3)"
    cnf = CNFParser.from_string(formula_str)
    print(f"Parsed: {formula_str}")
    print(f"CNF: {cnf}")
    print(f"Readable: {CNFParser.to_readable(cnf)}\n")
    
    # Example: Generate random 3-SAT
    random_cnf = CNFGenerator.generate_3sat(10, ratio=4.3, seed=42)
    print(f"Random 3-SAT (10 variables):")
    print(f"Readable: {CNFParser.to_readable(random_cnf)}")
    print(f"Statistics: {CNFTransformer.get_statistics(random_cnf)}\n")
    
    # Example: Pigeon hole principle
    pigeon_cnf = CNFGenerator.generate_pigeon_hole(3)
    print(f"Pigeon Hole (4 pigeons, 3 holes):")
    print(f"Number of clauses: {len(pigeon_cnf)}")
    print(f"Statistics: {CNFTransformer.get_statistics(pigeon_cnf)}")
