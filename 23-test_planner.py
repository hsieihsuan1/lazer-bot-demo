import unittest
from app.planner import plan
from app.scenario import _rain_scenario
class PlannerTests(unittest.TestCase):
 def payload(self,**kw):return dict(date='2026-10-10',group='familia',preference='misto',radius=6,budget=40,rain=40,**{})|kw
 def test_thresholds(self):
  for x,y in [(0,'sol'),(24,'sol'),(25,'incerto'),(64,'incerto'),(65,'chuva'),(100,'chuva')]:self.assertEqual(_rain_scenario(x),y)
 def test_rain_indoor(self):self.assertTrue(all(p['indoor'] for p in plan(self.payload(rain=90,preference='outdoor'))['primary']))
 def test_sun_outdoor(self):self.assertTrue(all(not p['indoor'] for p in plan(self.payload(rain=0))['primary']))
 def test_fallback_indoor(self):self.assertTrue(all(p['indoor'] for p in plan(self.payload())['fallback']))
 def test_budget(self):self.assertTrue(all(p['price']==0 for p in plan(self.payload(budget=0))['primary']))
 def test_radius(self):self.assertEqual(plan(self.payload(radius=1))['primary'],[])
 def test_family(self):self.assertTrue(all(p['family'] for p in plan(self.payload(radius=20,budget=500))['primary']))
 def test_indoor(self):self.assertTrue(all(p['indoor'] for p in plan(self.payload(preference='indoor'))['primary']))
 def test_invalid_dates(self):
  for date in ['2026-02-30','not a date']:
   with self.assertRaises(ValueError):plan(self.payload(date=date))
 def test_invalid_numbers(self):
  for rain in [-1,101,float('nan'),True,'50']:
   with self.assertRaises(ValueError):plan(self.payload(rain=rain))
 def test_bad_shape(self):
  for payload in [[],None,self.payload(group='unknown')]:
   with self.assertRaises(ValueError):plan(payload)
 def test_honest_labels(self):self.assertIn('fictícios',plan(self.payload())['note'])
