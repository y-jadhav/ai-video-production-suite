---
name: auto-cut-editor
description: >
  Automated video cutting and speech pacing: detect and remove silences, pauses, retakes, and dead air
  from raw talking-head and podcast footage using audio thresholding and voice activity detection (VAD).
  Use for "auto-cut", "remove silences", "jump cuts", "rough cut", "trim dead air", or cleaning up raw video.
---

# Auto-Cut Editor Skill

Automatically transform long, raw footage into a tight, engaging rough cut by detecting and trimming silent intervals, false starts, and speech hesitations.

## Core Capabilities
- **Silence & Dead-Air Removal**: Cut non-speech sections below a decibel threshold (e.g. `-35 dB`) lasting longer than a set duration (e.g. `0.4s`).
- **Pacing & Padding**: Keep customizable margin cushions (e.g. `0.08s` before and `0.12s` after speech) so words are never clipped unnaturally.
- **Retake & False-Start Filtering**: Identify and drop repeated takes or hesitation phrases when paired with Whisper transcripts.
- **Timeline Export**: Generate EDL (Edit Decision List), XML, or directly cut video using FFmpeg and Python.

## Quick Command & Python Pipeline
Using `auto-editor` or Python with FFmpeg `silencedetect`:
```bash
# Direct auto-editor CLI
auto-editor raw_clip.mp4 --margin 0.1s --edit audio:threshold=-32dB -o tight_cut.mp4
```

### FFmpeg Silence Detection Script
```python
import subprocess, re

def detect_silence(video_path, noise_db="-35dB", min_duration=0.4):
    cmd = [
        "ffmpeg", "-i", video_path,
        "-af", f"silencedetect=noise={noise_db}:d={min_duration}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    
    silences = []
    starts = re.findall(r"silence_start: (\d+\.?\d*)", res.stderr)
    ends = re.findall(r"silence_end: (\d+\.?\d*)", res.stderr)
    
    for s, e in zip(starts, ends):
        silences.append((float(s), float(e)))
    return silences
```

## Quality Rules
1. **Never Clip First Consonants**: Always keep an 80ms–100ms pre-pad before speech resumes.
2. **Breathing Room**: Retain natural dramatic pauses (>0.8s) if the speaker is emphasizing a major point; do not over-compress human cadence into robotic chatter.
3. **Audio Crossfade**: Apply a 10ms micro-crossfade between cut seams to eliminate digital pops or audio clicks.
