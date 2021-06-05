# Upload files to linux servers
Set-Location $LabStartupBaseFolder
Get-ChildItem -path ".\serverfiles" -Directory -Force | ForEach-Object {
    Write-Output "$(Get-Date) Copying files to $($_.Name)"
    $serverName = $_.Name + ".corp.local"
    $cmd = "echo y | pscp -r -l root -pw VMware1! -scp -noagent .\serverfiles\$($_.Name)\* $serverName`:/"
    Invoke-Expression -Command $cmd
}