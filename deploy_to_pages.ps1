# 江夏傳統整復推拿 板橋館 - GitHub Pages 一鍵部署腳本
# 執行方式： powershell .\deploy_to_pages.ps1

Write-Host "🚀 開始部署至 GitHub Pages..." -ForegroundColor Cyan

# 1. 複製 index.html 至 dist
Copy-Item -Path "index.html" -Destination "dist\index.html" -Force
Write-Host "✅ 已同步 index.html 至 dist/" -ForegroundColor Green

# 2. 進入 dist 目錄進行 git commit 與 push
Push-Location "dist"
try {
    git add .
    $status = git status --porcelain
    if ($status) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "deploy: Update landing page at $timestamp"
        git push origin main
        Write-Host "✅ 成功推送至 GitHub 倉庫 (main 分支)！" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ dist 目錄無內容異動，略過推送。" -ForegroundColor Yellow
    }
} finally {
    Pop-Location
}

Write-Host "🌐 線上網站網址：https://azach258.github.io/jiangxia-banqiao/" -ForegroundColor Magenta
