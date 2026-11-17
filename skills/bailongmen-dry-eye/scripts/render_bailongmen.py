#!/usr/bin/env python3
"""把函干啥嘛的 Markdown 成稿套进图库里医荟她的排版案例，输出公众号正文 HTML。

排版、组件和 Markdown 规则完全复用 wechat-medical-writer/scripts/render_yihui.py，本脚本只在
内存里把所用模板的品牌文字换成函哥（文章署名；公众号名是函干啥嘛），不改 styles.json。替换后正文里仍有“医荟她”时报错退出。

渲染后再做手机端适配，避开公众号“内容结构检测”的“居中布局不一致（#1.4 width）”：
表格（横向滚动容器）改成逐行卡片；参考文献去掉居中 inline-block 外壳和固定高度滚动框，完整展开。
处理后正文里仍有滚动容器时报错退出。

render_yihui.py 先在本脚本同目录找，找不到再到 ../../wechat-medical-writer/scripts/ 找。

用法：render_bailongmen.py <article.md> <styles.json> <out.html> [--layout ID] [--source-note TEXT] [--preview]
"""
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
for path in (HERE, os.path.join(HERE, '..', '..', 'wechat-medical-writer', 'scripts')):
    if os.path.exists(os.path.join(path, 'render_yihui.py')):
        sys.path.insert(0, os.path.abspath(path))
        break
import render_yihui  # noqa: E402

BRAND = '函哥'
# 先换带栏目名的整句，再换剩下的品牌名
REPLACEMENTS = [('医荟她健康 · 女性健康科普', BRAND + ' · 干眼科普'),
                ('医荟她健康 · 晚安科普', BRAND + ' · 晚安科普'),
                ('医荟她健康', BRAND),
                ('医荟她', BRAND)]

TABLE_RE = re.compile(r'<section style="overflow-x:auto;[^"]*">\s*<table[^>]*>(.*?)</table>\s*</section>', re.S)
ROW_RE = re.compile(r'<tr[^>]*>(.*?)</tr>', re.S)
CELL_RE = re.compile(r'<t([hd])[^>]*>(.*?)</t[hd]>', re.S)
CARD = '<section style="margin:0 0 10px;padding:10px 12px;background:#FDF1F4;border-left:3px solid #F3D3D8;">%s</section>'
CARD_TITLE = '<p style="margin:0 0 4px;padding:0;font-weight:bold;color:#333;">%s</p>'
CARD_LINE = '<p style="margin:0;padding:0;font-size:14px;">%s%s</p>'


def rebrand(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def rebranded_styles(styles_path):
    catalog = json.load(open(styles_path, encoding='utf-8'))
    for comp in catalog['components']:
        comp['html'] = rebrand(comp['html'])
    for style in catalog['styles']:
        shell = style.get('template', {}).get('shell')
        if shell:
            style['template']['shell'] = rebrand(shell)
    fd, out = tempfile.mkstemp(suffix='.json', prefix='bailongmen-styles-')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False)
    return out


def table_to_cards(m):
    rows = [CELL_RE.findall(r) for r in ROW_RE.findall(m.group(1))]
    rows = [r for r in rows if r]
    head = None
    if rows and all(kind == 'h' for kind, _ in rows[0]):
        head = [re.sub(r'<[^>]+>', '', c).strip() for _, c in rows.pop(0)]
    cards = []
    for row in rows:
        cells = [c.strip() for _, c in row]
        parts = [CARD_TITLE % cells[0]]
        for i, cell in enumerate(cells[1:], 1):
            label = head[i] if head and i < len(head) and head[i] else ''
            parts.append(CARD_LINE % ('<strong>%s：</strong>' % label if label else '', cell))
        cards.append(CARD % ''.join(parts))
    return '<section style="margin:0 0 16px;">%s</section>' % ''.join(cards)


def mobile_safe(html):
    html = TABLE_RE.sub(table_to_cards, html)
    html = re.sub(r'<section style="text-align:center;">(\s*)<section style="display:inline-block;width:100%;[^"]*">',
                  r'<section>\1<section>', html)
    html = re.sub(r'height:\d+px;overflow-y:auto;', '', html)
    return html


def main():
    argv = sys.argv[1:]
    args = [a for i, a in enumerate(argv)
            if not a.startswith('--') and (i == 0 or argv[i - 1] not in ('--layout', '--source-note'))]
    if len(args) != 3:
        raise SystemExit(__doc__)
    tmp = rebranded_styles(args[1])
    try:
        render_yihui.QA_CREDITS = render_yihui.QA_CREDITS.replace('医荟她健康', BRAND)
        sys.argv = [sys.argv[0]] + [tmp if a == args[1] else a for a in argv]
        render_yihui.main()
    finally:
        os.remove(tmp)
    out = mobile_safe(open(args[2], encoding='utf-8').read())
    with open(args[2], 'w', encoding='utf-8') as f:
        f.write(out)
    if '医荟她' in out:
        raise SystemExit('rebrand incomplete: 医荟她 still appears in %s' % args[2])
    if re.search(r'overflow-[xy]:auto|<table', out):
        raise SystemExit('mobile fix incomplete: scroll box or table still appears in %s' % args[2])


if __name__ == '__main__':
    main()
