#!/bin/bash

home_dir=$(dirname $(realpath $0))
echo home_dir=$home_dir
cd $home_dir/script/init_setup

./setup_dir.sh
./setup_envs.sh
./setup_data.sh
