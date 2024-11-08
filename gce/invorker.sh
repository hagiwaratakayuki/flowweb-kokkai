source ./gce/env/bin/activate
./gce/env/bin/pip install -r /opt/app/gce/requirements.txt
export ENVNAME="gce_debian"
sudo shutdown -h now