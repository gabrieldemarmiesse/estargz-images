set -e

containerd-stargz-grpc > /dev/null 2>&1 &
containerd > /dev/null 2>&1 &

sleep 10

# we verify that it works
nerdctl --snapshotter=stargz run ghcr.io/stargz-containers/python:3.10-esgz python -c "print('hello-world')"
