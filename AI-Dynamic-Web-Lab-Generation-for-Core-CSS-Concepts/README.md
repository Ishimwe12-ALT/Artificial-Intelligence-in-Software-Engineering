# AI: Dynamic Web Lab Generation for Core CSS Concepts

## Objective

This task demonstrates the use of sequential and contextual AI prompting to
generate complex, interactive single-file HTML/CSS/JS applications that
visualize core CSS concepts: the Box Model and modern layout systems
(Flexbox and Grid).

## AI Tool Used

[e.g. Gemini with Canvas / ChatGPT / Claude]

## Files in this folder

| File | Description |
|---|---|
| `box-model-refined.html` | Interactive CSS Box Model lab with side-specific (top/right/bottom/left) sliders for margin, padding, and border, plus a corner-radius slider and a display-property dropdown. Generated from an initial prompt, then refined with a follow-up prompt in the same AI session. |
| `flexbox-grid-playground.html` | Interactive playground for comparing Flexbox and Grid layouts. Dropdowns let you switch `display`, `flex-direction`, `justify-content`, `align-items`, and `grid-template-columns` in real time on a container with 5 child items. |

## Workflow

1. **Initial prompt** — asked the AI to generate a two-box CSS Box Model
   visualizer with sliders for padding, margin, border-width, and width,
   plus a display-property dropdown, updating in real time via JavaScript.
2. **Refinement prompt** — in the same conversation (so the AI retained
   context), asked it to upgrade the single sliders into per-side
   (top/right/bottom/left) controls for margin, padding, and border, and
   add a corner-radius slider.
3. **Flexbox/Grid prompt** — a separate, new prompt asking for a container
   with 5 items and dropdowns to control `display`, `flex-direction`,
   `justify-content`, `align-items`, and `grid-template-columns`.

## How to view

Open any of the `.html` files directly in a browser — each is fully
self-contained (HTML, CSS, and JS in one file, no external dependencies).

## Reflection

See the Google Doc submission for the full reflection on learning efficacy
and the AI iterative workflow.
