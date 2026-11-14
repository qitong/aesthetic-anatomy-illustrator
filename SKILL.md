---
name: aesthetic-anatomy-illustrator
description: Generate medical aesthetics anatomical illustrations, facial muscle biomechanics overlays, volume loss and fat pad diagrams, wrinkle mechanisms, retaining ligaments, vascular danger zones, and histological skin cross-sections. Use when the user asks to create cosmetic dermatology visuals, facial anatomy infographics, botox/filler injection anatomical guides, or prompts and HTML/SVG annotation layouts for Gemini, ChatGPT (GPT-4o), or Hunyuan (Hy4). When the user supplies identifiable clinical photographs, apply the mandatory local de-identification (eye-occlusion bar) workflow before any image generation.
---
# Aesthetic Anatomy Illustrator

Generate clinical-grade, high-fashion medical aesthetics (医美) anatomical illustrations combining photorealistic East Asian beauty portraits with semi-transparent anatomical overlays and precision UI typography.

## When to Use

- User asks to generate medical aesthetics anatomical diagrams (医美解剖图), facial muscle biomechanics (肌肉力学/拮抗关系), or anti-aging visuals.
- User wants visuals for wrinkles (动态纹/静态纹), facial volume/fat pads (浅层/深层脂肪分室/脂肪垫), retaining ligaments (支持韧带卡压), contour/bone resorption (轮廓固定/骨相), vascular danger zones (面部危险血管网), or skin problems (黑眼圈/色斑/胶原重塑).
- User needs structured prompts for image generation models (Gemini, ChatGPT/GPT-4o, Hunyuan/Hy4) or ready-to-render HTML/SVG infographic templates for leader-line annotations.

## Core Visual Paradigms

Route every user request into one or more of the 4 clinical aesthetic visual paradigms:

