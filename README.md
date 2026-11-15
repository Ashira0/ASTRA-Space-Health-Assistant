# ASTRA — Autonomous Space Telemetry & Risk Assessment

### AI-Powered Astronaut Health Monitoring & Emergency Decision Support

**NASA Space Apps Challenge 2026**  
**Team:** AstraVital-26  
**Project Type:** Astronaut Health Monitoring & Emergency Assistance  
**Development:** Python · Streamlit · Ollama · Qwen3

---

## Mission Overview

**ASTRA (Autonomous Space Telemetry & Risk Assessment)** is an intelligent astronaut health monitoring and emergency decision-support prototype designed to explore how future space crews could monitor their health and respond to medical concerns during long-duration missions.

Space exploration presents unique challenges to human health. Astronauts face radiation exposure, isolation, disrupted sleep, altered gravity, and limited access to immediate medical assistance. As missions extend farther from Earth, crews may need greater independence when interpreting physiological information and responding to emergencies.

ASTRA explores a potential solution by combining **health telemetry, anomaly detection, interactive emergency workflows, wellness tracking, NASA research data, and locally hosted artificial intelligence** in a single platform.

Rather than simply displaying health measurements, ASTRA demonstrates how a monitoring system could identify concerning conditions, gather additional context, explain its decisions, and support a crew through a simulated emergency.

> **Mission Objective:** Transform astronaut health monitoring from passive data observation into proactive, transparent, and context-aware decision support.

---

## Key Features

### 1. Live Astronaut Health Monitoring

ASTRA provides an interactive dashboard that visualizes simulated physiological and environmental indicators, including:

- Heart rate (bpm)
- Blood oxygen saturation (SpO₂)
- Sleep duration
- Synthetic radiation exposure index
- Crew-specific health trends and alerts

Users can select different crew members, explore simulated health scenarios, and adjust scenario intensity to observe how ASTRA responds to changing conditions.

The dashboard includes historical trends, alert indicators, and visualizations designed to help users identify potentially concerning measurements.

**Note:** Live crew telemetry is synthetic. The radiation index is dimensionless and does not represent a calibrated radiation dose.

### 2. Intelligent Anomaly Detection

ASTRA continuously evaluates simulated telemetry against predefined thresholds to identify concerning conditions.

The application can highlight:

- Low oxygen saturation
- Elevated heart rate
- Insufficient sleep
- Elevated synthetic radiation indicators
- Multiple simultaneous health concerns

Detected anomalies are presented through the dashboard's alert and analysis interfaces.

These alerts provide the starting point for further investigation through ASTRA's emergency decision-support system.

### 3. ARES-01 — Autonomous Response & Emergency Support

**ARES-01** is ASTRA's fictional, deterministic emergency-response engine.

When a concerning condition is detected, ARES-01 evaluates the available measurements and asks for additional context before selecting a simulated response pathway.

For example, during a low-oxygen scenario, the system may consider:

- Whether the oxygen reading has been confirmed
- Whether cabin conditions are reported as normal
- Whether a simulated oxygen-support kit is available
- Whether the astronaut is conscious and breathing
- Whether breathing difficulties are present
- Whether subsequent measurements indicate improvement

ARES-01 can then:

1. Classify the simulated emergency.
2. Request missing information.
3. Select an appropriate fictional response branch.
4. Present the next workflow step.
5. Track explicitly confirmed actions.
6. Reassess reported recovery measurements.
7. Generate an incident summary.

**A key design decision is that emergency workflow decisions are deterministic.** ARES-01's response logic is implemented in Python and does not depend on unrestricted language-model output.

This approach improves consistency, traceability, and explainability within the simulation.

ARES-01 does not operate medical equipment, provide medication doses, or represent validated clinical guidance.

### 4. ASTRA Copilot — Local AI Assistance

ASTRA includes an optional conversational assistant powered by **Ollama and Qwen3 1.7B**.

