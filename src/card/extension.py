from pathlib import Path
import html,math,re

def augment(page,rows,root):
    base=root/'src/card'
    arrow='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
    choices=''
    names={'1':'對話型 AI','2':'資料、圖表與簡報','3':'Vibe Coding'}
    for stage,title in names.items():
        choices+=f'<section class="choice-stage"><h3><span>{stage}</span>{title}</h3><div class="choice-grid">'
        for row in rows:
            if row['stage']==stage:choices+=f'<label class="topic-choice"><input type="checkbox" data-question="{row["id"]}" aria-label="我嘗試過{row["id"]} {html.escape(row["title"],quote=True)}"><b>{row["id"]}</b><span>{html.escape(row["title"])}</span></label>'
        choices+='</div></section>'
    ticks=''
    for i in range(38):
        a=i/38*math.pi*2-math.pi/2
        ticks+=f'<line class="dial-tick" x1="{50+math.cos(a)*42:.2f}" y1="{50+math.sin(a)*42:.2f}" x2="{50+math.cos(a)*46:.2f}" y2="{50+math.sin(a)*46:.2f}"/>'
    length=2*math.pi*36
    dial=f'<svg viewBox="0 0 100 100" aria-hidden="true">{ticks}<circle class="dial-circle" cx="50" cy="50" r="36"/><circle class="dial-progress" cx="50" cy="50" r="36" transform="rotate(-90 50 50)" style="stroke-dasharray:{length};stroke-dashoffset:{length}"/></svg>'
    card=(base/'card.html').read_text(encoding='utf-8').replace('QUESTION_CHOICES',choices).replace('DIAL',dial).replace('ARROW',arrow)
    css=(base/'card.css').read_text(encoding='utf-8')
    page=page.replace('</style>',css+'\n</style>')
    page=page.replace('<a href="#contents">解題筆記</a><a href="#methods">卡關方法</a>','<a href="#contents">解題筆記</a><a class="card-nav" href="#card">我的帶走卡</a><a href="#methods">卡關方法</a>')
    page=page.replace('<div class="sidebar-head">','<a class="sidebar-card-link" href="#card"><span>製作我的帶走卡</span>'+arrow+'</a><div class="sidebar-head">')
    page=page.replace('<h1 class="welcome-title">','<div class="welcome-hero"><div class="hero-orbit" aria-hidden="true">'+dial+'</div><h1 class="welcome-title">')
    page=page.replace('<details class="intro-details">','<div class="hero-actions"><a href="#card">製作我的帶走卡 '+arrow+'</a><a href="#catalog">找一題，繼續練習 '+arrow+'</a></div></div><details class="intro-details">')
    page=page.replace('<div class="catalog">','<div class="catalog" id="catalog">')
    page=page.replace('</section><article id="q-1-1"','</section>'+card+'<article id="q-1-1"',1)
    assert 'id="card"' in page
    page=page.replace('welcome.hidden=!!selected;',"const isCard=raw==='card';document.body.dataset.view=isCard?'card':selected?'reader':'contents';document.getElementById('card').hidden=!isCard;welcome.hidden=!!selected||isCard;")
    page=page.replace("document.title=selected?", "document.title=isCard?'我的帶走卡 · AI賦能會計':selected?")
    page=page.replace("document.getElementById('mobile-label').textContent=selected?", "document.getElementById('mobile-label').textContent=isCard?'我的帶走卡 · 也可以找一題解法':selected?")
    page=page.replace("}else if(raw==='methods'){", "}else if(raw==='catalog'){requestAnimationFrame(()=>document.getElementById('catalog').scrollIntoView({behavior:'instant'}));}else if(raw==='methods'){")
    page=page.replace('解題筆記 · AI賦能會計</title>','解題筆記與帶走卡 · AI賦能會計</title>')
    qr=(root/'vendor/qrcodegen.js').read_text(encoding='utf-8')
    runtime=root/'vendor'
    pdf=(runtime/'pdf-lib.min.js').read_text(encoding='utf-8')
    pdf=re.sub(r'//# sourceMappingURL=.*','',pdf)
    license=(runtime/'pdf-lib.LICENSE.md').read_text(encoding='utf-8')
    js=(base/'card.js').read_text(encoding='utf-8')
    page=page.replace('</script></body></html>', '</script><script>'+qr.replace('</script','<\\/script')+'</script><script>/*\n'+license+'\n*/\n'+pdf.replace('</script','<\\/script')+'</script><script>'+js+'</script></body></html>')
    return page
