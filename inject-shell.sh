BUILD=$(python getCurrentBuild.py)
echo "Toggling build number" $(($BUILD+1))
python toggleBuild -n $(($BUILD+1))
xterm -e "cd /var/lib/jenkins/workspace; sudo su -s /bin/bash jenkins"
trap "python toggleBuild -n"$(($BUILD+1)) EXIT