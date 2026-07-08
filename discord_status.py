#!/usr/bin/env python3
import json
import urllib.request
from xml.sax.saxutils import escape

USER_ID = "1060803221167280159"
API_URL = f"https://api.lanyard.rest/v1/users/{USER_ID}"
OUT_PATH = "discord-status.svg"

STATUS_COLOR = {
    "online": "#3ba55d",
    "idle": "#f0b132",
    "dnd": "#ed4245",
    "offline": "#6b7a9e",
}

IDLE_MESSAGE = {
    "online": "once in a miracle",
    "idle": "maybe on, maybe not",
    "dnd": "moment of focus",
    "offline": "asleep under the mountains",
}


def truncate(text, limit=34):
    text = text or ""
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def fetch_presence():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "renighted-profile-readme"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.load(resp)
    return payload["data"]


def build_label(data):
    if data.get("listening_to_spotify") and data.get("spotify"):
        sp = data["spotify"]
        song = sp.get("song") or "something"
        artist = sp.get("artist") or ""
        line = f"{song} — {artist}" if artist else song
        return f"\U0001F3A7 {truncate(line)}"

    for act in data.get("activities", []):
        # type 4 = custom status, type 0 = "Playing", 3 = "Watching"
        if act.get("type") == 4 and (act.get("state") or act.get("emoji")):
            emoji = ""
            if act.get("emoji") and act["emoji"].get("name") and not act["emoji"].get("id"):
                emoji = act["emoji"]["name"] + " "
            return truncate(f"{emoji}{act.get('state') or ''}".strip())
        if act.get("type") == 0 and act.get("name"):
            return f"\U0001F3AE Playing {truncate(act['name'])}"
        if act.get("type") == 3 and act.get("name"):
            return f"\U0001F4FA Watching {truncate(act['name'])}"

    status = data.get("discord_status", "offline")
    return IDLE_MESSAGE.get(status, IDLE_MESSAGE["offline"])


def render_svg(data):
    status = data.get("discord_status", "offline")
    color = STATUS_COLOR.get(status, STATUS_COLOR["offline"])
    user = data.get("discord_user", {})
    username = escape(user.get("global_name") or user.get("username") or "renighted")
    avatar_hash = user.get("avatar")
    user_id = user.get("id", USER_ID)

    if avatar_hash:
        ext = "gif" if avatar_hash.startswith("a_") else "png"
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.{ext}?size=64"
    else:
        avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"

    label = escape(build_label(data))

    svg = f'''<svg width="380" height="96" viewBox="0 0 380 96" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Discord presence for {username}">
  <defs>
    <linearGradient id="cardBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1b2a"/>
      <stop offset="100%" stop-color="#142242"/>
    </linearGradient>
    <clipPath id="avatarClip">
      <circle cx="48" cy="48" r="26"/>
    </clipPath>
  </defs>

  <rect x="1" y="1" width="378" height="94" rx="16" fill="url(#cardBg)" stroke="#2a3a5c" stroke-width="1"/>

  <image href="{avatar_url}" x="22" y="22" width="52" height="52" clip-path="url(#avatarClip)"/>
  <circle cx="48" cy="48" r="26" fill="none" stroke="#2a3a5c" stroke-width="2"/>

  <circle cx="68" cy="68" r="9" fill="#142242"/>
  <circle cx="68" cy="68" r="6" fill="{color}">
    <animate attributeName="opacity" values="1;0.6;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>

  <text x="96" y="42" font-family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="17" font-weight="600" fill="#eaf1ff">{username}</text>
  <text x="96" y="64" font-family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="13" fill="#b8c4d9">{label}</text>
</svg>
'''
    return svg


def main():
    try:
        data = fetch_presence()
    except Exception:
        data = {
            "discord_status": "offline",
            "activities": [],
            "discord_user": {"username": "renighted", "id": USER_ID},
        }
    svg = render_svg(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
