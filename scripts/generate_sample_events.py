#!/usr/bin/env python3
"""Generate sample JSON events for the book media pipeline."""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

EVENT_TYPES = [
    "session_start",
    "book_opened",
    "page_turned",
    "audio_played",
    "audio_paused",
    "video_played",
    "video_paused",
    "chapter_completed",
    "purchase",
    "session_end",
]

CONTENT_TYPES = ["ebook", "audiobook", "video"]
DEVICE_TYPES = ["web", "ios", "android"]
COUNTRIES = ["US", "CA", "GB", "DE", "AU"]


def random_event(base_ts: datetime, user_id: str) -> dict:
    content_type = random.choice(CONTENT_TYPES)
    event_type = random.choice(EVENT_TYPES)
    duration_seconds = random.uniform(5, 3600) if "played" in event_type else None
    progress_percent = random.uniform(0, 100) if event_type in {"page_turned", "chapter_completed"} else None
    price_usd = round(random.uniform(5, 25), 2) if event_type == "purchase" else None

    metadata = {
        "playback_speed": random.choice([0.75, 1.0, 1.25, 1.5]),
        "referrer": random.choice(["homepage", "search", "recommendations"]),
        "device_os": random.choice(["iOS", "Android", "Windows", "macOS"]),
    }

    return {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "event_ts": base_ts.isoformat(),
        "user_id": user_id,
        "session_id": str(uuid4()),
        "content_id": f"content_{random.randint(1000, 9999)}",
        "content_type": content_type,
        "chapter_id": f"chapter_{random.randint(1, 20)}",
        "device_type": random.choice(DEVICE_TYPES),
        "app_version": f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "country": random.choice(COUNTRIES),
        "duration_seconds": duration_seconds,
        "progress_percent": progress_percent,
        "price_usd": price_usd,
        "currency": "USD" if price_usd is not None else None,
        "metadata": metadata,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sample events.")
    parser.add_argument("--output", required=True, help="Output NDJSON file path")
    parser.add_argument("--events", type=int, default=200, help="Number of events")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)

    with output_path.open("w", encoding="utf-8") as handle:
        for idx in range(args.events):
            event_ts = now - timedelta(minutes=random.randint(0, 1440))
            user_id = f"user_{random.randint(1, 50)}"
            event = random_event(event_ts, user_id)
            json.dump(event, handle)
            if idx < args.events - 1:
                handle.write("\n")


if __name__ == "__main__":
    main()
