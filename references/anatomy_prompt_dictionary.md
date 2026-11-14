# 医美临床解剖与多模态生图映射词典 (Aesthetic Anatomy Prompt Dictionary)

本词典供 `aesthetic-anatomy-illustrator` Skill 在构建中英文生图提示词时查阅，确保解剖位置、肌纤维方向、组织色泽与医美临床痛点完全对应。
> **重要提示**：当涉及**浅层/深层脂肪分室（Fat Compartments）、支持韧带（Retaining Ligaments）、危险血管（Danger Zones）或深浅注射层次**时，必须同时查阅 [`references/fine_anatomy_spatial_atlas.md`](fine_anatomy_spatial_atlas.md) 获取精确的**几何形状、上下内外四至边界（Boundaries）与负面排他词**。

## 一、 上面部与眼周 (Upper Face & Periorbital)

| 中文名称 | 英文解剖术语 | 肌纤维走向与视觉特征 (Prompt 描述词) | 对应医美适应症/痛点 | 力学箭头方向 (Type A) |
| :--- | :--- | :--- | :--- | :--- |
| **额肌** | `Frontalis muscle` | `broad vertical pale-pink muscle fibers covering the forehead from the brow to the galeal aponeurosis, inserting into the eyebrow skin` | 抬头纹 (Forehead lines)、眉下垂、眉位平衡 | 暖金色向上箭头 (`upward lifting vector`) |
| **皱眉肌** | `Corrugator supercilii` | `oblique deep muscle fibers originating from the medial supraorbital ridge and extending upward and laterally to the middle eyebrow skin` | 川字纹/眉间垂直纹 (Glabellar vertical frown lines) | 冰蓝色向内下方箭头 (`inward-downward contraction vector`) |
| **降眉间肌** | `Procerus muscle` | `small pyramid-shaped vertical muscle fibers between the eyebrows at the nasal root bridge` | 鼻根横纹、眉心下压 | 冰蓝色垂直向下箭头 (`vertical downward vector`) |
| **降眉肌** | `Depressor supercilii` | `slender vertical fibers at the medial eyebrow head blending with medial orbicularis oculi` | 眉头下压、眉间纹辅助肌 | 冰蓝色向下箭头 |
| **眼轮匝肌** | `Orbicularis oculi (Palpebral & Orbital parts)` | `concentric circular sphincter muscle fibers surrounding the eye orbit and eyelids` | 鱼尾纹 (Crow's feet)、眼下动态细纹、卧蚕肥大 | 外侧与内侧向心性收缩箭头 |
| **颞肌** | `Temporalis muscle` | `fan-shaped muscle fibers in the temple fossa converging downward beneath the zygomatic arch toward the mandibular coronoid process` | 太阳穴凹陷评估、咀嚼代偿性肥大 | 向斜下方汇聚 |
| **眉下脂肪垫 (ROOF)** | `ROOF (Retro-Orbicularis Oculi Fat)` | `spindle-shaped amber-yellow deep fat pad lying deep to the superior orbicularis oculi along the superolateral orbital rim bone` | 上睑外侧饱满度支撑、眉弓深层容积 | 无（深层支撑垫） |

## 二、 中面部：浅/深层脂肪分室、支持韧带与提肌 (Midface Fat Compartments, Ligaments & Elevators)

| 中文名称 | 英文解剖术语 | 视觉形态、几何边界与组织特征 (Prompt 描述词) | 对应医美适应症/痛点 |
| :--- | :--- | :--- | :--- |
| **鼻唇沟浅层脂肪室** | `Nasolabial Superficial Fat Compartment` | `elongated oblique teardrop-shaped pale-yellow subcutaneous fat compartment lying IMMEDIATELY lateral to the nasal ala and directly above the nasolabial fold crease (from medial infraorbital rim to upper mouth corner)` | 法令纹外上方膨出压迫、浅层脂肪下移 |
| **内侧颊浅层脂肪室** | `Medial Cheek Superficial Fat Compartment` | `inverted-triangle / wedge-shaped plump pale-yellow subcutaneous fat compartment situated at the central malar apex, directly lateral to the nasolabial fat compartment and below the ORL` | 苹果肌浅层饱满度、下移后加重法令纹与印第安纹 |
| **中间颊浅层脂肪室** | `Middle Cheek Superficial Fat Compartment` | `broad vertically oriented rectangular pale-yellow subcutaneous fat compartment lateral to the medial cheek fat, superficial to zygomaticus major` | 面颊中段过渡、笑肌外侧浅层容积 |
| **眼轮匝肌下脂肪垫 (内/外侧 SOOF)** | `Medial & Lateral SOOF (Sub-Orbicularis Oculi Fat)` | `two-lobed flat crescentic amber-gold deep fat compartments lying DEEP to the orbicularis oculi muscle and immediately inferior to the Orbicularis Retaining Ligament (ORL) on the infraorbital bone` | 泪沟与睑颊沟深层支撑缺失、苹果肌深层基底萎缩 |
| **深层内侧颊脂垫 (DMCF)** | `Deep Medial Cheek Fat (DMCF)` | `triangular amber-gold deep fat pad lying DEEP to the levator labii superioris muscle directly on the anterior maxillary periosteum (posterior to the superficial nasolabial fat)` | 中面部前侧骨相支撑核心、萎缩后致面中扁平与法令纹塌陷 |
| **梨状孔深层空间 (Ristow 空间)** | `Deep Pyriform Space (Ristow's Space)` | `compact crescentic deep anatomical space on the bone around the lateral pyriform aperture directly beneath the nasal ala base` | 鼻基底凹陷、骨性法令纹深层支撑靶点 |
| **眼轮匝肌支持韧带 (ORL / 泪沟韧带)** | `Orbicularis Retaining Ligament (ORL) & TTL` | `curved pearlescent-white fibrous ligamentous tether attached tightly along the arc of the inferior orbital rim bone, separating the lower eyelid above from the SOOF below` | 泪沟凹陷 (Tear trough deformity)、眼袋下界卡压 |
| **颧皮韧带 / 颧弓韧带** | `Zygomatic Cutaneous Ligament` | `dense pearlescent-white fibrous tethering bundles along the inferior zygomatic arch ~1cm below the orbital rim, forming an oblique shelf across the malar fat` | 印第安纹/颧颊沟 (Malar mound / Midcheek groove) |
| **上颌支持韧带** | `Maxillary Retaining Ligament` | `deep white fibrous tethering fibers anchored along the lateral maxilla beside the nasal ala` | 法令纹上中段内侧深部锚定边界 |
| **提上唇鼻翼肌** | `Levator labii superioris alaeque nasi (LLSAN)` | `slender vertical pale-pink muscle running alongside the lateral nose to insert into the nasal ala and upper lip` | 露龈笑 (Gummy smile)、鼻翼牵拉、动态法令纹上段 |
| **颧大肌与颧小肌** | `Zygomaticus major & minor` | `paired oblique pale-pink strap muscles extending from the zygomatic bone downward and medially to the corner of the mouth and upper lip` | 苹果肌动态上提矢量、过强致动态笑纹 |

## 三、 下面部、唾液腺、下颌韧带与颈部轮廓 (Lower Face, Glands, Ligaments & Neck)

| 中文名称 | 英文解剖术语 | 视觉与组织特征 (Prompt 描述词 - 严禁混淆腺体、脂肪与肌肉) | 对应医美适应症/痛点 |
| :--- | :--- | :--- | :--- |
| **咬肌** | `Masseter muscle` | `thick rectangular multipennate pale-pink striated muscle over the angle and ramus of the mandible` | 下颌角肥大、国字脸、夜磨牙 |
| **颊脂垫 (Bichat 脂垫)** | `Buccal Fat Pad` | `smooth encapsulated rounded golden-yellow deep fat ball nestled in the deep space anterior to the masseter border and deep to the zygomaticus muscles` | 下面部婴儿肥、面颊深部膨出 |
| **下颌缘/口角下浅层脂肪室 (羊腮)** | `Superior & Inferior Jowl Fat Compartments` | `drooping ovoid pale-yellow subcutaneous fat pads located immediately lateral to the marionette line and DAO muscle, sagging across the mandibular border` | 口角囊袋（羊腮/嘟嘟肉）、下颌线中断 |
| **下颌骨支持韧带** | `Mandibular Retaining Ligament` | `focal cluster of pearlescent-white osteocutaneous fibers anchored to the anterior-inferior mandible just medial to the jowl fat pad` | 木偶纹下端卡压凹陷（Pre-jowl sulcus / 颌前沟） |
| **咬肌皮韧带** | `Masseteric Cutaneous Ligaments` | `vertical row of white fibrous tethers aligned along the anterior border of the masseter muscle` | 下面部外侧颊组织向前下滑动的分界韧带 |
| **腮腺** | `Parotid gland` | `buff-yellowish lobular acinar glandular tissue (NOT red muscle, NOT smooth fat) located anterior and inferior to the ear overlapping the posterior masseter` | 耳前/下颌角后方膨出（需与咬肌肥大鉴别） |
| **颌下腺** | `Submandibular gland` | `walnut-sized buff-yellowish lobular salivary gland beneath the inferior mandibular border in the submandibular triangle` | 下颌缘下方突出的“双下巴假象”、腺体下垂 |
| **降口角肌** | `Depressor anguli oris (DAO)` | `triangular pale-pink muscle fibers originating from the mandibular border and converging upward to the mouth corner (modiolus)` | 口角下垂（苦相脸）、木偶纹 (Marionette lines) |
| **降下唇肌** | `Depressor labii inferioris (DLI)` | `quadrangular pale-pink muscle located medial and slightly deep to the DAO, inserting into the lower lip` | 注射 DAO 时需严格避让的靶肌（误打会导致歪嘴） |
| **颏肌** | `Mentalis muscle` | `paired vertical conical pale-pink muscle fibers at the center of the chin tip originating from the incisive fossa` | 下巴核桃纹（卵石样外观）、肌肉紧绷性下巴后缩 |
| **颈阔肌** | `Platysma muscle` | `broad thin fan-like sheet of vertical pale-pink muscle fibers covering the anterior neck and crossing the jawline to blend with lower facial muscles` | 下颌缘轮廓模糊、火鸡颈/颈阔肌竖带 (Platysmal bands) |

## 四、 骨骼重吸收标志与高危血管神经网 (Skeletal Landmarks & Danger Zones)

| 中文名称 | 英文解剖术语 | 视觉与空间走行描述词 | 临床意义 |
| :--- | :--- | :--- | :--- |
| **面动脉-内眦动脉主干** | `Facial Artery to Angular Artery` | `tortuous crimson-red cylindrical artery crossing the inferior mandibular border at the anterior masseter edge, winding ~1cm lateral to the mouth corner, and ascending along the nasolabial fold beside the lateral nose toward the medial canthus` | 下颌缘、法令纹、鼻基底、鼻背注射第一防栓塞血管 |
| **滑车上动脉与眶上动脉** | `Supratrochlear & Supraorbital Arteries` | `paired vertical branching crimson-red arteries emerging from the medial orbital rim at the brow head and ascending vertically across the forehead` | 眉间、额部、隆鼻注射防失明核心血管 |
| **颞浅动脉** | `Superficial Temporal Artery` | `branching crimson-red artery ascending in front of the ear and coursing obliquely across the temple fossa within the superficial temporal fascia` | 太阳穴填充高危血管 |
| **梨状孔与上颌骨重吸收** | `Pyriform Aperture & Maxillary Bone Resorption` | `ivory-white craniofacial bone showing the nasal pyriform aperture rim and anterior maxilla beneath the nasal base` | 骨性鼻基底后缩、中面部骨相衰老 |
| **眶下孔与颏孔神经血管束** | `Infraorbital & Mental Foramina` | `distinct bone foramen (~1cm below mid-orbital rim / on anterior mandible below mouth corner) with a fan-like spray of fine golden-yellow nerve fibers` | 深层骨膜上注射需避让的神经出口 |

## 五、 皮肤微观组织学与纵向解剖层次 (3D Skin Histology & Longitudinal Planes)

| 皮肤层次/靶组织 | 英文解剖术语 | 3D 截面视觉描述词 |
| :--- | :--- | :--- |
| **表皮黑色素沉积** | `Epidermal melanin granules` | `dense dark-brown melanin pigment granules clustered in the basal layer of the epidermis and dermal-epidermal junction` |
| **真皮扩张毛细血管网** | `Dilated dermal capillary plexus` | `congested red and bluish-purple microvascular capillary network visible beneath a thin epidermis` |
| **真皮胶原纤维网断裂 vs 重建** | `Fragmented vs. remodeled collagen bundles` | `loose fragmented pale fibrils vs. dense interwoven pink-white collagen and elastin matrix in the dermis` |
| **浅层脂肪室 vs 深层脂肪室** | `Superficial vs. Deep Fat Compartments` | `plump pale-golden subcutaneous fat lobules above the white SMAS sheet vs. flat amber-gold deep fat pads beneath the muscle directly on the ivory periosteum` |
| **SMAS 筋膜层** | `SMAS (Superficial Musculoaponeurotic System)` | `distinct glistening pearlescent-white fibrous fascial sheet lying between subcutaneous fat and deep mimetic muscle` |
