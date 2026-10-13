# 江夏傳統整復推拿 板橋館 - GitHub Pages 一鍵部署腳本
# 執行方式： powershell .\deploy_to_pages.ps1

Write-Host "🚀 開始部署至 GitHub Pages..." -ForegroundColor Cyan

# 1. 複製前台最新代碼至根目錄 index.html 與 dist/index.html
Copy-Item -Path "test_front_booking.html" -Destination "index.html" -Force
Copy-Item -Path "test_front_booking.html" -Destination "dist\index.html" -Force
Write-Host "✅ 已同步前台 (test_front_booking.html -> index.html & dist/index.html)" -ForegroundColor Green

# 2. 複製後台最新代碼至 dist/dashboard/ 與 test_dashboard_v2.html
Copy-Item -Path "booking-dashboard\index.html" -Destination "booking-dashboard\test_dashboard_v2.html" -Force

if (-not (Test-Path "dist\dashboard")) {
    New-Item -ItemType Directory -Path "dist\dashboard" -Force | Out-Null
}
Copy-Item -Path "booking-dashboard\index.html" -Destination "dist\dashboard\index.html" -Force

if (-not (Test-Path "dist\booking-dashboard")) {
    New-Item -ItemType Directory -Path "dist\booking-dashboard" -Force | Out-Null
}
Copy-Item -Path "booking-dashboard\index.html" -Destination "dist\booking-dashboard\index.html" -Force
Write-Host "✅ 已同步後台 (booking-dashboard/index.html -> dist/dashboard/ & dist/booking-dashboard/)" -ForegroundColor Green

# 3. 進入 dist 目錄進行 git commit 與 push
Push-Location "dist"
try {
    git add .
    $status = git status --porcelain
    if ($status) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "feat: deploy booking system v2 with date pickers & price matrix at $timestamp"
        git push origin main
        Write-Host "✅ 成功推送至 GitHub 倉庫 (main 分支)！" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ dist 目錄無內容異動，略過推送。" -ForegroundColor Yellow
    }
} finally {
    Pop-Location
}

Write-Host "🌐 顧客線上官網：https://azach258.github.io/jiangxia-banqiao/" -ForegroundColor Magenta
Write-Host "📊 師傅排程看板：https://azach258.github.io/jiangxia-banqiao/dashboard/" -ForegroundColor Magenta
