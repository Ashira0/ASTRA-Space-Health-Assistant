# ASTRA — NASA Space Apps Challenge 2026 Submission Kit

**Team:** AstraVital-26  
**Project:** ASTRA — Autonomous Space Telemetry & Risk Assessment  
**Challenge:** Create Health Monitoring Software for Astronauts  
**Submission Date:** November 15, 2026  
**GitHub Repository:** https://github.com/Ashira0/ASTRA-Space-Health-Assistant

---

## 1. Project Name

**ASTRA — Autonomous Space Telemetry & Risk Assessment**

## 2. One-Line Pitch

An AI-assisted astronaut health monitoring platform that transforms concerning health measurements into explainable alerts, interactive emergency-response simulations, and context-aware decision support.

## 3. Project Summary

ASTRA (Autonomous Space Telemetry & Risk Assessment) is an AI-powered astronaut health monitoring and emergency assistance prototype designed for long-duration space missions.

Astronauts face unique health challenges, including radiation exposure, isolation, sleep disruption, and limited access to immediate medical support. ASTRA addresses these challenges by combining simulated health telemetry, anomaly detection, daily wellness check-ins, and interactive emergency-response workflows.

The platform monitors indicators such as heart rate, oxygen saturation, sleep duration, and a synthetic radiation index. When concerning measurements are detected, ASTRA's deterministic ARES-01 decision engine evaluates reported conditions, requests additional information, and guides users through fictional emergency-response procedures.

ASTRA also integrates historical NASA human research data, NASA space weather information, and an optional locally hosted AI Copilot powered by Ollama and Qwen3.

Our goal is to demonstrate how future astronaut health systems could evolve beyond passive monitoring into proactive, transparent, and context-aware decision support.

---

## 4. Project Description

### The Problem

Long-duration space exploration introduces significant challenges to astronaut health and safety.

Astronauts are exposed to space radiation, isolation and confinement, altered gravity, and hostile or closed environments. These conditions can contribute to physiological and psychological health concerns.

As missions travel farther from Earth, communication delays and limited access to medical specialists may require astronauts to take greater responsibility for monitoring and evaluating their own health.

Although monitoring systems can display physiological measurements, recognizing an abnormal reading is only part of the challenge. Astronauts also need to understand the situation, provide additional context, and determine appropriate next steps.

### Our Solution

ASTRA is an interactive health monitoring and emergency decision-support prototype designed to explore how intelligent software could assist astronauts during long-duration missions.

The application combines simulated crew telemetry, rule-based anomaly detection, daily wellness tracking, NASA research resources, and a conversational AI interface.

Its central innovation is **ARES-01**, a fictional deterministic emergency-response engine.

Rather than simply generating an alert, ARES-01 evaluates available measurements, requests additional information, selects a simulated response pathway, and records explicitly confirmed workflow actions.

For example, when ASTRA detects a concerning oxygen saturation reading, ARES-01 can ask whether the measurement has been confirmed, whether cabin conditions are normal, whether simulated oxygen-support equipment is available, and whether the astronaut is experiencing breathing difficulties.

Using these reported facts, the system determines the next step in its fictional emergency workflow.

The prototype demonstrates how future systems might connect health monitoring with structured decision support.

### Key Features

**Live Health Monitoring**

- Simulated astronaut heart rate, oxygen saturation, sleep, and radiation-related indicators
- Interactive visualizations and historical trends
- Crew selection and adjustable health scenarios
- Real-time evaluation of simulated telemetry

**Anomaly Detection**

- Rule-based identification of concerning measurements
- Health alerts and event analysis
- Recognition of simultaneous health concerns

**ARES-01 Emergency Response Engine**

- Deterministic emergency classification
- Context-sensitive follow-up questions
- Fictional emergency-response branch selection
- Explicit workflow confirmation
- Recovery reassessment
- Incident summaries and event logging

**ASTRA Copilot**

- Conversational interaction
- Optional local Qwen3 language model through Ollama
- Explanations of simulated health concerns
- Shared emergency workflow context
- Emergency decisions remain controlled by deterministic Python logic

**Wellness Check-ins**

- Sleep, mood, and fatigue tracking
- Manual symptom reporting
- Temperature, blood pressure, and blood glucose entry
- CSV export

**NASA Research Integration**

- Historical NASA OSD-575 human research data
- NASA Human Research Program references
- NASA DONKI space weather information

**Incident Documentation**

- Reported observations and conditions
- Selected simulated response pathways
- Confirmed workflow steps
- Recovery measurements
- Downloadable incident information

