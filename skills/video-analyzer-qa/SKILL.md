---
name: video-analyzer-qa
description: >
  Comprehensive video quality assurance and technical audit skill: verifies frame-by-frame visual continuity,
  audio-video sync offset, temporal flow, broadcast loudness standards (EBU R128 / -14 LUFS to -16 LUFS),
  black frame detection, safe-zone margins (16:9 / 9:16), and subtitle readability before delivery.
  Use for "check video", "QA audit", "is the video ready", "loudness check", or troubleshooting video glitches.
---

# Video Analyzer & QA Skill

The final quality gate before publishing or delivering any video project. Evaluates technical parameters, broadcast compliance, and human visual readability.

## Automated Audit Checklist

### 1. Audio Compliance
- **Target Loudness**:
  - YouTube / Web: `-14 LUFS` (±1 LUFS), True Peak `<= -1.0 dBFS`.
  - Social / Reels / TikTok: `-14 LUFS` to `-16 LUFS`.
  - Broadcast: `-23 LUFS` (EBU R128).
- **Measurement Command**:
```bash
ffmpeg -i video.mp4 -af "ebur128=framelog=verbose" -f null -
```

### 2. Video & Stream Consistency
- **Resolution & Aspect**:
  - Horizontal: `1920x1080` or `3840x2160` (16:9).
  - Vertical: `1080x1920` (9:16).
  - Square: `1080x1080` (1:1).
- **Frame Rate**: Constant frame rate (24, 25, 30, or 60 fps). Variable frame rate (VFR) must be normalized.
- **Pixel Format**: `yuv420p` for maximum web and device player compatibility.

### 3. Visual Defect Detection
- **Black Frames / Stutter**:
```bash
ffmpeg -i video.mp4 -vf "blackdetect=d=0.1:pix_th=0.10" -f null -
```
- **Frozen Frames**:
```bash
ffmpeg -i video.mp4 -vf "freezedetect=n=-60dB:d=0.5" -f null -
```

### 4. Layout & Safe Zones
- **Vertical Safe Zone (9:16)**:
  - Width: Keep copy inside `x: 120` to `960` px.
  - Height: Keep copy between `y: 200` to `1550` px (clearing UI buttons, comments, and captions).
- **Horizontal Safe Zone (16:9)**:
  - Margin: 5% inner title safe buffer (`96px` horizontally, `54px` vertically).
  - Face Clearance: Verify graphics never overlap the subject's face, mouth, or eyes.

### 5. Review Contact Sheet Generation
Extract contact strips every 2–5 seconds across the timeline to visually inspect all transitions:
```bash
ffmpeg -i video.mp4 -vf "fps=1/3,scale=640:-1,tile=4x3" -q:v 2 contact_sheet.jpg
```
