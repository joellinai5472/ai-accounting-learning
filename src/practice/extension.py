from pathlib import Path
import re,json,html

def augment(page,root):
    base=root/'src/practice'
    questions=json.loads((root/'.cache-build/practice.json').read_text(encoding='utf-8'))
    byid={q['id']:q for q in questions};esc=html.escape
    arrow='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
    fullpath='下載/AI賦能會計_完整練習包.zip'
    labels={'CSV':'CSV','XLSX':'Excel','PDF':'PDF','DOCX':'Word','TXT':'文字','PNG':'PNG'}
    def download(f):
        return f'<a class="asset-download" href="{esc(f["path"],quote=True)}" download="{esc(f["name"],quote=True)}">{labels[f["ext"]]}</a>'
    def materials(q):
        start=f'<section class="practice-materials"><div class="materials-heading"><h2>準備素材</h2><span>{q["materialCount"]} 個檔案</span></div>'
        if not q['groups']:return start+'<p class="no-materials">本題不需下載素材，直接依題目開始練習。</p></section>'
        result=start+'<p class="material-tip">先預覽；需要上傳給 AI 或編輯時再下載。</p>'
        for i,g in enumerate(q['groups']):
            is_receipt=q['id']=='2-2'
            preview_file=next((f for f in g['files'] if f['ext']=='PDF'),next((f for f in g['files'] if f['preview']),None))
            assert preview_file,q['id']+' '+g['title']
            kind=preview_file['preview']['kind'];preview_name='預覽圖片' if is_receipt else {'pdf':'預覽 PDF','table':'預覽表格','text':'預覽文字','image':'預覽圖片'}[kind]
            preview=f'<button class="asset-preview" type="button" data-preview-question="{q["id"]}" data-preview-group="{i}">{preview_name}</button>'
            file_meta=' · '.join(labels[f['ext']] for f in g['files']) if not is_receipt else '15 張 PNG 原圖'
            result+=f'<div class="material-group{" receipt-group" if is_receipt else ""}">'
            if is_receipt:
                result+=f'<div class="receipt-top"><div class="material-name">{g["title"]}<small>{file_meta}</small></div>{preview}</div><details class="receipt-file-list"><summary>個別下載 15 張收據</summary><div class="receipt-links">'
                result+=''.join(f'<a class="asset-download" href="{esc(f["path"],quote=True)}" download="{esc(f["name"],quote=True)}">{esc(f["title"])}</a>' for f in g['files'])+'</div></details>'
            else:result+=f'<div class="material-name">{esc(g["title"])}<small>{file_meta}</small></div><div class="material-actions">{preview}'+''.join(download(f) for f in g['files'])+'</div>'
            result+='</div>'
        result+=f'<div class="material-archive-actions"><a class="question-archive package-archive" href="{esc(q["archive"],quote=True)}" download>下載本題素材 · ZIP {arrow}</a><a class="complete-pack-mini package-archive" href="{fullpath}" download>下載完整練習包</a></div></section>'
        return result
    touched=[]
    def article(match):
        old=match.group(0);qid=match.group(1);q=byid[qid];touched.append(qid)
        step=old.index('<div class="step">');bottom=old.index('<nav class="reader-bottom"')
        heading=old[:step].replace('先看怎麼問，再看哪裡要停。最後，替成果做一次驗證。','先看題目，拿素材自己試。需要時，再展開參考解法。')
        question=f'<section class="practice-question"><h2>這題要做什麼</h2><p class="question-story">{esc(q["story"])}</p><p class="question-task">{esc(q["task"])}</p><p class="question-outcome"><b>成果要求：</b>{esc(q["requirement"])}</p></section>'
        solution=f'<details class="solution"><summary>看參考解法<span>起手需求、換招與驗證</span>{arrow}</summary><div class="solution-body">'+old[step:bottom]+'</div></details>'
        return heading+question+materials(q)+solution+old[bottom:]
    page=re.sub(r'<article id="q-(\d-\d)"[\s\S]*?</article>',article,page)
    assert len(touched)==19
    css=(base/'practice.css').read_text(encoding='utf-8');page=page.replace('</style>',css+'\n</style>')
    banner=f'<aside class="pack-banner"><div><h2>把整套練習一起帶走</h2><p>題目、素材與參考解法都包含在內，解壓後可離線開啟。</p></div><a class="full-pack-download package-archive" href="{fullpath}" download>下載完整練習包 · ZIP</a></aside>'
    page=page.replace('<div class="catalog" id="catalog">',banner+'<div class="catalog" id="catalog">')
    page=page.replace('挑一題做過或卡住的挑戰，回看第一句怎麼問、哪裡要停、怎麼換招。','挑一題重新試試看：完整題目、練習素材與參考解法，都在這裡。')
    page=page.replace('起手需求 → 換招 → 驗證','看題目 → 拿素材 → 動手練習')
    page=page.replace('解題筆記','練習與解題').replace('19 題練習與解題','19 題練習').replace('解題筆記與帶走卡','練習與帶走卡')
    dialog='''<dialog class="material-dialog" id="material-dialog" aria-labelledby="preview-title"><header class="material-preview-header"><div><h2 id="preview-title">素材預覽</h2><p id="preview-meta"></p></div><button type="button" class="preview-close" id="preview-close">關閉</button></header><div class="preview-content" id="preview-content"></div><footer class="material-preview-footer"><span id="preview-fallback"></span><a class="preview-open-link" id="preview-open" target="_blank" rel="noopener noreferrer">在新分頁開啟</a></footer></dialog>'''
    payload=json.dumps(questions,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    js=(base/'practice.js').read_text(encoding='utf-8').replace('PRACTICE_DATA',payload)
    page=page.replace('</body></html>',dialog+'<script>'+js+'</script></body></html>')
    return page
