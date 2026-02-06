"""Test Suite for SAT Solver

Comprehensive tests for the DPLL SAT solver implementation.
"""

import unittest
from sat_solver import SATSolver, parse_dimacs, cnf_to_dimacs
from cnf_parser import CNFParser, CNFGenerator, CNFTransformer


class TestSATSolver(unittest.TestCase):
    """Test cases for SAT Solver."""
    
    def test_simple_satisfiable(self):
        """Test simple satisfiable formula."""
        # (x1 OR x2) AND (NOT x1 OR x3)
        cnf = [[1, 2], [-1, 3]]
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertTrue(sat)
        self.assertIsNotNone(assignment)
        self.assertTrue(self._verify_assignment(cnf, assignment))
    
    def test_simple_unsatisfiable(self):
        """Test simple unsatisfiable formula."""
        # (x1) AND (NOT x1)
        cnf = [[1], [-1]]
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertFalse(sat)
        self.assertIsNone(assignment)
    
    def test_empty_formula(self):
        """Test empty formula (should be satisfiable)."""
        cnf = []
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertTrue(sat)
    
    def test_unit_clause(self):
        """Test unit clause propagation."""
        # (x1) AND (x1 OR x2) AND (NOT x1 OR x3)
        cnf = [[1], [1, 2], [-1, 3]]
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertTrue(sat)
        self.assertTrue(assignment[1])  # x1 must be True
        self.assertTrue(assignment[3])  # x3 must be True (from unit propagation)
    
    def test_pure_literal(self):
        """Test pure literal elimination."""
        # (x1 OR x2) AND (x1 OR x3) - x1 is pure (only positive)
        cnf = [[1, 2], [1, 3]]
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertTrue(sat)
        self.assertTrue(assignment[1])  # x1 should be True (pure literal)
    
    def test_three_sat(self):
        """Test 3-SAT instance."""
        # (x1 OR x2 OR x3) AND (NOT x1 OR x2 OR NOT x3) AND (NOT x2 OR x3 OR x4)
        cnf = [[1, 2, 3], [-1, 2, -3], [-2, 3, 4]]
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertTrue(sat)
        self.assertTrue(self._verify_assignment(cnf, assignment))
    
    def test_complex_satisfiable(self):
        """Test complex satisfiable formula."""
        # (x1 OR NOT x2) AND (x2 OR x3) AND (NOT x1 OR NOT x3) AND (x1 OR x2 OR x3)
        cnf = [[1, -2], [2, 3], [-1, -3], [1, 2, 3]]
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        self.assertTrue(sat)
        self.assertTrue(self._verify_assignment(cnf, assignment))
    
    def test_statistics(self):
        """Test solver statistics collection."""
        cnf = [[1, 2], [-1, 3], [-2, -3]]
        solver = SATSolver(cnf)
        solver.solve()
        
        stats = solver.get_statistics()
        
        self.assertIn('total_decisions', stats)
        self.assertIn('unit_propagations', stats)
        self.assertIn('pure_literals', stats)
        self.assertIn('branches', stats)
        self.assertIn('backtracks', stats)
        self.assertGreater(stats['total_decisions'], 0)
    
    def test_large_satisfiable(self):
        """Test larger satisfiable formula."""
        # Generate a satisfiable formula
        cnf = CNFGenerator.generate_random(5, 10, 3, seed=42)
        solver = SATSolver(cnf)
        sat, assignment = solver.solve()
        
        if sat:
            self.assertTrue(self._verify_assignment(cnf, assignment))
    
    def _verify_assignment(self, cnf, assignment):
        """Verify that assignment satisfies formula."""
        for clause in cnf:
            clause_satisfied = False
            for literal in clause:
                var = abs(literal)
                expected_value = literal > 0
                if var in assignment and assignment[var] == expected_value:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                return False
        return True


