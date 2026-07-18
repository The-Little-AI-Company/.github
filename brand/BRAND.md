# The Little AI Company brand

The Little AI Company owl is calm, quietly wise, mildly skeptical, warm, and
competent when it counts. It gives the company a recognizable human-scale
personality without turning the products into toys.

## Identity

- **Primary mark:** the owl head. Use it for the GitHub organization avatar,
  favicon, site header, footer, and other small placements.
- **Mascot:** the full owl figure. The reusable library includes welcome,
  checking, writing, memory, coffee, building, filing, relay, and teaching
  poses. Use a pose only when it supports the surrounding message.
- **Name:** always write `The Little AI Company`.
- **Public story:** this is simply the Little AI Company owl. Describe it through
  its role here and the traits in this guide.

## Personality guardrails

The owl should feel:

- calm, not sleepy;
- skeptical, not sarcastic;
- relaxed, not intoxicated;
- experienced, not superior;
- approachable, not childish.

Do not add AI badges, circuitry, robot parts, glowing brains, wizard props,
sports-mascot aggression, or school-crest framing.

## Palette

| Token | Value | Use |
| --- | --- | --- |
| Espresso | `#2B2118` | Primary ink and outlines |
| Warm cream | `#F3EBDD` | Primary light surface |
| Faded rust | `#B85C38` | Cardigan and warm accent |
| Muted teal | `#2D7A78` | Secondary accent |
| Signal teal | `#205F5D` | Accessible small text and focus states |

Website tokens may use nearby values when needed for accessible contrast, but
the owl itself should not be recolored.

## Typography

Use the existing TLAC pairing:

- Fraunces for display headings and the company name.
- Inter for body copy and interface text.
- JetBrains Mono only for small technical labels.

## Asset map

- `source/tlac-owl-mark.svg` is the full-color vector mark.
- `source/tlac-owl-mark-one-color.svg`, `-reversed.svg`, `-grayscale.svg`, and
  `-silhouette.svg` are the required mark variants.
- `source/tlac-owl-lockup-horizontal.svg` and `-compact.svg` are the wordmark
  lockups.
- `source/tlac-owl-mascot-neutral.svg` and `source/poses/` contain vector mascot
  masters.
- `source/raster/` contains the reviewed transparent source renders used by the
  deterministic vector export.
- `source/fonts/` contains the exact Fraunces and Inter font files and their
  SIL Open Font License texts.
- `dist/avatar/` contains GitHub and app-avatar exports.
- `dist/favicon/` contains SVG, ICO, browser, and app-icon exports.
- `dist/lockups/` contains transparent PNG lockups.
- `dist/mascot/` contains optimized transparent WebP poses.
- `dist/social/` contains the Open Graph card and social square.
- `proofs/` contains review sheets, not production assets.
- `archive/` contains the pre-rollout organization avatar for rollback.
- `MANIFEST.json` records file sizes and SHA-256 hashes for the generated kit.

To rebuild from a clean checkout:

```powershell
python -m venv brand/.working/.venv
brand/.working/.venv/Scripts/python.exe -m pip install -r brand/requirements.txt
brand/.working/.venv/Scripts/python.exe brand/scripts/export_assets.py
```

The exporter parses every SVG, rejects embedded image payloads, outlines the
bundled fonts for portable lockups and profile art, verifies the exact company
name in both lockups, and regenerates the manifest.

## Provenance and licenses

- The owl artwork was generated for The Little AI Company with OpenAI image
  generation on 2026-07-18, reviewed by Jeff, and converted into SVG geometry
  by the pinned exporter. The applicable OpenAI terms state the user's output
  rights: <https://openai.com/policies/terms-of-use/>.
- Fraunces and Inter come from the Google Fonts repository and are distributed
  under the SIL Open Font License. The license texts ship beside the font files.
- VTracer `0.6.15` and FontTools `4.63.0` are MIT-licensed. Pillow `12.3.0`
  uses the MIT-CMU license. These tools are dependencies of the exporter and
  are not embedded in the exported artwork.
- The bounded collision-screening receipt is
  `proofs/similarity-screen-2026-07-18.md`. It is a preliminary screen, not
  professional legal clearance.

## Usage

- Give the mark at least 12.5% of its width as clear space.
- Use the warm-cream avatar export for GitHub so it remains legible in light and
  dark themes.
- Use the reversed mark on charcoal or other very dark surfaces.
- Do not place the full mascot below 120 CSS pixels.
- Use useful alt text when the pose communicates meaning. Use empty alt text
  when the owl is decorative beside text that already states the message.
- Do not stretch, rotate, tint, outline, or place the mark inside another badge.
