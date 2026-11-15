"""Deterministic interpretation of explicitly reported facts for the ASTRA simulation.
No device control or real medical administration instructions.
"""
import re

def extract(question):
    q=question.lower()
    result={}
    if re.search(r'\b(confirm(?:ed)?|verified|rechecked|repeat(?:ed)?)\b',q) and re.search(r'\b(oxygen reading|spo2|saturation|reading)\b',q):
        result['signal']='Confirmed with repeat reading'
    if re.search(r'\b(cabin (?:pressure|conditions?|environment)|atmospher(?:e|ic))\b',q):
        if re.search(r'\b(normal|nominal|stable|within limits|fine)\b',q):
            result['atmosphere']='Cabin indicators nominal'
        elif re.search(r'\b(alarm|abnormal|low pressure|leak)\b',q):
            result['atmosphere']='Cabin alarm / abnormal pressure or oxygen'
    if re.search(r'\b(oxygen kit|oxygen equipment)\b',q):
        if re.search(r'\b(available|have|ready|on hand|accessible)\b',q) and not re.search(r'\b(not available|unavailable|don.t have|no oxygen kit)\b',q):
            result['oxygen_available']='Yes — simulated crew oxygen kit'
        elif re.search(r'\b(unavailable|don.t have|no oxygen kit)\b',q):
            result['oxygen_available']='No'
    if re.search(r'\b(unresponsive|unconscious|not breathing|abnormal breathing)\b',q):
        result['symptoms']='Unresponsive / abnormal breathing'
    elif re.search(r'\b(shortness of breath|difficulty breathing|can.t breathe)\b',q):
        result['symptoms']='Breathing difficulty'
    return result

def next_action(current, facts):
    from emergency import plan, PROTOCOL_VERSION
    symptoms=facts.get('symptoms','Unknown / not assessed')
    signal=facts.get('signal','Not yet verified')
    atmosphere=facts.get('atmosphere','Not checked / unknown')
    oxygen=facts.get('oxygen_available','Unknown')
    severity,steps=plan(current,symptoms,signal,atmosphere,oxygen)
    selected=next((s for s in steps if s.startswith('SIMULATED INTERVENTION:')),None)
    details='\n'.join(f'- **{k.replace("_"," ").title()}:** {v}' for k,v in facts.items())
    if selected:
        headline='**NEXT SIMULATED ACTION — Oxygen-support branch selected**'
        action=selected
    else:
        headline='**NEXT SIMULATED ACTION — Additional assessment required**'
        action=steps[-2] if len(steps)>2 else steps[0]
    return (f'**ASTRA ARES-01 · {severity}**\n\n'
            f'{headline}\n\n{action}\n\n'
            f'**Context captured**\n{details or "- No new context confirmed"}\n\n'
            '**Next check:** Report the crew member’s responsiveness and breathing symptoms. '
            'Continue simulated reassessment and document any changes.\n\n'
            f'*{PROTOCOL_VERSION}. Training demonstration only; no hardware is operated and no real treatment instructions are provided.*')
