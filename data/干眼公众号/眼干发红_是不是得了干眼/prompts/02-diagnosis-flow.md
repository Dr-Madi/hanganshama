# 提示词：02-diagnosis-flow

- 目标路径：`imgs/02-diagnosis-flow.png`
- 案例 ID：`canghe-article-scientific`
- 类型：流程图
- 比例：约 3:4 竖版（size=auto）
- 模型参数：quality=auto，size=auto，n=1，附该案例样图作参考图

## 完整提示词

```text
# scientific

Academic scientific illustration style for technical diagrams and processes

## Design Aesthetic

Academic scientific illustration aesthetic for biological, chemical, and technical diagrams. Clean, precise diagrams with proper labeling and clear visual flow. Educational clarity with professional polish. Textbook quality illustrations.

## Background

- Color: Off-White (#FAFAFA) or Light Blue-Gray (#F0F4F8)
- Texture: None or subtle paper grain

## Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Off-White | #FAFAFA | Primary background |
| Primary Text | Dark Slate | #1E293B | Labels, headers |
| Label Text | Medium Gray | #475569 | Annotations |
| Pathway 1 | Teal | #0D9488 | Primary pathway |
| Pathway 2 | Blue | #3B82F6 | Secondary pathway |
| Pathway 3 | Purple | #8B5CF6 | Tertiary pathway |
| Structure | Amber | #F59E0B | Membranes, structures |
| Alert | Red | #EF4444 | Key elements |
| Positive | Green | #22C55E | Products, outputs |

## Visual Elements

- Precise labeled diagrams
- Flow arrows showing direction
- Modular components with colors
- Chemical formulas and notation
- Cross-section views
- Numbered step sequences
- Molecule and cell representations
- Process summary boxes

## Style Rules

### Do

- Use precise consistent lines
- Label all components clearly
- Show directional flow
- Include technical notation
- Create clear numbered sequences

### Don't

- Use decorative elements
- Create imprecise diagrams
- Omit important labels
- Use inconsistent styling
- Add artistic flourishes

## Best For

Biology articles, chemistry explanations, medical content, research summaries, academic writing, technical documentation, process explanations

---
## 本图要求（替换内容，沿用上面科学图解风格）
流程图，竖版约 3:4，白色或近白底（#FAFAFA），精细线条、圆角矩形框、分区标注、案例分色。自上而下：
1. 顶部标题。
2. 第 1 步框（青绿色边框，左侧带圆形编号“1”）。
3. 向下箭头 → 第 2 步框（左侧圆形编号“2”）。
4. 向下箭头 → 第 3 步框（左侧圆形编号“3”）。
5. 第 3 步下方分成左右两条路径：
   - 左路径：路径上方小标签“直接诊断”；一个蓝色边框条件框 → 向下箭头 → 结果框“诊断干眼”。
   - 右路径：路径上方小标签“临界值”；一个紫色边框条件框 → 向下箭头 → “加做荧光素染色”框 → 向下箭头 → “染色阳性（≥5 个点）”框 → 向下箭头 → 结果框“诊断干眼”。
   - 两个“诊断干眼”结果框用同一种绿色填充（#22C55E 浅色底、绿色边框），大小一致。
6. 底部一行灰色小字。
箭头只表示检查顺序，用细灰线箭头。除圆形编号 1、2、3 外，框里的数字只能是清单原文里的数字，不得新增任何其他数字。

## 约束
- 图中文字只用中文，且只出现下面「中文标签清单」里的文字，逐字一致，不增不减，不写英文、除清单原文和步骤编号 1、2、3 外不加任何数字或公式；标签短而少，无错字、无乱码。
- 参考图只学配色、线条、版式和信息层次；参考图里的英文、示例内容、公式一律不照搬。
- 概念示意，不冒充真实影像；眼部用简洁线条示意。
- 不画真实人脸、Logo、二维码、商品包装、品牌、仿真病变或惊悚画面；不画血丝特写。
- 不把相关画成因果，不把非必然进展画成单向病程箭头。

## 中文标签清单（逐字）
- 图中标题：干眼诊断思路（中国干眼专家共识 2020 年）
- 第 1 步框：有干涩、烧灼等主观症状
- 第 2 步框：问卷评分：中国干眼问卷 ≥7 分，或眼表疾病指数问卷 ≥13 分
- 第 3 步框：泪膜与泪液检查
- 左路径标签：直接诊断
- 左路径条件框：荧光素泪膜破裂时间 ≤5 秒，或非接触泪膜破裂时间 <10 秒，或泪液分泌试验 ≤5 毫米/5 分钟
- 左结果框：诊断干眼
- 右路径标签：临界值
- 右路径条件框：荧光素泪膜破裂时间 5~10 秒，或非接触泪膜破裂时间 10~12 秒，或泪液分泌试验 5~10 毫米/5 分钟
- 右路径下一框：加做荧光素染色
- 右路径再下一框：染色阳性（≥5 个点）
- 右结果框：诊断干眼
- 底部小字：确诊后医生还会进一步判断干眼类型。数据来源：参考文献[2]

```
