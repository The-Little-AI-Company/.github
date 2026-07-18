# The Little AI Company visual-system specification

Status: canonical  
Owner: The Little AI Company  
Applies to: company website, GitHub, product pages, release notes, social media,
documentation, presentations, and downloadable brand assets

## 1. Strategic role

The owl is the company's primary distinctive visual asset. The mark creates
recognition at small sizes; the illustration library creates personality,
continuity, and a visual world that competitors cannot reproduce with a generic
AI gradient, robot, brain, spark, or chat bubble.

The system should feel like a small, capable software workshop:

- useful before impressive;
- relaxed without being careless;
- skeptical without being cynical;
- technical without looking corporate;
- warm without becoming childish.

Hollis, the Little AI Company owl, is the company's original visual signature.
`CHARACTER.md` owns his public story and voice; this document owns his visual
identity and production rules.

## 2. Asset hierarchy

### Tier 1 — identity

These assets identify the company and change rarely:

- owl-head mark;
- one-color, reversed, grayscale, and silhouette mark variants;
- horizontal and compact company-name lockups;
- avatar and favicon exports.

Use Tier 1 assets for identity, not storytelling.

### Tier 2 — character

The full owl communicates the company's personality. Canonical anatomy:

- half-lidded eyes with a calm, observant expression;
- espresso-brown feather mass and outline;
- cream facial discs, muzzle, and shirt;
- faded-rust cardigan;
- muted-teal trousers;
- mature proportions and grounded posture;
- practical wooden, paper, metal, and ceramic props.

The owl may look busy, curious, quietly amused, or satisfied. It must never look
drunk, manic, aggressive, infantile, mystical, or smug.

### Tier 3 — scenes

Scenes connect the owl to a specific job. Every scene needs one dominant action
and no more than three supporting props. A scene must remain legible at 160 CSS
pixels and should still read in silhouette at 64 pixels.

Canonical scene families:

| Family | Scenes | Primary use |
| --- | --- | --- |
| Welcome | welcome, coffee, celebrating | company, community, launches |
| Build | building, planning, debugging, testing | product and engineering |
| Knowledge | writing, research, teaching, presenting | guides and explanation |
| Trust | checking, protecting, filing, memory | safety, evidence, memory |
| Movement | relay, connecting, shipping | handoffs, integrations, releases |

## 3. Composition grammar

- Default canvas: square `1024 × 1024`.
- Keep the complete subject inside an 8% safe area.
- Use a centered or slightly asymmetrical editorial composition.
- Preserve a single clear focal action.
- Prefer three-quarter or front-facing views.
- Props must be ordinary, tactile objects: workbench, laptop, paper, pencil,
  index card, folder, file box, book, parcel, lock, cable, test rig, screen.
- Screens, papers, boards, cards, folders, and parcels contain no readable text.
  Simple unlabeled diagrams are allowed when they are the focal action.
- No floating interface chrome or decorative pseudo-data.
- No environmental background is baked into a reusable pose.
- No cast shadow, floor plane, glow, particle field, or vignette.

## 4. Illustration treatment

- Medium: crisp editorial line illustration.
- Line color: Espresso `#2B2118`.
- Line behavior: confident, slightly hand-drawn, consistent visual weight.
- Fill behavior: flat colors with restrained printed-paper texture only.
- Shading: minimal, warm, and subordinate to the silhouette.
- Detail: enough to reward large use, never enough to collapse at small size.
- Output background: transparent.

The owl's wardrobe and core colors are invariants. Props can use neighboring
warm woods, grays, and creams, but may not introduce a competing neon palette.

## 5. Palette

| Token | Value | Role |
| --- | --- | --- |
| Espresso | `#2B2118` | outline, primary ink |
| Warm cream | `#F3EBDD` | light field |
| Paper white | `#FFFDF8` | surface and reversed detail |
| Faded rust | `#B85C38` | cardigan and warm accent |
| Muted teal | `#2D7A78` | trousers and secondary accent |
| Signal teal | `#205F5D` | accessible UI accent |
| Muted brown | `#6E6456` | supporting copy and neutral props |
| Charcoal | `#201A15` | dark field |

Do not recolor the owl to match individual products. Products inherit the
company owl; the owl does not inherit product palettes.

## 6. Typography

- Fraunces Black: company name and display headlines.
- Inter Regular/Bold: interface and body copy.
- JetBrains Mono: short technical labels only.

Logos and downloadable SVG lockups use outlined glyph geometry. Public webpage
copy remains live HTML text.

## 7. SVG production standard

Every canonical SVG must:

- use a `viewBox` and omit fixed `width` and `height`;
- contain vector geometry only;
- contain no embedded raster image, external reference, script, animation,
  filter, mask, clip-path dependency, or live font;
- include `role="img"`;
- remain parseable by the Python standard library XML parser;
- avoid duplicate IDs;
- use lowercase, descriptive, kebab-case filenames;
- render with transparent corners unless it is an intentional field asset;
- pass the repository exporter's SVG and manifest checks.

Pose SVGs use `512 × 512` viewBox coordinates and the filename:

`tlac-owl-<action>.svg`

Raster source masters use:

`tlac-owl-<action>-master.png`

Web derivatives use:

`tlac-owl-<action>-<size>.webp`

## 8. Required derivatives

Each approved scene produces:

- one canonical vector SVG;
- one transparent raster master;
- lossless transparent WebP at 320, 640, and 1024 pixels;
- inclusion in the pose proof sheet;
- inclusion in `MANIFEST.json`.

Website releases may copy the SVG and one WebP fallback. The canonical source
continues to live in this repository.

## 9. Accessibility

- Use useful alt text when the scene adds meaning.
- Use empty alt text when nearby copy already communicates the same idea.
- Never place essential instructions inside an illustration.
- Preserve at least 3:1 contrast for meaningful non-text UI graphics.
- Do not use color alone to distinguish mark variants or scene categories.
- Respect reduced-motion preferences if an SVG is animated in a consuming
  product; canonical assets remain static.

## 10. Prohibited visual language

Do not use:

- robots, androids, cyborg parts, circuit-board feathers, or glowing eyes;
- brains, magic sparks, holograms, AI badges, neural-network diagrams, or
  floating chat bubbles;
- school crests, esports framing, capes, crowns, wizard props, or lab coats;
- alcohol, intoxication cues, smoking, or drug references;
- unapproved wardrobe, altered facial proportions, or unrelated mascot
  identities;
- logos, product names, slogans, watermarks, or readable text inside scenes;
- childish proportions, plush-toy treatment, glossy 3D, or stock-vector style.

## 11. Generation brief

New scene masters use the approved building and coffee masters as strict
identity references. Each prompt must state:

- same owl identity and mature proportions;
- same half-lidded expression, wardrobe, palette, and editorial line treatment;
- one named action and bounded prop set;
- flat solid `#FF00FF` chroma-key field;
- no shadow, text, logo, robot, circuitry, glow, or extra character;
- generous padding and complete subject visibility.

Generated masters are proposals until they pass visual inspection, alpha-edge
validation, vector tracing, proof-sheet review, and manifest verification.

## 12. Release gate

A visual-system release is complete only when:

1. source masters and SVGs exist for every declared scene;
2. the exporter finishes from a clean checkout;
3. the manifest contains every production asset with stable hashes;
4. the proof sheet shows no identity drift, clipped anatomy, unreadable props,
   magenta fringe, or accidental text;
5. consuming website files identify the exact source commit;
6. public pages use only approved assets.

This document governs production consistency. It does not claim trademark
registration or replace professional legal clearance.
