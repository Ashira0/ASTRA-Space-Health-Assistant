# ASTRA — NASA Space Apps submission kit

## Project name
**ASTRA — Autonomous Space Telemetry & Risk Assessment**

## One-line pitch
A crew-facing space health dashboard that turns concerning measurements into explainable, interactive emergency-response **simulations**, with optional offline local AI explanations.

## Project description (adapt for submission)
Long-duration space missions can limit timely access to medical specialists. Astronauts need tools that collect health indicators, recognize concerning patterns, and help them understand what to do next. ASTRA demonstrates a mission health console that combines synthetic heart rate, oxygen saturation, sleep and radiation-index telemetry; optional manual wellness entries; NASA human research context; and NASA space-weather information.

When a synthetic emergency occurs, ASTRA's fictional ARES-01 response engine evaluates the current measurements and the astronaut's answers. It then selects a relevant response branch, presents the next simulated action, asks for missing context, and logs completed steps. The crew can use a floating assistant from any dashboard tab or open a full conversation interface. Optional local Qwen3 explains the current workflow, but it does not select interventions or modify the decision rules.

The demonstration includes a fictional oxygen-support branch to illustrate how mission-authorized procedures could be incorporated in a future operational system. ASTRA does not administer treatment, control hardware, or claim that its demo protocols are clinically approved.

## Challenge alignment
- **Gather health indicators:** simulated vital signs plus manually entered sleep, mood, fatigue, symptoms, temperature, blood pressure, and glucose.
- **Evaluate health status:** alert rules and trend visualization.
- **Act on health status:** interactive response state machine, decision explanations, simulated intervention selection, follow-up questions, incident log.
- **Space-specific context:** NASA five hazards, historical NASA OSD-575 lab research, NASA DONKI event metadata, and CSA radiation-monitoring references.
- **Autonomy:** deterministic response engine remains available even when Ollama is unavailable or mission connectivity is interrupted.

## Architecture

```text
Synthetic telemetry / CSV import / manual wellness check-ins
                         |
                  Streamlit dashboard
                         |
                Rule-based alert engine
                         |
              ARES-01 response state machine
                  /                \
         Guided steps          Incident log
                  \                /
                 Shared conversation state
                         |
            Optional local Ollama explanations
                         |
              Floating + full-screen Copilot
```

## Live demo script (2–3 minutes)

**0:00–0:30** Introduce the problem and show four telemetry charts and crew selection. Clarify that the live values are synthetic.

**0:30–1:00** Select Multi-system emergency drill, 100%, sample 59. Highlight simultaneous SpO₂ and heart-rate alerts.

**1:00–1:45** Open the floating Copilot and type: “I've confirmed the oxygen reading. The cabin pressure is normal, and I have an oxygen kit available.” Show captured facts and fictional oxygen-support decision. Confirm a workflow step and show how the next instruction changes. Explain that actual interventions would require mission-approved rules and validation.

**1:45–2:15** Open full Copilot; show shared conversation and incident log export. Demonstrate wellness check-in.

**2:15–2:45** Show NASA OSD-575 historical lab data and NASA DONKI space weather. Explain they are not real-time crew vitals or personal dosimetry.

**2:45–3:00** Close with offline capability, transparency, and future integration with validated mission medical protocols.

## Evidence and attribution
- NASA HRP Five Hazards: https://www.nasa.gov/hrp/hazards/
- NASA HRP Risks: https://www.nasa.gov/hrp/risks/
- NASA HRP Ongoing Research: https://www.nasa.gov/hrp/ongoing-hrp-research/
- NASA-STD-3001 Volume 1: https://www.nasa.gov/reference/nasa-std-3001v1/
- NASA OSD-575: https://osdr.nasa.gov/osdr/data/osd/files/575
- NASA DONKI: https://ccmc.gsfc.nasa.gov/tools/DONKI/
- CSA radiation monitoring: https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp

## Submission checklist

- [ ] Run the app locally and visually inspect every tab.
- [ ] Run automated tests and the oxygen emergency scenario.
- [ ] Record a 2–3 minute demo video showing the workflow.
- [ ] Take 3–5 screenshots: overview, emergency step, Copilot, wellness, NASA research.
- [ ] Create a public repository with the project code, README, and source attribution (remove any personal/private data).
- [ ] Confirm the hackathon's submission form, required fields, licensing and actual deadline.
- [ ] Upload video link, repository link, screenshots, and description.
- [ ] Submit before the deadline and verify confirmation.

## Future development
Mission-specific verified protocols, clinician review, robust natural-language understanding, authenticated persistent records, real sensors, environment telemetry, equipment state, offline source document retrieval, and formal clinical validation.
