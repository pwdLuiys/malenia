# This script dynamically provisions and executes the MaleniaPF compiled payload directly via network stream.

$ErrorActionPreference = "Stop"

# Define the remote endpoint pointing to your latest GitHub compiled asset
$Url = "https://github.com/pwdLuiys/malenia/releases/latest/download/MaleniaPF.exe"
$TargetPath = "$env:TEMP\MaleniaPF.exe"

Write-Host "Downloading Malenia Post Format Tool components..." -ForegroundColor Cyan

# Checking if TLS 1.2/1.3 is enforced to prevent security handshakes from dropping on fresh Windows installs
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13

# Downloading the static standalone binary into the system's temporary memory pool
Invoke-WebRequest -Uri $Url -OutFile $TargetPath -UseBasicParsing

Write-Host "Launching automation kernel with elevated permissions..." -ForegroundColor Green

# -Verb RunAs triggers the Windows UAC pop-up to elevate the token to Administrator. (It is necessary to run as admin to do some of the functions)
# -Wait ensures the script pauses until the user finishes using MaleniaPF.
Start-Process -FilePath $TargetPath -Verb RunAs -Wait

# Post-execution cleanup: wiping the cached binary from temp to leave zero footprint on the machine
if (Test-Path $TargetPath)
{
    Remove-Item $TargetPath -Force
}
