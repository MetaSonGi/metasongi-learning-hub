import unittest,tempfile
from pathlib import Path
import app
class LearningTest(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.old=app.ROOT;app.ROOT=Path(self.tmp.name)
 def tearDown(self):app.ROOT=self.old;self.tmp.cleanup()
 def test_progress_idempotent_and_quiz(self):
  for _ in range(2):app.post('/api/complete',{'course':'robot','lesson':0})
  self.assertEqual(len(app.get('/api/courses')['progress']),1)
  self.assertFalse(app.post('/api/quiz',{'course':'robot','choice':1})['result']['success'])
  self.assertTrue(app.post('/api/quiz',{'course':'robot','choice':0})['result']['success'])
  self.assertEqual(app.get('/api/courses')['scores'],[('robot',1)])
 def test_invalid_actions(self):
  for data in ({'course':'missing','lesson':0},{'course':'robot','lesson':99},{'course':'robot','lesson':True}):
   with self.assertRaises(ValueError):app.post('/api/complete',data)
 def test_statement_shape(self):
  r=app.post('/api/complete',{'course':'xr','lesson':1})['statement']
  self.assertIn('actor',r);self.assertTrue(r['object']['id'].startswith('https://'));self.assertTrue(r['result']['completion']);self.assertEqual(len(app.get('/api/events')),1)
if __name__=='__main__':unittest.main()
