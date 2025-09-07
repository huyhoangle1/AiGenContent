import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from generate_content import ContentGenerator

class TestContentGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ContentGenerator()
    
    def test_generate_content(self):
        content = self.generator.generate_content("AI trong y tế")
        self.assertIsNotNone(content)
        self.assertGreater(len(content), 50)
    
    def test_optimize_seo(self):
        text = "Năng lượng mặt trời rất tốt"
        optimized = self.generator.optimize_seo(text, ["năng lượng sạch"])
        self.assertIn("năng lượng sạch", optimized)
    
    def test_grammar_check(self):
        text = "Năng lượng mặt trời rất tốt."
        errors = self.generator.check_grammar(text)
        self.assertEqual(errors, 0)

if __name__ == "__main__":
    unittest.main()