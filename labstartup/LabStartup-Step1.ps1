# wait for vcenter
Write-VpodProgress "Checking vCenter Services" 'STARTING'

Foreach ($entry in $vCenters) {
    ($vcserver, $type, $loginUser) = $entry.Split(":")
    $cisConnection = $null
    $applianceService = $null

    Do {
        Try {
            if (!$cisConnection.IsConnected) {
                $cisConnection = Connect-CisServer -Server $vcserver -User $vcuser -Password $password -ErrorAction Stop 2> $null
            }
            $vapi_service = (Get-CisService).Count
            Write-Output "vAPI Service found: $vapi_service"
            if ($vapi_service -lt 1) { Continue }

            $applianceService = Get-CisService com.vmware.appliance.vmon.service
            $vcsaServicesStopped = $applianceService.list_details().GetEnumerator() | Where-Object { $_.Value.startup_type -eq "AUTOMATIC" -and $_.Value.state -ne "STARTED" -and $_.Value.health -ne "HEALTHY" }
            if ($vcsaServicesStopped) {
                $vcsaServicesStoppedLog = ""
                $vcsaServicesStopped | ForEach-Object {
                    $vcsaServicesStoppedLog += "$($_.Key) ($($_.Value.state)), "
                    if ($_.Value.startup_type -eq "AUTOMATIC" -and $_.Value.state -eq "STOPPED") {
                        Write-Output "Start Automatic service '$($_.Key)'"
                        $applianceService.start($_.Key)
                    }
                }
                Write-Output "Waiting for vCenter AUTOMATIC Services to start: $vcsaServicesStoppedLog"
                if ($cisConnection) { $cisConnection | Disconnect-CisServer -Confirm:$false | Out-Null  2> $null }
                Start-Sleep 30
            }
        }
        Catch {
            Write-Output "An issue occured while vCenter services are started ($vcserver as $vcuser): $($Error[0].Exception.Message)"
            if ($cisConnection) { $cisConnection | Disconnect-CisServer -Confirm:$false | Out-Null  2> $null }
            Start-Sleep 20
        }
    } Until ($cisConnection.IsConnected -and !$vcsaServicesStopped)

    #$applianceService.list_details().Values | Format-Table -Property name_key, state, health | Write-Output
    ($applianceService.list_details().GetEnumerator() | ForEach-Object { "$($_.Key) ($($_.Value.state)/$($_.Value.health))" } | Out-String).Trim().Replace("`r`n", ", ") | Write-Output

    Write-Output "Connection to vCenter OK, all AUTOMATIC services are started"
    $cisConnection | Disconnect-CisServer -Confirm:$false | Out-Null  2> $null
}