<#
Run this from the repository root (D:\skillsprint).

What it does:
- Detects processes that mention 'uvicorn', 'python' or 'skillsprint.db' in their commandline.
- Shows them and optionally stops them.
- Runs `pre_migration_snapshot.ps1` with bypassed execution policy.
- Locates the newest snapshot zip, expands it to `migration\snapshot_temp` and checks for `backend\app\skillsprint.db`.
- If the DB is present, copies a timestamped copy into `db_backups\`.

Usage:
  Open an elevated PowerShell prompt (if needed), then:
    Set-Location D:\skillsprint
    .\migration\run_full_snapshot_and_verify.ps1

Notes:
- The script will not restart any stopped services. Restart manually if needed.
- Do NOT commit the produced zip or DB backup to git.
#>

Set-StrictMode -Version Latest

function Pause-Continue {
    param([string]$msg = 'Press ENTER to continue...')
    Write-Host $msg -ForegroundColor Yellow
    Read-Host | Out-Null
}

Write-Host "Running pre-checks in: $(Get-Location)" -ForegroundColor Cyan

# find processes that might hold the DB
$procs = Get-CimInstance Win32_Process | Where-Object { 
    ($_.CommandLine -and ($_.CommandLine -match 'uvicorn' -or $_.CommandLine -match 'python' -or $_.CommandLine -match 'skillsprint.db'))
} | Select-Object ProcessId, CommandLine

if ($procs -and $procs.Count -gt 0) {
    Write-Host "Found the following candidate processes that may hold the DB file:" -ForegroundColor Yellow
    $procs | ForEach-Object { Write-Host "PID: $($_.ProcessId)  CMD: $($_.CommandLine)" }

    $ans = Read-Host "Stop these processes now? (Y/N)"
    if ($ans -match '^[Yy]') {
        foreach ($p in $procs) {
            try {
                Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop
                Write-Host "Stopped PID $($p.ProcessId)" -ForegroundColor Green
            } catch {
                Write-Host "Failed to stop PID $($p.ProcessId): $_" -ForegroundColor Red
            }
        }
        Pause-Continue 'Processes stopped. Press ENTER to run the snapshot script.'
    } else {
        Write-Host "User chose not to stop processes. The snapshot may still fail if the DB is locked." -ForegroundColor Yellow
        $cont = Read-Host "Continue and attempt the snapshot anyway? (Y/N)"
        if ($cont -notmatch '^[Yy]') { Write-Host 'Aborting.'; exit 1 }
    }
} else {
    Write-Host "No uvicorn/python/skillsprint.db processes found." -ForegroundColor Green
}

# run the existing snapshot script
$snapshotScript = Join-Path (Get-Location) 'pre_migration_snapshot.ps1'
if (-not (Test-Path $snapshotScript)) {
    Write-Host "Could not find $snapshotScript - aborting." -ForegroundColor Red
    exit 2
}

Write-Host "Running snapshot script: $snapshotScript" -ForegroundColor Cyan
try {
    powershell -ExecutionPolicy Bypass -File $snapshotScript
} catch {
    Write-Host "Snapshot script returned an error: $_" -ForegroundColor Red
}

# locate newest snapshot zip
$zip = Get-ChildItem -Path (Get-Location) -Filter 'skillsprint_snapshot_*.zip' -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $zip) {
    Write-Host "No snapshot zip found with pattern 'skillsprint_snapshot_*.zip'." -ForegroundColor Red
    Write-Host "List of all .zip files under repo:" -ForegroundColor Yellow
    Get-ChildItem -Path (Get-Location) -Filter '*.zip' -Recurse | Select-Object FullName, LastWriteTime | Format-Table -AutoSize
    exit 3
}

Write-Host "Found snapshot: $($zip.FullName)" -ForegroundColor Green

$dest = Join-Path (Join-Path (Get-Location) 'migration') 'snapshot_temp'
Remove-Item -LiteralPath $dest -Recurse -Force -ErrorAction SilentlyContinue

try {
    Expand-Archive -Path $zip.FullName -DestinationPath $dest -Force
} catch {
    Write-Host "Failed to expand archive: $_" -ForegroundColor Red
    exit 4
}

$dbPath = Join-Path $dest 'backend\app\skillsprint.db'
if (Test-Path $dbPath) {
    Write-Host "SUCCESS: snapshot contains the SQLite DB at $dbPath" -ForegroundColor Green

    # ensure db_backups exists
    $backupsDir = Join-Path (Get-Location) 'db_backups'
    if (-not (Test-Path $backupsDir)) { New-Item -ItemType Directory -Path $backupsDir | Out-Null }

    $ts = Get-Date -Format 'yyyyMMdd_HHmmss'
    $copyDest = Join-Path $backupsDir "skillsprint.db.$ts"
    Copy-Item -Path $dbPath -Destination $copyDest -Force
    Write-Host "Copied DB to $copyDest" -ForegroundColor Green
} else {
    Write-Host "The snapshot does not contain 'backend\app\skillsprint.db'." -ForegroundColor Yellow
    Write-Host "You can stop the backend processes and re-run this helper, or copy the DB file manually from the host after stopping the server." -ForegroundColor Yellow
    exit 5
}

Write-Host "Done. Remember not to commit the zip or DB backup to git." -ForegroundColor Cyan
