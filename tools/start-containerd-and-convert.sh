set -eux

containerd -v
containerd &

sleep 5

# we verify that it works
nerdctl run hello-world

# login and start converting
echo $GHCR_TOKEN | nerdctl login ghcr.io -u $ --password-stdin
echo $GHCR_TOKEN | crane auth login -u $ --password-stdin ghcr.io
python -u ./convert_and_push_images.py