The Copilot supports:

- Natural-language interaction
- Explanations of health-related information
- Questions about the simulated mission environment
- Contextual discussion of research resources
- Interaction with the emergency workflow interface
- Review of reported incident information

The AI model runs locally on the user's computer, reducing dependence on external cloud-based language-model services.

**Important:** The language model does not authorize interventions or override ARES-01's deterministic emergency decisions.

ASTRA's emergency workflow remains functional even when Ollama is unavailable.

### 5. Daily Wellness Check-ins

ASTRA allows users to manually record additional wellness information, including:

- Sleep duration
- Mood
- Fatigue
- Symptoms
- Body temperature
- Blood pressure
- Blood glucose

These check-ins provide a way to explore how subjective wellness reports and manually entered measurements could complement continuous telemetry.

Entries can be exported as CSV files for further analysis.

Check-in information is stored within the active Streamlit session and is not automatically incorporated into the simulated live telemetry.

### 6. NASA Human Research Integration

ASTRA includes authentic research data from the **NASA Open Science Data Repository (OSDR)**.

The prototype uses the OSD-575 comprehensive metabolic panel dataset to demonstrate how historical human spaceflight research measurements can be explored alongside a health monitoring interface.

This research component helps connect ASTRA's simulated monitoring environment with real scientific resources.

Historical research data is clearly distinguished from the synthetic crew telemetry.

### 7. Space Weather Monitoring

ASTRA integrates with NASA's **DONKI (Space Weather Database of Notifications, Knowledge, Information)** resources.

This component allows users to explore space weather events and their relevance to the broader space environment.

Space weather information is retrieved from NASA resources when network connectivity is available.

These records are not presented as direct measurements of an individual astronaut's radiation exposure.

### 8. Incident Logging and Data Export

ASTRA records information reported during simulated emergency scenarios, including:

- Confirmed observations
- Reported environmental conditions
- Available simulated resources
- Selected response branches
- Explicitly confirmed workflow steps
- Recovery measurements
- Incident event history

Incident information can be exported in JSON format.

The system distinguishes between actions that were recommended and actions explicitly confirmed by the user, avoiding unsupported claims that a response step was completed.

---

## System Architecture

ASTRA is built as a modular Python application.

| Component | Responsibility |
|---|---|
| `app.py` | Main Streamlit application, simulated telemetry, visualizations, and research interfaces |
| `response_engine.py` | Deterministic ARES-01 emergency decision engine |
| `copilot.py` | Conversational assistant, local AI integration, and incident export |
| `checkin.py` | Wellness check-ins and CSV export |
| `donki.py` | NASA DONKI space weather integration |
| `nasa_osd575_cmp.csv` | Historical NASA OSD-575 research dataset |
| `tests/test_response_engine.py` | Automated tests for emergency-response logic |
| `requirements.txt` | Python dependencies |
| `SUBMISSION.md` | Supporting submission documentation and demonstration guidance |

### Decision-Support Architecture

ASTRA separates three responsibilities:

**Monitoring Layer**

Generates and displays simulated physiological measurements, identifies anomalies, and presents health trends.

**Deterministic Decision Layer**

ARES-01 evaluates the current emergency state, reported context, and confirmed workflow actions to determine the next simulated response step.

**Conversational Layer**

The optional local language model provides explanations and natural-language assistance without controlling the underlying emergency decision engine.

This separation is intended to prevent language-model responses from independently determining simulated medical interventions.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development and decision logic |
| Streamlit | Interactive dashboard and user interface |
| Pandas | Data processing and analysis |
| Plotly | Interactive data visualizations |
| Ollama | Local language-model runtime |
| Qwen3 1.7B | Optional conversational AI |
| NASA OSDR | Historical human research data |
| NASA DONKI | Space weather information |
| Python unittest | Automated testing |

The prototype was developed using freely available tools and does not require paid cloud infrastructure.

---

