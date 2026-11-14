# 真实患者照片：脱敏与写实质感规范

> 本文件是 `SKILL.md` 中 `## Privacy Gate: Real Patient Photos (MANDATORY)` 的完整执行规范。
> 适用场景：用户上传了可识别真人的临床照片，并希望生成**写实解剖图**。

## 1. 为什么需要这道门槛

历史上出现过两种失败模式，都要避免：

| 失败模式 | 后果 |
| :-- | :-- |
| 为保护隐私，把真人照片改成**纯本地矢量色块**叠加 | 隐私保住了，但风格从「照片级写实解剖」退化成扁平示意图，与系列其他图不一致 |
| 为追求写实质感，换成**生成式通用人像** | 风格对了，但丢掉了该受试者的真实脸型与解剖特征，用户要的个体化信息没了 |

**正确路径**：本地脱敏 → 只上传脱敏版做 image-to-image → 写实解剖由生成底图承担 → 本地矢量只做精准标注。三者（真实个体特征 / 写实质感 / 隐私合规）同时满足。

## 2. 触发判定

只要满足任一条即触发：
- 用户明确说「用我上传的照片 / 这几张临床照 / 患者照片」并附了人像文件。
- 图片是可识别真人面部（正面 / 斜位 / 侧位标准化临床摄影、病例照片、术前术后照）。
- 无法确认是否为模特图或已脱敏素材。

**存疑时一律按可识别处理。** 只有用户明确授权，才允许跳过本地脱敏直接上传。

## 3. 遮挡条规格

坐标基于 **500×650 标准化正面照**参考系；脚本会按实际图片尺寸等比缩放。

| 模式 | 矩形 (x1,y1,x2,y2) | 覆盖范围 | 适用 |
| :-- | :-- | :-- | :-- |
| **默认窄条**（推荐） | `(118, 296, 382, 340)` | 双侧眼裂 + 鼻梁上段 | 需显示眶缘、眼轮匝肌、眉位的上面部/全脸解剖图 |
| 宽条 `--wide` | `(100, 262, 400, 378)` | 眉下至眶下皮肤 | 目标不在眶周，或用户要求更严格脱敏 |

默认窄条**保留**：眉毛、眶上/下缘骨性标志、眶下皮肤、鼻、口、下巴、发际线、耳。这样眼轮匝肌环形纤维与眶缘骨环仍在遮挡条上下可见。

颜色默认纯黑 `(15,15,15)`，圆角 8（按比例缩放），完全不透明。临床摄影背景多为纯黑，遮挡条可自然融入。

自定义：`--bar X1 Y1 X2 Y2`、`--color R G B`、`--radius N`、`--ref-width/--ref-height`。

## 4. 完整流程

### Step 1 · 本地脱敏（不出本地）

```bash
# 单张
python scripts/deidentify_portrait.py photos/front.jpg --out photos/front_deidentified.png

# 批量（三视角）
python scripts/deidentify_portrait.py photos/*.jpg --out-dir photos/masked/

# 更严格
python scripts/deidentify_portrait.py photos/front.jpg --out photos/front_deidentified.png --wide
```

脚本特性：纯 PIL、无网络、无删除、不修改原图；输出已存在时默认拒绝覆盖（`--force` 才允许）；输出路径与输入相同时直接报错。

**必须目视检查**脱敏结果：虹膜与眼型完全不可见，且眉毛/眶下结构未被误遮。检查不过就调 `--bar` 重跑。

### Step 2 · 生图（只传脱敏版）

- 调用 image-to-image，`image1` = **脱敏版**，设 `input_fidelity=high`，`size` 与版式人像区比例接近（如 `1024x1536`），`quality=high`。
- **生成前告知用户积分消耗**（单张约 5–10 积分）。
- 原照绝不作为参数传入。

### Step 3 · 提示词必须包含的句子

英文模板（按范式替换解剖描述）：

```text
Using the provided de-identified clinical portrait as the base, preserve EXACTLY
the subject's face shape, hairline, skin tone, head pose, lighting and background.
The input has a solid black rounded de-identification bar across both eyes —
KEEP THIS BAR EXACTLY AS IT IS: do not remove it, do not reconstruct eyes, do not
draw realistic eyeballs, irises or any identifiable eye features.

Add a high-end semi-transparent anatomical overlay [插入本范式解剖描述，如 split-face:
LEFT HALF pearlescent ivory-white skeletal framework ... RIGHT HALF aesthetic
pale-pink musculature with correct fiber orientation ...].

high-end cosmetic dermatology visual style, clean aesthetic pale-pink striated
muscle fibers and pearlescent white tendons, soft feather-edged transparency
blending seamlessly into flawless East Asian female skin, non-gory, bloodless,
studio beauty lighting, 8k medical illustration.
Absolutely no text, no letters, no labels, no numbers, no watermark, no arrows,
no graphic UI.
```

中文要点（Hy4 / 国内模型）：「严格保留原照脸型、发际线、肤色、头位与背景；**完整保留黑色眼部遮挡条**，不得移除、不得重建眼睛或画出虹膜与任何可识别眼部特征；其余为半透明羽化解剖叠加……无任何文字与标签。」

