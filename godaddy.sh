#!/bin/sh
OLD_PWD=$PWD
ROOT_DIR=$(dirname $0)
cd $ROOT_DIR
if [ ! -d .venv27 ] ; then
  curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
  tar xvfz virtualenv-1.9.tar.gz
  python virtualenv-1.9/virtualenv.py .venv27
fi
source .venv27/bin/activate
pip install -q --upgrade pif pygodaddy
./godaddy.py
deactivate
cd $OLD_PWD
