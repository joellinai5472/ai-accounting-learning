const cardForm=document.getElementById('card-form'),draftKey='ai-learning-card.v1';
const fields={name:document.getElementById('card-name'),group:document.getElementById('card-group'),reflection:document.getElementById('card-reflection'),url:document.getElementById('card-url')};
const stageNames={'1':'對話型 AI','2':'資料、圖表與簡報','3':'Vibe Coding'};
let cardBusy=false;
function stateFromForm(){return {name:fields.name.value.slice(0,32),group:fields.group.value.slice(0,24),reflection:fields.reflection.value.slice(0,120),url:fields.url.value.slice(0,400),selected:[...cardForm.querySelectorAll('[data-question]:checked')].map(input=>input.dataset.question)};}
function validWorkUrl(raw){if(!raw.trim())return {valid:true,url:''};try{const url=new URL(raw.trim());if(!['https:','http:'].includes(url.protocol)||!url.hostname)return {valid:false,url:''};return {valid:true,url:url.href};}catch(e){return {valid:false,url:''};}}
function paintQr(canvas,url){const qr=qrcodegen.QrCode.encodeText(url,qrcodegen.QrCode.Ecc.MEDIUM),scale=6,pad=4;canvas.width=canvas.height=(qr.size+pad*2)*scale;const ctx=canvas.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#141110';for(let y=0;y<qr.size;y++)for(let x=0;x<qr.size;x++)if(qr.getModule(x,y))ctx.fillRect((x+pad)*scale,(y+pad)*scale,scale,scale);}
function updateCard(save=true){
 const state=stateFromForm(),selected=new Set(state.selected),work=validWorkUrl(state.url);
 if(save&&!cardBusy)document.getElementById('card-feedback').textContent='';
 document.getElementById('preview-identity').textContent=[state.name.trim(),state.group.trim()].filter(Boolean).join(' · ')||'每一次嘗試，都有下一步。';
 document.getElementById('preview-count').textContent=selected.size;
 document.getElementById('mobile-preview-count').textContent=selected.size?'已記錄 '+selected.size+' 題 · 看我的帶走卡':'還沒選題目 · 看我的帶走卡';
 const arc=document.querySelector('#card-preview .dial-progress');arc.style.strokeDashoffset=String(2*Math.PI*36*(1-selected.size/19));
 document.querySelectorAll('#card-preview .dial-tick').forEach((line,index)=>line.classList.toggle('lit',index<Math.round(selected.size/19*38)));
 const stages=document.getElementById('preview-stages');stages.replaceChildren();
 for(const stageId of ['1','2','3']){
  const all=rows.filter(r=>r.stage===stageId),chosen=all.filter(r=>selected.has(r.id)),section=document.createElement('div');section.className='preview-stage';
  const heading=document.createElement('div');heading.className='preview-stage-heading';const title=document.createElement('h3');title.textContent=stageId+' · '+stageNames[stageId];const count=document.createElement('span');count.textContent=chosen.length+' / '+all.length+' 題';heading.append(title,count);
  const dots=document.createElement('div');dots.className='footprint-dots';dots.setAttribute('aria-hidden','true');all.forEach(row=>{const dot=document.createElement('i');dot.classList.toggle('lit',selected.has(row.id));dots.append(dot);});
  const list=document.createElement('p');list.className='preview-stage-list';if(chosen.length){chosen.forEach((row,index)=>{if(index)list.append(document.createTextNode(' · '));const link=document.createElement('a');link.href='#q-'+row.id;link.title='再練一次：'+row.title;link.textContent=row.id+' '+row.title;list.append(link);});}else{list.textContent='還沒勾選，之後也可以再試。';}section.append(heading,dots,list);stages.append(section);
 }
 const reflection=document.getElementById('preview-reflection');reflection.textContent=state.reflection.trim()||'把一個想法，變成可以試試看的事。';reflection.classList.toggle('placeholder',!state.reflection.trim());
 const error=document.getElementById('url-error');error.textContent='請填入完整的 http:// 或 https:// 網址，或留空。';error.hidden=work.valid;fields.url.setAttribute('aria-invalid',String(!work.valid));
 const workArea=document.getElementById('preview-work');workArea.hidden=!work.url;const workLink=document.getElementById('preview-work-link');workLink.removeAttribute('href');workLink.textContent='';
 if(work.url){try{paintQr(document.getElementById('preview-qr'),work.url);workLink.href=work.url;workLink.textContent=work.url;}catch(e){workArea.hidden=true;error.textContent='這個網址無法製作 QR，請使用較短的分享網址，或留空。';error.hidden=false;fields.url.setAttribute('aria-invalid','true');}}
 if(save){try{localStorage.setItem(draftKey,JSON.stringify(state));document.getElementById('draft-status').textContent='草稿已存在這個瀏覽器，不會送給老師。';}catch(e){document.getElementById('draft-status').textContent='這個瀏覽器無法保存草稿；請先下載帶走卡。';}}
}
function restoreDraft(){try{const saved=JSON.parse(localStorage.getItem(draftKey)||'null');if(saved&&typeof saved==='object'){for(const [key,field] of Object.entries(fields))field.value=typeof saved[key]==='string'?saved[key].slice(0,Number(field.maxLength)):'';if(Array.isArray(saved.selected))cardForm.querySelectorAll('[data-question]').forEach(input=>input.checked=saved.selected.includes(input.dataset.question));}}catch(e){document.getElementById('draft-status').textContent='暫時無法讀取草稿，仍可製作與下載帶走卡。';}updateCard(false);}
cardForm.addEventListener('submit',e=>e.preventDefault());cardForm.addEventListener('input',()=>updateCard());cardForm.addEventListener('change',()=>updateCard());
document.getElementById('jump-preview').addEventListener('click',()=>document.getElementById('card-preview').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'}));
cardForm.querySelectorAll('[data-idea]').forEach(button=>button.addEventListener('click',()=>{fields.reflection.value=button.dataset.idea;updateCard();fields.reflection.focus();}));
document.getElementById('clear-draft').addEventListener('click',()=>{cardForm.reset();try{localStorage.removeItem(draftKey);document.getElementById('draft-status').textContent='草稿已清除。新的嘗試，隨時可以開始。';}catch(e){document.getElementById('draft-status').textContent='畫面已清除；這個瀏覽器暫時無法更新儲存。';}document.getElementById('card-feedback').textContent='';updateCard(false);});

async function makeCardPdf(state){
 await document.fonts.ready;
 const canvas=document.createElement('canvas');canvas.width=1654;canvas.height=2339;const ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height,M=88;
 const color={bg:'#faf7f2',dark:'#141110',ink:'#231f1d',muted:'#665b53',orange:'#d04a02',amber:'#f28c28',line:'#dfd2c4'};
 ctx.fillStyle=color.bg;ctx.fillRect(0,0,W,H);
 function font(size,weight=400){ctx.font=weight+' '+size+'px "Microsoft JhengHei","Noto Sans TC",sans-serif';ctx.textBaseline='top';}
 function text(value,x,y,size=28,fill=color.ink,weight=400){font(size,weight);ctx.fillStyle=fill;ctx.fillText(value,x,y);}
 function wrap(value,x,y,width,size=28,line=43,fill=color.ink,weight=400){font(size,weight);ctx.fillStyle=fill;let next=y;for(const paragraph of value.split('\n')){let segment='';for(const char of paragraph){if(ctx.measureText(segment+char).width>width&&segment){ctx.fillText(segment,x,next);next+=line;segment=char;}else segment+=char;}ctx.fillText(segment,x,next);next+=line;}return next;}
 function rule(y){ctx.fillStyle=color.line;ctx.fillRect(M,y,W-2*M,2);}
 ctx.fillStyle=color.dark;ctx.fillRect(0,0,W,400);ctx.fillStyle=color.orange;ctx.fillRect(0,0,W,12);
 text('AI 賦能會計',M,70,28,color.amber,700);text('我的學習足跡',M,130,72,'#f6f0ea',700);
 const identity=[state.name.trim(),state.group.trim()].filter(Boolean).join(' · ')||'每一次嘗試，都有下一步。';
 wrap(identity,M,235,1000,29,43,'#d2c3b7');text('自己記錄的嘗試 · 不是通關分數或能力認證',M,340,23,'#c8b6a7');
 const cx=1350,cy=195,r=112;ctx.lineWidth=8;ctx.strokeStyle='#4a3525';ctx.beginPath();ctx.arc(cx,cy,r,0,2*Math.PI);ctx.stroke();
 if(state.selected.length){ctx.strokeStyle=color.amber;ctx.beginPath();ctx.arc(cx,cy,r,-Math.PI/2,-Math.PI/2+2*Math.PI*state.selected.length/19);ctx.stroke();}
 for(let i=0;i<38;i++){const a=i/38*2*Math.PI-Math.PI/2;ctx.strokeStyle=i<Math.round(state.selected.length/19*38)?color.amber:'#76583e';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(cx+Math.cos(a)*128,cy+Math.sin(a)*128);ctx.lineTo(cx+Math.cos(a)*141,cy+Math.sin(a)*141);ctx.stroke();}
 ctx.textAlign='center';text(String(state.selected.length),cx,135,85,'#f6f0ea',700);text('題嘗試',cx,235,24,'#c8b6a7');ctx.textAlign='left';
 let y=455;const chosen=new Set(state.selected),colWidth=(W-2*M-40)/2;
 for(const stageId of ['1','2','3']){
  const all=rows.filter(r=>r.stage===stageId),items=all.filter(r=>chosen.has(r.id));
  text(stageId+' · '+stageNames[stageId],M,y,31,color.orange,700);ctx.textAlign='right';text(items.length+' / '+all.length+' 題',W-M,y,26,color.muted);ctx.textAlign='left';y+=55;
  if(items.length){let rowHeight=0;for(let i=0;i<items.length;i+=2){rowHeight=44;for(let j=0;j<2;j++){const item=items[i+j];if(!item)continue;const end=wrap(item.id+'  '+item.title,M+j*(colWidth+40),y,colWidth,26,38);rowHeight=Math.max(rowHeight,end-y);}y+=rowHeight+12;}}else{y=wrap('還没勾選，之後也可以再試。'.replace('没','沒'),M,y,W-2*M,25,40,color.muted);}
  y+=19;rule(y);y+=26;
 }
 text('下一次，我想用 AI 做……',M,y,28,color.orange,700);y+=49;
 y=wrap(state.reflection.trim()||'把一個想法，變成可以試試看的事。',M,y,W-2*M,30,45);y+=25;
 const work=validWorkUrl(state.url);let annotationRect=null;
 if(work.url){rule(y);y+=26;const qr=document.createElement('canvas');paintQr(qr,work.url);ctx.imageSmoothingEnabled=false;ctx.drawImage(qr,M,y,200,200);text('我想保留的作品',M+235,y+8,27,color.ink,700);
  const label=work.url.length>80?work.url.slice(0,77)+'…':work.url;wrap(label,M+235,y+59,W-2*M-235,23,35,color.muted);
  text('掃 QR，或點這一區開啟作品。',M+235,y+152,22,color.muted);
  annotationRect=[M,y,W-M,y+200];y+=226;
 }
 const footerY=Math.max(y+12,H-366);if(footerY>H-275)throw Error('內容太長，請縮短名字或反思後重試。');
 rule(footerY);text('卡關時可以怎麼做',M,footerY+27,29,color.orange,700);
 const methodLabels=['看不懂題目，先問 AI','換個說法','拆小','給範例','換工具','問 AI 怎麼問'];
 methodLabels.forEach((label,i)=>text(label,M+(i%3)*((W-2*M)/3),footerY+88+Math.floor(i/3)*48,24,color.ink,500));
 text('AI 賦能會計 · 我的學習卡',M,H-110,22,color.muted);
 text('想繼續練習？回到講師提供的解題筆記入口。',M,H-71,21,color.muted);
 const doc=await PDFLib.PDFDocument.create();doc.setTitle('我的 AI 學習卡');doc.setAuthor('');doc.setSubject('自填學習紀錄');
 const image=await doc.embedJpg(canvas.toDataURL('image/jpeg',0.96)),page=doc.addPage([595.28,841.89]);page.drawImage(image,{x:0,y:0,width:595.28,height:841.89});
 if(annotationRect){const [x0,y0,x1,y1]=annotationRect;const link=doc.context.register(doc.context.obj({Type:'Annot',Subtype:'Link',Rect:[x0/W*595.28,841.89-y1/H*841.89,x1/W*595.28,841.89-y0/H*841.89],Border:[0,0,0],A:{Type:'Action',S:'URI',URI:PDFLib.PDFString.of(work.url)}}));page.node.set(PDFLib.PDFName.of('Annots'),doc.context.obj([link]));}
 return await doc.save();
}
document.getElementById('download-card').addEventListener('click',async()=>{
 if(cardBusy)return;const button=document.getElementById('download-card'),feedback=document.getElementById('card-feedback'),state=stateFromForm(),work=validWorkUrl(state.url);
 if(!work.valid||fields.url.getAttribute('aria-invalid')==='true'){feedback.textContent='請先修正作品網址，或把它留空。';fields.url.focus();return;}
 cardBusy=true;button.disabled=true;button.firstChild.textContent='正在整理你的帶走卡… ';feedback.textContent='';
 try{const bytes=await makeCardPdf(state),blob=new Blob([bytes],{type:'application/pdf'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='AI學習卡_'+(state.name.trim().replace(/[<>:"/\\|?*\x00-\x1f]/g,'_')||'我的成果')+'.pdf';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);feedback.textContent='PDF 已準備完成。手機可在下載或預覽畫面中儲存；想繼續練習，回解題筆記找下一題。';}
 catch(e){feedback.textContent='PDF 下載暫時失敗；草稿仍在，請重試，或用「列印／另存 PDF」。';}
 finally{cardBusy=false;button.disabled=false;button.firstChild.textContent='下載我的帶走卡 ';}
});
document.getElementById('print-card').addEventListener('click',()=>{if(!validWorkUrl(stateFromForm().url).valid){document.getElementById('card-feedback').textContent='請先修正作品網址，或把它留空。';fields.url.focus();return;}window.print();});
restoreDraft();
