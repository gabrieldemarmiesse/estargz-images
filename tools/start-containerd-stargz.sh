set -e

systemctl enable --now containerd-stargz-grpc
systemctl enable --now containerd

sleep 5

# we verify that it works
nerdctl --snapshotter=stargz run ghcr.io/stargz-containers/python:3.10-esgz python -c "print('hello-world')"
