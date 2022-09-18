set -eux

containerd -v
containerd &

sleep 5

# we verify that it works
nerdctl run hello-world

# login and start converting
echo $GHCR_TOKEN | nerdctl login ghcr.io -u $ --password-stdin
echo $GHCR_TOKEN | crane auth login -u $ --password-stdin ghcr.io
crane manifest ghcr.io/gabrieldemarmiesse/estargz-images/alpine:3.15.3-org
python -u ./convert_and_push_images.py
