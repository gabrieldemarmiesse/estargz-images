set -e

systemctl enable --now containerd

sleep 5

# we verify that it works
nerdctl run python:3.10 python -c "print('hello-world')"
