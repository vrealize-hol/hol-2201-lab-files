Write-Output "Start vRA (/opt/scripts/deploy.sh)"
echo y | plink root@vr-automation.corp.local -pw VMware1! -noagent "/opt/scripts/deploy.sh &"