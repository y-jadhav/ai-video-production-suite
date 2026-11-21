---
name: manim-motion-graphics
version: "1.0.0"
description: >
  Create programmatic motion graphics, kinetic typography, math/data animations, logo reveals,
  and formula explainers using Manim (Python). Use for "manim animation", "math video", "kinetic text",
  "data viz animation", "code motion graphics", or educational science and tech visual sequences.
---

# Manim Motion Graphics Skill

The Manim Motion Graphics skill creates vector-sharp, mathematically accurate animations and kinetic motion design using Python and the Manim engine.

## Core Capabilities
- **Kinetic Typography**: Word-by-word reveals, scale bounce, glitch text, and dynamic text effects.
- **Mathematical & Data Animation**: Plotting functions, geometric transformations, vectors, coordinate systems, and neural network diagrams.
- **Logo Reveals & Title Sequences**: Particle convergence, glowing outlines, and stylized brand sequences.
- **Counters & Stats**: Rolling number counters, percentage bars, and live data charts.

## Design Principles
- **Style**: Cohesive typography, dark backgrounds (`#0a0a0a` or `#16213e`), and high-contrast accents (Gold `#FFD700`, Cyan `#00FFFF`, Red `#FF3366`).
- **Anticipation & Overshoot**: Elements prepare before moving and settle with `ease_out_back` or `ease_out_cubic`.
- **Rhythm**: Paced to speech with visual holds on climax frames.

## Ready Templates

### 1. Kinetic Typography (Word-by-Word Reveal)
```python
from manim import *

class KineticTypography(Scene):
    def construct(self):
        self.camera.background_color = "#0e1117"
        words = ["THE", "FUTURE", "IS", "HERE"]
        colors = [WHITE, BLUE_C, WHITE, GOLD]

        for word, color in zip(words, colors):
            text = Text(word, font_size=96, color=color, weight=BOLD)
            text.scale(0)
            self.add(text)
            self.play(text.animate.scale(1), rate_func=rate_functions.ease_out_back, run_time=0.35)
            self.wait(0.25)
            self.play(text.animate.shift(UP * 1.5).set_opacity(0), rate_func=rate_functions.ease_in_cubic, run_time=0.25)
            self.remove(text)

        final = Text("THE FUTURE IS HERE", font_size=52, color=GOLD, weight=BOLD)
        self.play(Write(final), run_time=0.8)
        self.play(Indicate(final, scale_factor=1.1, color=WHITE))
        self.wait(1)
```

### 2. Animated Rolling Counter
```python
from manim import *

class CounterAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#161b22"
        counter = ValueTracker(0)

        number = always_redraw(lambda: Text(
            f"{int(counter.get_value()):,}",
            font_size=110,
            color=WHITE,
            weight=BOLD
        ))
        label = Text("COMMUNITY MEMBERS", font_size=28, color=BLUE_C)
        label.next_to(number, DOWN, buff=0.4)

        self.add(number, label)
        self.play(counter.animate.set_value(500000), run_time=2.5, rate_func=rate_functions.ease_out_cubic)
        self.play(Indicate(number, scale_factor=1.15, color=GOLD), run_time=0.5)
        self.wait(1)
```

### 3. Glitch & Brand Reveal
```python
from manim import *

class GlitchBrandReveal(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        brand = Text("ANTIGRAVITY", font_size=100, color=WHITE, weight=BOLD)
        red_copy = brand.copy().set_color(RED).shift(LEFT * 0.06 + UP * 0.03)
        blue_copy = brand.copy().set_color(BLUE).shift(RIGHT * 0.06 + DOWN * 0.03)

        self.add(red_copy, blue_copy, brand)
        for _ in range(4):
            self.play(red_copy.animate.shift(RIGHT * 0.12), blue_copy.animate.shift(LEFT * 0.12), run_time=0.06)
            self.play(red_copy.animate.shift(LEFT * 0.12), blue_copy.animate.shift(RIGHT * 0.12), run_time=0.06)

        self.play(red_copy.animate.move_to(brand.get_center()), blue_copy.animate.move_to(brand.get_center()), run_time=0.2)
        self.remove(red_copy, blue_copy)
        self.wait(1)
```

## Easing Reference
- **Entrance pop**: `rate_functions.ease_out_back`
- **Punchy move**: `rate_functions.ease_out_expo`
- **Smooth organic**: `rate_functions.ease_in_out_sine`
- **Gentle exit**: `rate_functions.ease_in_cubic`

## Execution
Run with: `manim -pql scene.py SceneName` (preview low quality) or `manim -qh --format=mp4 scene.py SceneName` (1080p high quality).