**关键**：明确写「保留黑条」，否则模型常把遮挡条当成待补全区域，画出可识别眼睛，脱敏就失效了。

### Step 4 · 后处理

1. 生图工具右下角有固定水印 → 裁掉。例：`im.crop((0, 110, 1024, 1441))`（1024×1536 原图，得到 0.769 比例），再缩放到版式人像窗口（如 550×715）。
2. **重新校准所有标注坐标（使用 `scripts/calibrate_grid.py`）**。生成底图的脸部大小、位置与原始临床照不同，绝对不能复用旧坐标。先运行：
   ```bash
   python scripts/calibrate_grid.py <cropped_base.png> --viewbox 1280 720 --out <base_grid.png>
   ```
   用图像查看工具读取 `<base_grid.png>` 上的刻度网格，精确读出：分界线 x、发际线 y、遮挡条上下边界、眉/眼/鼻/口/下巴 y，以及各靶结构中心 `(x, y)`，再写入 SVG 引线。
3. 版式背景色与底图匹配：纯黑临床照用 `#080706`；暖米色生成图用取样色渐变（如 `#a68e7e → #b8a292 → #c5ae99`），避免硬边。

### Step 5 · 合成与交付

- 写实骨骼 / 肌肉 / 韧带 / 脂肪**全部来自底图**；本地矢量只做：结构标签、双层引线（白色粗衬底 + 深棕细主线）、锚点圆、分区卡、图例。
- 成品必须带：`已脱敏 / DE-IDENTIFIED` 徽标、图例中的「眼部遮挡条」色块、底部免责声明（可直接选用 `templates/type_b_layered_cutaway.html`）。
- 渲染使用 `scripts/render_infographic.py`（自动优先调用本机 Chrome 无头模式，无需安装 playwright）：

```bash
python scripts/render_infographic.py layout.html output.png
```

- 交付物：4K PNG + 自包含 HTML + 提示词与说明 md；脱敏后的中间图单独保留，供用户核对（临时 `*_grid.png` 校准网格图在核对无误后清理）。

## 5. 三种方案的优先级

| 优先级 | 方案 | 何时用 |
| :-- | :-- | :-- |
| **1（默认）** | 本地脱敏原照 → （可选叠加 `build_anatomy_guide.py` 几何引导）→ 脱敏版生图 → 矢量标注 | 用户提供真实照片且要写实解剖图 |
| 2 | 生成式通用人像（不碰原照）→ 矢量标注 | 用户**明确选择**放弃个体特征，或照片完全不可用 |
| 3 | 纯本地矢量叠加（零上传、零积分） | 用户明确要求不外传任何图像；**必须主动告知风格会降级**，不要静默切换 |

## 6. 常见错误

- ❌ 未脱敏就把原照传给生图模型。
- ❌ 脱敏后模型重建了眼睛 —— 提示词没写「保留黑条」。
- ❌ 画浅层/深层脂肪垫或支持韧带时未查阅 `references/fine_anatomy_spatial_atlas.md`，导致脂肪分室位置乱飞或糊成一团。
- ❌ 换了底图却沿用旧的标注坐标，或未用 `calibrate_grid.py` 标尺校准导致引线全部错位。
- ❌ 忘记裁水印，或裁切把下巴/发际线切掉。
- ❌ 用 SVG 椭圆、色块充当肌肉和骨骼，还当作交付级写实图。
- ❌ 成品里没有脱敏徽标 / 图例 / 免责声明。
- ❌ 忘记在生图前告知积分消耗。

## 7. 合规提醒

遮挡条只去除眼部识别特征，**脸型、耳廓、发际线、皮肤特征仍可能构成可识别信息**。对外发布、论文插图、学术汇报前仍需受试者**知情同意**；必要时使用 `--wide`、叠加其他脱敏处理，或改用方案 2。成品一律标注「科普示意，非临床诊断依据」。

## 8. 技能包相关文件

```
aesthetic-anatomy-illustrator/
├── SKILL.md                                  # 含 Privacy Gate、Step 0 交互确认与 Step 3 视觉质检
├── scripts/
│   ├── deidentify_portrait.py                # 本地脱敏（本规范 Step 1）
│   ├── build_anatomy_guide.py                # 标准解剖几何参考图谱生成 & 图生图空间引导叠加
│   ├── calibrate_grid.py                     # 像素/viewBox 坐标网格标尺校准工具
│   └── render_infographic.py                 # Chrome Headless / Playwright 双引擎 4K 渲染
├── references/
│   ├── anatomy_prompt_dictionary.md          # 全景解剖术语、纤维方向与临床痛点词典
│   ├── fine_anatomy_spatial_atlas.md         # 浅/深层脂肪分室、五大韧带、危险血管几何四至与质检库
│   └── deidentification_and_realism.md       # 本文件
└── templates/                                # Type A / B / C / D 工业级 HTML/SVG 标注模板
    ├── type_a_biomechanics_overlay.html
    ├── type_b_layered_cutaway.html
    ├── type_c_callout_grid.html
    └── type_d_histology_pip.html
```