---

## 5. Challenge Alignment

ASTRA addresses the challenge's main objectives in the following ways.

### Gather Health Indicators

ASTRA presents simulated physiological telemetry and supports manual wellness entries, including sleep, mood, fatigue, symptoms, temperature, blood pressure, and glucose.

### Evaluate Health Status

The platform evaluates measurements using predefined alert rules and displays trends, anomalies, and relevant context.

### Support Action Based on Health Status

ARES-01 demonstrates how an intelligent system could guide astronauts through fictional emergency-response workflows using structured questions, decision explanations, and follow-up assessments.

### Incorporate Space-Specific Health Context

ASTRA references NASA's five hazards of human spaceflight, historical OSD-575 laboratory research, NASA DONKI space weather records, and Canadian Space Agency radiation research.

### Support Greater Crew Autonomy

The deterministic emergency engine operates locally and does not require an internet connection or an active language model.

This illustrates a possible approach to supporting crews during missions with limited communication availability.

---

## 6. System Architecture

ASTRA is implemented as a modular Python application.

### Monitoring Layer

The Streamlit dashboard generates and displays simulated astronaut health telemetry, evaluates measurements, and presents visualizations and alerts.

### Emergency Decision Layer

The ARES-01 response engine evaluates the simulated emergency state, reported context, and confirmed workflow actions.

It determines the next fictional response step through explicit Python rules.

### Conversational Layer

ASTRA Copilot provides a natural-language interface and optional local AI explanations.

The language model cannot independently authorize or modify emergency-response decisions.

### Research and Data Layer

The application includes historical NASA OSD-575 laboratory data and retrieves NASA DONKI space weather information when internet access is available.

### Data Export Layer

Users can export wellness check-ins and simulated emergency incident information.

### Main Project Files

| File | Purpose |
|---|---|
| `app.py` | Main dashboard, telemetry simulation, and Streamlit interface |
| `response_engine.py` | Deterministic ARES-01 emergency workflow |
| `copilot.py` | Conversational interface, local AI integration, and incident export |
| `checkin.py` | Manual wellness tracking and CSV export |
| `donki.py` | NASA DONKI integration |
| `nasa_osd575_cmp.csv` | Historical NASA research dataset |
| `tests/test_response_engine.py` | Automated response-engine tests |
| `requirements.txt` | Python dependencies |
| `README.md` | Installation and project documentation |

---

## 7. Technologies Used

- **Python:** Application logic, telemetry processing, and emergency workflows
- **Streamlit:** Interactive web application
- **Pandas:** Data processing and research dataset exploration
- **Plotly:** Interactive data visualization
- **Ollama:** Local language-model runtime
- **Qwen3 1.7B:** Optional conversational AI
- **NASA Open Science Data Repository:** Historical human research data
- **NASA DONKI:** Space weather event information
- **Python unittest:** Automated testing

ASTRA was developed using freely available software without requiring paid cloud infrastructure.

---

## 8. Official NASA Space Apps Demonstration

### Video Requirement

**Maximum video duration: 30 seconds.**

Alternatively, the submission permits a slide presentation containing no more than seven slides, including the title and introduction.

The official demonstration must be hosted at a publicly accessible URL that does not require a password, permission request, or account registration.

### Recommended 30-Second Video

**0:00–0:05 — Introduce ASTRA**

Display the ASTRA dashboard.

On-screen caption:

"ASTRA — AI-Powered Astronaut Health Monitoring"

**0:05–0:10 — Monitor Crew Health**

Show the heart rate, oxygen saturation, sleep, and synthetic radiation indicators.

On-screen caption:

"Continuous Monitoring & Anomaly Detection"

**0:10–0:17 — Detect an Emergency**

Select Commander Vega and the Multi-system emergency drill at 100% intensity, sample 59.

Highlight the concerning oxygen saturation and heart-rate readings.

On-screen caption:

"Critical Health Anomaly Detected"

**0:17–0:25 — Demonstrate ARES-01**

Show the Copilot identifying the oxygenation concern and selecting the simulated oxygen-support branch after receiving confirmed context.

On-screen caption:

"Context-Aware Emergency Decision Support"

**0:25–0:30 — Show Additional Capabilities**

Briefly show wellness tracking, NASA research, and space weather.

On-screen caption:

"Wellness • NASA Research • Space Weather"

End with:

"ASTRA | AstraVital-26"

### Video Production Notes

