# Render 部署步驟（Flask 天氣應用）

本機已完成 git commit，接下來需將程式推上 GitHub，再在 Render 建立服務。

## 一、推送到 GitHub

遠端倉庫：`https://github.com/jinying-chen/flask`（目前為**空倉庫**）

### 若 `git push` 出現 403

代表 `TOKEN_JINYINGYA.txt` 的 Personal Access Token **沒有寫入權限**。請到 GitHub 重新建立 Token：

1. 開啟 https://github.com/settings/tokens
2. **Fine-grained token** 或 **Classic token** 需勾選：
   - **Contents**: Read and write
   - **Metadata**: Read
   - （Classic 則勾選 `repo` 完整權限）
3. 若組織有 SSO，需按 **Authorize** 授權

### 推送指令（PowerShell）

```powershell
cd c:\Users\jinying\Downloads\AI_TEST\FLASK

# 設定遠端（若尚未設定）
git remote add origin https://github.com/jinying-chen/flask.git

# 將 YOUR_TOKEN 換成具寫入權限的 Token
git push https://jinying-chen:YOUR_TOKEN@github.com/jinying-chen/flask.git main
```

推送成功後，GitHub 上應能看到 `app.py`、`templates/`、`Procfile`、`render.yaml` 等檔案。

---

## 二、在 Render 建立 Web Service

1. 登入 https://dashboard.render.com
2. 點 **New +** → **Web Service**
3. 選 **Connect GitHub** → 授權 → 選擇倉庫 **`jinying-chen/flask`**
4. 設定如下：

| 欄位 | 值 |
|------|-----|
| **Name** | `flask-weather`（自訂即可） |
| **Region** | Singapore 或離你最近的區域 |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

5. **Instance Type** 選 **Free**
6. 點 **Create Web Service**，等待 Build 與 Deploy 完成（約 2～5 分鐘）

部署完成後，Render 會提供網址，例如：`https://flask-weather-xxxx.onrender.com`

---

## 三、驗證部署

- 首頁：應顯示「天氣搜尋」介面
- 狀態 API：`https://你的網址.onrender.com/api/status`
- 搜尋台北等城市應回傳 JSON 天氣資料

---

## 四、使用 Blueprint（可選）

專案已含 `render.yaml`，也可在 Render Dashboard：

**New +** → **Blueprint** → 連接同一 GitHub 倉庫 → 依提示建立服務。

---

## 注意事項

- 免費方案閒置約 15 分鐘會休眠，首次開啟需等待冷啟動（約 30～60 秒）
- 勿將 API Token 提交到 Git（`TOKEN_JINYINGYA.txt` 已加入 `.gitignore`）
- 若曾將 Token 推上 GitHub，建議在 GitHub **撤銷並重新產生** Token
