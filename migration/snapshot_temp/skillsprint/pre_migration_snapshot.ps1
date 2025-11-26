<#
pre_migration_snapshot.ps1
Creates a safe repo backup, creates a branch+tag snapshot, updates .gitignore, creates a local .env template,
and prepares a migration folder for manual env backup.  Run from repo root (D:\skillsprint).
#>

# --- Config (edit if you want) ---
$tagPrefix = "pre-azure-migration-"
$branchName = "azure-migration-safety"
$backupDir = ".."   # parent folder for the zip
$timestamp = (Get-Date -Format yyyyMMdd_HHmm)

# --- 1) Create ZIP backup of repo (one level up) ---
$zipPath = Join-Path $backupDir ("skillsprint_backup_$timestamp.zip")
Write-Host "Creating zip backup at $zipPath ..."
Compress-Archive -Path . -DestinationPath $zipPath -Force
if (Test-Path $zipPath) {
  Write-Host "Backup created: $zipPath"
} else {
  Write-Error "Failed to create backup zip."
  exit 1
}

# --- 2) Create git branch and tag snapshot ---
# Ensure we're in a git repo
if (!(Test-Path ".git")) {
  Write-Error "This directory doesn't look like a git repository (.git missing). Abort."
  exit 1
}

Write-Host "Creating branch '$branchName' ..."
git checkout -b $branchName

Write-Host "Creating an empty commit snapshot (if nothing to commit) ..."
git commit --allow-empty -m "azure-migration: pre-migration snapshot"

$tagName = "$tagPrefix$timestamp"
Write-Host "Creating tag '$tagName' ..."
git tag -a $tagName -m "Pre-Azure migration snapshot $timestamp"

# Attempt to push branch and tags (may prompt for credentials)
Write-Host "Pushing branch to origin (may prompt for credentials) ..."
git push origin $branchName

Write-Host "Pushing tags to origin (may prompt for credentials) ..."
git push origin --tags

# --- 3) Append safe ignores to .gitignore ---
$gitignoreEntries = @"
# Local env files and DB backups (added by migration script)
.env
.env.local
secrets.json
*.sqlite3
skillsprint.db
skillsprint.db.bak
migration/render_env_backup.txt
db_backups/
"@
Write-Host "Appending safe ignores to .gitignore ..."
Add-Content -Path .gitignore -Value $gitignoreEntries

# --- 4) Create a local .env template (DO NOT commit) ---
$envPath = ".env"
if (!(Test-Path $envPath)) {
  Write-Host "Creating .env template (do NOT commit this file) at $envPath ..."
  $envContent = @"
# Local development env (DO NOT commit)
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/skillsprint
SECRET_KEY=CHANGE_ME
CORS_ORIGINS=http://localhost:5173
"@
  $envContent | Out-File -FilePath $envPath -Encoding utf8
} else {
  Write-Host ".env already exists, skipping template creation."
}

# Ensure .env is not tracked
$result = git ls-files --error-unmatch .env 2>$null
if ($LASTEXITCODE -eq 0) {
  Write-Host ".env is tracked by git - removing from index (won't delete file)..."
  git rm --cached .env
} else {
  Write-Host ".env not tracked by git (good)."
}

# --- 5) Prepare migration folder and backup placeholder file ---
$migrationDir = "migration"
New-Item -ItemType Directory -Path $migrationDir -Force | Out-Null
$backupFile = Join-Path $migrationDir "render_env_backup.txt"
if (!(Test-Path $backupFile)) {
  Write-Host "Creating placeholder file for Render env backup at $backupFile ..."
  "Paste your Render env variables here (DO NOT commit this file)." | Out-File -FilePath $backupFile -Encoding utf8
} else {
  Write-Host "$backupFile already exists."
}

# --- 6) Create db_backups folder for dumps ---
$dumpDir = "db_backups"
New-Item -ItemType Directory -Path $dumpDir -Force | Out-Null
Write-Host "Created $dumpDir for DB dumps (store dumps here)."

Write-Host "Pre-migration snapshot script completed successfully."
Write-Host "Next: manually paste Render env vars into $backupFile and DO NOT commit that file."
