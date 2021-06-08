# Upload files to linux servers
Set-Location $LabStartupBaseFolder
Get-ChildItem -path ".\serverfiles" -Directory -Force | ForEach-Object {
    Write-Output "$(Get-Date) Copying files to $($_.Name)"
    $serverName = $_.Name + ".corp.local"
    $cmd = "echo y | pscp -r -l root -pw VMware1! -scp -noagent .\serverfiles\$($_.Name)\* $serverName`:/"
    Invoke-Expression -Command $cmd
}

#Deploy VRA
Write-Output "Start vRealize Automation (/opt/scripts/deploy.sh)"
cmd /c echo y | plink root@vr-automation.corp.local -pw VMware1! -noagent "nohup /opt/scripts/deploy.sh > /tmp/labstartup-deploy.out 2> /tmp/labstartup-deploy.err < /dev/null &"