## Installation and Setup

### Requirements

- Python 3.10 or newer
- A computer capable of running Streamlit
- Internet access for initial dependency installation and live NASA API requests
- Optional: Ollama for local AI explanations

### 1. Clone the Repository

```bash
git clone https://github.com/Ashira0/ASTRA-Space-Health-Assistant.git
cd ASTRA-Space-Health-Assistant
```

### 2. Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch ASTRA

```bash
streamlit run app.py
```

Open the local address displayed in Terminal, typically:

`http://localhost:8501`

### 5. Optional — Enable the AI Copilot

Install Ollama from:

https://ollama.com/

Download the local language model:

```bash
ollama pull qwen3:1.7b
```

Ensure the Ollama service is running and accessible at:

`http://localhost:11434`

ASTRA can operate its deterministic emergency workflows without Ollama.

---

## Demonstration Walkthrough

The following walkthrough provides a more detailed demonstration of ASTRA's functionality. The official NASA Space Apps submission demonstration is provided separately and follows the competition's duration or slide-count requirements.

### Scenario: Multi-System Emergency

**Step 1 — Initialize the Scenario**

Launch ASTRA and select:

- Crew member: Commander Vega
- Scenario: Multi-system emergency drill
- Intensity: 100%
- Sample: 59

The dashboard displays simulated concerning measurements, including reduced oxygen saturation and elevated heart rate.

**Step 2 — Open ASTRA Copilot**

Navigate to the ASTRA Copilot tab or open the floating assistant.

Enter:

> My oxygen saturation and heart rate are both critical. What should I do?

ARES-01 identifies the simulated oxygenation concern and presents the initial emergency-response step.

**Step 3 — Provide Additional Context**

Enter:

> I've confirmed the oxygen reading. The cabin pressure is normal, and I have an oxygen kit available. What do I do next?

ARES-01 records the reported conditions and selects the fictional simulated oxygen-support response branch.

**Step 4 — Report Symptoms**

Enter:

> The astronaut is conscious and breathing, but is having difficulty breathing.

The system incorporates this information into the incident context.

**Step 5 — Track Workflow Progress**

Use the workflow confirmation controls to record completed simulated actions.

The incident log only treats explicitly confirmed steps as completed.

**Step 6 — Report Recovery**

Enter:

> The oxygen saturation has improved to 96% and the heart rate is now 88 bpm.

ARES-01 transitions into a recovery-review state and requests confirmation of the improved measurements.

**Step 7 — Generate an Incident Summary**

Enter:

> Summarize the emergency and every action we took.

ASTRA produces an incident summary containing the reported context, latest measurements, event history, and confirmed workflow actions.

**Step 8 — Explore Additional Features**

Visit the Wellness Check-in, Human Research, and Space Weather interfaces to explore the broader platform.

---

## NASA Data and Research Resources

ASTRA draws on publicly available NASA scientific resources and research documentation.

### NASA Open Science Data Repository

Historical human research measurements used within ASTRA's research interface.

https://osdr.nasa.gov/bio/repo/data/studies/OSD-575

### NASA DONKI

Space weather event information used within ASTRA's space weather interface.

https://kauai.ccmc.gsfc.nasa.gov/DONKI/

### NASA Human Research Program — Five Hazards

Background research on the major hazards affecting human health during spaceflight.

https://www.nasa.gov/hrp/hazards/

### NASA Human Research Program — Risks

Research context regarding human health and performance risks during space exploration.

https://www.nasa.gov/hrp/risks/

### NASA-STD-3001

NASA spaceflight human-system standards used as background reference material.

https://www.nasa.gov/reference/nasa-std-3001v1/

### Canadian Space Agency

Additional space health and radiation research context.

https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp

**Data provenance:** NASA research measurements, NASA space weather records, and ASTRA's simulated astronaut telemetry are separate data sources. No historical research measurements are represented as live astronaut readings.

---

