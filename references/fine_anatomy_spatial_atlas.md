# 面部深层与精细解剖：几何四至、分室形态与生图约束图谱库 (Fine Anatomy Spatial & Morphological Atlas)

> 本图谱库专门解决通用生图大模型在绘制**浅层脂肪室、深层脂肪室、面部支持韧带、危险血管网及分层平面**时经常出现的**位置偏移、形状失真、分室粘连成一团或层次颠倒**问题。
> **强制规则**：只要用户需求涉及脂肪垫、深层容积、韧带卡压、泪沟/法令纹/印第安纹/木偶纹机制或注射平面，Agent 必须先查阅本图谱库，将对应的**「几何形状 + 四至边界（Superior/Inferior/Medial/Lateral）+ 负面排他约束（Negative Constraints）」**完整嵌入生图 Prompt，并在生成后按本库的「视觉验收清单（Vision QA Checklist）」逐项核验。

---

## 一、 为什么大模型画不好脂肪垫与韧带？（核心误区与纠偏原则）

| 常见 AI 幻觉错误 | 真实临床解剖形态（Rohrich & Pessa / Mendelson 经典标准） | 强制纠偏策略 |
| :--- | :--- | :--- |
| 把“浅层苹果肌脂肪垫”画成脸颊中央孤立的一团圆形黄球 | 中面部浅层脂肪是由 **3 个紧密拼贴但有清晰隔膜分界的独立几何分室**（鼻唇沟脂肪室 + 内侧颊脂肪室 + 中间颊脂肪室）组成的马赛克拼图 | Prompt 必须明确写出 **分室数量、各自几何形状（泪滴长条形 vs 倒三角形 vs 纵向长板形）及中间的白色纤维隔膜（Septal boundaries）** |
| 把“深层脂肪室（SOOF / DMCF）”画在皮肤正下方，盖住眼轮匝肌和提上唇肌 | 深层脂肪位于**表情肌深面（骨膜上方）**，表面必须有半透明的肌肉纤维（如眼轮匝肌、提上唇肌）跨过 | Prompt 必须强调 **层次前后遮挡关系（Layered depth）**，或使用 `scripts/build_anatomy_guide.py` 生成标准解剖位置引导图辅助控图 |
| 把“支持韧带”画成横在脸上的一根粗白绳 | 支持韧带是自骨膜或深筋膜发出、穿行于脂肪室交界缝隙、树枝状锚定至真皮的**致密珍珠白纤维束带（Fibrous tethering bands）** | 强调韧带位于**上下脂肪室的交界凹陷槽（Boundary groove）**处，呈现紧绷的锚定拉扯感 |

---

## 二、 浅层脂肪室精准四至与几何形态库 (Superficial Fat Compartments)

面部浅层脂肪位于**真皮下方、SMAS 筋膜层上方**，色泽为**饱满亮润的淡金黄色/奶油黄色分叶状脂肪组织（Plump pale-golden lobular adipose compartments separated by thin white fibrous septa）**。

### 1. 中面部核心三联浅层脂肪室（苹果肌与法令纹区 — 最常画区域）

这三个脂肪室从内到外像三块拼图一样紧密排列在眶下缘下方至口角上方之间：

| 分室中文名称 | 英文标准解剖名 | 精确几何形状 (Shape) | 解剖四至边界 (Exact Anatomical Boundaries) | 专用英文 Prompt 空间锁定描述词 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 鼻唇沟浅层脂肪室** | `Nasolabial Superficial Fat Compartment` | **斜向狭长泪滴形 / 香蕉长条状**（上窄下宽，沿鼻唇沟内上方斜行） | **上界**：眶下缘内侧、眼轮匝肌支持韧带（ORL）下方<br>**内界**：紧贴鼻翼外侧沟与法令纹折痕（绝对不越过法令纹进入上唇白唇区）<br>**外界**：与内侧颊脂肪室紧密相邻<br>**下界**：口角外上方（止于上唇外侧上方） | `an elongated, oblique teardrop-shaped pale-yellow adipose compartment lying IMMEDIATELY lateral to the nasal ala and directly above the nasolabial fold crease, extending from the medial infraorbital rim down toward the superior corner of the mouth` |
| **2. 内侧颊浅层脂肪室** | `Medial Cheek Superficial Fat Compartment` | **倒三角形 / 楔形分叶块**（位于苹果肌正中央最高点） | **上界**：眶下缘中段（ORL 韧带下方）与颧皮韧带上方交界<br>**内界**：紧贴鼻唇沟脂肪室的外侧缘<br>**外界**：与中间颊脂肪室相邻（大约在瞳孔外侧缘垂线）<br>**下界**：颊中沟上方，不延伸至下颌缘 | `a distinct inverted-triangle / wedge-shaped pale-yellow fat compartment situated at the central malar prominence directly lateral to the nasolabial fat compartment and below the inferior orbital rim` |
| **3. 中间颊浅层脂肪室** | `Middle Cheek Superficial Fat Compartment` | **纵向长边形 / 宽带状分叶块**（位于颧骨体向下面颊过渡区） | **上界**：颧弓体前部下方<br>**内界**：紧贴内侧颊脂肪室的外侧缘<br>**外界**：咬肌前缘垂线（与外侧颞颊脂肪室分界）<br>**下界**：向下延伸至口角水平线外侧 | `a broad vertically oriented rectangular pale-yellow fat compartment located lateral to the medial cheek fat, lying superficial to the zygomaticus major muscle over the mid-lateral cheek` |

