from pathlib import Path
from collections import OrderedDict
import json,re,hashlib,shutil,zipfile,csv,io

root=Path.cwd();base=root/'.cache-build';out=root/'_site';student=root/'素材'
cards=json.loads((root/'content/questions.json').read_text(encoding='utf-8'))
source_fields=['id','stage','title','story','task','materials','check_note']
hashes={str(root.joinpath('content/questions.json').relative_to(root)).replace('\\','/'):hashlib.sha256((root/'content/questions.json').read_bytes()).hexdigest()}
requirements={c['id']:c['requirement'] for c in cards}
assert len(cards)==19
files=[];practice=[]
for card in cards:
    groups=OrderedDict()
    for source in card['materials']:
        p=student/source;assert p.is_file(),source
        resolved=p.resolve();assert resolved.is_relative_to(student.resolve()),source
        data=p.read_bytes();target=out/'素材'/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
        assert target.read_bytes()==data
        hashes[str(p.relative_to(root)).replace('\\','/')]=hashlib.sha256(data).hexdigest()
        suffix=p.suffix.lower();title=re.sub(r'^\d-\d_','',p.stem)
        key='receipt-gallery' if card['id']=='2-2' else title
        group=groups.setdefault(key,{'title':'15 張收據圖片' if key=='receipt-gallery' else title.replace('_',' · '),'files':[]})
        item={'path':'素材/'+source,'name':p.name,'ext':suffix[1:].upper(),'bytes':len(data),'title':title}
        if suffix=='.csv':
            table=list(csv.reader(io.StringIO(data.decode('utf-8-sig'))));item['preview']={'kind':'table','columns':table[0] if table else [],'rows':table[1:],'totalRows':max(0,len(table)-1)}
        elif suffix=='.txt':item['preview']={'kind':'text','text':data.decode('utf-8-sig')}
        elif suffix=='.pdf':item['preview']={'kind':'pdf'}
        elif suffix=='.png':item['preview']={'kind':'image'}
        else:item['preview']=None
        group['files'].append(item);files.append(item)
    question={'id':card['id'],'stage':str(card['stage']),'title':card['title'],'story':card['story'],'task':card['task'],'requirement':requirements[card['id']],'groups':list(groups.values()),'materialCount':len(card['materials'])}
    if card['materials']:
        downloads=out/'下載';downloads.mkdir(exist_ok=True)
        zipname=card['id']+'_本題素材.zip';question['archive']='下載/'+zipname
        with zipfile.ZipFile(downloads/zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for source in card['materials']:z.write(student/source,arcname=source)
        question['archiveBytes']=(downloads/zipname).stat().st_size
    practice.append(question)
assert len(files)==56 and len({f['path'] for f in files})==56
(base/'practice.json').write_text(json.dumps(practice,ensure_ascii=False,indent=2),encoding='utf-8')
(base/'source-hashes.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2),encoding='utf-8')
(base/'asset-manifest.json').write_text(json.dumps({'files':files,'totalBytes':sum(x['bytes'] for x in files)},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'questions':len(cards),'materialsCopied':len(files),'sourceBytes':sum(f['bytes'] for f in files),'questionArchives':sum(bool(c.get('archive')) for c in practice)},ensure_ascii=False))
