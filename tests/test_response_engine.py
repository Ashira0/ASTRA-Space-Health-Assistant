import unittest
from response_engine import ResponseState, parse_facts, workflow, update, next_step, summary

BASE={'SpO₂ (%)':84.9,'Heart rate (bpm)':150.1,'Sleep (h)':2.8,'Radiation index (relative)':3.53}
class ResponseTests(unittest.TestCase):
    def test_context_from_user_example(self):
        facts=parse_facts("I've confirmed the oxygen reading. The cabin pressure is normal, and I have an oxygen kit available.")
        self.assertEqual(facts,{'signal':'confirmed','cabin':'nominal','kit':'available'})
        state=ResponseState('Vega','Emergency','signature');update(state,facts)
        _,_,steps=workflow(BASE,state.facts)
        self.assertIn('oxygen_support',[s['id'] for s in steps]);self.assertIn('oxygen-support branch selected',summary(state,BASE))
    def test_unavailable_kit(self):
        facts=parse_facts("I don't have an oxygen kit")
        self.assertEqual(facts['kit'],'unavailable')
        _,_,steps=workflow(BASE,facts)
        self.assertNotIn('oxygen_support',[s['id'] for s in steps])
    def test_abnormal_cabin_overrides(self):
        _,_,steps=workflow(BASE,{'cabin':'alarm','signal':'confirmed','kit':'available'})
        self.assertEqual(steps[0]['id'],'alert');self.assertNotIn('oxygen_support',[s['id'] for s in steps])
    def test_unresponsive_overrides(self):
        branch,_,steps=workflow(BASE,{'breathing':'unresponsive','cabin':'nominal','signal':'confirmed','kit':'available'})
        self.assertEqual(branch,'UNRESPONSIVE CREW')
    def test_nominal(self):
        normal=dict(BASE);normal.update({'SpO₂ (%)':98,'Heart rate (bpm)':72,'Sleep (h)':7,'Radiation index (relative)':.5})
        branch,_,steps=workflow(normal,{})
        self.assertEqual(branch,'ROUTINE MONITORING')
    def test_step_progression(self):
        state=ResponseState('Vega','Emergency','sig')
        _,_,step,_=next_step(state,BASE)
        self.assertEqual(step['id'],'alert')
        state.completed.append('alert')
        _,_,step,_=next_step(state,BASE)
        self.assertEqual(step['id'],'breathing')
    def test_no_kit_false_positive(self):
        self.assertEqual(parse_facts('oxygen kit not available')['kit'],'unavailable')
    def test_sensor_negation(self):
        self.assertEqual(parse_facts('the oxygen reading is not confirmed')['signal'],'unreliable')
if __name__=='__main__':unittest.main()
