echo "Toggling build number" "$1"
python toggleBuild -n "$1"
xterm -e "cd /var/lib/jenkins/workspace; sudo su -s /bin/bash jenkins"
trap "python toggleBuild -n""$1" EXIT