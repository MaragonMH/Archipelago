# CHANGE HERE START
$CemuPath = "C:/Software/Cemu/"
$Autostart = $true
# CHANGE HERE END

Set-Location $PSScriptRoot
$CemuGraphicPacksPath = $CemuPath + "graphicPacks/"
$ClientFilesRelPath = "../cemuGraphicPack/"
Write-Output "The target destination is: $CemuGraphicPacksPath"
Write-Output "Copy folder: $ClientFilesRelPath"
Copy-Item -Force -Recurse $ClientFilesRelPath "$($CemuGraphicPacksPath)Archipelago"

if($Autostart){
	Write-Output "Open Cemu"
	& "$($CemuPath)Cemu.exe"
	Write-Output "Start test server"
	python testServer.py
}