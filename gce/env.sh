sudo apt update
apt install -yq git python pip mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file
pip install --upgrade pip virtualenv
virtualenv -p python3 ~/envs/gce
