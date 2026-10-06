from pathlib import Path
import json,re,zipfile,hashlib
root=Path.cwd();out=root/'_site'
questions=json.loads((root/'content/questions.json').read_text(encoding='utf-8'))
s=(out/'index.html').read_text(encoding='utf-8')
assert len(questions)==19 and s.count('class="practice-question"')==19
assert s.count('class="asset-download"')==56
assert s.count('class="question-archive package-archive"')==14
for q in questions:
    for file in q['materials']:
        source=root/'素材'/file;target=out/'素材'/file
        assert source.is_file() and source.read_bytes()==target.read_bytes(),file
for name in ['app.js','qrcodegen.js','pdf-lib.js','card.js','practice.js','style.css']:
    assert (out/'assets'/name).is_file(),name
for path in ['index.html','assets/app.js','assets/card.js','assets/practice.js']:
    text=(out/path).read_text(encoding='utf-8')
    assert not any(mark in text for mark in ['chatgpt.com/c/','@gmail.com','C:/Users/','C:\\Users\\','speaker_note','human_todo']),path
archive=out/'下載/AI賦能會計_完整練習包.zip'
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and len(z.namelist())==58
    page=z.read('index.html').decode('utf-8')
    assert 'data-offline-package="true"' in page
    assert '<script src=' not in page and '<link rel="stylesheet"' not in page
    for q in questions:
        for file in q['materials']:assert z.read('素材/'+file)==(root/'素材'/file).read_bytes()
print('PASS: 19 questions, 56 materials, 14 question archives, complete offline archive and publication boundary.')
