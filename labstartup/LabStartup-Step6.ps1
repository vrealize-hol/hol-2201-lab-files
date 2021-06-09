###
#Testing vRA
Write-VpodProgress "Checking vRA" 'GOOD-8'
Write-Output "$(Get-Date) Testing vRA"
Do {
    LabStartup-Sleep $sleepSeconds
    $vra_deploy = Invoke-Plink -remoteHost vr-automation.corp.local -login root -passwd VMware1! -command 'vracli status deploy'
    Write-Output "$(Get-Date) vRA Deploy Check $vra_deploy"
    if ($vra_deploy -ne "Deployment complete") { Continue }
    $vra_status = Invoke-Plink -remoteHost vr-automation.corp.local -login root -passwd VMware1! -command 'vracli status services'
    Write-Output "$(Get-Date) vRA Services Check $vra_status"
} Until ($vra_deploy -eq "Deployment complete" -and $vra_status -eq "Ready")
Write-Output "$(Get-Date) Finished testing vRA"


#Write-VpodProgress "vRA Initial Config" 'GOOD-8'