> **【三联组合生图黄金句式（Midface Superficial Fat Triad）】**：
> `"Reveal the midface superficial fat compartments arranged side-by-side like an anatomical mosaic from medial to lateral: (1) Medially, the elongated oblique teardrop-shaped Nasolabial fat compartment hugging the lateral nasal ala right above the nasolabial crease; (2) Centrally, the wedge-shaped Medial Cheek fat compartment over the malar apex; (3) Laterally, the broader vertical Middle Cheek fat compartment. Each compartment consists of plump pale-golden lobular adipose tissue clearly demarcated by thin pearlescent-white inter-compartmental fibrous septa. Do NOT merge them into a single round blob; do NOT place fat over the nasal bridge or upper lip."`

### 2. 眶周、额部与下面部浅层脂肪室

| 分室中文名称 | 英文标准解剖名 | 精确几何形状 (Shape) | 解剖四至边界 (Exact Anatomical Boundaries) | 专用英文 Prompt 空间锁定描述词 |
| :--- | :--- | :--- | :--- | :--- |
| **4. 眶下浅层脂肪（眼轮匝肌浅面）** | `Infraorbital Superficial Fat` | **薄层新月形细小脂肪颗粒带** | 位于下眼睑睑袋下方、ORL 与颧皮韧带之间的狭窄新月区（印第安纹/颧颊沟上方） | `a thin crescent-shaped band of fine pale-yellow subcutaneous fat situated along the lower orbital rim between the orbicularis retaining ligament above and the zygomatic cutaneous ligament below` |
| **5. 外侧颞颊浅层脂肪室** | `Lateral Temporal-Cheek Fat Compartment` | **纵贯耳前的狭长垂直带状** | 从太阳穴外侧一直垂直向下跨越颧弓、覆盖腮腺咬肌筋膜表面直达下颌角 | `a long continuous vertical band of subcutaneous yellow fat running immediately anterior to the ear, spanning from the lateral temple across the zygomatic arch down to the mandibular angle` |
| **6. 下颌缘/口角下浅层脂肪室（羊腮脂肪垫）** | `Superior & Inferior Jowl Fat Compartments` | **卵圆形/水滴状下垂脂肪团** | **内界**：降口角肌（DAO）外侧缘及下颌骨韧带后方（形成木偶纹外侧隆起）<br>**下界**：跨过下颌骨下缘向下膨出，破坏下颌线流畅度 | `two distinct drooping ovoid pale-yellow fat pads (Superior and Inferior Jowl fat) located immediately lateral to the marionette line and depressor anguli oris muscle, sagging across the inferior mandibular border` |
| **7. 额部三联浅层脂肪室** | `Central, Middle & Lateral Temporal Forehead Fat` | **3 条纵向并排的扁平条状脂肪室** | 正中额脂肪室（眉间至发际线正中）+ 左右两侧眉上方额中脂肪室，被眶上神经血管束分隔 | `flat, vertically aligned pale-yellow subcutaneous fat compartments across the forehead (central and paired middle forehead compartments) separated by vertical fibrous septa` |

---

## 三、 深层脂肪室精准四至与几何形态库 (Deep Fat Compartments)

深层脂肪位于**面部表情肌（眼轮匝肌、提上唇肌、颧大肌）深面、紧贴骨膜表面（Supraperiosteal plane）**。视觉上应表现为**比浅层脂肪略深一点的琥珀金黄色（Amber-gold deep adipose pads），且局部被半透明的浅层粉红色肌肉或白色韧带半遮挡**，以体现真实的空间纵深感。

