from pathlib import Path
import re, json, html, hashlib

root = Path.cwd()
base = root / '.cache-build'
out = root / '_site'
md = (root / 'content/solutions.md').read_text(encoding='utf-8')
esc = html.escape
parts = re.split(r'(?m)^## (\d-\d) (.+)\n', md)
rows = []
for i in range(1, len(parts), 3):
    qid, title, body = parts[i:i+3]
    steps = re.split(r'(?m)^### [①②③④] .+\n', body)[1:]
    label, prompt = steps[0].strip().split('\n\n', 1)
    prompt = '\n'.join(re.sub(r'^> ?', '', line) for line in prompt.splitlines())
    method, follow = steps[2].strip().split('\n\n', 1)
    method = re.sub(r'^\*\*方法：|\*\*$', '', method)
    rows.append(dict(id=qid, title=title, stage=qid[0], prompt_label=label.rstrip('：'), prompt=prompt, stop=steps[1].strip(), method=method, follow=follow.strip(), verify=steps[3].strip()))
assert len(rows) == 19
intro = parts[0].split('# AI賦能會計｜19題解題過程\n\n', 1)[1].split('## 卡關時可以怎麼做')[0].strip()
method_text = parts[0].split('## 卡關時可以怎麼做\n\n', 1)[1].strip()
methods = re.findall(r'^- \*\*(.+?)\*\*：(.+)$', method_text, re.M)
stages = {'1': ('對話型 AI', '把需求說清楚，把回應問明白。'), '2': ('資料、圖表與簡報', '從一份資料，走到能交付的成果。'), '3': ('Vibe Coding', '把想法做成可以操作的小工具。')}
arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
rail = ''
catalog = ''
for stage, (name, subtitle) in stages.items():
    items = [r for r in rows if r['stage'] == stage]
    rail += f'<section class="rail-group" data-group="{stage}"><h3>階段{stage} <span>{name}</span></h3>'
    rail += ''.join(f'<a class="question-link" href="#q-{r["id"]}" data-id="{r["id"]}"><span class="link-id">{r["id"]}</span><span>{esc(r["title"])}</span></a>' for r in items) + '</section>'
    catalog += f'<section class="catalog-stage" data-group="{stage}"><div class="stage-heading"><span class="stage-number">{stage}</span><div><h3>{name}</h3><p>{subtitle}</p></div><span class="stage-size">{len(items)} 題</span></div><div class="catalog-rows">'
    catalog += ''.join(f'<a class="catalog-link" href="#q-{r["id"]}" data-id="{r["id"]}"><span class="link-id">{r["id"]}</span><span>{esc(r["title"])}</span>{arrow}</a>' for r in items) + '</div></section>'
articles = ''
for r in rows:
    qid = r['id']
    def text(value): return esc(value).replace('\n', '<br>')
    articles += f'''<article id="q-{qid}" class="reader" hidden tabindex="-1" aria-labelledby="title-{qid}">
<div class="reader-meta"><span>階段{r['stage']} · {stages[r['stage']][0]}</span><span>{qid}</span></div>
<h1 id="title-{qid}">{esc(r['title'])}</h1><p class="reader-desc">先看怎麼問，再看哪裡要停。最後，替成果做一次驗證。</p>
<div class="step"><span class="step-number">1</span><div class="step-content"><div class="step-heading"><h2>第一句怎麼問</h2><button class="copy" data-copy="{qid}" type="button">複製提示詞</button></div><p class="source">{esc(r['prompt_label'])}</p><blockquote id="prompt-{qid}">{text(r['prompt'])}</blockquote></div></div>
<div class="step"><span class="step-number">2</span><div class="step-content"><h2>AI 卡在哪／哪裡要停</h2><p>{text(r['stop'])}</p></div></div>
<div class="step"><span class="step-number">3</span><div class="step-content"><h2>怎麼追問／換招</h2><p class="method">方法：{esc(r['method'])}</p><p>{text(r['follow'])}</p></div></div>
<div class="step"><span class="step-number">4</span><div class="step-content"><details class="verify"><summary><span>怎麼驗</span><span class="verify-hint">展開驗證與答案</span>{arrow}</summary><p>{text(r['verify'])}</p></details></div></div>
<nav class="reader-bottom" aria-label="閱讀下一題">{f'<a href="#q-{rows[rows.index(r)-1]["id"]}">上一題</a>' if rows.index(r) else '<span></span>'}<a href="#contents">回題目總覽</a>{f'<a href="#q-{rows[rows.index(r)+1]["id"]}">下一題 {arrow}</a>' if rows.index(r)<18 else '<span></span>'}</nav></article>'''
page=(root/'src/base.html').read_text(encoding='utf-8').replace('BASE_STYLE',(root/'src/base.css').read_text(encoding='utf-8')).replace('BASE_SCRIPT',(root/'src/base.js').read_text(encoding='utf-8'))
replacements = {'ARROW':arrow, 'RAIL':rail, 'INTRO':''.join(f'<p>{esc(p)}</p>' for p in intro.split('\n\n')), 'CATALOG':catalog, 'METHODS':''.join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a,b in methods), 'ARTICLES':articles, 'DATA':json.dumps(rows, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')}
for key,value in replacements.items(): page=page.replace(key,value)
page=page.replace('</style>', '.reader:focus{outline:none}</style>')
feature = root / 'src/card/extension.py'
if feature.exists():
    import runpy
    page = runpy.run_path(str(feature))['augment'](page, rows, root)
practice_feature = root / 'src/practice/extension.py'
if practice_feature.exists():
    import runpy
    page = runpy.run_path(str(practice_feature))['augment'](page, root)
(out/'index.html').write_text(page,encoding='utf-8')
(base/'rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
assert md==(root/'content/solutions.md').read_text(encoding='utf-8')
print('Generated 19 questions from authoritative Markdown; Markdown unchanged.')
