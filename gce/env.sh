sudo apt update
apt install -yq git python pip mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file
pip install --upgrade pip virtualenv
virtualenv -p python3 ~/envs/gce
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
./bin/install-mecab-ipadic-neologd -n -y -a
