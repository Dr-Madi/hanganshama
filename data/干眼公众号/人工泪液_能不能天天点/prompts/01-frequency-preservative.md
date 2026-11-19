# 01-frequency-preservative 绘图记录

- 目标路径：imgs/01-frequency-preservative.png
- 案例 ID：canghe-article-scientific（沿用其背景 #FAFAFA、深灰文字、青绿 #0D9488 / 蓝 #3B82F6 分色和精细线条）
- 类型：数据图（代码绘制，未调用生图模型）
- 内容：使用频率与防腐剂选择：国内外建议对比（中国干眼专家共识 2020：每天 6 次以上；美国眼科学会干眼指南 2023：每天超过 4 次）
- 比例与尺寸：宽 8 英寸 × 200 dpi = 1600 像素（2 倍清晰度），保存时等比缩放到宽 1536
- 字体：Noto Sans CJK SC Regular / Bold（notofonts/noto-cjk，Sans/OTF/SimplifiedChinese）
- 图中文字：与 配图需求.md 清单逐字一致；刻度 0~8 为需求规定的每 1 次一个刻度
- 来源核对（均读取全文）：参考文献[1] 中国干眼专家共识：治疗（2020年）原文“须长期及高频率（如每天6次以上）使用人工泪液者，应优先选择不含防腐剂的人工泪液”；参考文献[5] AAO Dry Eye Syndrome PPP（2023-09-22 批准）原文 “used frequently and chronically (e.g., more than four times a day), nonpreserved tear substitutes are generally recommended”；参考文献[6] 健康中国辟谣科普“开封后4周”“单支装24小时内用完”“保质期针对未开封状态”“遵循说明书”。
- 运行：python3.13 draw_charts.py <字体目录> <输出目录>（两张图共用同一脚本）

## 绘图脚本

