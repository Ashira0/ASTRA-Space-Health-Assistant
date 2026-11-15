"""ASTRA fictional ARES-01 training workflows. No real treatment instructions.
Deterministic state machine; pure functions suitable for unit tests.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import re

VERSION = 'ARES-01 SIM-MED-002 v2.0 — team-authored demonstration'
DEFAULTS = {'signal':'unknown','cabin':'unknown','kit':'unknown','breathing':'unknown','responder':'unknown','support':'unknown','recheck':'unknown','radiation':'unknown','fatigue':'unknown'}

@dataclass
class ResponseState:
    crew: str
    scenario: str
    signature: str
    facts: dict = field(default_factory=lambda: dict(DEFAULTS))
    completed: list = field(default_factory=list)
    events: list = field(default_factory=list)
    chat: list = field(default_factory=list)
    focus: str = ''
    reported: dict = field(default_factory=dict)


def classify(current, facts, focus=''):
    spo2=float(current['SpO₂ (%)']); hr=float(current['Heart rate (bpm)'])
    if facts.get('breathing') == 'unresponsive': return 'UNRESPONSIVE CREW', 'critical'
    if facts.get('cabin') == 'alarm': return 'CABIN ENVIRONMENT', 'critical'
    if focus == 'oxygen' and spo2 >= 94: return 'OXYGENATION RECOVERY', 'review'
    if focus == 'oxygen': return 'OXYGENATION CONCERN', 'critical' if spo2 < 90 else 'review'
    if spo2 < 90: return 'OXYGENATION CONCERN', 'critical'
    if spo2 < 94: return 'OXYGENATION CONCERN', 'review'
    if hr > 120: return 'ELEVATED HEART RATE', 'review'
    if float(current['Radiation index (relative)']) > 2: return 'RADIATION SENSOR FLAG', 'review'
    if float(current['Sleep (h)']) < 5: return 'FATIGUE CONCERN', 'review'
    return 'ROUTINE MONITORING', 'nominal'


def workflow(current, facts, focus=''):
    branch, severity = classify(current, facts, focus)
    steps=[]
    def add(key, title, instruction, reason, question=None, options=None):
        steps.append(dict(id=key,title=title,instruction=instruction,reason=reason,question=question,options=options or []))
    if branch == 'ROUTINE MONITORING':
        add('log','Record the health check','Record the current measurements and any symptoms. Continue routine scheduled checks.','No active demonstration threshold was crossed.')
    elif branch == 'OXYGENATION RECOVERY':
        add('recovery','Confirm recovery readings','Confirm the reported improved SpO₂ and heart rate, reassess symptoms, and document the outcome. Do not assume the incident is resolved from one report.','Improvement requires confirmation and follow-up.')
        add('reassess','Complete follow-up assessment','Record subsequent trends and whether symptoms have resolved; keep the incident history.','A single improved reading is not proof of sustained recovery.')
    elif branch == 'UNRESPONSIVE CREW':
        add('alert','Activate crew emergency response','Alert the crew responder immediately and activate the simulated unresponsive-crew emergency response.','The crew member was reported unresponsive or breathing abnormally.')
        add('status','Confirm emergency status','Record responsiveness and breathing observations for the responder. Do not wait for sensor verification.','Clinical status takes priority over instrument data.')
        add('reassess','Continue the response','Record changes and follow the scenario response team instructions.','ASTRA does not supply resuscitation or equipment operation instructions.')
    elif branch == 'CABIN ENVIRONMENT':
        add('alert','Raise spacecraft environment alarm','Alert flight operations and the crew responder; activate the simulated cabin-environment emergency branch.','A cabin alarm was reported, independently of the physiological reading.')
        add('environment','Review environmental indications','Review the displayed cabin oxygen, pressure, and life-support alarms. Record readings for the response team.','A nominal pressure report alone does not establish normal oxygen partial pressure.')
        add('reassess','Reassess crew and environment','Recheck the crew member and environment, and log changes.','Physiological and environmental emergencies can occur together.')
    elif branch == 'OXYGENATION CONCERN':
        add('alert','Activate crew medical response','Notify the crew responder now and assess responsiveness and breathing.','The scenario displays a concerning oxygen reading.')
        if facts.get('breathing') == 'unknown':
            add('breathing','Assess crew status','Assess whether the crew member is responsive and breathing normally.','A change in responsiveness changes the emergency branch.','Crew status',['Responsive and breathing','Breathing difficulty','Unresponsive / abnormal breathing'])
        if facts.get('signal') == 'unknown':
            add('signal','Confirm the measurement','Check sensor signal and repeat the reading if feasible without delaying the crew response.','A poor pulse-oximeter signal can produce unreliable values.','Repeat measurement',['Confirmed','Unreliable'])
        if facts.get('cabin') == 'unknown':
            add('cabin','Check cabin indicators','Review available cabin oxygen, pressure, and atmosphere alarms.','Cabin pressure alone does not prove oxygen availability.','Cabin indicators',['Nominal','Alarm / abnormal'])
        if facts.get('kit') == 'unknown':
            add('kit','Check response resources','Confirm whether the fictional crew oxygen kit is available.','Equipment availability determines the simulated intervention branch.','Oxygen kit',['Available','Unavailable'])
        if float(current['SpO₂ (%)']) < 90 and facts.get('signal') == 'confirmed' and facts.get('cabin') == 'nominal' and facts.get('kit') == 'available' and facts.get('breathing') != 'unresponsive':
            add('oxygen_support','SIMULATED INTERVENTION: Oxygen support','ARES-01 selects simulated supplemental oxygen support. Mark the oxygen-support intervention as initiated in the drill; do not operate real equipment.','The low reading was confirmed, cabin indicators were reported nominal, and the fictional kit is available. This is team-authored simulation logic, not a treatment order.','Intervention status',['Simulated support initiated','Not initiated'])
        elif facts.get('kit') == 'unavailable':
            add('resource','Report resource constraint','Report that the simulated oxygen kit is unavailable and request responder assistance.','A required demonstration resource is unavailable.')
        elif facts.get('signal') == 'unreliable':
            add('signal_issue','Investigate sensor reliability','Flag the reading as unreliable and seek an alternate measurement while maintaining symptom-based response.','The reported reading is not confirmed.')
        else:
            add('pending','Await required decision facts','Complete the missing checks above. The simulated oxygen-support branch cannot be selected until its required inputs are available.','No intervention is selected from an incomplete context.')
        add('reassess','Reassess and document','Recheck oxygen saturation, heart rate, symptoms, and relevant cabin indicators; record whether the simulated intervention changed the readings.','A single measurement does not show response over time.','Follow-up status',['Improved','Unchanged','Worse'])
    elif branch == 'ELEVATED HEART RATE':
        add('alert','Assess cardiovascular symptoms','Check recent activity, palpitations, chest discomfort, dizziness and breathing. Alert the crew responder if concerning.','The scenario heart-rate alert needs symptom and activity context.')
        add('signal','Review measurement quality','Repeat the pulse reading where feasible and review the recent trend.','A single high pulse may reflect exercise or a measurement artifact.')
        add('reassess','Track recovery','Record pulse, activity and symptoms during reassessment.','Trend and context matter more than an isolated value.')
    elif branch == 'RADIATION SENSOR FLAG':
        add('verify','Verify radiation measurement','Review calibrated dosimeter readings or a verified environmental alert; the synthetic index is not a dose.','A unitless index cannot establish individual exposure.')
        add('respond','Activate simulated radiation review','Log the alert and ask the crew responder to review the fictional radiation-event workflow.','Space-weather events and personal radiation dose are different measurements.')
    else:
        add('fatigue','Assess fatigue','Record sleep, workload, concentration and symptoms; consider simulated workload adjustment and rest planning.','Sleep data can help identify fatigue-related operational concerns.')
        add('reassess','Reassess readiness','Document subsequent rest and any change in alertness.','The model cannot diagnose fatigue from sleep duration alone.')
    return branch, severity, steps


def parse_facts(message):
    """Conservative extraction; negation checked before positive matches."""
    q=message.lower(); facts={}
    if re.search(r'\b(unresponsive|unconscious|not breathing|abnormal breathing)\b',q): facts['breathing']='unresponsive'
    elif re.search(r'\b(shortness of breath|difficulty breathing|struggling to breathe|can.t breathe)\b',q): facts['breathing']='difficulty'
    elif re.search(r'\b(responsive|breathing normally|breathing is normal)\b',q): facts['breathing']='responsive'
    if re.search(r'\b(oxygen reading|spo2|saturation|pulse ox|pulse oximeter|measurement)\b',q):
        if re.search(r'\b(unreliable|false reading|bad signal|not confirmed|couldn.t confirm|cannot confirm)\b',q): facts['signal']='unreliable'
        elif re.search(r'\b(confirmed|verified|rechecked|repeat reading|checked twice)\b',q): facts['signal']='confirmed'
    if re.search(r'\b(cabin|atmosphere|pressure|life support)\b',q):
        if re.search(r'\b(alarm|abnormal|leak|low pressure|not normal)\b',q): facts['cabin']='alarm'
        elif re.search(r'\b(normal|nominal|stable|within limits)\b',q): facts['cabin']='nominal'
    if re.search(r'\b(oxygen kit|oxygen equipment|oxygen supply)\b',q):
        if re.search(r'\b(unavailable|no oxygen kit|don.t have|do not have|not available|missing)\b',q): facts['kit']='unavailable'
        elif re.search(r'\b(available|have|ready|on hand|accessible)\b',q): facts['kit']='available'
    if re.search(r'\b(oxygen support|supplemental oxygen|intervention)\b',q):
        if re.search(r'\b(not initiated|haven.t initiated|not started)\b',q): facts['support']='not_started'
        elif re.search(r'\b(initiated|started|simulated|completed)\b',q): facts['support']='initiated'
    if re.search(r'\b(improved|better|recovering)\b',q): facts['recheck']='improved'
    elif re.search(r'\b(worse|deteriorat|declining)\b',q): facts['recheck']='worse'
    elif re.search(r'\b(unchanged|same as before|no change)\b',q): facts['recheck']='unchanged'
    return facts


def answer_option(key, answer):
    mapping={
        'breathing':{'Responsive and breathing':'responsive','Breathing difficulty':'difficulty','Unresponsive / abnormal breathing':'unresponsive'},
        'signal':{'Confirmed':'confirmed','Unreliable':'unreliable'},
        'cabin':{'Nominal':'nominal','Alarm / abnormal':'alarm'},
        'kit':{'Available':'available','Unavailable':'unavailable'},
        'oxygen_support':{'Simulated support initiated':'initiated','Not initiated':'not_started'},
        'reassess':{'Improved':'improved','Unchanged':'unchanged','Worse':'worse'},
    }
    dest={'oxygen_support':'support','reassess':'recheck'}.get(key,key)
    return dest,mapping.get(key,{}).get(answer)


def log_event(state,kind,detail):
    state.events.append({'timestamp_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'crew':state.crew,'scenario':state.scenario,'type':kind,'detail':detail})


def update(state, changes):
    for k,v in changes.items():
        if k in DEFAULTS and v in ('unknown','confirmed','unreliable','nominal','alarm','available','unavailable','responsive','difficulty','unresponsive','initiated','not_started','improved','unchanged','worse') and state.facts.get(k)!=v:
            state.facts[k]=v; log_event(state,'context',f'{k} = {v}')


def state_current(state, current):
    """Overlay explicitly reported measurements without mutating dashboard telemetry."""
    merged=dict(current)
    merged.update(state.reported)
    return merged


def parse_measurements(message):
    """Only capture explicitly reported values; never infer numbers."""
    q=message.lower(); out={}
    oxygen=re.search(r'(?:spo2|sp[o₂]2|oxygen saturation|oxygen reading|saturation)\s*(?:is|of|at|:|=|has improved to|improved to)?\s*(\d{2,3}(?:\.\d+)?)\s*%',q)
    heart=re.search(r'(?:heart rate|pulse)\s*(?:is|of|at|:|=|now|has improved to|is now)?\s*(\d{2,3}(?:\.\d+)?)\s*(?:bpm)?',q)
    if oxygen and 0 <= float(oxygen.group(1)) <= 100: out['SpO₂ (%)']=float(oxygen.group(1))
    if heart and 0 <= float(heart.group(1)) <= 300: out['Heart rate (bpm)']=float(heart.group(1))
    return out


def incident_report(state,current):
    observed=state_current(state,current)
    lines=[f'**Incident summary — {state.crew}**',f'Scenario: {state.scenario}',
           f'Latest assessment readings: SpO₂ {float(observed["SpO₂ (%)"]):.1f}%, heart rate {float(observed["Heart rate (bpm)"]):.1f} bpm',
           '**Reported context:** '+(', '.join(f'{k}: {v}' for k,v in state.facts.items() if v!='unknown') or 'None'),
           '**Confirmed workflow steps:** '+(', '.join(state.completed) or 'None'),
           '**Event history:**']
    lines.extend('- '+e['detail'] for e in state.events)
    lines.append('Unconfirmed steps are not recorded as performed. Fictional training scenario.')
    return '\n\n'.join(lines)


def next_step(state,current):
    branch,severity,steps=workflow(state_current(state,current),state.facts,state.focus)
    for s in steps:
        if s['id'] not in state.completed: return branch,severity,s,steps
    return branch,severity,None,steps


def summary(state,current):
    branch,severity,step,steps=next_step(state,current)
    text=f'**{branch} — {severity.upper()} (simulation)**\n\n'
    selected=next((s for s in steps if s['id']=='oxygen_support'),None)
    if selected and selected['id'] not in state.completed:
        text+='**DECISION: Simulated oxygen-support branch selected**\n\n'+selected['instruction']+'\n\n'
    if step:
        text+=f'**NEXT ACTION: {step["title"]}**\n\n{step["instruction"]}\n\n**Why:** {step["reason"]}'
        if step['question']: text+=f'\n\n**Please confirm:** {step["question"]} — {", ".join(step["options"])}.'
    else: text+='All currently applicable steps have been marked complete. Continue monitoring and start a new assessment if the situation changes.'
    text+='\n\n*ARES-01 is a fictional training workflow; actions are simulated and no medical equipment is controlled.*'
    return text
