# 部署說明（針對 FLASK 專案）

此文件說明如何將 `FLASK` 資料夾內的 Flask 天氣搜尋應用部署到常見免費/低成本平台（以 Render 為主要示範），並提供 Railway/Fly.io 替代方案。

準備工作（在本機）

1. 建立虛擬環境並安裝套件：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 本機測試：

```powershell
python app.py
# 或使用 gunicorn（production-like）
gunicorn app:app
```

Render（推薦，簡單且對小型 Flask 應用友好）

1. 把專案推到 GitHub：

```powershell
git init
git add .
git commit -m "deploy flask app"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

2. 在 Render 建立 Web Service：
- 登入 https://render.com ，新增新服務 → 連接 GitHub repo
- 選擇 `Web Service`，Branch 選 `main`，Build Command 可留空或 `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- 選擇免費方案（若可用）並建立

3. 等待部署完成，Render 會提供一個公開 URL。

Railway / Fly.io（替代）

- Railway: 連接 GitHub repo 或使用 `railway init`，設定服務為 Python，指定 `gunicorn app:app` 作為啟動指令。
- Fly.io: 安裝 `flyctl`，初始化 `fly launch`，若需要，建立 `Dockerfile` 或使用 Buildpacks；啟動命令設定為 `gunicorn app:app`。

注意事項

- 請勿將敏感 API keys 推到公開 repo；使用平台提供的 Secret/Environment 變數管理。
- 免費方案通常有睡眠/冷啟動、流量或執行時間限制。
- 若需要 HTTPS 或自訂網域，平台通常提供設定並自動申請 SSL。

進一步幫助

若你要我替你：
- 把 `FLASK` 專案初始化為 Git repo 並示範推上 GitHub（我可以直接在本機建立 commit）
- 或直接示範在 Render 上建立服務（我會提供 step-by-step 指令與 UI 指引）

請選擇下一步：`初始化 Git 並推上 GitHub` 或 `直接輸出 Render 部署步驟`。
