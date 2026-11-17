---
name: bailongmen-dry-eye
description: 为个人公众号「摆龙门」写干眼主题医学科普：领域选题地图、三种写作风格（患者常见问题 / 科普 / 最新研究进展）及洗牌袋抽取规则、摆龙门品牌约束与排版适配。医学证据约束和配图约束复用 wechat-medical-writer。
---

# 摆龙门 · 干眼科普适配层

「摆龙门」是作者的个人公众号，这套规范只用于它的干眼主题文章。写作、配图、排版流程沿用医荟她健康（`wechat-medical-writer`），这里只放摆龙门特有的内容：

| 需要 | 读取 |
|---|---|
| 医学证据边界（最重要） | `../wechat-medical-writer/references/medical-constraints.md` |
| 数据图、科学图约束 | `../wechat-medical-writer/references/medical-figure-design.md` |
| 干眼选题范围与权威来源 | [干眼领域](references/dry-eye.md) |
| 三种风格怎么写、怎么抽 | [写作风格](references/writing-styles.md) |
| 谁在说话、署名、落款 | [摆龙门品牌](references/brand-bailongmen.md) |
| 排版 | `scripts/render_bailongmen.py`：沿用图库里医荟她的排版案例，只把品牌文字换成摆龙门 |

与医荟她的区别：

- 发布主体是**摆龙门**，不出现医荟她健康的名称、Logo、落款；医荟她的品牌文件不读。
- 文章放本仓库（Dr-Madi/bailongmen）的 `data/干眼公众号/`，不放 `data/医学公众号/`。
- 不写种草文：不推荐具体品牌、商品、店铺、机构，不写带货或测评。
- 问答稿回答一方署「摆龙门」（`**摆龙门答：**`）。
- 摆龙门是未认证的个人号，没有草稿箱接口：配图任务把排好版的粘贴版网页发到本仓库的 GitHub Pages，作者打开后复制粘贴进公众号编辑器，人工审读后手动发表。不调用任何草稿或发布接口，也不用医荟她、小团子Java 的令牌。
