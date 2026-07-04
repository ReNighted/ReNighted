#!/usr/bin/env python3
"""Render a small SVG chip showing the current local time at a fixed
UTC offset, styled to match the profile's night-sky palette."""
from datetime import datetime, timedelta, timezone

OFFSET_HOURS = 3  # UTC+3
OUT_PATH = "local-time.svg"


def render_svg():
    tz = timezone(timedelta(hours=OFFSET_HOURS))
    now = datetime.now(tz)
    time_str = now.strftime("%I:%M %p").lstrip("0")
    label = f"{time_str} · UTC+{OFFSET_HOURS}"

    svg = f'''<svg width="190" height="30" viewBox="0 0 190 30" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Current local time">
  <defs>
    <linearGradient id="chipBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1b2a"/>
      <stop offset="100%" stop-color="#142242"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="189" height="29" rx="14" fill="url(#chipBg)" stroke="#2a3a5c" stroke-width="1"/>
  <text x="16" y="20" font-family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="13" fill="#b8c4d9">\U0001F550&#160;{label}</text>
</svg>
'''
    return svg


def main():
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(render_svg())


if __name__ == "__main__":
    main()
