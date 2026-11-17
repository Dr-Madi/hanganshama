#!/usr/bin/env python3
"""把 personal-workbench 里配好图的函干啥嘛文章同步到本仓库，并生成粘贴版网页。

云端任务把稿件和配图写进私有仓库 personal-workbench；私有仓库开不了免费 Pages，
图片也没有公网地址，粘贴到公众号编辑器时会丢图。本脚本在作者电脑上定时运行：

1. 拉取两个仓库；
2. 同步 data/干眼公众号/ 的三个记录文件；
3. 配图需求里列出的图都已生成的文章，复制正文、配图需求、imgs/、prompts/；
4. 渲染 paste.html（图片改成 Pages 绝对地址，带「复制正文」按钮）和首页 index.html；
5. 只提交这些路径，推送到 Dr-Madi/hanganshama。

用法：sync_from_workbench.py <personal-workbench 目录> [--dry-run]
"""
import argparse
import datetime
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUBDIR = Path('data') / '干眼公众号'
PAGES = 'https://dr-madi.github.io/hanganshama/'
RECORDS = ['选题清单.md', '风格记录.md', '封面轮换.md']
RENDER = REPO / 'skills' / 'bailongmen-dry-eye' / 'scripts' / 'render_bailongmen.py'
STYLES = REPO / 'gallery' / 'styles.json'
IMG_REF = re.compile(r'imgs/[A-Za-z0-9._\-]+\.(?:png|jpg|jpeg|webp)')
LAYOUT_REF = re.compile(r'文章排版[^`\n]*`([a-z0-9-]+)`')
DONE_ENTRY = re.compile(r'^- \[x\] 【(.+?)】(.+?)（`([^`/]+)/')


def log(msg):
    print('%s %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg), flush=True)


def git(repo, *args, check=True):
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode != 0:
        raise SystemExit('git %s 失败：%s' % (' '.join(args), (r.stderr or r.stdout).strip()))
    return r.stdout.strip()


def page_url(folder, name):
    return PAGES + urllib.parse.quote('%s/%s/%s' % (SUBDIR.as_posix(), folder, name))


def article_md(src_dir):
    mds = [p for p in src_dir.glob('*.md') if p.name != '配图需求.md']
    return mds[0] if len(mds) == 1 else None


def ready(src_dir):
    """配图需求里列出的图都已存在且非空，才算可以发布。"""
    req = src_dir / '配图需求.md'
    md = article_md(src_dir)
    if not req.exists() or md is None:
        return False
    need = set(IMG_REF.findall(req.read_text(encoding='utf-8'))) | set(IMG_REF.findall(md.read_text(encoding='utf-8')))
    need.add('imgs/cover.png')
    return all((src_dir / n).is_file() and (src_dir / n).stat().st_size > 0 for n in need)


def copy_tree(src, dst):
    changed = False
    for f in src.rglob('*'):
        if not f.is_file() or f.name == 'paste.html':
            continue
        t = dst / f.relative_to(src)
        if t.exists() and t.read_bytes() == f.read_bytes():
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, t)
        changed = True
    return changed


