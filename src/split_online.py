from pathlib import Path
import re
root=Path.cwd();out=root/'_site';p=out/'index.html';s=p.read_text(encoding='utf-8')
styles=re.findall(r'<style>([\s\S]*?)</style>',s);scripts=re.findall(r'<script>([\s\S]*?)</script>',s)
assert len(styles)==1 and len(scripts)==5
assets=out/'assets';assets.mkdir(exist_ok=True)
(assets/'style.css').write_text(styles[0],encoding='utf-8')
s=re.sub(r'<style>[\s\S]*?</style>','<link rel="stylesheet" href="assets/style.css">',s,count=1)
names=['app.js','qrcodegen.js','pdf-lib.js','card.js','practice.js']
for name,script in zip(names,scripts):
    (assets/name).write_text(script,encoding='utf-8')
    s=s.replace('<script>'+script+'</script>','<script src="assets/'+name+'" defer></script>',1)
s=s.replace('><','>\n<')
p.write_text(s,encoding='utf-8')
(out/'.nojekyll').write_text('',encoding='utf-8')
print('Online CSS and JavaScript separated; offline archive remains self-contained.')
