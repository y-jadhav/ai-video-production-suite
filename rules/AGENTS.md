# Workspace Rules for AI Video Production & Editing Agents

## 🎬 1. Event Footage Policy: Twitter/X Wire Agencies ONLY (Strict Whitelist)
When sourcing video footage for any news, political, social, or real-world event:
1. **Source Platform:**
   - **Twitter/X ONLY** — NEVER use YouTube for event/news reporting footage.
2. **Authorized Sources (Strict Whitelist):**
   - **ANI** (`@ANI`)
   - **PTI** (`@PTI_News`)
   - **IANS** (`@IANS_India` / `@ians_news`)
   - **NO OTHER CLIPS ALLOWED:** Never pull event clips from random accounts, unverified users, or secondary re-uploads.
3. **Mandatory On-Screen Attribution:**
   - In every video edit, the lower-third or corner badge MUST explicitly credit the source:
     - `"Clip Source: ANI"`
     - `"Clip Source: PTI"`
     - `"Clip Source: IANS"`
4. **Automated Acquisition:**
   - Use the **TwitSave automated pipeline**:
     ```powershell
     python auto_fetch_twitter_clip.py --url "<tweet_url>" --source "ANI" --output-dir "public/<project>_assets" [--aspect 9:16|16:9] [--fps 30]
     ```
   - Or search specifically within allowed handles:
     ```powershell
     python auto_fetch_twitter_clip.py --query "<event keywords>" --agency ANI --output-dir "public/<project>_assets"
     ```

---

## 🎵 2. YouTube Usage Policy (Restricted Scope)
YouTube is strictly reserved for non-event creative assets only:
- **Stock Footage** (abstract city timelapses, nature, tech backgrounds)
- **Green Screen Footage** (effects, overlays, keyed graphics)
- **Background Music (BGM)** (ducked instrumental beds)
- **Sound Effects (SFX)** (foley, impacts, whooshes, risers)
- **DO NOT** use YouTube for primary event or news documentation.

---

## 📱 3. Asset Staging & Mobile Safe Zones
1. **Staging Path:** Always save assets directly to `public/<project_name>_assets/` for instant Remotion `staticFile(...)` serving.
2. **Safe Zones:** Keep all titles, attribution tags (`Clip Source: ANI`), and critical subjects clear of the top 12% (`y < 230px`) and bottom 16% (`y > 1620px`) on 9:16 vertical videos.

---

## 🤖 4. Autonomous Multi-Agent Video Pipeline Protocol
When the user submits a video script:
1. **Script Parser Agent:** Breaks down the script, timestamps, and scene asset matrix.
2. **Concurrent Sourcing Phase:**
   - **Twitter Wire Agent:** Queries ANI, PTI, and IANS on Twitter/X and downloads video clips via TwitSave (`auto_fetch_twitter_clip.py`).
   - **Web Crawling Agent (Firecrawl):** Scrapes verified news headlines, official statements, and broadsheets.
   - **Audio Master Agent:** Generates timed TTS voiceover, Foley SFX, and ducked background music.
3. **Video Editor Agent:** Synthesizes the staged assets into Remotion TSX, mounts clips with `"Clip Source: <Agency>"` credit badges, verifies safe zones, and triggers the headless Remotion render.
4. **Quality Auditor Agent:** Extracts review stills for every scene and runs technical verification.
