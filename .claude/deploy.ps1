# deploy.ps1 - Auto commit + push dos portais sabendo.app
# Executado automaticamente pelo hook Stop do Claude

$ErrorActionPreference = "SilentlyContinue"

function Push-If-Changed {
    param([string]$RepoPath, [string]$Name)

    if (-not (Test-Path "$RepoPath\.git")) {
        Write-Host "[$Name] Repo nao encontrado: $RepoPath"
        return
    }

    Push-Location $RepoPath

    $status = git status --porcelain 2>$null
    if (-not $status) {
        Write-Host "[$Name] Sem alteracoes."
        Pop-Location
        return
    }

    $date = Get-Date -Format "dd/MM/yyyy HH:mm"
    git add -A 2>$null
    $files = git diff --cached --name-only 2>$null | Select-Object -First 5
    $fileList = $files -join ", "
    $msg = "deploy $date - $fileList"

    git commit -m $msg 2>&1 | Out-Null
    $pushResult = git push origin HEAD 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[$Name] Push OK"
    } else {
        Write-Host "[$Name] ERRO: $pushResult"
    }

    Pop-Location
}

$BASE = "C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos"

Push-If-Changed -RepoPath $BASE -Name "Andre 5o ano"
Push-If-Changed -RepoPath "$BASE\_landing" -Name "sabendo.app"
Push-If-Changed -RepoPath "C:\Users\wizar\OneDrive\Documentos\Projeto Estudos\estudos-2ano" -Name "Lis 2o ano"

Write-Host "Deploy concluido."
