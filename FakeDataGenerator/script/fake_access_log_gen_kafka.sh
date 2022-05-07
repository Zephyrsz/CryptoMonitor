#!/bin/bash

# Author: Wenyi Xu
# Copyright (c) 2016 WenyiXu
export VISORHOME=$(dirname "$PWD")
#echo $VISORHOME
python ../fake_log_gen/fake_log_producer.py -m access -o fake_access_file.log



