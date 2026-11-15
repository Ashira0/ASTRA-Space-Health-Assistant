# ASTRA — Autonomous Space Telemetry & Risk Assessment

**Final hackathon demonstration build · 15 November 2026**

ASTRA is an offline-capable, Streamlit-based crew health monitoring and *fictional* emergency-response simulator. It combines synthetic crew telemetry, research context, user-entered wellness check-ins, and a deterministic ARES-01 response engine. Local Ollama Qwen3 is optional for explanatory questions; workflow decisions never depend on model output.

## Quick start (macOS, Python 3.10+)

```bash
cd astra_final
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Optional AI explanations: install Ollama, run `ollama pull qwen3:1.7b`, and ensure Ollama is listening on `localhost:11434`. **Emergency workflow runs without Ollama.**

## 90-second demo

1. Launch ASTRA and select **Commander Vega**.
2. Select **Multi-system emergency drill**, intensity **100%**, sample **59**.
3. Open the **ASTRA COPILOT** tab or the floating bottom-right launcher.
4. Enter: `I've confirmed the oxygen reading. The cabin pressure is normal, and I have an oxygen kit available.`
5. ASTRA captures those facts and identifies the fictional oxygen-support intervention branch. Use the step confirmation interface; answer crew status and follow-up questions. Note: the branch is a **simulated selection** and no real oxygen is delivered.
6. Export the incident JSON; switch to **Wellness Check-in**, save a sample entry, export CSV.
7. Show **Human Research** (historical NASA OSD-575 lab dataset) and **Space Weather** (NASA DONKI records if network is available). Explicitly distinguish those data sources from the synthetic crew vital signs.

## Design and safety boundaries

- **Deterministic**: `response_engine.py` owns branch selection, next step, facts, confirmations, and event logging. The LLM cannot authorize or change actions.
- **Simulated intervention**: when the fictional rules find a confirmed SpO₂ <90%, nominal cabin indicators, available fictional oxygen kit, and no report of unresponsiveness, the demo selects *simulated oxygen support*. It does **not** provide oxygen flow settings, equipment operation instructions, medication doses, or real clinical advice.
- **Sources**: NASA/CSA research links are curated background summaries, not verified flight medical procedure manuals. ARES-01 is authored for this demo; no NASA endorsement or clinical validation is implied.
- **Data separation**: synthetic telemetry ≠ historical OSD-575 comprehensive metabolic panel ≠ NASA DONKI space weather. Radiation index is unitless and not a personal dose.
- **Privacy**: check-ins and incident logs are held in Streamlit session state and can be downloaded. No authentication, encrypted storage, or persistent database is provided. Do not enter actual private medical records.
- **No hardware control**: the app never operates spacecraft or medical devices.

## Files

- `app.py` — dashboard, telemetry generation, source-specific research/weather tabs, Streamlit shell
- `response_engine.py` — deterministic fictional response state machine
- `copilot.py` — persistent chat, optional local explanations, full and floating UI, incident export
- `checkin.py` — manual wellness check-ins and CSV export
- `donki.py` — NASA DONKI API adapter
- `nasa_osd575_cmp.csv` — historical NASA OSD-575 lab data
- `tests/test_response_engine.py` — unit tests
- `SUBMISSION.md` — ready-to-adapt project description, architecture, demo narration, and submission checklist

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

## Limitations

This is a research/hackathon prototype, **not** a medical device, certified emergency system, or validated clinical decision support tool. The fictional branch thresholds are team-authored. Symptom extraction is intentionally conservative and supports a limited vocabulary; ambiguous statements may need explicit confirmation. The app has not been evaluated on astronauts or real emergencies. Offline response workflows work without Ollama, but source API retrieval needs internet.
