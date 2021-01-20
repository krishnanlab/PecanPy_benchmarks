#!/bin/bash

echo Setting up environments for testing...

home_dir=$(dirname $(dirname $(dirname $(realpath $0))))
echo home_dir=$home_dir
echo

cd $home_dir/envs
for i in $(ls); do
    echo Setting up $(basename $i)
    conda env create -f $i
done

cd $home_dir/script/interface
echo Pulling source code for python node2vec...
git clone git@github.com:aditya-grover/node2vec.git

cd node2vec_cpp
echo Pulling source code for c++ node2vec...
git clone git@github.com:snap-stanford/snap.git

echo Replace source with timed version, building node2vec...
cp n2v_timed.cpp snap/snap-adv/n2v.cpp
cp node2vec_timed.cpp snap/examples/node2vec/node2vec.cpp

cd snap/examples/node2vec
make
cp nod2vec ../../../../node2vec_cpp_cli

echo Done
echo

