# wait for vcenter
Foreach ($entry in $vCenters) {
    ($vcserver, $type, $loginUser) = $entry.Split(":")
    $cisConnection = $null
    $applianceService = $null

    Do {
        Try {
            if (!$cisConnection.IsConnected) {
                $cisConnection = Connect-CisServer -Server $vcserver -User $vcuser -Password $password -ErrorAction Stop 2> $null
            }
            Write-Output "vAPI Service found: $((Get-CisService).Count)"

            $applianceService = Get-CisService com.vmware.appliance.vmon.service
            $vcsaServicesStopped = $applianceService.list_details().Values | Where-Object { $_.startup_type -eq "AUTOMATIC" -and $_.state -ne "STARTED" -and $_.health -ne "HEALTHY" }
            if ($vcsaServicesStopped) { 
                $vcsaServicesStopped | Format-Table -Property name_key, state, health | Write-Output
                $cisConnection | Disconnect-CisServer -Confirm:$false | Out-Null  2> $null
                Start-Sleep 30
            }
        }
        Catch {
            Write-Output "Failed to connect to server $vcserver or a service as $vcuser"
            Write-Output $Error[0].Exception
            Start-Sleep 20
        }
    } Until ($cisConnection.IsConnected -and !$vcsaServicesStopped)

    $applianceService.list_details().Values | Format-Table -Property name_key, state, health | Write-Output
    Write-Output "vAPI Service found: $((Get-CisService).Count)"

    Write-Output "Connected to vCenter, all services are started"
    $cisConnection | Disconnect-CisServer -Confirm:$false | Out-Null  2> $null

    LabStartup-Sleep 10
}