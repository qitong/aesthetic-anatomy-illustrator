---
name: aesthetic-anatomy-illustrator
description: Generate medical aesthetics anatomical illustrations, facial muscle biomechanics overlays, volume loss and fat pad diagrams, wrinkle mechanisms, and histological skin cross-sections. Use when the user asks to create cosmetic dermatology visuals, facial anatomy infographics, botox/filler injection anatomical guides, or prompts and HTML/SVG annotation layouts for Gemini, ChatGPT (GPT-4o), or Hunyuan (Hy4). When the user supplies identifiable clinical photographs, apply the mandatory local de-identification (eye-occlusion bar) workflow before any image generation.
---
# Aesthetic Anatomy Illustrator

Generate clinical-grade, high-fashion medical aesthetics (医美) anatomical illustrations combining photorealistic East Asian beauty portraits with semi-transparent anatomical overlays and precision UI typography.

## When to Use

- User asks to generate medical aesthetics anatomical diagrams (医美解剖图), facial muscle biomechanics (肌肉力学/拮抗关系), or anti-aging visuals.
- User wants visuals for wrinkles (动态纹/静态纹), facial volume/fat pads (面部容积/脂肪垫/韧带), contour (轮廓固定/骨相), or skin problems (黑眼圈/色斑/毛孔).
- User needs structured prompts for image generation models (Gemini, ChatGPT/GPT-4o, Hunyuan/Hy4) or ready-to-render HTML/SVG infographic templates for leader-line annotations.

## Core Visual Paradigms

Route every user request into one or more of the 4 clinical aesthetic visual paradigms:

