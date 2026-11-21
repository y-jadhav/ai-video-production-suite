---
name: multi-agent-director
description: Autonomous multi-agent video production pipeline. Orchestrates script parsing, Twitter wire agency sourcing (ANI, PTI, IANS via TwitSave), web article crawling (Firecrawl), audio master generation, and Remotion video compilation end-to-end. Trigger whenever the user provides a video script or asks for autonomous multi-agent video production.
---

# 🤖 Multi-Agent Autonomous Video Production Pipeline

This skill orchestrates a team of specialized AI agents working together from a single script to deliver a finished, fully edited, broadcast-ready video.

```mermaid
flowchart TD
    UserScript["User Video Script (.md)"] --> ScriptParser["1. Script Parser Agent\n(Scene Breakdown & Asset Matrix)"]
    
    subgraph SourcingPhase["Concurrent Sourcing Phase"]
        ScriptParser --> TwitterAgent["2. Twitter Wire Agent\n(ANI, PTI, IANS via TwitSave)"]
        ScriptParser --> CrawlAgent["3. Web Crawling Agent\n(Firecrawl Broadsheets & Articles)"]
        ScriptParser --> AudioAgent["4. Audio & Foley Agent\n(Edge-TTS + SFX + BGM)"]
    end
    
    TwitterAgent --> Staging["Asset Staging\npublic/<project>_assets/"]
    CrawlAgent --> Staging
    AudioAgent --> Staging
    
    Staging --> EditorAgent["5. Video Editor & Compositor Agent\n(Remotion TSX + Safe Zones + Attributions)"]
    EditorAgent --> Render["6. Headless Remotion Render\n& Quality Assurance Audit"]
    Render --> FinalVideo["Final MP4 Video Output\n(1080x1920 or 1920x1080 @ 30 FPS)"]
```

---

## 👥 The 5 Agent Roles

### 1. 📝 Script Parser Agent
- **Input:** Video script markdown (e.g. `script.md`).
- **Function:** Breaks down the script into scene timing blocks, voiceover text, and visual requirements.
- **Output:** Structured asset requirement matrix identifying which scenes require event clips, newspaper clippings, or sound effects.

### 2. 🐦 Twitter Wire Agency Agent
- **Function:** Sourcing authentic event, protest, and political footage.
- **Strict Rule:** Sources **exclusively** from verified wire services: **ANI** (`@ANI`), **PTI** (`@PTI_News`), **IANS** (`@IANS_India` / `@ians_news`).
- **Engine:** Automated **TwitSave (`https://twitsave.com/en`)** pipeline.
- **Output:** Standardized MP4 clips (`9:16` or `16:9` @ 30 FPS) with mandatory on-screen credit: `"Clip Source: ANI"`.

### 3. 🕷️ Web Crawling & Research Agent
- **Function:** Sourcing verified articles, headlines, press releases, and legal notices.
- **Engine:** **Firecrawl MCP** (`firecrawl_scrape`, `firecrawl_search`).
- **Output:** Authentic broadsheet newspaper graphics (The Hindu, TOI), official notices, and highlighted evidence cards.

### 4. 🎵 Audio & Foley Sound Agent
- **Function:** Dialogue and soundscape engineering.
- **Engine:** Local `edge-tts` (fast, expressive narration) + tactile Foley audio libraries.
- **Output:** Synced master audio track (-14 to -16 LUFS) with paper slides, marker writing, rubber stamp slams, and ducked musical beds.

### 5. 🎬 Video Editor & Compositor Agent
- **Function:** Visual compilation and final render.
- **Engine:** Remotion / React.
- **Enforcements:**
  - Mobile safe zones (top 12% `y < 230px`, bottom 16% `y > 1620px`).
  - Tactile Vox styling: `#F3EFE6` warm paper ground, yellow highlighter sweeps, red rubber stamps.
  - Automatic frame extraction for visual QA.

---

## ⚡ Execution Command

To execute the autonomous pipeline:
```powershell
python multi_agent_video_pipeline.py --script "<path_to_script.md>" --project-name "<project_name>" --aspect "9:16|16:9"
```