## Testing and Validation

ASTRA includes automated tests for its deterministic emergency-response engine.

To run the tests:

```bash
python -m unittest discover -s tests -v
```

To check Python source compilation:

```bash
python -m compileall -q .
```

The emergency workflow has also been exercised through a multi-step simulated scenario involving critical readings, contextual information gathering, response branch selection, recovery reporting, and incident summarization.

These tests assess software behavior within the prototype. They do not establish medical safety, clinical validity, or operational readiness.

---

## Innovation and Intended Impact

ASTRA explores how astronaut health monitoring could evolve beyond simply displaying measurements.

Its main contributions are:

**1. From Detection to Decision Support**

ASTRA connects concerning telemetry readings with structured follow-up questions and simulated response pathways.

**2. Explainable Emergency Logic**

The emergency engine uses explicit decision rules rather than relying on an unrestricted language model to determine interventions.

**3. Offline-Capable Operation**

Core monitoring and emergency workflow functionality can operate locally without an internet connection after setup.

**4. Integration of Multiple Health Contexts**

The prototype combines simulated telemetry, user-entered wellness information, historical NASA research, and space weather resources within one application.

**5. Transparent Incident Documentation**

ASTRA tracks reported facts and distinguishes recommended actions from confirmed actions.

### Long-Term Vision

Future exploration missions may experience significant communication delays and reduced access to immediate Earth-based assistance.

Systems inspired by ASTRA could eventually help crews recognize developing health concerns, organize relevant information, and support timely decision-making.

Before any operational use, such systems would require extensive medical, engineering, privacy, and reliability validation.

---

## Limitations and Safety

**ASTRA is an educational research prototype and fictional emergency-response simulator. It is not a medical device or certified clinical decision-support system.**

Important limitations include:

- Live crew telemetry is entirely simulated.
- The radiation index is unitless and is not a personal radiation dose.
- ARES-01 protocols and thresholds were created for the demonstration and are not validated flight medical procedures.
- The system does not administer treatment or control spacecraft or medical equipment.
- The AI Copilot does not independently authorize emergency interventions.
- Symptom extraction supports a limited vocabulary and may require explicit confirmation.
- Wellness records and incident information are held in Streamlit session state rather than a persistent, secured medical database.
- Users should not enter actual private medical records.
- NASA and CSA research resources provide scientific context and do not imply endorsement or validation of ASTRA.
- NASA API retrieval requires internet access.
- The prototype has not been tested in actual spaceflight or real medical emergencies.

---

## Responsible AI and SI Disclosure

Super Intelligence (SI) and generative AI tools were used to assist with aspects of ASTRA's development, including brainstorming, research support, code development, debugging, documentation, and visual design.

ASTRA also integrates a locally hosted Qwen3 language model through Ollama for optional conversational assistance.

The application's deterministic emergency-response engine remains separate from the language model.

AI-assisted content and generated visual assets should be identified in accordance with NASA Space Apps Challenge submission requirements. Any SI-generated images or videos used in the submission must carry the required visible identification.

---

## Future Improvements

Potential future extensions include:

- Integration with real physiological monitoring devices
- Additional health indicators and longitudinal analysis
- Expanded NASA research retrieval
- More comprehensive symptom interpretation
- Medical expert review and validation of response pathways
- Secure storage and access controls for sensitive health information
- More advanced explainability and incident analysis
- Testing under simulated communication delays
- Integration with spacecraft environmental monitoring systems

---

## Team

**AstraVital-26**

Developed for the **NASA Space Apps Challenge 2026**.

**Project:** ASTRA — Autonomous Space Telemetry & Risk Assessment

**Focus:** Astronaut health monitoring, artificial intelligence, explainable decision support, and space exploration.

---

*ASTRA demonstrates a possible direction for intelligent astronaut health assistance: combining monitoring, contextual reasoning, and transparent emergency workflows to support future exploration beyond Earth.*
