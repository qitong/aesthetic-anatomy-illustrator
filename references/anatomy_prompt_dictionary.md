# 医美临床解剖与多模态生图映射词典 (Aesthetic Anatomy Prompt Dictionary)

本词典供 `aesthetic-anatomy-illustrator` Skill 在构建中英文生图提示词时查阅，确保解剖位置、肌纤维方向、组织色泽与医美临床痛点完全对应。

## 一、 上面部与眼周 (Upper Face & Periorbital)

| 中文名称 | 英文解剖术语 | 肌纤维走向与视觉特征 (Prompt 描述词) | 对应医美适应症/痛点 | 力学箭头方向 (Type A) |
| :--- | :--- | :--- | :--- | :--- |
| **额肌** | `Frontalis muscle` | `broad vertical pale-pink muscle fibers covering the forehead, inserting into the eyebrow skin` | 抬头纹 (Forehead lines)、眉下垂、眉位平衡 | 暖金色向上箭头 (`upward lifting vector`) |
| **皱眉肌** | `Corrugator supercilii` | `oblique deep muscle fibers extending upward and laterally from the glabella to the middle eyebrow` | 川字纹/眉间垂直纹 (Glabellar vertical frown lines) | 冰蓝色向内下方箭头 (`inward-downward contraction vector`) |
| **降眉间肌** | `Procerus muscle` | `pyramid-shaped vertical muscle fibers between the eyebrows at the nasal root` | 鼻根横纹、眉心下压 | 冰蓝色垂直向下箭头 (`vertical downward vector`) |
| **降眉肌** | `Depressor supercilii` | `slender vertical fibers at the medial eyebrow head blending with orbicularis oculi` | 眉头下压、眉间纹辅助肌 | 冰蓝色向下箭头 |
| **眼轮匝肌** | `Orbicularis oculi` | `concentric circular sphincter muscle fibers surrounding the eye orbit and eyelids` | 鱼尾纹 (Crow's feet)、眼下动态细纹、卧蚕肥大 | 外侧与内侧向心性收缩箭头 |
| **颞肌** | `Temporalis muscle` | `fan-shaped muscle fibers in the temple fossa converging downward toward the mandibular coronoid process` | 太阳穴凹陷评估、咀嚼代偿性肥大 | 向斜下方汇聚 |

## 二、 中面部：容积、脂肪垫与支持韧带 (Midface Volume, Fat Pads & Ligaments)

| 中文名称 | 英文解剖术语 | 视觉与组织特征 (Prompt 描述词) | 对应医美适应症/痛点 |
| :--- | :--- | :--- | :--- |
| **眼轮匝肌支持韧带** | `Orbicularis Retaining Ligament (ORL)` | `pearlescent white fibrous ligamentous tether attaching along the inferior orbital rim` | 泪沟凹陷 (Tear trough deformity)、眼袋下界卡压 |
| **颧皮韧带/颧弓韧带** | `Zygomatic retaining ligament` | `dense white fibrous tethering points along the zygomatic arch` | 印第安纹/颧颊沟 (Malar mound / Festoons) |
| **深层颊脂垫/SOOF** | `Deep medial cheek fat & SOOF (Sub-orbicularis oculi fat)` | `soft golden-yellow lobular adipose compartments deep to the muscle layer` | 中面部骨相容积流失、苹果肌干瘪、泪沟深层支撑缺失 |
| **浅层苹果肌脂肪垫** | `Superficial nasolabial & malar fat pads` | `plump pale-yellow subcutaneous fat compartments sliding inferiorly` | 脂肪垫下移导致的法令纹压迫加深 |
| **提上唇鼻翼肌** | `Levator labii superioris alaeque nasi (LLSAN)` | `slender vertical muscle running alongside the lateral nose to the upper lip and nostril wing` | 露龈笑 (Gummy smile)、鼻翼宽大牵拉、动态法令纹上段 |

## 三、 下面部、唾液腺与颈部轮廓 (Lower Face, Glands & Neck)

| 中文名称 | 英文解剖术语 | 视觉与组织特征 (Prompt 描述词 - 严禁混淆腺体与肌肉) | 对应医美适应症/痛点 |
| :--- | :--- | :--- | :--- |
| **咬肌** | `Masseter muscle` | `thick rectangular multipennate striated muscle over the angle of the mandible` | 下颌角肥大、国字脸、夜磨牙 |
| **腮腺** | `Parotid gland` | `yellowish lobular glandular tissue (NOT red muscle) located anterior and inferior to the ear` | 耳前/下颌角后方膨出（需与咬肌肥大鉴别） |
| **颌下腺** | `Submandibular gland` | `walnut-sized yellowish lobular salivary gland beneath the inferior mandibular border` | 下颌缘下方突出的“双下巴假象”、腺体下垂 |
| **降口角肌** | `Depressor anguli oris (DAO)` | `triangular pale-pink muscle fibers from the mandibular border converging upward to the mouth corner` | 口角下垂（苦相脸）、木偶纹 (Marionette lines) |
| **颏肌** | `Mentalis muscle` | `paired vertical conical muscle fibers at the center of the chin tip` | 下巴核桃纹（卵石样外观）、肌肉紧绷性下巴后缩 |
| **颈阔肌** | `Platysma muscle` | `broad thin fan-like sheet of vertical muscle fibers covering the anterior neck and crossing the jawline` | 下颌缘轮廓模糊、火鸡颈/颈阔肌竖带 (Platysmal bands) |

## 四、 皮肤微观组织学截面 (3D Skin Histology PIP)

| 皮肤层次/靶组织 | 英文解剖术语 | 3D 截面视觉描述词 |
| :--- | :--- | :--- |
| **表皮黑色素沉积** | `Epidermal melanin granules` | `dense dark-brown melanin pigment granules clustered in the basal layer of the epidermis` |
| **真皮扩张毛细血管网** | `Dilated dermal capillary plexus` | `congested red and bluish-purple microvascular capillary network visible beneath a thin epidermis` |
| **真皮胶原纤维网断裂 vs 重建** | `Fragmented vs. remodeled collagen bundles` | `loose fragmented pale fibrils vs. dense interwoven pink-white collagen and elastin matrix in the dermis` |
| **SMAS 筋膜层** | `SMAS (Superficial Musculoaponeurotic System)` | `distinct glistening white fibrous fascial sheet lying between subcutaneous fat and deep muscle` |
