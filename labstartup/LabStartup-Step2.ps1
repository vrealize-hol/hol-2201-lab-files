Write-Output "Wait vRA first-boot"
Do {
    LabStartup-Sleep $sleepSeconds
    $vra_deploy = Invoke-Plink -remoteHost vr-automation.corp.local -login root -passwd VMware1! -command 'vracli status first-boot'
    Write-Output "$(Get-Date) vRA First-Boot Status $vra_deploy"
} Until ($vra_deploy -eq "First boot complete")

Write-Output "Start vRealize Automation (/opt/scripts/deploy.sh)"
cmd /c echo y | plink root@vr-automation.corp.local -pw VMware1! -noagent "nohup /opt/scripts/deploy.sh > /tmp/labstartup-deploy.out 2> /tmp/labstartup-deploy.err < /dev/null &"

Write-Output "Disable datastore storage usage alarm"
Get-Datastore local_esx-01a | Get-AlarmDefinition -Name "Datastore usage on disk" | Set-AlarmDefinition -enabled:$false | Out-Null
Get-Datastore local_esx-02a | Get-AlarmDefinition -Name "Datastore usage on disk" | Set-AlarmDefinition -enabled:$false | Out-Null
Get-Datastore local_esx-03a | Get-AlarmDefinition -Name "Datastore usage on disk" | Set-AlarmDefinition -enabled:$false | Out-Null
Get-Datastore local_esx-04a | Get-AlarmDefinition -Name "Datastore usage on disk" | Set-AlarmDefinition -enabled:$false | Out-Null
Get-Datastore local_esx-05a | Get-AlarmDefinition -Name "Datastore usage on disk" | Set-AlarmDefinition -enabled:$false | Out-Null

Write-Output "Disable Host memory usage alarm"
Get-VMHost esx-01a.corp.local | Get-AlarmDefinition -Name "Host memory usage" | Set-AlarmDefinition -enabled:$false | Out-Null
Get-VMHost esx-02a.corp.local | Get-AlarmDefinition -Name "Host memory usage" | Set-AlarmDefinition -enabled:$false | Out-Null
