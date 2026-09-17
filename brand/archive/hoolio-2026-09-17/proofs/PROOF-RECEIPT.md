# TLAC owl brand proof receipt

Date: 2026-07-18

## Reviewed artifacts

- Mark proof: `tlac-mark-proof-sheet.png`
- SVG browser render: `svg-variant-render-1440.png`
- Mascot poses: `tlac-mascot-pose-sheet.png`
- Horizontal and compact lockups: `tlac-lockup-proof-sheet.png`
- GitHub profile desktop: `github-profile-desktop-1200x1000.png`
- GitHub profile narrow layout: `github-profile-mobile-390x844.png`
- GitHub profile preview source: `github-profile-preview.html`
- Bounded collision screen: `similarity-screen-2026-07-18.md`
- Previous organization avatar: `../archive/github-avatar-before-2026-07-18.png`
- Exact exported file inventory and hashes: `../MANIFEST.json`

## Checks

- Full-color, one-color, reversed, grayscale, and outline-free silhouette marks
  render from SVG geometry with no embedded image payload.
- The reversed mark remains readable on charcoal.
- Avatar and circular-crop proofs cover 20, 40, 64, and 200 px, with additional
  16 and 32 px checks.
- Horizontal and compact lockups use the exact company name.
- Five useful mascot poses are present as SVG masters and WebP derivatives.
- The GitHub profile preview has no clipped hero text or horizontal page
  overflow at 1200 and 390 px.
- Preview images load with nonzero natural width and the browser console has no
  warnings or errors.
- The old organization avatar is archived for rollback.
- Public publication remains held for Jeff's explicit proof approval.

## Rebuild

The clean-checkout commands and dependency licenses are recorded in
`../BRAND.md`. Running the exporter verifies every SVG and regenerates
`../MANIFEST.json`.