PASTE_SHELL = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title} · 函干啥嘛粘贴版</title>
<style>
body{{margin:0;background:#f2f2f2;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}
.bar{{position:sticky;top:0;z-index:9;background:#1f2a24;color:#fff;padding:10px 16px;font-size:14px;line-height:1.6}}
.bar b{{font-size:15px}} .bar a{{color:#9fe0b8}}
.bar button{{margin:6px 8px 0 0;padding:6px 14px;border:0;border-radius:4px;background:#3fa36b;color:#fff;font-size:14px;cursor:pointer}}
.bar .tip{{opacity:.8;font-size:12px}}
.page{{max-width:578px;margin:16px auto;background:#fff;padding:20px 16px}}
.cover{{max-width:578px;margin:16px auto 0}} .cover img{{width:100%;display:block}}
</style></head><body>
<div class="bar"><b>{title}</b><br>
<button id="copy-body">复制正文</button><button id="copy-title">复制标题</button>
<a href="{cover}" download>下载封面</a> · <a href="{home}">返回列表</a>
<div class="tip">复制正文后到公众号编辑器里粘贴；封面单独上传。发表前请通读正文、核对配图和医学引用。<span id="msg"></span></div></div>
<div class="cover"><img src="{cover}" alt="封面"></div>
<div class="page"><div id="article">{body}</div></div>
<script>
function copyNode(node){{var r=document.createRange();r.selectNodeContents(node);var s=getSelection();s.removeAllRanges();s.addRange(r);var ok=document.execCommand('copy');s.removeAllRanges();return ok}}
function say(t){{document.getElementById('msg').textContent=' '+t}}
document.getElementById('copy-body').onclick=function(){{say(copyNode(document.getElementById('article'))?'已复制正文':'复制失败，请手动全选正文复制')}};
document.getElementById('copy-title').onclick=function(){{var n=document.createElement('span');n.textContent={title_js};document.body.appendChild(n);var ok=copyNode(n);n.remove();say(ok?'已复制标题':'复制失败')}};
</script></body></html>
'''


def render_paste(dst_dir, folder):
    md = article_md(dst_dir)
    text = md.read_text(encoding='utf-8')
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith('# ')), md.stem)
    m = LAYOUT_REF.search((dst_dir / '配图需求.md').read_text(encoding='utf-8'))
    layout = m.group(1) if m else ('layout-yihui-interview' if ('**函哥答：**' in text or '**摆龙门答：**' in text) else 'layout-current')
    tmp = dst_dir / '.fragment.html'
    r = subprocess.run([sys.executable, str(RENDER), str(md), str(STYLES), str(tmp), '--layout', layout],
                       capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError('%s 排版失败：%s' % (folder, (r.stderr or r.stdout).strip()))
    body = tmp.read_text(encoding='utf-8')
    tmp.unlink()
    body = re.sub(r'(src=["\'])(imgs/[^"\']+)', lambda x: x.group(1) + page_url(folder, x.group(2)), body)
    out = PASTE_SHELL.format(title=html.escape(title), title_js=json.dumps(title, ensure_ascii=False),
                             cover='imgs/cover.png', home=PAGES, body=body)
    (dst_dir / 'paste.html').write_text(out, encoding='utf-8')
    return title, layout


def render_index(dst_root, published):
    done = []
    for line in (dst_root / '选题清单.md').read_text(encoding='utf-8').splitlines():
        m = DONE_ENTRY.match(line.strip())
        if m and m.group(3) in published:
            done.append((m.group(1), m.group(2), m.group(3)))
    listed = {d[2] for d in done}
    done += [('', published[f], f) for f in sorted(published) if f not in listed]
    rows = '\n'.join('<li><a href="%s">%s</a> <small>%s</small></li>' % (
        html.escape(urllib.parse.quote('%s/%s/paste.html' % (SUBDIR.as_posix(), f))), html.escape(t), html.escape(s))
        for s, t, f in reversed(done))
    (REPO / 'index.html').write_text('''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>函干啥嘛粘贴版</title>
<style>body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;max-width:640px;margin:24px auto;padding:0 16px;line-height:1.8}
small{color:#888}</style></head><body>
<h1>函干啥嘛 · 干眼科普</h1><p>最新的在最上面。点进去后「复制正文」，到公众号编辑器粘贴，审读后手动发表。</p>
<ul>
%s
</ul></body></html>
''' % (rows or '<li>还没有配好图的文章</li>'), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('workbench')
    ap.add_argument('--dry-run', action='store_true', help='只在本地生成，不拉取、不提交')
    a = ap.parse_args()
    wb = Path(a.workbench).resolve()

    if not a.dry_run:
        git(wb, 'pull', '--ff-only', '-q', 'origin', 'main')
        git(REPO, 'pull', '--ff-only', '-q', 'origin', 'main')
    src_root, dst_root = wb / SUBDIR, REPO / SUBDIR
    dst_root.mkdir(parents=True, exist_ok=True)
    for name in RECORDS:
        if (src_root / name).exists():
            shutil.copy2(src_root / name, dst_root / name)

    published, errors = {}, []
    for src_dir in sorted(p for p in src_root.glob('*') if p.is_dir()):
        folder = src_dir.name
        if not ready(src_dir):
            log('未配齐图，跳过：%s' % folder)
            continue
        dst_dir = dst_root / folder
        changed = copy_tree(src_dir, dst_dir)
        try:
            if changed or not (dst_dir / 'paste.html').exists():
                title, layout = render_paste(dst_dir, folder)
                log('已生成粘贴版：%s（%s）%s' % (title, layout, page_url(folder, 'paste.html')))
        except RuntimeError as e:
            errors.append(str(e))
            log(str(e))
            continue
        md = article_md(dst_dir)
        published[folder] = next((l[2:].strip() for l in md.read_text(encoding='utf-8').splitlines()
                                  if l.startswith('# ')), md.stem)
    render_index(dst_root, published)

    if a.dry_run:
        log('dry-run：本地已生成 %d 篇，未提交' % len(published))
    else:
        git(REPO, 'add', '--', SUBDIR.as_posix(), 'index.html')
        if git(REPO, 'diff', '--cached', '--name-only'):
            git(REPO, 'commit', '-q', '-m', 'sync: 同步函干啥嘛文章与粘贴版（%d 篇）' % len(published))
            git(REPO, 'push', '-q', 'origin', 'main')
            log('已推送：%s' % PAGES)
        else:
            log('没有变化')
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
