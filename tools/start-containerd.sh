set -e -x

containerd -v
containerd &

sleep 5

# we verify that it works
nerdctl run hello-world
