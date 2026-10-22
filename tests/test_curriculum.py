"""Executa os códigos autorais e verifica o recorte curricular da turma."""
import ast
import contextlib
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))
from build import QUESTOES

class CurriculumTests(unittest.TestCase):
    def test_outputs(self):
        for q in QUESTOES:
            if q.expected_output is None:
                continue
            with self.subTest(title=q.title):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    exec(compile(q.code, '<questao>', 'exec'), {})
                self.assertEqual(out.getvalue().strip(), q.expected_output)

    def test_scope(self):
        forbidden = (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp,
                     ast.SetComp, ast.GeneratorExp, ast.Import, ast.ImportFrom,
                     ast.For, ast.While)
        for q in QUESTOES:
            with self.subTest(title=q.title):
                tree = ast.parse(q.code)
                self.assertTrue(q.source)
                self.assertIn(q.seconds, (60,90,120))
                for node in ast.walk(tree):
                    self.assertNotIsInstance(node, forbidden)
                    if isinstance(node, ast.ClassDef):
                        self.assertFalse(node.bases)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, ('type', 'len', 'input'))

    def test_missing_self_fix(self):
        q = QUESTOES[1]
        fixed = q.code.replace('        paginas_lidas = 0', '        self.paginas_lidas = 0')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exec(compile(fixed, '<correcao>', 'exec'), {})
        self.assertEqual(out.getvalue().strip(), '0')

    def test_numeric_options_match_execution(self):
        for index in (0,3,5,7,12,13):
            q = QUESTOES[index]
            self.assertEqual(q.options[q.answer], q.expected_output)

if __name__ == '__main__':
    unittest.main()