```python
"""绘制《人工泪液能天天点吗》两张数据图。用法：python3.13 draw_charts.py <字体目录> <输出目录>"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

FONT_DIR, OUT = Path(sys.argv[1]), Path(sys.argv[2])
for f in ("NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Bold.otf"):
    font_manager.fontManager.addfont(str(FONT_DIR / f))
plt.rcParams["font.family"] = "Noto Sans CJK SC"

# canghe-article-scientific 配色
BG, TEXT, LABEL = "#FAFAFA", "#1E293B", "#475569"
TEAL, BLUE, LINE = "#0D9488", "#3B82F6", "#CBD5E1"
TEAL_FILL, BLUE_FILL = "#CCFBF1", "#DBEAFE"

W_IN, DPI = 8.0, 200  # 8 英寸 x 200 dpi = 1600 像素宽（逻辑宽 800，2 倍清晰度）


def new_fig(h_in):
    fig = plt.figure(figsize=(W_IN, h_in), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h_in / W_IN)
    ax.axis("off")
    return fig, ax


def card(ax, x, y, w, h, edge):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6",
                                fc="white", ec=edge, lw=1.2))


# ---------------- 图 1：使用频率与防腐剂 ----------------
def chart_frequency():
    fig, ax = new_fig(6.0)
    H = 100 * 6.0 / W_IN  # 75
    ax.text(50, H - 6, "点得越勤，越要避开防腐剂", ha="center", va="center",
            fontsize=19, fontweight="bold", color=TEXT)
    ax.plot([50, 50], [9, H - 13], color=LINE, lw=1)  # 中间细灰分隔线

    cols = [
        dict(x0=4, src="中国干眼专家共识（2020 年）", thr=6, thr_lab="每天 6 次以上",
             note="需长期、高频率使用时，优先选不含防腐剂的人工泪液", c=TEAL, fill=TEAL_FILL),
        dict(x0=54, src="美国眼科学会干眼指南（2023 年）", thr=4, thr_lab="每天超过 4 次",
             note="频繁、长期使用时，一般推荐不含防腐剂的人工泪液", c=BLUE, fill=BLUE_FILL),
    ]
    cw, top, bot = 42, H - 13, 9
    for c in cols:
        x0 = c["x0"]
        card(ax, x0, bot, cw, top - bot, c["c"])
        ax.add_patch(Rectangle((x0, top - 6.5), cw, 6.5, fc=c["c"], ec="none"))
        ax.text(x0 + cw / 2, top - 3.25, c["src"], ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="white")
        # 刻度轴：0~8 次，两栏长度一致
        a0, a1, ay = x0 + 4, x0 + cw - 4, 34
        unit = (a1 - a0) / 8
        tx = a0 + c["thr"] * unit
        ax.add_patch(Rectangle((tx, ay), a1 - tx, 14, fc=c["fill"], ec="none"))
        ax.plot([a0, a1], [ay, ay], color=TEXT, lw=1.2)
        for i in range(9):
            xi = a0 + i * unit
            ax.plot([xi, xi], [ay, ay - 1.2], color=TEXT, lw=1)
            ax.text(xi, ay - 3.2, str(i), ha="center", va="center", fontsize=8, color=LABEL)
        ax.text((a0 + a1) / 2, ay - 7.5, "每天使用次数", ha="center", va="center",
                fontsize=8.5, color=LABEL)
        # 浅色填充区图例
        lx = (a0 + a1) / 2 - 7.5
        ax.add_patch(Rectangle((lx, 20.6), 2.6, 2.4, fc=c["fill"], ec=c["c"], lw=0.8))
        ax.text(lx + 3.6, 21.8, "优先选不含防腐剂", ha="left", va="center",
                fontsize=8.5, color=c["c"], fontweight="bold")
        ax.plot([tx, tx], [ay, ay + 15.5], color=c["c"], lw=2.2)
        ax.text(tx, ay + 18, c["thr_lab"], ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=c["c"])
        # 说明
        ax.text(x0 + cw / 2, 14.5, c["note"], ha="center", va="center", fontsize=8.3,
                color=TEXT, wrap=False)
    ax.text(50, 4, "具体用法请遵医嘱。数据来源：参考文献[1][5]", ha="center", va="center",
            fontsize=8.5, color=LABEL)
    out = OUT / "01-frequency-preservative.png"
    fig.savefig(out, dpi=DPI, facecolor=BG)
    plt.close(fig)
    return out


# ---------------- 图 2：开封后能用多久 ----------------
def draw_bottle(ax, cx, by):
    """简洁线条瓶装滴眼液轮廓（无文字、无品牌）。"""
    kw = dict(fc="white", ec=TEAL, lw=1.6)
    ax.add_patch(FancyBboxPatch((cx - 4.5, by), 9, 13, boxstyle="round,pad=0,rounding_size=1.4", **kw))
    ax.add_patch(Rectangle((cx - 2.2, by + 13), 4.4, 2.2, **kw))
    ax.add_patch(FancyBboxPatch((cx - 1.2, by + 15.2), 2.4, 3.6,
                                boxstyle="round,pad=0,rounding_size=1.0", **kw))


def draw_vial(ax, cx, by):
    """简洁线条单支装小管轮廓（无文字、无品牌）。"""
    kw = dict(fc="white", ec=BLUE, lw=1.6)
    ax.add_patch(FancyBboxPatch((cx - 2.4, by), 4.8, 11, boxstyle="round,pad=0,rounding_size=1.6", **kw))
    ax.add_patch(Rectangle((cx - 0.9, by + 11), 1.8, 3.2, **kw))
    ax.add_patch(Rectangle((cx - 2.6, by + 14.2), 5.2, 4.2, **kw))


def chart_after_opening():
    fig, ax = new_fig(6.4)
    H = 100 * 6.4 / W_IN  # 80
    ax.text(50, H - 6, "人工泪液开封后能用多久", ha="center", va="center",
            fontsize=19, fontweight="bold", color=TEXT)
    ax.plot([50, 50], [24, H - 13], color=LINE, lw=1)
    cw, top, bot = 42, H - 14, 24
    specs = [
        dict(x0=4, title="瓶装", bar="开封后一般不超过 4 周", small="开封时记下日期",
             c=TEAL, fill=TEAL_FILL, icon=draw_bottle),
        dict(x0=54, title="单支装", bar="开封后一般 24 小时内用完", small="有剩余也不要再用",
             c=BLUE, fill=BLUE_FILL, icon=draw_vial),
    ]
    for s in specs:
        x0 = s["x0"]
        cx = x0 + cw / 2
        card(ax, x0, bot, cw, top - bot, s["c"])
        ax.text(cx, top - 4.2, s["title"], ha="center", va="center", fontsize=14,
                fontweight="bold", color=s["c"])
        s["icon"](ax, cx, bot + 16)
        # 时间条：两栏各自独立，不按同一比例
        bx0, bx1, byy = x0 + 4, x0 + cw - 4, bot + 7.5
        ax.add_patch(FancyBboxPatch((bx0, byy), bx1 - bx0, 5.5,
                                    boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=s["fill"], ec=s["c"], lw=1.2))
        ax.text(cx, byy + 2.75, s["bar"], ha="center", va="center", fontsize=10,
                fontweight="bold", color=s["c"])
        ax.text(cx, bot + 3.8, s["small"], ha="center", va="center", fontsize=9, color=LABEL)
    # 通栏提示条
    ax.add_patch(FancyBboxPatch((4, 11), 92, 8, boxstyle="round,pad=0,rounding_size=1.4",
                                fc="#F0F4F8", ec=LINE, lw=1))
    ax.text(50, 15, "瓶身保质期指未开封状态；说明书另有规定的，以说明书为准",
            ha="center", va="center", fontsize=10, color=TEXT)
    ax.text(50, 5, "数据来源：参考文献[6]", ha="center", va="center", fontsize=8.5, color=LABEL)
    out = OUT / "02-after-opening.png"
    fig.savefig(out, dpi=DPI, facecolor=BG)
    plt.close(fig)
    return out


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for p in (chart_frequency(), chart_after_opening()):
        print(p)
```
