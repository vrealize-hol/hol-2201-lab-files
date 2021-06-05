###
#Testing GitLab
Write-VpodProgress "Checking GitLab" 'GOOD-6'
Write-Output "$(Get-Date) Testing GitLab"
Do { 
    $status = Invoke-Plink -remoteHost dev-tools.corp.local -login root -passwd VMware1! -command 'docker ps `| grep gitlab'
    Write-Output "$(Get-Date) GitLab Status Check"
    if ($status -like "*(unhealthy)*") {
        Invoke-Plink -remoteHost dev-tools.corp.local -login root -passwd VMware1! -command 'docker restart gitlab'
        Write-Output "$(Get-Date) Restart GitLab as it is unhealthy"
    }
    LabStartup-Sleep $sleepSeconds
} Until ($status -like "*(healthy)*")
Write-Output "$(Get-Date) Finished testing GitLab"

# Create GitLab repos
Set-Location $LabStartupBaseFolder
$curPath = Get-Location
Get-ChildItem -path ".\repos" -Directory -Force | ForEach-Object {
    Write-Output "Update git repo $($_.Name)"
    $repo_path = $curPath | Join-Path -ChildPath "repos" | Join-Path -ChildPath $_.Name
    Set-Location $repo_path
    If (-Not (Test-Path -Path ".git" -PathType Container)) {
        Invoke-Command -ScriptBlock { git init -b main }
        Invoke-Command -ScriptBlock { git remote add origin https://gitlab.hol/hol/$($_.Name) }
    }
    Invoke-Command -ScriptBlock { git add . }
    Invoke-Command -ScriptBlock { git commit -m "$(Get-Date) Refresh" }
    Invoke-Command -ScriptBlock { git push -f -u origin main }
}

###
# Starting TKC cluster
$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP = '172.16.21.129'
$VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE = "rainpole"
$VSPHERE_WITH_TANZU_CLUSTER_NAME = "dev-project"
$VSPHERE_WITH_TANZU_USERNAME = 'administrator@corp.local'
$ENV:KUBECTL_VSPHERE_PASSWORD = 'VMware1!'

# Connect to Supervisor cluster
kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify
kubectl config use-context $VSPHERE_WITH_TANZU_CONTROL_PLANE_IP

# Wait until it is applied
Do {
    kubectl apply -f $(Join-Path $LabStartupBaseFolder "build/vsphere/wcp/rainpole/tkc-dev-project.yaml")
    if ($LastExitCode -ne 0) {
        kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify
        Continue
    }
    Start-Sleep -Seconds 20
    $tkc = kubectl get tkc/$VSPHERE_WITH_TANZU_CLUSTER_NAME -n $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE -o json | ConvertFrom-Json
    Write-Output ("Worker Nodes: " + $tkc.spec.topology.workers.count)
} While ($tkc.spec.topology.workers.count -lt 1)

# Wait until 1 worker node is ready
Do {
    Start-Sleep -Seconds 20
    $tkc = kubectl get tkc/$VSPHERE_WITH_TANZU_CLUSTER_NAME -n $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE -o json | ConvertFrom-Json
    if ($LastExitCode -ne 0) {
        kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify
        Continue
    }
    $workernodes = $tkc.status.nodeStatus | Get-Member | ForEach-Object { If ($_.Name -like "*workers*") { @{$_.Name = $tkc.status.nodeStatus.($_.Name) } } }
    $workernodes | Format-Table -HideTableHeaders -AutoSize | Out-String
} 
While (-Not $workernodes.Values.Contains("ready") -or $workernodes.Values.Contains("notready"))

# Deploy app
kubectl config use-context $VSPHERE_WITH_TANZU_CLUSTER_NAME
kubectl apply -f (Join-Path $LabStartupBaseFolder "labfiles/HOL-2201-08/Module 7/cadvisor.yml")
