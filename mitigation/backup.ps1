param(
    [string]$sourcePath,
    [string]$destinationPath
)

# Create a timestamp for the backup folder
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$backupFolder = Join-Path $destinationPath "backup_$timestamp"

# Create the backup folder
New-Item -ItemType Directory -Path $backupFolder | Out-Null

# Perform the incremental backup using robocopy
robocopy $sourcePath $backupFolder /E /Z /R:3 /W:5 /NP /NFL /NDL /NJH /NJS /NC /NS

Write-Host "Backup completed successfully."

