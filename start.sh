#!/bin/sh

. env/bin/activate
which python3

export PYTHONPATH=.

python=python3

$python main.py $*
