# 函干啥嘛 · 干眼科普工作流

个人公众号「函干啥嘛」的干眼主题稿件和写作规范。写稿和配图由两个 Claude 云端定时任务完成，产物先写进私有仓库 personal-workbench；作者电脑上的计划任务再把配好图的文章同步到本仓库，生成公开的粘贴版网页：

| 任务 | 台北时间 | 做什么 |
|---|---|---|
| 写稿 | 周一、三、五 07:37 | 按选题清单和风格洗牌袋写一篇，写好配图需求，提交到 `data/干眼公众号/` |
| 配图 | 周一、三、五 11:00 | 生成封面和正文配图，推送后发通知 |
| 同步（作者电脑） | 周一、三、五 11:40，错过则开机补跑 | `tools/sync_from_workbench.py`：复制配好图的文章，渲染 `paste.html` 和首页，推送到 Pages |

函干啥嘛是未认证的个人号，没有草稿箱接口。作者打开 https://dr-madi.github.io/hanganshama/ ，点进文章后「复制正文」，粘贴到公众号编辑器，人工审读后手动发表。

## 目录

- `data/干眼公众号/`：选题清单、风格记录、封面轮换，以及每篇文章的目录（正文、配图需求、`imgs/`、`paste.html`）
- `skills/bailongmen-dry-eye/`：函干啥嘛适配层（干眼选题、三种风格、品牌约束、排版脚本）
- `skills/wechat-medical-writer/`：沿用的医学证据约束、科学图约束和排版脚本 `render_yihui.py`
- `skills/content-research-writer/`：通用写作流程（MIT，见其 LICENSE 和 UPSTREAM.md）
- `tools/sync_from_workbench.py`：同步脚本，用法 `python tools/sync_from_workbench.py <personal-workbench 目录> [--dry-run]`；`--dry-run` 只在本地生成，不拉取、不提交
- `gallery/`：所用排版、封面和配图风格的案例（`styles.json`）和样图，来源见 `gallery/THIRD_PARTY_NOTICES.md`

## 本地排版

```
python skills/bailongmen-dry-eye/scripts/render_bailongmen.py <文章.md> gallery/styles.json <输出.html> --layout layout-current --preview
```

可选排版：`layout-yihui-interview`（问答稿）、`layout-current`、`layout-yihui-sakura`、`layout-yihui-mint`、`layout-yihui-lavender`。

文章只做健康科普，不替代面诊；不推荐具体品牌、商品或机构。
