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
Write-VpodProgress "Creating GitLab repos" 'GOOD-6'
Write-Output "$(Get-Date) Creating GitLab repos"
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

<#
###
Write-VpodProgress "Configuring Tanzu" 'GOOD-6'
Write-Output "$(Get-Date) Configuring Tanzu"

# Clean kubeconfig
$KUBECTL_CONFIG_FOLDER = "C:\Users\Administrator\.kube"
If (Test-Path -Path $KUBECTL_CONFIG_FOLDER) { Remove-Item -Path $KUBECTL_CONFIG_FOLDER -Recurse -Force -Confirm:$false }

# Starting TKC cluster
$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP = '172.16.21.129'
$VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE = "rainpole"
$VSPHERE_WITH_TANZU_CLUSTER_NAME = "dev-project"
$VSPHERE_WITH_TANZU_USERNAME = 'administrator@corp.local'
$ENV:KUBECTL_VSPHERE_PASSWORD = 'VMware1!'

# Connect to Supervisor cluster
Write-Output "Login to Supervisor Cluster $VSPHERE_WITH_TANZU_CONTROL_PLANE_IP"
kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify | Out-Null

# Wait until it is applied
Do {
    Write-Output "Update TKC cluster"
    kubectl config use-context $VSPHERE_WITH_TANZU_CONTROL_PLANE_IP | Out-String | Write-Output
    kubectl apply -f $(Join-Path $LabStartupBaseFolder "build/vsphere/wcp/rainpole/tkc-dev-project.yaml") | Out-String | Write-Output
    if ($LastExitCode -ne 0) {
        kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify | Out-Null
        LabStartup-Sleep $sleepSeconds
        Continue
    }
    LabStartup-Sleep $sleepSeconds
    $tkc = kubectl get tkc/$VSPHERE_WITH_TANZU_CLUSTER_NAME -n $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE -o json | ConvertFrom-Json
    Write-Output ("Worker Nodes: " + $tkc.spec.topology.workers.count)
} While ($tkc.spec.topology.workers.count -lt 1)

# Wait until 1 worker node is ready
Do {
    LabStartup-Sleep $sleepSeconds
    Write-Output "Wait for worker node"
    kubectl config use-context $VSPHERE_WITH_TANZU_CONTROL_PLANE_IP | Out-String | Write-Output
    $tkc = kubectl get tkc/$VSPHERE_WITH_TANZU_CLUSTER_NAME -n $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE -o json | ConvertFrom-Json
    if ($LastExitCode -ne 0) {
        kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify | Out-Null
        LabStartup-Sleep $sleepSeconds
        Continue
    }
    $workernodes = $null
    if ($tkc) { $workernodes = $tkc.status.nodeStatus | Get-Member | ForEach-Object { If ($_.Name -like "*workers*") { @{$_.Name = $tkc.status.nodeStatus.($_.Name) } } } }
    if ($workernodes) { ($workernodes | Format-Table -HideTableHeaders -AutoSize | Out-String).Trim() | Write-Output }
} 
While (-Not $workernodes -or -Not $workernodes.Values.Contains("ready") -or $workernodes.Values.Contains("notready"))

# Clean system pod
$allpods = kubectl get pods --all-namespaces -o json | ConvertFrom-Json
$allpods.items | where-object { $_.status.phase -eq "Failed" -and $_.status.reason -eq "NodeAffinity" } | ForEach-Object {
    kubectl delete pod/$($_.metadata.name) -n $($_.metadata.namespace)
}

# Deploy app
kubectl config use-context $VSPHERE_WITH_TANZU_CLUSTER_NAME
Do {
    kubectl apply -f (Join-Path $LabStartupBaseFolder "build/vsphere/wcp/rainpole/dev-project/cadvisor.yml")
    Start-Sleep -Seconds 10
    $pods = kubectl get pods -n kube-system -o json | ConvertFrom-Json
} While (($pods.items.metadata.name -like "cadvisor*").Count -eq 0)

# Clean kubeconfig
Remove-Item -Path $KUBECTL_CONFIG_FOLDER -Recurse -Force -Confirm:$false

#>


## Added 5/16/22 by Gregg Parsons to force vRA to redeploy pods.
Write-VpodProgress "Deploying vRA" 'GOOD-7'
Write-Output "$(Get-Date) Checking status of initial vRA deployment"
Do {
    LabStartup-Sleep $sleepSeconds
    $vra_deploy = Invoke-Plink -remoteHost vr-automation.corp.local -login root -passwd VMware1! -command 'vracli status deploy'
    Write-Output "$(Get-Date) vRA Initial Deployment Check: $vra_deploy"
    # if ($vra_deploy -ne "Deployment complete") { Continue }
    # $vra_status = Invoke-Plink -remoteHost vr-automation.corp.local -login root -passwd VMware1! -command 'vracli status services'
    # Write-Output "$(Get-Date) vRA Services Check $vra_status"
} Until ($vra_deploy -eq "Deployment complete")

Write-Output "$(Get-Date) Initiating vRA deployment again"
cmd /c echo y | plink root@vr-automation.corp.local -pw VMware1! -noagent "nohup /opt/scripts/deploy.sh > /tmp/labstartup-deploy-2.out 2> /tmp/labstartup-deploy-2.err < /dev/null &"


## Clear expired token for SaltStack
Invoke-Plink -remoteHost saltstack.corp.local -login root -passwd VMware1! -command 'rm /var/cache/salt/master/auth_token.jwt'
Invoke-Plink -remoteHost saltstack.corp.local -login root -passwd VMware1! -command 'systemctl restart salt-master.service'