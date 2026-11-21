---
name: motion-overlays
description: >
  Brand motion graphics and overlays for creator videos and talking heads — Remotion / React component kit
  (key phrases, lower thirds, checklist chips, comparison cards, big words, quote boxes) timed to spoken words,
  rendered as transparent video or composited directly with face-safe and caption-safe layout rules.
  Use for "graphic overlays", "lower thirds", "on-screen cards", "package my video", or dressing up talking-head footage.
---

# Motion Overlays (Remotion Kit)

Add graphic overlays **on top** of existing footage without modifying the raw footage. Elements glide in smoothly, hold for the spoken phrase, and ease out cleanly.

## Core Component Catalog

| Component | Usage & Best Practices |
|---|---|
| `LowerThird` | Name + handle + role, first appearance or guest introduction. |
| `KeyPhrase` | Important thesis statement or quote (`*word*` gets accent highlight). |
| `ListReveal` | Step-by-step points or checklist items popping on each spoken beat. |
| `BeforeAfter` | Split comparison card illustrating a transformation or contrast. |
| `CountUp` | Rolling number counter for stats, revenue, followers, percentages. |
| `QuoteCard` | Emphasized personal quote or tweet-style social proof card. |
| `BigWord` | Single impactful keyword filling the frame for 1–2 seconds. |
| `ChapterTag` | Subtle header pill marking section changes. |

## Layout & Safety Doctrine (Non-Negotiable)

1. **Face-Safe Zone**:
   - In 16:9 compositions, keep graphic panels anchored to the outer 30% of the screen (left or right third), at least 80 px from the edge.
   - In 9:16 vertical reels, place cards in the lower-chest or upper safe zone, never over the chin, mouth, or eyes.
2. **Caption-Safe Clearance**:
   - Bottom-anchored elements must sit above the subtitle keep-out band (`bottom >= 220px` in 9:16).
3. **Pacing**:
   - One smooth `ease-in-out` move per element: glide in (0.35s), hold across the phrase (1.5s–3s), glide out (0.25s).
   - Avoid aggressive bouncing or rapid flashing that distracts from the speaker.
4. **Rendering**:
   - Render transparent overlay with ProRes 4444 (`codec: 'prores'`, `proresProfile: '4444'`) or WebM VP9 with alpha channel (`codec: 'vp9'`), ready for DaVinci Resolve, Premiere Pro, or direct FFmpeg composite.
