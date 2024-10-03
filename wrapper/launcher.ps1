param(
  [Parameter(Mandatory = $true)]
  [string] $WoodPath = "\\libraries\\Wood.exe"
)

# Set working directory to script location
Set-Location (Split-Path -Path $PSScriptRoot -PathType Directory)

# Construct path to Wood.exe
$WoodExecutable = Join-Path (Get-Location) -ChildPath $WoodPath

# Open Wood.exe
Start-Process $WoodExecutable -WindowStyle Normal