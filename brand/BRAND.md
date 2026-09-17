# The Little AI Company brand

Adopted 2026-09-17. The previous owl identity (Hoolio) is retired and kept
under `archive/hoolio-2026-09-17/` for reference. Do not reuse it.

## Mark

The mark is a rabbit skull: two upright ears, round eye sockets, a nasal cut,
two front teeth. One flat color, no outline, no gradient. It reads at 16 px.

| File | Use |
| --- | --- |
| `skull-bunny/skull-bunny-mark.svg` | Ink mark on a transparent background. Default. |
| `skull-bunny/skull-bunny-mark-reversed.svg` | Bone mark for dark surfaces. |
| `skull-bunny/favicon.svg` | Mark that switches ink and bone with the viewer's color scheme. |
| `skull-bunny/avatar-*.png` | GitHub organization avatar, bone background. Upload `avatar-1024.png`. |
| `skull-bunny/avatar-dark-1024.png` | Avatar for dark contexts, ink background. |
| `skull-bunny/favicon-*.png`, `favicon.ico` | Browser and app icons, transparent. |
| `../profile/assets/hero.svg` | The organization profile banner. |

`skull-bunny/SHA256SUMS` lists the hashes of every raster export.

Rules:

- Keep the mark in one color. Never add gradients, outlines, glow, or a face.
- Keep the whole mark. Do not crop to the ears or the eyes.
- Do not rotate it, tilt it, or place it inside a circle or a shield.
- Leave clear space around it of at least one ear width.

## Palette

| Token | Value | Use |
| --- | --- | --- |
| Ink | `#111111` | Text, the mark on light surfaces, dark surfaces |
| Bone | `#EDE9E0` | Light surface, the mark on dark surfaces |
| Concrete | `#8A8A85` | Secondary text, rules, disabled states |
| Safety orange | `#FF5A1F` | One accent per view: links, the active state, one badge color |
| Steel | `#2A2D31` | Raised panels on dark surfaces |

Use safety orange once per view. If two things are orange, one of them is
wrong.

## Type

- Monospace for headings, labels, navigation, and badges. Prefer the system
  monospace stack: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.
  If a web font is needed, use JetBrains Mono.
- A plain grotesk for body text. Inter is fine.
- Headings in caps with letter spacing. Body text in sentence case.

## Badges

Use [shields.io](https://shields.io) with these parameters on every badge:

```text
style=flat-square&labelColor=111111
```

Color the value side `EDE9E0` for facts (license, site) and `FF5A1F` for
versions. A build status badge keeps the shields.io state colors, since green
and red carry the fact. Keep badges on one line under the title. No emoji in
badges or headings.

## Name

Write `The Little AI Company` in prose. In the mark's lockup and in monospace
headings, write `THE LITTLE AI COMPANY`. Do not abbreviate to TLAC in public.

## Voice

Say what the tool does and what it does not do. Name limits before claims.
State versions and status as they are. No hype words, no exclamation points,
no mascot dialogue. The skull bunny is a mark, not a character.
