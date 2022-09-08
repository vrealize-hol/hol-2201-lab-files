kubectl config use-context rainpole
$Secret = kubetcl get secret dev-project-kubeconfig -o jsonpath='{.data.value}'
[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($Secret)) > C:\Users\Administrator\dev-tkg-kubeconfig.json
code C:\Users\Administrator\dev-tkg-kubeconfig.json

# Define variables
$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP = '172.16.21.129'
$VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE = "rainpole"
$VSPHERE_WITH_TANZU_CLUSTER_NAME = "dev-project"
$VSPHERE_WITH_TANZU_USERNAME = 'administrator@corp.local'
$ENV:KUBECTL_VSPHERE_PASSWORD = 'VMware1!'

# Connect to Supervisor cluster
kubectl vsphere login --vsphere-username $VSPHERE_WITH_TANZU_USERNAME --server=$VSPHERE_WITH_TANZU_CONTROL_PLANE_IP --tanzu-kubernetes-cluster-name $VSPHERE_WITH_TANZU_CLUSTER_NAME --tanzu-kubernetes-cluster-namespace $VSPHERE_WITH_TANZU_CLUSTER_NAMESPACE --insecure-skip-tls-verify | Out-Null

# Retrieve kubeconfig secret, decode, and open in VS Code
kubetcl get secret dev-project-kubeconfig -o jsonpath='{.data.value}' > [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String($Secret)) > code