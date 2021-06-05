###
#Testing vRA
Write-VpodProgress "Checking vRA" 'GOOD-8'
Write-Output "$(Get-Date) Testing vRA"
Do { 
    $vra_status = Invoke-Plink -remoteHost vr-automation.corp.local -login root -passwd VMware1! -command 'vracli status services'
    Write-Output "$(Get-Date) vRA Status Check $vra_status"
    LabStartup-Sleep $sleepSeconds
} Until ($vra_status -eq "Ready")
Write-Output "$(Get-Date) Finished testing vRA"


#Write-VpodProgress "vRA Initial Config" 'GOOD-8'