1. **Type A: Biomechanical Vector Overlay (生物力学拮抗图)** — Template: `templates/type_a_biomechanics_overlay.html`
   - **Target**: Dynamic wrinkles & neuromodulator (Botox) mechanisms (e.g., glabella frown lines, forehead lines, crow's feet, jaw slimming, Nefertiti neck lift).
   - **Visual**: Close-up portrait + semi-transparent target muscles + directional force arrows (warm yellow/orange for elevator muscles, cool blue/cyan for depressor/contraction muscles).
2. **Type B: Multi-Layer Anatomical Cutaway (深/浅层脂肪分室、韧带与骨相透视解剖图)** — Template: `templates/type_b_layered_cutaway.html`
   - **Target**: Superficial fat compartments (nasolabial, medial cheek, middle cheek, jowl), deep fat compartments (SOOF, DMCF, Ristow's pyriform space, buccal fat), retaining ligaments (ORL, zygomatic, maxillary, masseteric, mandibular), SMAS layer, and periosteum volume loss.
   - **Visual**: Split-face or localized feather-edged transparency showing clearly demarcated pale-golden superficial fat lobules, amber-gold deep fat pads beneath semi-transparent muscles, or pearlescent-white ligament tethers blending cleanly into flawless skin.
3. **Type C: Full-Face Callout Grid Infographic (全景多维卡片导览图)** — Template: `templates/type_c_callout_grid.html`
   - **Target**: Comprehensive facial assessment (e.g., lower-face contour, salivary glands vs. muscles, full-face anti-aging targets).
   - **Visual**: Left-side beauty portrait with white anchor dots and dual-stroke leader lines connecting to a right-side grid of 4-7 rounded cards showing localized anatomical close-ups and clinical notes.
4. **Type D: Clinical Macro + 3D Histology PIP (宏观表征+微观组织学画中画)** — Template: `templates/type_d_histology_pip.html`
   - **Target**: Dermatology, pigmentation, vascular dark circles, collagen remodeling, energy-based devices (lasers/RF/ultrasound), or multi-layer needle/cannula depth cross-sections.
   - **Visual**: Side-by-side or single macro clinical skin view with a rounded bottom-right Picture-in-Picture (PIP) card displaying a 3D cross-section of epidermis, dermis, subcutaneous fat, SMAS, and periosteum.

## Privacy Gate: Real Patient Photos (MANDATORY)

**Trigger**: the user supplies a real clinical photograph with an identifiable face (e.g. `photos/`, case-report images, standardized frontal / oblique / profile shots). When in doubt, treat any uploaded face photo as identifiable and apply this gate.

**Non-negotiable rules**

1. **Never upload the original photo** to a cloud image model or any external service. No exceptions without explicit user authorization.
2. **De-identify locally first**: add an opaque eye-occlusion bar, then use **only the masked copy** as the image-to-image input.
3. **Keep the mask in the final artwork** as a visible compliance marker; prompt the model not to reconstruct eyes, irises or any identifiable eye feature.
4. **Realistic anatomy comes from the generated base image; local vector SVG only does annotation** (labels, leader lines, anchors, zone cards, legends). Never substitute flat vector blobs for muscle / bone / ligament rendering — that collapses into a schematic and breaks visual consistency with the rest of the series.
5. **Do not silently swap in a generated generic look-alike portrait.** It is a fallback only when the user explicitly chooses it; the default is the de-identified original, preserving that subject's real face shape and anatomy.

**Procedure** (full spec: [`references/deidentification_and_realism.md`](references/deidentification_and_realism.md))

1. Run `scripts/deidentify_portrait.py <input> --out <masked.png>` to add the bar. Default bar covers only the eye fissures + upper nasal bridge, preserving brows, infraorbital skin, nose, mouth and chin so the orbital rim and orbicularis oculi stay visible. Use `--wide` for stricter masking when the target is not the orbital region.
2. Inspect the masked image: eyes fully covered, no brow / infraorbital structure lost.
3. Image-to-image with `input_fidelity=high`. The prompt must: preserve face shape / hairline / skin tone / head pose / background; **keep the black bar exactly as it is**; forbid realistic eyeballs / irises / identifiable eye features; render the paradigm's anatomy; include the Mandatory Aesthetic Guardrails from Step 2. **State the credit cost before generating.**
4. Crop any fixed bottom-right tool watermark if present, resize to the layout's portrait window, then **re-calibrate all annotation coordinates against the new base image using `scripts/calibrate_grid.py`** — never reuse coordinates from an earlier image.
5. Compose the Track 2 HTML/SVG overlay + print-resolution PNG. Add a `已脱敏 / DE-IDENTIFIED` badge, a legend entry for the bar, and the disclaimer.
6. Remind the user that publication still requires informed consent: a bar removes only eye features, and face shape may remain identifiable.

**Gotcha**: an eye bar conflicts with periorbital anatomy diagrams. Keep it narrow by default; widen only when the orbital region is not the target or the user asks for stricter masking.

---

## Workflow Steps

### Step 0: Interactive Anatomical Verification (MANDATORY for Fine / Deep Structures)

Generic image models easily render macro muscles and bones, but **frequently hallucinate the location and shape of fine or deep structures** (superficial fat compartments, deep fat pads, retaining ligaments, vascular danger zones, and layered planes).

Whenever the user requests **fat pads (脂肪垫/脂肪室), deep volume (深层容积), ligaments (韧带), tear troughs / nasolabial / midcheek grooves (泪沟/法令纹/印第安纹/木偶纹), or injection layers**, **DO NOT blindly generate an image immediately**. First consult [`references/fine_anatomy_spatial_atlas.md`](references/fine_anatomy_spatial_atlas.md) and confirm with the user:

1. **Exact Sub-Compartments & Layer**:
   - Example for "浅层脂肪垫 (Superficial Fat Pads)": Clarify whether the focus is the **Midface Superficial Fat Triad** (*Nasolabial fat* 鼻唇沟浅层脂肪室 + *Medial cheek fat* 内侧颊浅层脂肪室 + *Middle cheek fat* 中间颊浅层脂肪室), or also includes *Infraorbital fat* (眶下浅脂), *Jowl fat* (口角下羊腮脂肪室), and *Lateral temporal-cheek fat* (外侧颞颊脂肪室).
   - Clarify whether to pair it with **Deep Fat Pads** (*Medial/Lateral SOOF*, *DMCF* 深层内侧颊脂垫, *Ristow's pyriform space* 梨状孔深层空间) or **Retaining Ligaments** (*ORL* 眼轮匝肌支持韧带, *Zygomatic ligament* 颧皮韧带, *Mandibular ligament* 下颌骨支持韧带) to illustrate tethering and sagging mechanics.
2. **Visual Layout & Comparison Mode**:
   - Confirm whether they prefer a **Split-Face Comparison** (e.g., Left half = Deep fat & bone foundation vs. Right half = Superficial fat mosaic & ligament tethers) or a **Localized Single-Side Cutaway Window**.
3. **Reference Atlas Preview (Optional but Recommended)**:
   - Offer to run `python scripts/build_anatomy_guide.py --preset <preset> --out guide_preview.png` so the user can verify the exact compartment geometry before invoking cloud image generation.

---

### Step 1: Clinical & Anatomical Mapping (Consult the Dual Reference Libraries)

Map the user's clinical scenario to exact anatomical structures, **plus their geometric shapes, 4-sided boundaries (Superior/Inferior/Medial/Lateral), and tissue color codes** using:
- [`references/anatomy_prompt_dictionary.md`](references/anatomy_prompt_dictionary.md) (Master bilingual lookup table)
- [`references/fine_anatomy_spatial_atlas.md`](references/fine_anatomy_spatial_atlas.md) (Exact spatial boundaries & geometry for fat compartments, ligaments, vessels, and layers)

Key anatomical groups:
- **Upper Face & Periorbital (上面部与眼周)**:
  - *Frontalis* (额肌 - 垂直肌纤维), *Corrugator supercilii* (皱眉肌 - 斜向内下), *Procerus* (降眉间肌 - 眉心垂直), *Orbicularis oculi* (眼轮匝肌 - 同心环形), *Temporalis* (颞肌 - 扇形向下), *ROOF* (眉下深层脂肪垫).
- **Midface Superficial & Deep Fat Compartments + Retaining Ligaments (中面部深浅脂肪室与支持韧带)**:
  - **Superficial Fat Mosaic (浅层奶油金黄分叶脂肪室)**: *Nasolabial fat* (鼻唇沟脂肪室 — **斜向狭长泪滴形，紧贴鼻翼外侧与法令纹内上方，绝不越过法令纹到上唇**), *Medial cheek fat* (内侧颊脂肪室 — **倒三角形，位于苹果肌中央、鼻唇沟脂肪室外侧**), *Middle cheek fat* (中间颊脂肪室 — **纵向长板形，位于颧大肌浅面**).
  - **Deep Fat Pads (深层琥珀金黄骨膜上脂肪垫，位于表情肌深面)**: *Medial & Lateral SOOF* (眼轮匝肌下脂肪垫 — **紧贴眶下缘 ORL 韧带下方的骨膜表面，绝不画成眼袋**), *Deep Medial Cheek Fat - DMCF* (深层内侧颊脂垫 — **提上唇肌深面、上颌骨前壁骨膜上**), *Deep Pyriform / Ristow's space* (梨状孔外侧深层空间 — **鼻翼基底正下方骨膜上**).
  - **Retaining Ligaments (珍珠白高张力骨皮韧带束)**: *Orbicularis retaining ligament - ORL* (眼轮匝肌支持韧带 — **沿眶下缘弧形卡压出泪沟**), *Zygomatic cutaneous ligament* (颧皮韧带 — **眶下缘下 1cm 斜行卡压出印第安纹**), *Maxillary ligament* (上颌支持韧带).
- **Lower Face, Glands, Ligaments & Neck (下面部、唾液腺、韧带与颈部)**:
  - *Masseter* (咬肌), *Buccal fat pad* (颊脂垫 - 咬肌前缘深部平滑脂肪球), *Superior & Inferior Jowl fat* (口角下/下颌缘羊腮浅层脂肪室), *Mandibular ligament* (下颌骨支持韧带 - 固定于羊腮内侧形成木偶纹下端卡压槽), *Depressor anguli oris - DAO* (降口角肌), *Mentalis* (颏肌), *Platysma* (颈阔肌), *Parotid gland* (腮腺 - 耳前米黄色桑葚状腺泡结构，严禁画成红肌肉), *Submandibular gland* (颌下腺).
- **Vascular Danger Zones & Nerves (高危血管与神经)**:
  - *Facial-to-Angular artery* (面动脉-内眦动脉 - 下颌缘咬肌前缘上行，经口角外侧 1cm 沿鼻唇沟贴鼻侧壁上行), *Supratrochlear & Supraorbital arteries* (滑车上/眶上动脉), *Superficial temporal artery* (颞浅动脉), *Infraorbital & Mental foramina* (眶下孔与颏孔神经束).

---

### Step 2: Generate Dual-Engine Visual Prompts (with Spatial & Negative Constraints)

Always provide two prompt versions so the user can directly trigger native generation or paste into their preferred model.

> **CRITICAL RULE FOR FAT PADS & DEEP STRUCTURES**: Never write vague phrases like `"show superficial fat pads on the cheek"`. You MUST copy the **exact geometric shape, 4-sided boundary descriptions, tissue color distinction, and negative constraints** from [`references/fine_anatomy_spatial_atlas.md`](references/fine_anatomy_spatial_atlas.md)!

1. **Direct Native Generation / English Master Prompt (for Gemini / ChatGPT / Midjourney)**
   - **Mandatory Aesthetic Guardrails**: Always include `"high-end cosmetic dermatology visual style, clean aesthetic pale-pink striated muscle fibers, plump pale-golden lobular superficial fat compartments separated by thin pearlescent-white fibrous septa, amber-gold deep supraperiosteal fat pads, soft feather-edged transparency blending seamlessly into flawless East Asian female skin, non-gory, bloodless, studio beauty lighting, 8k medical illustration. Absolutely no text, no letters, no labels, no numbers, no watermark, no UI."`
2. **Chinese Structured Prompt (for Hunyuan Hy4 / Domestic Models)**
   - Use clear spatial directives, geometric shapes, boundaries, and anatomical terminology in Chinese.

---

### Step 2.5: Spatial Guide Image-to-Image Control (For Complex Fat / Ligament / Vessel Requests)

When generating **superficial/deep fat compartments, retaining ligaments, or vascular danger zones**, pure text prompts alone can still drift by 1-2 cm on the face. Use [`scripts/build_anatomy_guide.py`](scripts/build_anatomy_guide.py) to physically lock the anatomical positions:

1. **Standalone Reference Atlas Mode** (when generating from scratch):
   ```bash
   python scripts/build_anatomy_guide.py --preset superficial_fat --out scratch_atlas_ref.png
   ```
   Pass `scratch_atlas_ref.png` in `ImagePaths` (or reference image input) when calling the image generator, instructing the model:
   `"Use the compartment layout and geometric boundaries shown in the reference diagram to place each anatomical fat compartment in its exact facial zone..."`

2. **Portrait Overlay Mode** (when working from a de-identified clinical photo or an existing clean portrait):
   ```bash
   python scripts/build_anatomy_guide.py --base front_deidentified.png --preset midface_fat_ligaments --side right --alpha 0.38 --out front_guided.png
   ```
   Pass `front_guided.png` to image-to-image generation and instruct the model to convert the semi-transparent colored guide regions into photorealistic 3D lobular adipose compartments and pearlescent fibrous ligament bands within those exact boundaries.

---

### Step 3: Post-Generation Anatomical Fidelity QA Loop (MANDATORY Before Annotation)

**Never skip directly from image generation to HTML/SVG annotation.** Immediately inspect the generated image with `view_file` against the **Vision QA Checklist** in [`references/fine_anatomy_spatial_atlas.md`](references/fine_anatomy_spatial_atlas.md#L127-L148):

1. **Position & Four-Boundary Check**:
   - Did the *Nasolabial fat compartment* stay strictly lateral to the nasal ala and above the nasolabial fold crease? (If it spilled onto the upper lip, nasal bridge, or temple → **REJECT**).
   - Did *SOOF* stay on the infraorbital bone below the *ORL* ligament? (If it turned into an intra-orbital lower-eyelid bag → **REJECT**).
2. **Morphology & Septation Check**:
   - Are individual fat compartments separated by visible white fibrous septa with their distinct shapes (teardrop vs. inverted triangle vs. vertical rectangle), rather than merged into one amorphous yellow blob?
3. **Self-Correction on Failure**:
   - If the generated anatomy fails the QA check, **do not deliver it**. Run `scripts/build_anatomy_guide.py` to generate a spatial guide overlay and re-generate with explicit boundary corrections, or ask the user to confirm adjustments.

---

### Step 4: Coordinate Calibration & Precision Annotation (Dual Track)

Once the anatomical base image passes Step 3 QA:

1. **Run the Coordinate Calibration Grid (`scripts/calibrate_grid.py`)**:
   - **Never guess SVG pixel coordinates by eye.** Run:
     ```bash
     python scripts/calibrate_grid.py <clean_base_image.png> --viewbox 1280 720 --out <base_grid_preview.png>
     ```
   - Inspect `<base_grid_preview.png>` using `view_file` to read the exact `(x, y)` coordinates of each anatomical target center, ligament line, and facial landmark.
2. **Compose the HTML/SVG Overlay (`templates/`)**:
   - **Track 1: One-Shot Native Text Prompting (直出带字版)**: Include explicit label instructions in the prompt if the user only wants a quick single-shot image.
   - **Track 2: Zero-Defect HTML/SVG Overlay Code (工业级图文合成版 - Recommended Default)**:
     - Select the matching template (`type_a_biomechanics_overlay.html`, `type_b_layered_cutaway.html`, `type_c_callout_grid.html`, or `type_d_histology_pip.html`).
     - Update the SVG `<line>` / `<polyline>` coordinates using the exact readings from `calibrate_grid.py`. All leader lines must use the **high-contrast dual-stroke style** (thick white under-stroke + crisp dark main stroke).
     - Render to 4K PNG via [`scripts/render_infographic.py`](scripts/render_infographic.py) (automatically uses zero-dependency local Chrome Headless first, falling back to Playwright):
       ```bash
       python scripts/render_infographic.py <custom_layout.html> <final_output_4k.png>
       ```
     - Visually inspect `<final_output_4k.png>` to verify that no leader lines cross awkwardly or miss their targets, then delete temporary `*_grid.png` scratch files.

---

## Prompt Templates by Paradigm

### Template 1: Type A (Muscle Biomechanics & Force Vectors)

```text
[Subject & Framing]: Extreme close-up / portrait of a young East Asian woman focusing on [Target Region, e.g., glabella and periorbital area], symmetrical face, flawless skin, neutral calm expression.
[Anatomical Overlay]: Seamless, semi-transparent medical illustration overlay on [Specific Area], revealing anatomically accurate [Target Structures, e.g., Frontalis with vertical fibers, Corrugator supercilii with oblique inward-downward fibers, and Procerus with vertical fibers]. Pale coral-pink muscle striation and pearlescent white tendon insertions blending softly into the surrounding skin.
[Biomechanics / Vectors]: Smooth 3D glowing translucent arrows overlaid on the muscle fibers: warm golden-yellow upward arrows along the [Elevator muscle] indicating lifting force, and cool ice-blue inward/downward arrows on the [Depressor muscle] indicating contraction force.
[Style & Quality]: High-end aesthetic medicine textbook illustration, non-gory, bloodless, clean clinical studio lighting, ultra-detailed 8k resolution. Absolutely no text, no letters, no numbers, no watermark.
```

### Template 2: Type B (Superficial vs. Deep Fat Compartments & Retaining Ligaments Cutaway)

```text
[Subject & Framing]: Frontal / 45-degree oblique portrait of a young East Asian woman, calm neutral expression, studio beauty lighting.
[Anatomical Cutaway Window]: Seamless feather-edged translucent anatomical cutaway across the mid-to-lower face.
- [Superficial Fat Mosaic]: Reveal the distinct superficial subcutaneous fat compartments arranged like a mosaic with thin pearlescent-white fibrous septa between them: (1) Medially, the elongated oblique teardrop-shaped Nasolabial fat compartment hugging the lateral nasal ala right above the nasolabial crease; (2) Centrally over the malar prominence, the inverted-triangle Medial Cheek fat compartment; (3) Laterally, the vertical rectangular Middle Cheek fat compartment; (4) Along the lower jawline lateral to the marionette fold, the ovoid Superior and Inferior Jowl fat compartments. Rendered as plump, pale-golden yellow lobular adipose tissue.
- [Deep Fat & Ligament Tethers]: Along the inferior orbital rim bone, show the curved pearlescent-white Orbicularis Retaining Ligament (ORL) and ~1cm below it the oblique Zygomatic cutaneous ligament. Deep to the translucent orbicularis oculi and levator muscles directly on the ivory maxilla bone, reveal the deeper amber-gold Medial/Lateral SOOF and triangular Deep Medial Cheek Fat (DMCF).
[Negative Constraints]: Do NOT merge the fat pads into a single round blob; do NOT place fat on the nasal bridge or upper lip; non-gory, bloodless, no text, no labels, no watermark, 8k medical illustration.
```

### Template 3: Type C (Full-Face Callout Grid Infographic)

```text
A professional medical aesthetics infographic layout (16:9 horizontal). Left side (40% width): A glamorous beauty portrait of a young East Asian woman with clean white anchor dots and thin leader lines on her temple, jaw angle, chin, and neck. Right side (60% width): A structured grid of 5-7 rounded beige information cards. Each card contains a dark-green header tag, brief clinical explanation text, and a close-up anatomical cutaway portrait showing the exact structure: (1) Temporalis muscle, (2) Masseter muscle, (3) Parotid gland (buff-yellow lobular acinar gland structure anterior to the ear, distinct from red muscle and smooth fat), (4) Depressor anguli oris & Mentalis, (5) Submandibular gland, (6) Platysma muscle along the neck. Clean editorial cosmetic clinic style, non-gory, 8k.
```

### Template 4: Type D (Macro Skin + 3D Histology PIP)

```text
Split-screen side-by-side medical dermatology comparison of an East Asian woman's close-up eye area. Left panel: Pigmented dark circles with brownish epidermal hyperpigmentation under the eye; bottom-right corner features a rounded rectangular Picture-in-Picture (PIP) inset showing a 3D histological skin cross-section with brown melanin granules densely accumulated in the basal epidermis and dermal-epidermal junction. Right panel: Vascular dark circles with bluish-purple undertint under the lower eyelid; bottom-right corner features a matching 3D skin cross-section PIP inset showing dilated red and blue capillary networks visible through thin dermis over yellow subcutaneous fat. High-end cosmetic dermatology visual, 8k.
```

---

## Gotchas

- **Avoid Gory Cadaver Aesthetics**: Without explicit modifiers like `"aesthetic pale-pink fibers, bloodless, seamless translucent overlay, cosmetic dermatology style"`, image models default to dark red, visceral surgical dissection. Always enforce the non-gory beauty guardrail.
- **Prevent Fat Compartment Drift & Blobbing**: Never prompt for `"facial fat pads"` generically. Always specify the **exact geometric shape, 4-sided boundaries, and inter-compartmental white septa** from [`references/fine_anatomy_spatial_atlas.md`](references/fine_anatomy_spatial_atlas.md), and use [`scripts/build_anatomy_guide.py`](scripts/build_anatomy_guide.py) when precise compartment placement is required.
- **Distinguish Glands, Superficial Fat, Deep Fat, and Muscles**:
  - Striated Muscles = `pale coral-pink striated muscle fibers`
  - Superficial Fat Compartments = `plump pale-golden yellow subcutaneous fat lobules above SMAS`
  - Deep Fat Pads = `flat amber-gold deep adipose cushions beneath muscle on the ivory bone surface`
  - Salivary Glands (*Parotid* 腮腺 / *Submandibular* 颌下腺) = `buff-yellowish lobular acinar glandular tissue (NOT red muscle, NOT smooth adipose fat)`
  - Retaining Ligaments & SMAS = `pearlescent ivory-white dense fibrous tethers / fascial sheet`
- **Correct Muscle Fiber Orientation**: Always specify fiber direction in prompts (e.g., *Frontalis* = vertical fibers; *Orbicularis oculi* = concentric circular fibers around eye; *Corrugator* = oblique inward-downward fibers) to prevent anatomically incorrect AI hallucinations.
- **Always Calibrate Coordinates with `calibrate_grid.py`**: Never guess `(x, y)` leader-line coordinates by eye on a newly generated or cropped portrait. Always run `scripts/calibrate_grid.py` and read the exact coordinates from the grid overlay.
- **Real Patient Photos Require the Privacy Gate**: Never send an identifiable face to an image model unmasked; see `## Privacy Gate: Real Patient Photos (MANDATORY)` above. Local de-identification is a prerequisite, not an optional nicety.
- **Vector Blobs Are Not Anatomy**: Flat SVG ellipses / color blocks are acceptable only as a declared zero-upload fallback or as a pre-generation spatial guide input (`build_anatomy_guide.py`). For publication-grade realism, generate the anatomical base image and let vector code handle annotations only. Always tell the user when a style downgrade is being made instead of silently switching.
