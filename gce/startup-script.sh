#! /bin/bash
set -v
CLONE_URL = "your_clone"

curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &


apt-get update
apt-get install -yq \
    git build-essential python python-dev python-pip libffi-dev \
    libssl-dev  jq
cd ~
PYENV_INSTALLER = "pyenv-installer"
if [-f ${PYENV_INSTALLER}]; then
  MODE="update"


  #conda uodate
else
  MODE="create"
  wget https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer
  bash pyenv-installer
fi

export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PATH="~/.pyenv/versions/miniconda-latest:$PATH"
if [ $MODE = "create"]; then

  pyenv install miniconda-latest
  conda update conda
  echo ". /home/master/.pyenv/versions/miniconda-latest/etc/profile.d/conda.sh" >> ~/.bash_profile
  bash -l
fi
if [ $MODE = "update"]; then
  conda update conda

fi

export HOME=/root
git config --global credential.helper gcloud.sh
git clone $CLONE_URL /opt/app

cd /opt/app



pip install yq
NAME=$(yq environment.yml .name)

if [ $MODE = "create"]; then
  conda env create --file=environment.yml

fi

activate $NAME

if [ $MODE = "update"]; then
  conda env update
fi


nohup bash invorker.sh &
