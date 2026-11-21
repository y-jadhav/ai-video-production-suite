---
name: blender-video-tools
description: >
  Create, edit, render, and script videos with Blender Python (bpy), the Video Sequence Editor (VSE),
  procedural compositing, 3D titles, camera tracking, and FFmpeg pipeline integration. Use for programmable
  Blender media production, multi-track timeline automation, and procedural video renders.
---

# Blender Video Tools & VSE Scripting

Treat Blender as a headless, scriptable media-production and non-linear editing (NLE) environment.

## When to Use
- **Automated VSE Timelines**: Assembling multi-track video sequences, image strips, audio beds, and text overlays via Python scripts.
- **3D Titles & Overlays**: Compositing 3D animated objects, titles, or logo models over 2D live footage.
- **Speed Ramping & Transitions**: Scripted time remapping, crossfades, wipes, and glow filters.
- **Motion Tracking**: Camera stabilization or attaching graphic callouts to tracked video points.

## Headless Execution Pattern
Run Python scripts inside Blender without opening the GUI:
```bash
blender --background --factory-startup --python-exit-code 1 --python script.py -- --out output.mp4
```

## VSE Scripting Boilerplate (Python / `bpy`)
```python
import bpy, os, sys

# Initialize blank sequencer scene
scene = bpy.context.scene
scene.render.fps = 30
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

if not scene.sequence_editor:
    scene.sequence_editor_create()

seq = scene.sequence_editor.sequences

# Add video strip on Channel 1
movie_strip = seq.new_movie(
    name="MainFootage",
    filepath="path/to/clip.mp4",
    channel=1,
    frame_start=1
)

# Add text overlay on Channel 2
text_strip = seq.new_effect(
    name="TitleOverlay",
    type='TEXT',
    channel=2,
    frame_start=1,
    frame_end=90
)
text_strip.text = "PRODUCED WITH BLENDER PYTHON"
text_strip.font_size = 64
text_strip.location[0] = 0.5
text_strip.location[1] = 0.15

# Output settings
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = os.path.abspath("output_video.mp4")

# Render animation
bpy.ops.render.render(animation=True)
```

## Best Practices
- **Inspect Source Media**: Check frame rates, timebases, and audio sampling rates before creating sequencer strips.
- **Audio Muxing**: Explicitly map audio channels when rendering final MP4 deliverables; verify audio loudness with FFmpeg `loudnorm`.
- **Channel Discipline**: Keep raw video on Channel 1, B-roll on Channel 2, graphic overlays on Channel 3, and audio tracks on Channel 5+.