| 深层脂肪室名称 | 英文标准解剖名 | 精确几何形状 (Shape) | 解剖四至与层次关系 (Planes & Boundaries) | 专用英文 Prompt 空间锁定描述词 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 眼轮匝肌下脂肪垫（内侧/外侧 SOOF）** | `Medial & Lateral SOOF (Sub-Orbicularis Oculi Fat)` | **横向分内、外两叶的扁平新月形/椭圆形垫** | **层次**：眼轮匝肌（Orbicularis oculi）深面、眶下缘骨膜表面<br>**上界**：紧贴眼轮匝肌支持韧带（ORL）下缘（绝不进入眼眶内变成眼袋眶隔脂肪）<br>**内侧叶**：内眦垂线至瞳孔中线<br>**外侧叶**：瞳孔中线至外眦及颧骨体上方 | `deep to the translucent concentric fibers of the orbicularis oculi muscle and immediately inferior to the white Orbicularis Retaining Ligament (ORL), reveal the two-lobed amber-yellow SOOF (Medial and Lateral Sub-Orbicularis Oculi Fat) resting directly on the maxilla and zygomatic bone surface` |
| **2. 深层内侧颊脂肪垫（DMCF）** | `Deep Medial Cheek Fat (Medial & Lateral parts)` | **三角形/多边形厚实支撑垫（分内侧部与外侧部）** | **层次**：位于提上唇肌（LLS）与颧小肌深面、上颌骨前壁骨膜上（鼻唇沟浅层脂肪室的正后方深处）<br>**临床意义**：中面部骨相支撑核心，萎缩后导致苹果肌塌陷与法令纹加深 | `deep beneath the semi-transparent levator labii superioris muscle and posterior to the superficial nasolabial fat, reveal the triangular amber-gold Deep Medial Cheek Fat (DMCF) resting directly on the anterior maxillary periosteum` |
| **3. 梨状孔深层空间（Ristow 空间）** | `Deep Pyriform Space (Ristow's Space)` | **紧贴鼻翼基底骨面的小新月形/三角形深腔** | **位置**：鼻翼软骨基底部正下方、梨状孔外侧骨缘骨膜上、提上唇鼻翼肌深面<br>**临床意义**：鼻基底凹陷、法令纹上段骨性支撑靶点 | `a compact crescentic deep anatomical space (Deep Pyriform / Ristow's space) located directly on the bone around the lateral pyriform aperture beneath the nasal ala base, deep to the levator labii superioris alaeque nasi muscle` |
| **4. 颊脂垫（体部与颊突）** | `Buccal Fat Pad (Bichat's Fat Pad)` | **光滑圆润的卵圆形深部脂肪球** | **位置**：位于咬肌前缘深面、颊肌外侧的深部间隙（面颊中下部深处，婴儿肥核心结构） | `a smooth, encapsulated rounded golden-yellow deep fat ball (Buccal fat pad of Bichat) nestled in the deep masticatory space anterior to the masseter muscle border and deep to the zygomaticus muscles` |
| **5. 眉下脂肪垫（ROOF）** | `ROOF (Retro-Orbicularis Oculi Fat)` | **沿眉弓外中段分布的横向梭形厚垫** | **位置**：眉毛中后段区域的眼轮匝肌深面、眶上缘骨膜表面（上睑外侧饱满度支撑） | `a spindle-shaped amber-yellow deep fat pad (ROOF) lying deep to the superior orbicularis oculi muscle along the superolateral orbital rim bone beneath the eyebrow` |

---

## 四、 面部五大支持韧带与隔膜系统 (Retaining Ligaments & Septa)

支持韧带在医美图像中必须渲染为**珍珠白色、具高张力纤维束质感的韧带结构（Pearlescent ivory-white fibrous ligamentous tethers / bands）**，并且必须体现**“上方脂肪室下垂堆积 + 韧带死死拉住皮肤形成凹陷沟槽（Tethering groove）”**的力学关系。

