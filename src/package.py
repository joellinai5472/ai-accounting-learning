from pathlib import Path
import zipfile,json,hashlib
root=Path.cwd();base=root/'.cache-build';out=root/'_site'
manifest=json.loads((base/'asset-manifest.json').read_text(encoding='utf-8'))
page=(out/'index.html').read_text(encoding='utf-8');offline=page.replace('<body>','<body data-offline-package="true">',1)
assert 'data-offline-package="true"' in offline
instructions='''AI 賦能會計｜練習與帶走卡

1. 先把整個 ZIP 完整解壓縮，再開啟 index.html。
   請保留 index.html 與「素材」資料夾的相對位置。
2. 每題先看情境、任務与成果要求，再預覽或取用素材。
   點「看參考解法」才會展開四步筆記與答案。
3. 所有題目需要的素材都已保存在「素材」資料夾，
   不用另外連入課堂遊戲。可在每題下載原檔，交給 AI 或編輯。
4. 我的帶走卡可勾選題目、選填反思與作品連結，下載一頁 PDF。
   草稿只保存在自己的瀏覽器，不會送給老師。
5. 題目與素材、筆記與帶走卡可離線閱讀或操作。
   需要 AI、搜尋最新資訊、排程或開啟外部作品時，仍需網路或對應工具。
6. PDF 預覽是否直接顯示依瀏覽器而異；可使用「在新分頁開啟」或下載閱讀。
   這份包已在 Windows Edge 實測；手機實機仍待驗證。

素材為教學練習資料；請依每題說明與原始檔案核對。
提示詞保留試跑日期與當時限制，已去除學校與活動名稱，方便跨校重用。
'''.replace('与','與')
zip_path=out/'下載/AI賦能會計_完整練習包.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('index.html',offline)
    z.writestr('使用說明.txt',instructions)
    for f in manifest['files']:z.write(out/f['path'],arcname=f['path'])
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    assert len(z.namelist())==58
    assert len([p for p in z.namelist() if p.startswith('素材/')])==56
summary={'package':str(zip_path.relative_to(root)).replace('\\','/'),'bytes':zip_path.stat().st_size,'sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'entries':58,'materials':56,'questions':19,'questionArchivesExcludedToAvoidDuplicateMaterials':True}
(base/'package-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
