const practiceData=PRACTICE_DATA;
const materialDialog=document.getElementById('material-dialog'),previewContent=document.getElementById('preview-content'),previewTitle=document.getElementById('preview-title'),previewMeta=document.getElementById('preview-meta'),previewOpen=document.getElementById('preview-open');
function materialUrl(path){return new URL(path,location.href.split('#')[0]).href;}
function openPreview(questionId,groupIndex){
 const question=practiceData.find(q=>q.id===questionId),group=question.groups[groupIndex];if(!group)return;
 const allImages=group.files.every(f=>f.preview&&f.preview.kind==='image'),item=group.files.find(f=>f.ext==='PDF')||group.files.find(f=>f.preview)||group.files[0];
 previewContent.replaceChildren();previewTitle.textContent=question.id+' · '+group.title;previewMeta.textContent='';previewOpen.hidden=false;previewOpen.href=materialUrl(item.path);previewOpen.textContent='在新分頁開啟';
 if(allImages&&group.files.length>1){
  const gallery=document.createElement('div');gallery.className='receipt-gallery';for(const file of group.files){const figure=document.createElement('figure'),link=document.createElement('a'),img=document.createElement('img'),caption=document.createElement('figcaption');link.href=materialUrl(file.path);link.target='_blank';link.rel='noopener';img.src=materialUrl(file.path);img.alt=file.title;img.loading='lazy';caption.textContent=file.title;link.append(img);figure.append(link,caption);gallery.append(figure);}previewContent.append(gallery);previewMeta.textContent=group.files.length+' 張教學收據；點圖片可在新分頁看原圖。';previewOpen.hidden=true;
 }else if(item.preview.kind==='table'){
  const wrapper=document.createElement('div');wrapper.className='preview-table-scroll';const table=document.createElement('table');table.className='preview-table';const head=document.createElement('thead'),header=document.createElement('tr'),body=document.createElement('tbody');item.preview.columns.forEach(value=>{const th=document.createElement('th');th.scope='col';th.textContent=value;header.append(th);});head.append(header);item.preview.rows.forEach(values=>{const tr=document.createElement('tr');for(const value of values){const td=document.createElement('td');td.textContent=value;tr.append(td);}body.append(tr);});table.append(head,body);wrapper.append(table);previewContent.append(wrapper);previewMeta.textContent='CSV 原始資料 · '+item.preview.totalRows+' 列；表格可左右捲動。';
 }else if(item.preview.kind==='text'){
  const text=document.createElement('pre');text.textContent=item.preview.text;previewContent.append(text);previewMeta.textContent='素材文字版；可選取、複製，或下載後交給 AI。';
 }else if(item.preview.kind==='pdf'){
  const frame=document.createElement('iframe');frame.className='preview-pdf';frame.title=group.title+' PDF預覽';frame.src=materialUrl(item.path);previewContent.append(frame);previewMeta.textContent='PDF 閱讀版。';
 }else if(item.preview.kind==='image'){
  const img=document.createElement('img');img.className='preview-image';img.alt=group.title;img.src=materialUrl(item.path);previewContent.append(img);previewMeta.textContent='原始圖片預覽。';
 }
 document.getElementById('preview-fallback').textContent=item.preview.kind==='pdf'?'若 PDF 預覽未顯示，可在新分頁開啟或下載。':'要上傳給 AI 或編輯時，請下載原檔。';
 materialDialog.showModal();previewContent.scrollTop=0;
}
document.querySelectorAll('[data-preview-question]').forEach(button=>button.addEventListener('click',()=>openPreview(button.dataset.previewQuestion,Number(button.dataset.previewGroup))));
document.getElementById('preview-close').addEventListener('click',()=>materialDialog.close());
materialDialog.addEventListener('close',()=>previewContent.replaceChildren());
materialDialog.addEventListener('click',event=>{if(event.target===materialDialog){const rect=materialDialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)materialDialog.close();}});
if(document.body.dataset.offlinePackage==='true'){
 document.querySelectorAll('.package-archive').forEach(link=>{const span=document.createElement('span');span.className='included-materials';span.textContent=link.classList.contains('question-archive')?'本題素材已保存在練習包內。':link.classList.contains('full-pack-download')?'完整題目與素材已在這個資料夾。':'已包含完整練習素材';link.replaceWith(span);});
}
let practicePrint=false,practicePrintStates=[];
window.addEventListener('beforeprint',()=>{if(practicePrint)return;practicePrint=true;practicePrintStates=[...document.querySelectorAll('.solution')].map(d=>d.open);document.querySelectorAll('.solution').forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>{if(!practicePrint)return;document.querySelectorAll('.solution').forEach((d,i)=>d.open=practicePrintStates[i]);practicePrint=false;});
