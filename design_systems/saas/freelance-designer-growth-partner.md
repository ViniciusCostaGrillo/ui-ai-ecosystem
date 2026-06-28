[Back to design systems](/design-systems)

freelance-designer-growth-partner-DESIGN.md

# Freelance Designer & Growth Partner

Freelance Designer Feature Section is designed for highlighting product capabilities and value points. Key features include reusable structure, responsive behavior, and production-ready presentation. It is suitable for component libraries and responsive product interfaces.

HTML Preview

freelance-designer-growth-partner.html

DESIGN.md

## Prompt context source

| Frontmatter | Value |
| --- | --- |
| **version** | "neuform" |
| **name** | "Freelance Designer & Growth Partner" |
| **description** | "Freelance Designer Feature Section is designed for highlighting product capabilities and value points. Key features include reusable structure, responsive behavior, and production-ready presentation. It is suitable for component libraries and responsive product interfaces." |
| **colors** | token group |
| **primary** | "#CCFF00" |
| **secondary** | "#7B61FF" |
| **accent** | "#CCFF00" |
| **background** | "#111111" |
| **surface** | "#18181B" |
| **text-primary** | "#CCFF00" |
| **text-secondary** | "#7B61FF" |
| **border** | "#27272A" |
| **typography** | token group |
| **display-lg** | token group |
| **body-md** | token group |
| **label-md** | token group |
| **spacing** | token group |
| **base** | "8px" |
| **gap** | "16px" |
| **card-padding** | "24px" |
| **section-padding** | "80px" |
| **rounded** | token group |
| **card** | "8px" |
| **pill** | "9999px" |

## Freelance Designer & Growth Partner

Source: Neuform Trending templates. Views: 499; favorites: 14; remixes: 13.

## Overview

The design aesthetic is high-contrast and authoritative, built upon a "Neon on Noir" core. The mood is premium and industrial, characterized by a vibrant neon-yellow accent against a deep, matte-black background. Composition relies on extreme vertical scale and negative space, anchored by a full-bleed, nested-frame structure that creates a "monitor-within-a-monitor" focus.

## Colors

* Primary Accent: #ccff00 (Neon Yellow/Lime) – used for hero typography, navigation, and core identity markers.
* Surfaces: #111111 (Matte Black) – used as the primary background for content containers.
* Secondary/Interactive: #7b61ff (Deep Purple) – reserved for primary action buttons (CTAs).
* Neutral/Atmospheric: White (Typography/UI icons) and custom gradients (black to transparent) for vignetting and text legibility.

## Typography

* Display: A massive, fluid headline utilizing `clamp(3rem, 10vw, 9rem)` with a tight line-height of 0.85 and negative letter-spacing (-0.04em). Applied in uppercase for impact.
* Body: A clean, system-stack sans-serif for optimal readability at smaller scales, utilizing generous line-height for contrast.
* Label: Uppercase, tracking-widest style (tracking-widest) used for metadata, nav links, and UI identifiers to maintain a technical, deliberate aesthetic.

## Layout

* Frame: The viewport acts as a secondary border, with padding (p-3 to p-8) defining a structural "gutter" that separates content from the edge.
* Container: A central flex-column architecture utilizes `flex-grow` to ensure content spans the full available height.
* Rhythm: Spacing is non-linear; the top of the container uses heavy vertical padding (12-24 units) to force the headline to the center-top, while the base employs auto-margins to anchor footer content to the bottom edge.

## Elevation & Depth

* Surface Recipe: The main container uses a custom "premium-surface" border—a 1px gradient (145deg, rgba(255,255,255,0.1) to black/0.5) applied via `mask-composite: exclude` to achieve a glass-like perimeter.
* Shadows: A high-intensity `shadow-2xl` is applied to the main wrapper to lift it from the background.
* Overlays: Moody photography is layered using a mix-blend-luminosity and a layered gradient vignette (gradient-to-r and gradient-to-t) to ensure text remains legible without sacrificing dark-mode intensity.

## Shapes

* Radius Hierarchy: Rounded-2xl to rounded-[2rem] is used for the primary container to soften the industrial black box.
* Geometry: Iconography and UI elements (buttons/chips) follow a strict pill-shape (full-radius).
* Identity: The logo mark utilizes a 2x2 grid system with 1px/2px corner radii, maintaining a pixel-perfect, modular design language.

## Components

* Hero: Staggered, overflow-hidden word segments that reveal from bottom-up.
* CTA: Fully rounded pills with hover-state transitions (300ms) to alternate colors for immediate feedback.
* Nav: Minimalist link-list with uppercase text; hover effects toggle from primary yellow to white to indicate active interaction.
* Metadata: Small, tight grid-based graphic markers used to identify the "author/partner" identity.

## Do's and Don'ts

* Do prioritize massive, tight-leading headlines to maintain the editorial, "poster" style.
* Do keep the background imagery at low opacity (approx. 60%) with a luminosty blend mode to ensure the neon-yellow text remains the hero.
* Don't drift from the primary color palette; only utilize purple for CTA components to avoid muddying the neon-yellow identity.
* Don't use standard drop shadows; leverage the 1px gradient mask method for a premium, edge-lit aesthetic.

## Motion

* Entrance: Hero text utilizes a vertical mask-reveal (`y: 100%` to `0%`) with `power4.out` easing, staggered by 0.1s.
* Sequence: Content elements at the base of the design (location, secondary links) employ a fade-in/slide-up reveal with a `power3.out` curve.
* Ambient: All hero imagery must include a long-duration (10s) slow-zoom effect (`scale 1.05` to `1.0`) to provide a subtle "living" quality without causing distraction.

Author

Meng To

Design system creator

1.3k

views

43

uses

dark mode

mode

Updated

June 27, 2026

Created April 28, 2026

Visual cards

Colors

Typography

Aa

Display Lg

BlinkMacSystemFont

64px / w500

Aa

Body Md

BlinkMacSystemFont

16px / w400

Aa

Label Md

JetBrains Mono

12px / w600

Spacing

Base8px

Gap16px

Card Padding24px

Section Padding80px

Radius

Card8px

Pill9999px

Motion

Levelmoderate

150ms200ms

Easingease

Hovertext / color

Mode

Background

Surface

ModeDark mode

Text#CCFF00

Muted#7B61FF

Surface

Cards

CardsButtonsForms