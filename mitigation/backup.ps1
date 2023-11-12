param(
    [string]$sourcePath = "",
    [string]$destinationPath = ""
)

# Create a timestamp for the backup folder
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$backupFolder = Join-Path $destinationPath "backup_$timestamp"

# Create the backup folder
New-Item -ItemType Directory -Path $backupFolder | Out-Null

# Perform the incremental backup using robocopy
robocopy $sourcePath $backupFolder /E /Z /R:3 /W:5 /NP /NFL /NDL /NJH /NJS /NC /NS

# Get the current date and time
$currentDate = Get-Date

# Calculate the date one week ago
$oneWeekAgo = $currentDate.AddDays(-7)

# Get a list of backup folders older than one week
$oldBackups = Get-ChildItem -Path $destinationPath -Directory | Where-Object { $_.Name -like "backup_*" -and $_.LastWriteTime -lt $oneWeekAgo }

# Delete old backup folders
foreach ($oldBackup in $oldBackups) {
    Remove-Item -Path $oldBackup.FullName -Recurse -Force
}

Write-Host "Backup completed successfully."
