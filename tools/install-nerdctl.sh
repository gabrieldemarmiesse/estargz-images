set -e
wget https://github.com/containerd/nerdctl/releases/download/v0.22.2/nerdctl-full-0.22.2-linux-amd64.tar.gz -O /tmp/nerdctl.tar.gz

tar Cxzvvf /usr/local /tmp/nerdctl.tar.gz

mkdir /etc/containerd/
cat ./tools/containerd-config.toml >> /etc/containerd/config.toml
