# CHANGE HERE START
$CemuPath = "C:/Software/Cemu/"
$Autostart = $true
# CHANGE HERE END

Set-Location $PSScriptRoot
$CemuGraphicPacksPath = $CemuPath + "graphicPacks/"
Write-Output "The target destination is: $CemuGraphicPacksPath"
Get-ChildItem . -Directory | ForEach-Object{
	Write-Output "Copy folder: $($_.Name)"
	Copy-Item -Force -Recurse $_.Name "$CemuGraphicPacksPath$($_.Name)"
}
if($Autostart){
	Write-Output "Open Cemu"
	& "$($CemuPath)Cemu.exe"
	Write-Output "Start test server"
	python testServer.py
}