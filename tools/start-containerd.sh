set -e -x

containerd -v
systemctl enable --now containerd

sleep 5

# we verify that it works
nerdctl run hello-world
