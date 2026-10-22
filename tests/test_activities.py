import ast
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'python'))
from activities import extra_questions,execute

class ActivityTests(unittest.TestCase):
    def test_repair_outputs_are_real(self):
        for q in extra_questions():
            if q['activity']!='repair':continue
            with self.subTest(title=q['title']):
                self.assertEqual(execute(q['code']),q['repair_original_output'])
                for v in q['repair_variants']:
                    self.assertEqual(execute(v['code']),v['output'])
                    self.assertEqual(v['passed'],v['output']==q['repair_expected'])

    def test_new_snippets_stay_in_curriculum(self):
        forbidden=(ast.List,ast.Dict,ast.Set,ast.Import,ast.ImportFrom,ast.For,ast.While,ast.ListComp,ast.DictComp)
        for q in extra_questions():
            for code in [q['code']]+[v['code'] for v in q.get('repair_variants',[])]:
                for node in ast.walk(ast.parse(code)):
                    self.assertNotIsInstance(node,forbidden)
                    if isinstance(node,ast.ClassDef):self.assertFalse(node.bases)

    def test_generated_bank_matches_python_sources(self):
        from build import QUESTOES
        from dataclasses import asdict
        from activities import make_bank
        base=[]
        for q in QUESTOES:
            data=asdict(q);data.pop('expected_output');base.append(data)
        actual=json.loads((ROOT/'site/questions.json').read_text())
        self.assertEqual(make_bank(base),actual)

if __name__=='__main__':unittest.main()
