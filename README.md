# AI 賦能會計｜練習與帶走卡

19 題完整練習、素材預覽與下載、參考解法、個人帶走卡與一頁 PDF。題目與素材隨站保存，可下載完整 ZIP 解壓後離線閱讀。

網站：<https://joellinai5472.github.io/ai-accounting-learning/>

## 更新內容

| 修改項目 | 檔案 |
|---|---|
| 題目情境、任務、成果要求與素材對應 | `content/questions.json` |
| 19 題解題內容、提示詞、追問與答案 | `content/solutions.md` |
| 首頁與閱讀版面 | `src/base.html`、`src/base.css` |
| 搜尋、切換題目與複製提示 | `src/base.js` |
| 帶走卡與 PDF | `src/card/` |
| 題目、素材與預覽 | `src/practice/` |
| 練習原始檔案 | `素材/` |

提交修改到 `main` 後，GitHub Actions 自動重建網頁、每題素材 ZIP 與完整離線包，再更新 GitHub Pages。可在 Actions 查看發布成功或錯誤訊息。

本機建置只需 Python 3 標準函式庫：

```sh
python3 build.py
python3 -m http.server 8000 --directory _site
```

網站產物放在 `_site/`，不直接編輯或提交。線上版分開 CSS／JavaScript，離線 ZIP 內的 HTML 包含必要程式，不依賴 CDN。PDF 與 QR 所使用的第三方 MIT 授權保留於 `vendor/`。

帶走卡草稿只存在訪客自己的瀏覽器，不會送到 GitHub 或老師。題目與素材可離線閱讀；使用 AI、查新聞、排程及外部作品連結仍需網路與對應工具。PDF 文字以影像輸出。
