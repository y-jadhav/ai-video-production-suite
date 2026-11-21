---
name: twitter-video-fetcher
description: Automatically search, fetch, and download video assets and B-roll clips from Twitter/X using the TwitSave (twitsave.com) workflow and twitter-mcp. Use whenever editing a video (Vox explainer, reels, documentary, news promo) and needing real clips, viral footage, interviews, statements, or protest footage from Twitter/X.
---

# 🐦 Twitter Wire Agency Video Fetcher (ANI · PTI · IANS)

This skill enables video editing agents to automatically source, download, and format real event video clips strictly from authorized wire agencies (**ANI**, **PTI**, **IANS**) via **TwitSave (`https://twitsave.com/en`)**.

---

## 🚨 Strict Event Sourcing Rules
1. **Event Footage Platform:**
   - **Twitter/X ONLY** — NEVER use YouTube for event/news reporting footage.
2. **Authorized Sources (Strict Whitelist):**
   - **ANI** (`@ANI`)
   - **PTI** (`@PTI_News`)
   - **IANS** (`@IANS_India` / `@ians_news`)
   - **No other accounts permitted:** Do NOT use random accounts or secondary re-uploads.
3. **Mandatory On-Screen Attribution:**
   - Every video edit that mounts an event clip must display an on-screen lower-third badge:
     - `"Clip Source: ANI"`
     - `"Clip Source: PTI"`
     - `"Clip Source: IANS"`
4. **YouTube Permitted Scope:**
   - YouTube may **ONLY** be used for:
     - Generic stock footage (timelapses, nature, abstract backgrounds)
     - Green screen VFX assets & overlays
     - Background music (BGM beds)
     - Sound effects (SFX)

---

## ⚡ Automated Commands

### 1. Fetch by Wire Agency Tweet URL
```powershell
# Auto-detects agency and outputs attribution badge
python auto_fetch_twitter_clip.py --url "https://x.com/ANI/status/1234567890" --aspect 9:16 --fps 30 --output-dir "public/cjp_reel_assets"
```

### 2. Search Specific Wire Agency
```powershell
# Queries ANI specifically
python auto_fetch_twitter_clip.py --query "jantar mantar protest" --agency ANI --aspect 9:16 --output-dir "public/cjp_reel_assets"

# Queries across ANI, PTI, and IANS simultaneously
python auto_fetch_twitter_clip.py --query "election commission press conference" --aspect 16:9 --output-dir "public/vox_assets"
```

---

## 📺 Remotion On-Screen Attribution Component

When inserting wire clips into Remotion, include the mandatory attribution tag:

```tsx
import { Video, staticFile } from 'remotion';

// Video Container with Source Credit Badge
<div style={{ position: 'relative', width: '100%', height: '100%' }}>
  <Video src={staticFile('cjp_reel_assets/event_clip.mp4')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
  
  {/* Mandatory Source Attribution Badge */}
  <div
    style={{
      position: 'absolute',
      bottom: 240, // Above mobile safe zone
      right: 40,
      backgroundColor: 'rgba(0,0,0,0.85)',
      color: '#FFDE00',
      fontFamily: 'Impact, Arial Black',
      fontSize: 18,
      padding: '4px 12px',
      borderRadius: 4,
      letterSpacing: 1,
      borderLeft: '4px solid #C8102E',
    }}
  >
    CLIP SOURCE: ANI
  </div>
</div>
```
