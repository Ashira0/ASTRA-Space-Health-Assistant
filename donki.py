"""NASA DONKI solar energetic particle event integration.

DONKI SEP records are *space-weather event metadata*, not astronaut dosimetry.
The NASA public endpoints are queried at runtime; no NASA data are fabricated.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

import requests

CCMC_URL = "https://ccmc.gsfc.nasa.gov/DONKI-API/get/SEP"
NASA_URL = "https://api.nasa.gov/DONKI/SEP"


def validate_dates(start: date, end: date) -> None:
    if start > end:
        raise ValueError("Start date must not be after end date.")
    if (end - start).days > 59:
        raise ValueError("Select a period of 60 days or less.")
    if end > date.today():
        raise ValueError("End date cannot be in the future.")


def parse_events(payload: Any) -> list[dict[str, str]]:
    """Extract source fields without assigning unmeasured radiation intensity."""
    if isinstance(payload, dict):
        for key in ("data", "results", "content", "events"):
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break
    if not isinstance(payload, list):
        raise ValueError("NASA endpoint did not return an event list.")
    events: list[dict[str, str]] = []
    for record in payload:
        if not isinstance(record, dict):
            continue
        event_time = record.get("eventTime") or record.get("startTime") or ""
        if not event_time:
            continue
        instruments = record.get("instruments") or []
        if isinstance(instruments, list):
            instrument_names = ", ".join(
                str(i.get("displayName") or i.get("name") or "Unknown")
                if isinstance(i, dict) else str(i)
                for i in instruments
            )
        else:
            instrument_names = ""
        linked = record.get("linkedEvents") or []
        events.append({
            "Event time (UTC)": str(event_time),
            "Event ID": str(record.get("sepID") or record.get("activityID") or "Not provided"),
            "Instruments": instrument_names or "Not listed",
            "Linked events": str(len(linked)) if isinstance(linked, list) else "Not listed",
            "Catalog": str(record.get("catalog") or "Not provided"),
        })
    return sorted(events, key=lambda e: e["Event time (UTC)"])


def fetch_sep_events(start: date, end: date, timeout: int = 12) -> dict[str, Any]:
    """Fetch genuine NASA event metadata, trying both NASA-hosted public routes."""
    validate_dates(start, end)
    params = {"startDate": start.isoformat(), "endDate": end.isoformat()}
    failures = []
    for url in (CCMC_URL, NASA_URL):
        query = dict(params)
        if url == NASA_URL:
            query["api_key"] = "DEMO_KEY"
        try:
            response = requests.get(url, params=query, timeout=timeout, headers={"Accept": "application/json"})
            response.raise_for_status()
            payload = response.json()
            events = parse_events(payload)
            return {
                "events": events,
                "raw": payload,
                "source": url,
                "retrieved_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                "start": start.isoformat(),
                "end": end.isoformat(),
            }
        except (requests.RequestException, ValueError) as exc:
            failures.append(f"{url}: {str(exc)[:140]}")
    raise RuntimeError("Unable to retrieve NASA DONKI events. " + " | ".join(failures))