- Aim for approximately 27–29 seconds to stay safely below the limit.
- Use a screen recording of the actual application.
- Prepare the emergency scenario before recording.
- Pre-enter or prepare relevant messages to minimize typing time.
- Use short, readable captions.
- Avoid displaying private information.
- Clearly identify any SI-generated visual or video content as required by the competition.
- Upload the final demonstration to YouTube or another publicly accessible hosting service.
- Test the video URL in a private browser window before submitting.

### Optional Extended Walkthrough

The following sequence can be used for local testing or a longer informal presentation. It is not the official 30-second submission video.

1. Launch ASTRA and select Commander Vega.
2. Select Multi-system emergency drill, intensity 100%, sample 59.
3. Open ASTRA Copilot.
4. Report the critical oxygen saturation and heart-rate measurements.
5. Confirm the oxygen reading, nominal cabin conditions, and simulated oxygen-kit availability.
6. Report that the astronaut is conscious but experiencing breathing difficulty.
7. Demonstrate the workflow confirmation controls.
8. Report improved oxygen saturation and heart rate.
9. Generate the incident summary.
10. Explore wellness check-ins, NASA OSD-575 research, and NASA DONKI space weather information.

---

## 9. NASA Data and Resources

The following NASA resources were used for project data, integration, or scientific background.

### NASA Open Science Data Repository — OSD-575

Historical human research laboratory measurements used in ASTRA's Human Research interface.

https://osdr.nasa.gov/osdr/data/osd/files/575

### NASA DONKI — Space Weather Database

NASA space weather event information used in ASTRA's Space Weather interface.

https://ccmc.gsfc.nasa.gov/tools/DONKI/

### NASA Human Research Program — Five Hazards

Scientific background on major hazards affecting astronauts during spaceflight.

https://www.nasa.gov/hrp/hazards/

### NASA Human Research Program — Risks

Research context for human health and performance risks.

https://www.nasa.gov/hrp/risks/

### NASA Human Research Program — Ongoing Research

Background information on NASA's human spaceflight research activities.

https://www.nasa.gov/hrp/ongoing-hrp-research/

### NASA-STD-3001 Volume 1

Background reference on spaceflight crew health standards.

https://www.nasa.gov/reference/nasa-std-3001v1/

These resources provide research context and data. They do not imply NASA approval, endorsement, or clinical validation of ASTRA's fictional response procedures.

---

## 10. Space Agency Partner and Other Resources

### Canadian Space Agency — Radiation Monitoring

https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp

### Canadian Space Agency — Science in Space

https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp

### Development Tools

- Python: https://www.python.org/
- Streamlit: https://streamlit.io/
- Pandas: https://pandas.pydata.org/
- Plotly: https://plotly.com/python/
- Ollama: https://ollama.com/
- Qwen3: https://ollama.com/library/qwen3

Additional external assets and dependencies used in the final project should be attributed in accordance with their licenses.

---

## 11. Use of Super Intelligence (SI)

SI and generative AI tools were used during ASTRA's development.

### Applicable SI Categories

- Ideation or Brainstorming
- Research or Information Gathering
- Building SI/ML Into the Project
- Coding, Debugging, or Troubleshooting
- Writing, Editing, or Translation
- Visual Design or Image Creation

Additional categories should be selected if applicable to the final submission materials.

### SI Use Description

ChatGPT and other AI-assisted tools supported project brainstorming, research exploration, software development, debugging, documentation, and visual design.

ASTRA also incorporates a locally hosted Qwen3 1.7B language model through Ollama for optional conversational explanations.

The ARES-01 emergency-response engine uses explicit Python decision rules rather than allowing unrestricted language-model output to determine simulated interventions.

SI-generated visual assets included in the submission must carry the required visible watermark or identification.

AI-assisted code, text, and other materials should be acknowledged as required by the competition.

No generated materials should contain prohibited NASA branding, logos, flags, or mission identifiers.

---

## 12. Testing and Verification

ASTRA includes automated tests for its deterministic emergency-response engine.

### Run Unit Tests

```bash
python -m unittest discover -s tests -v
```

### Check Python Compilation

```bash
python -m compileall -q .
```

### Emergency Workflow Test

The following six messages can be used to exercise ARES-01's simulated emergency workflow.

**Message 1**

"My oxygen saturation and heart rate are both critical. What should I do?"

Expected: Oxygenation concern identified as critical.

**Message 2**

"I've confirmed the oxygen reading. The cabin pressure is normal, and I have an oxygen kit available. What do I do next?"

Expected: Reported conditions recorded and simulated oxygen-support branch selected.

**Message 3**