| 韧带中文名称 | 英文标准解剖名 | 起止位置与空间走向 | 对应的临床凹陷线 / 纹路 | 专用英文 Prompt 空间锁定描述词 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 眼轮匝肌支持韧带（ORL / 泪沟韧带）** | `Orbicularis Retaining Ligament (ORL) & Tear Trough Ligament` | 沿整个眶下缘骨膜弧形发出（内侧坚韧紧密称为泪沟韧带 TTL，外侧较宽），穿过眼轮匝肌锚定至下睑真皮 | **泪沟（Tear Trough）** 与 **睑袋下界（Palpebromalar groove）**（上方是眶隔脂肪，下方是 SOOF） | `a distinct, curved pearlescent-white fibrous band (Orbicularis Retaining Ligament / Tear Trough Ligament) attached tightly along the arc of the inferior orbital rim bone, creating a sharp tethering boundary between the lower eyelid above and the SOOF/malar fat below` |
| **2. 颧弓韧带 / 颧皮韧带** | `Zygomatic Cutaneous Ligament (McGregor's Patch)` | 起自颧骨下缘与颧弓前部骨膜（眶下缘下方约 1cm 处斜行向外），穿行于浅层脂肪室下界锚定至真皮 | **印第安纹 / 颧颊沟（Midcheek groove / Malar mound lower border）** | `dense pearlescent-white fibrous tethering bundles (Zygomatic cutaneous ligament) originating from the inferior border of the zygomatic arch ~1cm below the orbital rim, forming an oblique shelf that tethers the malar fat pad and creates the midcheek Indian line` |
| **3. 上颌支持韧带** | `Maxillary Retaining Ligament` | 位于鼻唇沟上中段深处，紧邻鼻翼外侧上颌骨面，固定鼻唇沟内侧边界 | **法令纹上中段深部锚定边界** | `deep white fibrous tethering fibers (Maxillary ligament) anchored along the lateral maxilla beside the nasal ala, reinforcing the upper nasolabial crease boundary` |
| **4. 咬肌皮韧带** | `Masseteric Cutaneous Ligaments` | 沿咬肌前缘垂直排列的一列白色纤维束带，从咬肌筋膜穿出连接至面颊皮肤 | **中下面部外侧松弛分界线**（前方颊部脂肪向前下滑动） | `a vertical row of white fibrous ligamentous tethers (Masseteric cutaneous ligaments) aligned along the anterior border of the masseter muscle` |
| **5. 下颌骨支持韧带** | `Mandibular Retaining Ligament` | 位于下颌骨体前部下缘（颏孔前下方、降口角肌内侧缘，距下巴正中约 3-4cm 处）的强力骨皮韧带 | **木偶纹下端卡压点（Pre-jowl sulcus）**：韧带前方固定不动，韧带后方的羊腮脂肪垫（Jowl fat）向下越过下颌缘垂出 | `a strong focal cluster of pearlescent-white osteocutaneous fibers (Mandibular ligament) anchored firmly to the anterior-inferior mandibular border just medial to the jowl fat pad, creating the sharp pre-jowl indentation of the marionette line` |

---

## 五、 面部核心血管危险区与神经标志 (Vascular Danger Zones & Nerves)

当用户要求绘制“注射安全区/危险区、血管解剖、栓塞风险避让”时，血管必须与粉色肌肉和黄色脂肪产生**极高的色彩区分度**：动脉使用**鲜亮珊瑚红/朱红色光滑管状结构（Smooth cylindrical crimson-red arterial vessels）**，神经使用**亮柠檬黄/金色细丝分支（Fine luminous golden-yellow nerve branches）**。

| 结构名称 | 英文标准解剖名 | 精确解剖走行轨迹 (Trajectory & Landmarks) | 临床危险关联 | 专用英文 Prompt 空间锁定描述词 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 面动脉 → 内眦动脉主干** | `Facial Artery to Angular Artery` | 从**咬肌前缘与下颌骨下缘交界处**绕过下颌缘上行 → 呈迂曲蛇行状经过**口角外侧约 1cm 处** → 沿**鼻唇沟（法令纹）深浅层之间**贴鼻侧壁上行延续为**内眦动脉**（至内眼角） | 下颌缘、法令纹、鼻基底、鼻背注射第一高危血管 | `a tortuous, clearly defined crimson-red cylindrical artery (Facial-to-Angular artery) winding upward from the anterior border of the masseter at the mandibular border, passing ~1cm lateral to the mouth corner, and ascending along the nasolabial fold beside the lateral nose toward the medial canthus` |
| **2. 滑车上动脉与眶上动脉** | `Supratrochlear & Supraorbital Arteries` | 自眉头内侧（滑车上切迹）与眉弓中内 1/3 交界处（眶上孔/切迹）穿出，沿额肌深面向额部垂直分支上行 | 眉间纹、额部、鼻根注射导致失明的高危血管 | `paired vertical branching crimson-red arteries (Supratrochlear and Supraorbital arteries) emerging from the medial orbital rim at the eyebrow head and ascending vertically across the forehead` |
| **3. 颞浅动脉（额支）** | `Superficial Temporal Artery (Frontal branch)` | 自耳屏前方上行，在颞浅筋膜（STF）层内沿太阳穴斜向前上方走行至额角外侧 | 太阳穴（颞部）填充高危血管 | `a prominent branching crimson-red artery (Superficial temporal artery) ascending in front of the ear and coursing obliquely forward and upward across the temple fossa toward the lateral forehead` |
| **4. 眶下神经血管束 & 颏神经血管束** | `Infraorbital & Mental Neurovascular Bundles` | **眶下孔**：瞳孔中线垂线、眶下缘下方约 8-10mm 处骨孔穿出呈扇形辐射<br>**颏孔**：下颌第二前磨牙下方（口角垂线与下颌下缘中点）骨孔穿出 | 中面部深层骨膜上注射、下巴/木偶纹深层注射需避开的骨孔 | `a distinct bone foramen (Infraorbital foramen ~1cm below the mid-infraorbital rim / Mental foramen on the anterior mandible) with a fan-like spray of fine golden-yellow nerve fibers and small red vessels emerging onto the bone surface` |

