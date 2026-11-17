#!/usr/bin/env python3
"""把摆龙门的 Markdown 成稿套进图库里医荟她的排版案例，输出公众号正文 HTML。

排版、组件和 Markdown 规则完全复用 wechat-medical-writer/scripts/render_yihui.py，本脚本只在
内存里把所用模板的品牌文字换成函哥（文章署名；公众号名仍是摆龙门），不改 styles.json。替换后正文里仍有“医荟她”时报错退出。

render_yihui.py 先在本脚本同目录找，找不到再到 ../../wechat-medical-writer/scripts/ 找。

用法：render_bailongmen.py <article.md> <styles.json> <out.html> [--layout ID] [--source-note TEXT] [--preview]
"""
import json
import os
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
    out = open(args[2], encoding='utf-8').read()
    if '医荟她' in out:
        raise SystemExit('rebrand incomplete: 医荟她 still appears in %s' % args[2])


if __name__ == '__main__':
    main()
