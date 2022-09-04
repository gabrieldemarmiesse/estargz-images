set -e

systemctl enable --now containerd

sleep 10

# we verify that it works
nerdctl run python:3.10 python -c "print('hello-world')"
