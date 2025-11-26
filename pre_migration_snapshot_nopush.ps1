# pre_migration_snapshot_nopush.ps1
# Same as before but excludes certain paths from the ZIP and doesn't push to Git.

$backupDir = ".."
$timestamp = (Get-Date -Format yyyyMMdd_HHmm)
$zipPath = Join-Path $backupDir ("skillsprint_backup_$timestamp.zip")

# Build list of files to include excluding patterns
$excludePatterns = @("*.db","venv","__pycache__",".git",".venv")
# Get all files but filter out excluded patterns
$files = Get-ChildItem -Recurse -File | Where-Object {
    $full = $_.FullName.ToLower()
    -not ($excludePatterns | ForEach-Object { $full -like ("*"+($_.ToLower())+"*") } | Where-Object { $_ })
}

if ($files.Count -eq 0) {
  Write-Error "No files found to archive. Aborting."
  exit 1
}

# Create a temporary list of file paths for Compress-Archive
$tempList = Join-Path $env:TEMP "skillsprint_files_$timestamp.txt"
$files | ForEach-Object { $_.FullName } | Out-File -FilePath $tempList -Encoding utf8

Write-Host "Creating zip backup at $zipPath (excluding .db, venv, __pycache__, .git) ..."
Compress-Archive -LiteralPath (Get-Content $tempList) -DestinationPath $zipPath -Force

if (Test-Path $zipPath) {
  Write-Host "Backup created: $zipPath"
} else {
  Write-Error "Failed to create backup zip."
  exit 1
}

# Create branch/tag locally (no push)
if (Test-Path ".git") {
  $branchName = "azure-migration-safety"
  git checkout -b $branchName
  git commit --allow-empty -m "azure-migration: pre-migration snapshot"
  $tagName = "pre-azure-migration-" + $timestamp
  git tag -a $tagName -m "Pre-Azure migration snapshot $timestamp"
  Write-Host "Created local branch $branchName and tag $tagName (no push)."
} else {
  Write-Host "Not a git repo; skipping git steps."
}

# Append safe .gitignore entries
$gitignoreEntries = @"
.env
.env.local
secrets.json
*.sqlite3
skillsprint.db
skillsprint.db.bak
migration/render_env_backup.txt
db_backups/
"@
Add-Content -Path .gitignore -Value $gitignoreEntries

# Create .env template if missing
if (!(Test-Path ".env")) {
  @"
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/skillsprint
SECRET_KEY=CHANGE_ME
CORS_ORIGINS=http://localhost:5173
"@ | Out-File -FilePath .env -Encoding utf8
}

# Ensure .env not tracked
git ls-files --error-unmatch .env 2>$null
if ($LASTEXITCODE -eq 0) {
  git rm --cached .env
}

# Prepare migration folder and db_backups
New-Item -ItemType Directory -Path migration -Force | Out-Null
"Paste your Render env variables here (DO NOT commit this file)." | Out-File -FilePath migration\render_env_backup.txt -Encoding utf8 -Force
New-Item -ItemType Directory -Path db_backups -Force | Out-Null

Write-Host "Pre-migration nopush snapshot completed. Note: DB files were excluded from the zip. Store DB dumps separately."
