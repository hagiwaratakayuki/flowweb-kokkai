
set -ev


apt-get update
apt-get install -y python3 python3-pip python3-distutils mecab libmecab-dev mecab-ipadic-utf8  make curl xz-utils file
pip3 install --upgrade pip virtualenv



curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install