"The astronaut is conscious and breathing, but is having difficulty breathing."

Expected: Breathing difficulty recorded in the incident context.

**Message 4**

"I've completed that step. What comes next?"

Expected: The system requests explicit workflow confirmation rather than assuming an action occurred.

**Message 5**

"The oxygen saturation has improved to 96% and the heart rate is now 88 bpm."

Expected: Transition to recovery review.

**Message 6**

"Summarize the emergency and every action we took."

Expected: Incident summary containing the latest readings, reported context, event history, and confirmed workflow steps.

These tests demonstrate software behavior within the fictional scenario. They do not establish medical accuracy or operational safety.

---

## 13. Responsible Design and Safety Boundaries

ASTRA is an educational research prototype and fictional emergency-response simulator.

It is not a certified medical device, approved spacecraft system, or clinically validated decision-support tool.

### Key Limitations

- Live astronaut telemetry is synthetic.
- The radiation index is dimensionless and does not represent a calibrated personal radiation dose.
- Historical NASA research data is separate from simulated live measurements.
- NASA DONKI records describe space weather events, not individual astronaut exposure.
- ARES-01 thresholds and response procedures were authored for this demonstration.
- The application does not administer treatment or operate medical equipment.
- The AI language model does not control emergency-response decisions.
- Symptom interpretation is limited and may require explicit confirmation.
- Wellness check-ins and incident records are stored in Streamlit session state rather than a secured persistent database.
- Users should not enter real private medical records.
- Online research and space weather retrieval require network access.
- The prototype has not been evaluated in real emergencies or operational spaceflight.

### Design Priorities

ASTRA emphasizes:

1. Explainable decision logic
2. Separation of simulated and authentic research data
3. Clear identification of fictional interventions
4. Explicit confirmation of completed actions
5. Offline-capable emergency workflows
6. Transparent documentation of limitations

---

## 14. Future Development

Potential future improvements include:

- Integration with real physiological sensors
- Expanded medical and environmental telemetry
- Expert-reviewed, mission-specific medical protocols
- More advanced natural-language understanding
- Secure persistent health records and authentication
- Offline retrieval of validated source documents
- Improved incident analysis and explainability
- Testing under realistic communication delays
- Integration with spacecraft environmental systems
- Formal software reliability, medical, and safety validation

ASTRA's long-term vision is to explore how intelligent, explainable health systems could support astronauts during increasingly autonomous exploration missions.

---

## 15. Project Links

**GitHub Repository**

https://github.com/Ashira0/ASTRA-Space-Health-Assistant

**Official Demonstration Video**

(https://www.youtube.com/watch?v=F1c-4f6kJUM)

**NASA Space Apps Team**

AstraVital-26

**Project Name**

ASTRA — Autonomous Space Telemetry & Risk Assessment

---

## 16. Final Submission Checklist

### Project Preparation

- [x] Develop ASTRA application
- [x] Implement simulated crew telemetry
- [x] Implement ARES-01 emergency-response engine
- [x] Integrate optional local AI Copilot
- [x] Include NASA research and space weather resources
- [x] Exercise the six-message emergency workflow
- [x] Create public GitHub repository
- [x] Prepare README and submission documentation
- [ ] Verify all required files are publicly accessible
- [ ] Run final automated tests
- [ ] Confirm all external resources are attributed

### Demonstration

- [ ] Record official video (30 seconds maximum), or create a presentation of no more than seven slides
- [ ] Add required SI-generated content identification
- [ ] Upload demonstration to a publicly accessible hosting service
- [ ] Verify demonstration duration and accessibility

### NASA Space Apps Submission

- [ ] Enter project name
- [ ] Enter project summary
- [ ] Enter project details
- [ ] Add public GitHub repository URL
- [ ] Add public demonstration URL
- [ ] List NASA data and resources
- [ ] List Space Agency Partner and other resources
- [ ] Complete SI-use disclosure
- [ ] Review originality and attribution requirements
- [ ] Agree to terms and conditions
- [ ] Submit before the official deadline
- [ ] Verify submission confirmation

---

## 17. Closing Statement

ASTRA demonstrates how astronaut health monitoring could move beyond passive observation toward proactive, context-aware decision support.

By combining simulated telemetry, explainable emergency workflows, optional local AI assistance, wellness tracking, and authentic NASA research resources, the project explores a possible foundation for future autonomous crew health systems.

**ASTRA — Supporting astronaut health beyond Earth.**

**Team AstraVital-26 | NASA Space Apps Challenge 2026**
