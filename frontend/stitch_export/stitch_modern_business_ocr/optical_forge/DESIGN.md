---
name: Optical Forge
colors:
  surface: '#13131b'
  surface-dim: '#13131b'
  surface-bright: '#393841'
  surface-container-lowest: '#0d0d15'
  surface-container-low: '#1b1b23'
  surface-container: '#1f1f27'
  surface-container-high: '#292932'
  surface-container-highest: '#34343d'
  on-surface: '#e4e1ed'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e4e1ed'
  inverse-on-surface: '#303038'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#b9c8de'
  on-secondary: '#233143'
  secondary-container: '#39485a'
  on-secondary-container: '#a7b6cc'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#d4e4fa'
  secondary-fixed-dim: '#b9c8de'
  on-secondary-fixed: '#0d1c2d'
  on-secondary-fixed-variant: '#39485a'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#13131b'
  on-background: '#e4e1ed'
  surface-variant: '#34343d'
typography:
  display:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  container-max: 1280px
  margin-mobile: 16px
  padding-card: 20px
---

## Brand & Style

The design system is engineered for a high-performance developer environment, prioritizing speed, technical precision, and visual clarity. Drawing inspiration from industry leaders like Vercel and Linear, it employs a **Modern Technical** aesthetic that balances minimalist utility with sophisticated depth.

The UI targets developers and data engineers, evoking a sense of "Visual Intelligence." It feels like a high-end IDE: focused, unobtrusive, and highly responsive. The style leverages deep tonal layering, subtle glassmorphism for overlays, and sharp, high-contrast typography to ensure data—whether raw JSON or OCR confidence scores—remains the primary focus.

**Key Principles:**
- **Mechanical Precision:** Every element is aligned to a strict 4px/8px grid.
- **Atmospheric Depth:** Using "dark mode" as the primary canvas to reduce eye strain during long integration sessions.
- **State-Driven Feedback:** The UI breathes through motion and color shifts during the OCR lifecycle (upload to completion).

## Colors

This design system utilizes a sophisticated **Dark Mode** palette centered around Deep Indigo and Slate.

- **Primary Canvas:** The background uses a near-black Slate (`#020617`), providing maximum contrast for white text and vibrant accents.
- **Accent Indigo:** Reserved for primary actions, progress indicators, and active states.
- **OCR Lifecycle Palette:** 
    - **Idle:** Neutral slate for inactive dropzones.
    - **Dragging:** Bright indigo glow to signify interaction readiness.
    - **Uploading/Processing:** Sky blue and Purple for active, non-final states.
    - **Completed/Error:** Semantic Green and Red for finality and troubleshooting.
- **Glassmorphism:** Overlays use a semi-transparent version of the surface color (`rgba(15, 23, 42, 0.7)`) with a 12px background blur.

## Typography

The typography system is built for legibility and technical hierarchy. We use **Geist** for its neutral, modernist qualities and high readability in dense UI layouts.

- **Code & Metadata:** All OCR output, JSON payloads, and confidence scores must use **JetBrains Mono**. This differentiates data from UI controls.
- **Hierarchy:** High-contrast ratios between headers and body text. Headers use tight tracking (letter-spacing) to feel "engineered" and sturdy.
- **Labels:** Small caps with increased tracking are used for secondary metadata and table headers to provide structure without visual weight.

## Layout & Spacing

The layout follows a **Hybrid Grid** system. While the dashboard uses a fluid 12-column grid for flexibility, internal components and code editors follow a strict 8px rhythmic spacing.

- **Dashboard Layout:** 12 columns with 24px gutters. Sidebars are fixed at 280px on desktop to ensure consistent navigation.
- **Density:** High information density is encouraged. Use `padding-card` (20px) to separate logic blocks.
- **Mobile Reflow:** On mobile, columns collapse to a single stack, margins reduce to 16px, and sidebars transform into a bottom-sheet or full-screen overlay.

## Elevation & Depth

Hierarchy is established through **Tonal Layering** and **Glassmorphism** rather than traditional heavy shadows.

- **Base Layer:** Background (`#020617`).
- **Surface Layer:** Elevated cards and containers use `#0f172a` with a 1px solid border of `#1e293b`.
- **Active Layer:** Elements like modals or floating tooltips use backdrop filters (`blur(12px)`) and a subtle inner-glow (1px white at 5% opacity) to appear "closer" to the user.
- **Shadows:** Only used for floating menus. Use a sharp, multi-layered shadow: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`.

## Shapes

The shape language is "Modern Soft." While the brand is technical, the use of larger radii prevents the UI from feeling aggressive or dated.

- **Primary Components:** Buttons, inputs, and small cards use a **12px (`rounded-lg`)** radius.
- **Containers:** Large upload dropzones and main dashboard panels use a **16px (`rounded-xl`)** radius.
- **Icons:** Enclosed in 8px containers for a cohesive, geometric look.

## Components

### Buttons
- **Primary:** Indigo background, white text, 12px radius. Subtle scale-down (0.98) on click.
- **Secondary:** Ghost style. Transparent background with a `#1e293b` border.

### OCR Dropzone & States
- **Idle:** Dashed border (`#1e293b`). Gray icon.
- **Dragging:** Border transitions to solid Indigo. Background gains a 5% Indigo tint.
- **Uploading:** Display a thin (2px) indeterminate progress bar at the top of the container.
- **Processing:** Pulsing opacity animation (0.7 to 1.0) on the uploaded file thumbnail.
- **Completed:** Success green border, checkmark icon, and a "View JSON" button appearing.

### Input Fields
- Dark slate background. Focus state: 1px Indigo border and a 2px outer glow (`rgba(99, 102, 241, 0.2)`).

### Data Chips
- Small, 13px JetBrains Mono text. Background matches the state color (e.g., green for 'High Confidence') at 10% opacity.

### Code Editor
- Integrated Monokai-inspired theme. Line numbers in slate. Active line highlighted with a subtle `#1e293b` background.