class TestDIMACS(unittest.TestCase):
    """Test cases for DIMACS parser."""
    
    def test_parse_dimacs(self):
        """Test DIMACS parsing."""
        dimacs = """c This is a comment
        p cnf 3 2
        1 -2 0
        2 3 0
        """
        
        cnf = parse_dimacs(dimacs)
        
        self.assertEqual(len(cnf), 2)
        self.assertEqual(cnf[0], [1, -2])
        self.assertEqual(cnf[1], [2, 3])
    
    def test_cnf_to_dimacs(self):
        """Test CNF to DIMACS conversion."""
        cnf = [[1, -2], [2, 3]]
        dimacs = cnf_to_dimacs(cnf)
        
        self.assertIn('p cnf', dimacs)
        self.assertIn('1 -2 0', dimacs)
        self.assertIn('2 3 0', dimacs)
    
    def test_round_trip(self):
        """Test DIMACS round-trip conversion."""
        original_cnf = [[1, -2, 3], [-1, 2], [2, -3]]
        
        # Convert to DIMACS and back
        dimacs = cnf_to_dimacs(original_cnf)
        parsed_cnf = parse_dimacs(dimacs)
        
        self.assertEqual(original_cnf, parsed_cnf)


class TestCNFParser(unittest.TestCase):
    """Test cases for CNF Parser."""
    
    def test_parse_readable(self):
        """Test parsing human-readable format."""
        formula = "(1 OR -2) AND (2 OR 3)"
        cnf = CNFParser.from_string(formula)
        
        self.assertEqual(len(cnf), 2)
        self.assertIn(1, cnf[0])
        self.assertIn(-2, cnf[0])
    
    def test_to_readable(self):
        """Test conversion to readable format."""
        cnf = [[1, -2], [2, 3]]
        readable = CNFParser.to_readable(cnf)
        
        self.assertIn('x1', readable)
        self.assertIn('¬', readable)
        self.assertIn('∨', readable)
        self.assertIn('∧', readable)
    
    def test_parse_list_format(self):
        """Test parsing list format."""
        formula = "[[1, -2], [2, 3]]"
        cnf = CNFParser.from_string(formula)
        
        self.assertEqual(cnf, [[1, -2], [2, 3]])


class TestCNFGenerator(unittest.TestCase):
    """Test cases for CNF Generator."""
    
    def test_generate_random(self):
        """Test random CNF generation."""
        cnf = CNFGenerator.generate_random(5, 10, 3, seed=42)
        
        self.assertEqual(len(cnf), 10)
        for clause in cnf:
            self.assertLessEqual(len(clause), 3)
            for lit in clause:
                self.assertLessEqual(abs(lit), 5)
    
    def test_generate_3sat(self):
        """Test 3-SAT generation."""
        cnf = CNFGenerator.generate_3sat(10, ratio=4.3, seed=42)
        
        self.assertEqual(len(cnf), 43)  # 10 * 4.3
        for clause in cnf:
            self.assertLessEqual(len(clause), 3)
    
    def test_pigeon_hole(self):
        """Test pigeon hole principle generation."""
        cnf = CNFGenerator.generate_pigeon_hole(2)
        
        # 3 pigeons, 2 holes - should be unsatisfiable
        solver = SATSolver(cnf)
        sat, _ = solver.solve()
        
        self.assertFalse(sat)  # Pigeon hole is unsatisfiable
    
    def test_reproducibility(self):
        """Test random generation reproducibility."""
        cnf1 = CNFGenerator.generate_random(5, 10, 3, seed=123)
        cnf2 = CNFGenerator.generate_random(5, 10, 3, seed=123)
        
        self.assertEqual(cnf1, cnf2)


class TestCNFTransformer(unittest.TestCase):
    """Test cases for CNF Transformer."""
    
    def test_simplify(self):
        """Test CNF simplification."""
        # Formula with tautology and duplicate
        cnf = [[1, -1], [1, 2], [1, 2], [2, 3]]
        simplified = CNFTransformer.simplify(cnf)
        
        # Tautology should be removed, duplicates should be removed
        self.assertLess(len(simplified), len(cnf))
        self.assertNotIn([1, -1], simplified)
    
    def test_get_variables(self):
        """Test variable extraction."""
        cnf = [[1, -2], [2, 3], [-1, -3]]
        variables = CNFTransformer.get_variables(cnf)
        
        self.assertEqual(variables, {1, 2, 3})
    
    def test_get_statistics(self):
        """Test formula statistics."""
        cnf = [[1, -2, 3], [2, 3], [-1]]
        stats = CNFTransformer.get_statistics(cnf)
        
        self.assertEqual(stats['num_variables'], 3)
        self.assertEqual(stats['num_clauses'], 3)
        self.assertEqual(stats['max_clause_length'], 3)
        self.assertEqual(stats['min_clause_length'], 1)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