---

## 六、 纵向解剖层次与注射平面规范 (Longitudinal Planes & Injection Depth)

当绘制 Type B（分层剖面）或 Type D（3D 皮肤/软组织截面与针头层次）时，自浅入深必须严格遵循以下 **6 层解剖顺序**，绝不可颠倒：

1. **表皮与真皮层 (`Epidermis & Dermis`)**：最表层半透明肤色角质与致密粉白真皮胶原层。
2. **浅层脂肪室 (`Superficial Fat Layer / Subcutaneous Fat`)**：淡金黄色饱满脂肪分叶，内含垂直穿行的支持韧带终末分支。
3. **SMAS 筋膜层 / 浅表肌腱膜系统 (`SMAS / Superficial Musculoaponeurotic System` / 眼周为眼轮匝肌层)**：**标志性的亮白色致密连续纤维筋膜薄片（Glistening pearlescent-white continuous fascial sheet）**，将浅层脂肪与深层结构彻底隔开。
4. **面部表情肌层 (`Mimetic Muscles`)**：浅珊瑚粉色条纹状肌纤维（与 SMAS 层紧密融合或位于其下）。
5. **深层脂肪室与滑动间隙 (`Deep Fat Compartments & Glide Planes`)**：琥珀金黄色深部脂肪垫（SOOF / DMCF / Ristow 空间），面动脉深段与运动神经分支多走行于此层。
6. **骨膜与骨骼层 (`Periosteum & Craniofacial Bone`)**：最底层象牙白致密颅面骨骼（上颌骨、颧骨、下颌骨），大分子高 G' 填充剂通常锚定在骨膜上层（`Supraperiosteal bolus`）。

---

## 七、 生成后视觉解剖验收清单 (Post-Generation Vision QA Checklist)

**在将生成的解剖底图送入 HTML/SVG 模板加标注之前，Agent 必须读取生成出来的图片，对照以下 4 条硬指标进行自检**：

1. **位置四至核验（Location Check）**：
   - 如果是**鼻唇沟浅层脂肪室**：它是否紧贴鼻翼外侧、位于法令纹折痕的**外上方**？（如果画到了上嘴唇、鼻梁上或脸颊最外侧 → **不合格，需重绘或叠加引导图**）。
   - 如果是 **SOOF（深层眼轮匝肌下脂肪）**：它是否位于眶下缘骨头表面、眼袋下方？（如果画成了眼眶里面的眼袋或者画到了苹果肌下半部 → **不合格**）。
2. **分室与形态核验（Morphology & Septation Check）**：
   - 多个脂肪室同框时，是否有清晰的**分块几何形态与白色纤维隔膜边界**？（如果糊成了一大片无分界的黄色油漆斑 → **不合格**）。
3. **组织色泽与材质区分度（Tissue Color Coding Check）**：
   - 肌肉 = **淡珊瑚粉条纹（Pale coral-pink striated fibers）**
   - 浅层脂肪 = **淡奶油金黄分叶（Plump pale-golden lobules）**
   - 深层脂肪 = **琥珀金黄深层垫（Amber-gold deep pads）**
   - 韧带/筋膜/肌腱 = **珍珠亮白致密纤维（Pearlescent ivory-white fibrous bands）**
   - 唾液腺（腮腺/颌下腺） = **米黄/浅黄桑葚状腺泡分叶（Buff-yellow lobular acinar gland）**
   - 动脉 = **鲜朱红光滑圆管（Crimson-red smooth vessels）**
4. **如果自检发现纯文本 Prompt 生成的位置仍然漂移怎么办？**
   - **立即启用空间几何引导重绘（Spatial Guide Image-to-Image）**：运行 `python scripts/build_anatomy_guide.py` 在原图/脱敏图上精确绘制半透明解剖分区色块作为位置锚点，再传给生图模型进行高保真转化（详见 `SKILL.md` Step 2.5）。