1. **Type A: Biomechanical Vector Overlay (生物力学拮抗图)**
   - **Target**: Dynamic wrinkles & neuromodulator (Botox) mechanisms (e.g., glabella frown lines, forehead lines, crow's feet, jaw slimming, Nefertiti neck lift).
   - **Visual**: Close-up portrait + semi-transparent target muscles + directional force arrows (warm yellow/orange for elevator muscles, cool blue/cyan for depressor/contraction muscles).
2. **Type B: Multi-Layer Anatomical Cutaway (局部透视解剖图)**
   - **Target**: Deep/superficial fat pads, retaining ligaments, SMAS layer, periosteum volume loss, tear troughs, nasolabial folds.
   - **Visual**: Split-face or localized feather-edged transparency showing muscle fibers, pale-yellow fat compartments, or white ligament tethers blending cleanly into flawless skin.
3. **Type C: Full-Face Callout Grid Infographic (全景多维卡片导览图)**
   - **Target**: Comprehensive facial assessment (e.g., lower-face contour, salivary glands vs. muscles, full-face anti-aging targets).
   - **Visual**: Left-side beauty portrait with white anchor dots and leader lines connecting to a right-side grid of 4-6 rounded cards showing localized anatomical close-ups and clinical notes.
4. **Type D: Clinical Macro + 3D Histology PIP (宏观表征+微观组织学画中画)**
   - **Target**: Dermatology, pigmentation, vascular dark circles, collagen remodeling, energy-based devices (lasers/RF/ultrasound).
   - **Visual**: Side-by-side or single macro clinical skin view with a rounded bottom-right Picture-in-Picture (PIP) card displaying a 3D cross-section of epidermis, dermis, and subcutaneous fat.

## Privacy Gate: Real Patient Photos (MANDATORY)

**Trigger**: the user supplies a real clinical photograph with an identifiable face (e.g. `photos/`, case-report images, standardized frontal / oblique / profile shots). When in doubt, treat any uploaded face photo as identifiable and apply this gate.

**Non-negotiable rules**

1. **Never upload the original photo** to a cloud image model or any external service. No exceptions without explicit user authorization.
2. **De-identify locally first**: add an opaque eye-occlusion bar, then use **only the masked copy** as the image-to-image input.
3. **Keep the mask in the final artwork** as a visible compliance marker; prompt the model not to reconstruct eyes, irises or any identifiable eye feature.
4. **Realistic anatomy comes from the generated base image; local vector SVG only does annotation** (labels, leader lines, anchors, zone cards, legends). Never substitute flat vector blobs for muscle / bone / ligament rendering — that collapses into a schematic and breaks visual consistency with the rest of the series.
5. **Do not silently swap in a generated generic look-alike portrait.** It is a fallback only when the user explicitly chooses it; the default is the de-identified original, preserving that subject's real face shape and anatomy.

**Procedure** (full spec: `references/deidentification_and_realism.md`)

1. Run `scripts/deidentify_portrait.py <input> --out <masked.png>` to add the bar. Default bar covers only the eye fissures + upper nasal bridge, preserving brows, infraorbital skin, nose, mouth and chin so the orbital rim and orbicularis oculi stay visible. Use `--wide` for stricter masking when the target is not the orbital region.
2. Inspect the masked image: eyes fully covered, no brow / infraorbital structure lost.
3. Image-to-image with `input_fidelity=high`. The prompt must: preserve face shape / hairline / skin tone / head pose / background; **keep the black bar exactly as it is**; forbid realistic eyeballs / irises / identifiable eye features; render the paradigm's anatomy; include the Mandatory Aesthetic Guardrails from Step 2. **State the credit cost before generating.**
4. Crop the tool's fixed bottom-right watermark, resize to the layout's portrait window, then **re-calibrate all annotation coordinates against the new base image** — never reuse coordinates from an earlier image.
5. Compose the Track 2 HTML/SVG overlay + print-resolution PNG. Add a `已脱敏 / DE-IDENTIFIED` badge, a legend entry for the bar, and the disclaimer.
6. Remind the user that publication still requires informed consent: a bar removes only eye features, and face shape may remain identifiable.

**Gotcha**: an eye bar conflicts with periorbital anatomy diagrams. Keep it narrow by default; widen only when the orbital region is not the target or the user asks for stricter masking.

## Workflow Steps

### Step 1: Clinical & Anatomical Mapping

Identify the user's clinical scenario and map it to exact anatomical structures (both English anatomical terms for visual accuracy and Chinese clinical terms for annotations):

- **Upper Face & Periorbital (上面部与眼周)**:
  - *Frontalis* (额肌 - 上提眉部), *Corrugator supercilii* (皱眉肌 - 内收眉间), *Procerus* (降眉间肌 - 下拉眉心), *Depressor supercilii* (降眉肌), *Orbicularis oculi* (眼轮匝肌 - 环绕眼周/鱼尾纹), *Temporalis* (颞肌 - 太阳穴容积与咀嚼).
- **Midface & Volume Compartments (中面部与容积/韧带)**:
  - *Malar fat pad / SOOF / ROOF* (苹果肌/眼轮匝肌下脂肪垫/眉下脂肪垫), *Zygomaticus major & minor* (颧大肌/颧小肌), *Levator labii superioris alaeque nasi* (提上唇鼻翼肌 - 露龈笑/鼻基底), *Orbicularis retaining ligament - ORL* (眼轮匝肌支持韧带 - 泪沟成因), *Zygomatic retaining ligament* (颧弓韧带 - 印第安纹).
- **Lower Face, Glands & Neck (下面部、腺体与颈部)**:
  - *Masseter* (咬肌 - 下颌角宽大), *Depressor anguli oris - DAO* (降口角肌 - 口角下垂/木偶纹), *Mentalis* (颏肌 - 下巴核桃纹/后缩), *Platysma* (颈阔肌 - 下颌线模糊/颈纹下拉力), *Parotid gland* (腮腺 - 耳前膨出，黄色腺泡结构), *Submandibular gland* (颌下腺 - 下颌缘双下巴假象).
- **Skin Layers (皮肤组织学层次)**:
  - *Stratum corneum & Epidermis* (角质层与表皮层 - 黑色素颗粒 Melanin granules), *Superficial/Deep Dermis* (真皮浅/深层 - 胶原纤维网 Collagen bundles & 扩张毛细血管网 Dilated capillary plexus), *Subcutaneous adipose tissue* (皮下脂肪层), *SMAS fascia* (SMAS筋膜层).

### Step 2: Generate Dual-Engine Visual Prompts

Always provide two prompt versions so the user can directly trigger native generation or paste into their preferred model:

1. **Direct Native Generation / English Master Prompt (for Gemini / ChatGPT / Midjourney)**
   - **Mandatory Aesthetic Guardrails**: Always include `"high-end cosmetic dermatology visual style, clean aesthetic pale-pink striated muscle fibers and pearlescent white tendons, soft feather-edged transparency blending seamlessly into flawless East Asian female skin, non-gory, bloodless, studio beauty lighting, 8k medical illustration"`.
2. **Chinese Structured Prompt (for Hunyuan Hy4 / Domestic Models)**
   - Use clear spatial directives, lighting descriptors, and anatomical terminology in Chinese: `"高定医美科普视觉图，年轻亚洲女性高清写实特写，无暇肌肤，柔和影棚布光。在[目标区域]采用半透明羽化解剖叠加效果，清晰展示粉白色泽的[目标肌群/脂肪垫/韧带]纹理，无血腥感，边缘与真实皮肤自然过渡，医学教科书级精准解剖..."`

### Step 3: Provide Precision Annotation Solution (Dual Track)

Since image models vary in small Chinese text rendering capability, always offer:

- **Track 1: One-Shot Native Text Prompting (直出带字版)**: Include explicit label instructions in the prompt (e.g., `clean minimal white leader lines pointing to the muscle with crisp Chinese typography labels: "皱眉肌"`).
- **Track 2: Zero-Defect HTML/SVG Overlay Code (工业级图文合成版 - Recommended for Publication)**: Provide a self-contained, single-file HTML/Tailwind/SVG template from `templates/` where the user can drop in the generated clean anatomical image to get crisp vector arrows, leader lines, and rounded glassmorphic info cards matching medical literature standards.

## Prompt Templates by Paradigm

### Template 1: Type A & B (Muscle Biomechanics & Transparent Cutaway)

```text
[Subject & Framing]: Extreme close-up / portrait of a young East Asian woman focusing on [Target Region, e.g., glabella and periorbital area], symmetrical face, flawless skin, neutral calm expression.
[Anatomical Overlay]: Seamless, semi-transparent medical illustration overlay on [Specific Area], revealing anatomically accurate [Target Structures, e.g., Frontalis, Corrugator supercilii, and Procerus muscles]. Pale coral-pink muscle striation and pearlescent white tendon insertions blending softly into the surrounding skin.
[Biomechanics / Vectors (Optional for Type A)]: Smooth 3D glowing translucent arrows overlaid on the muscle fibers: warm golden-yellow upward arrows along the [Elevator muscle] indicating lifting force, and cool ice-blue inward/downward arrows on the [Depressor muscle] indicating contraction force.
[Style & Quality]: High-end aesthetic medicine textbook illustration, non-gory, bloodless, clean clinical studio lighting, ultra-detailed 8k resolution.
```

### Template 2: Type C (Full-Face Callout Grid Infographic)

```text
A professional medical aesthetics infographic layout (16:9 horizontal). Left side (40% width): A glamorous beauty portrait of a young East Asian woman with clean white anchor dots and thin leader lines on her temple, jaw angle, chin, and neck. Right side (60% width): A structured grid of 5 rounded beige information cards. Each card contains a dark-green header tag, brief clinical explanation text, and a close-up anatomical cutaway portrait showing the exact structure: (1) Temporalis muscle, (2) Masseter muscle, (3) Parotid gland (yellow lobular gland structure, distinct from muscle), (4) Depressor anguli oris & Mentalis, (5) Platysma muscle along the neck. Clean editorial cosmetic clinic style, non-gory, 8k.
```

### Template 3: Type D (Macro Skin + 3D Histology PIP)

```text
Split-screen side-by-side medical dermatology comparison of an East Asian woman's close-up eye area. Left panel: Pigmented dark circles with brownish epidermal hyperpigmentation and fine freckles under the eye; bottom-right corner features a rounded rectangular Picture-in-Picture (PIP) inset showing a 3D histological skin cross-section with brown melanin granules densely accumulated in the epidermis and dermal-epidermal junction. Right panel: Vascular dark circles with bluish-purple undertint under the lower eyelid; bottom-right corner features a matching 3D skin cross-section PIP inset showing dilated red and blue capillary networks visible through thin dermis over yellow subcutaneous fat. High-end cosmetic dermatology visual, 8k.
```

## Gotchas

- **Avoid Gory Cadaver Aesthetics**: Without explicit modifiers like `"aesthetic pale-pink fibers, bloodless, seamless translucent overlay, cosmetic dermatology style"`, image models default to dark red, visceral surgical dissection. Always enforce the non-gory beauty guardrail.
- **Distinguish Glands from Muscles**: When illustrating salivary glands (*Parotid gland* 腮腺, *Submandibular gland* 颌下腺) or fat pads (*Malar fat pad* 苹果肌脂肪垫), explicitly specify `"pale yellow lobular glandular tissue"` or `"soft golden-yellow adipose compartments"` so the model does not render them as red striated muscle.
- **Correct Muscle Fiber Orientation**: Always specify fiber direction in prompts (e.g., *Frontalis* = vertical fibers; *Orbicularis oculi* = concentric circular fibers around eye; *Corrugator* = oblique inward-downward fibers) to prevent anatomically incorrect AI hallucinations.
- **Real Patient Photos Require the Privacy Gate**: Never send an identifiable face to an image model unmasked; see `## Privacy Gate: Real Patient Photos (MANDATORY)` above. Local de-identification is a prerequisite, not an optional nicety.
- **Vector Blobs Are Not Anatomy**: Flat SVG ellipses / color blocks are acceptable only as a declared zero-upload fallback. For publication-grade realism, generate the anatomical base image and let vector code handle annotations only. Always tell the user when a style downgrade is being made instead of silently switching.
