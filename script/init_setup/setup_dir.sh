#!/bin/bash

echo Settingup directories for holding results...

home_dir=$(dirname $(dirname $(dirname $(realpath $0))))
cd $home_dir
echo home_dir=$home_dir

# slurm history folder, contains slurm output files
if [ ! -d SLURM_history ]; then
    mkdir SLURM_history
fi

# result folder, contains embeddings and stats
if [ ! -d result ]; then
	mkdir result
fi

if [ ! -d result/emb ]; then
    mkdir result/emb # directory for holding embeddings
fi

if [ ! -d result/stat ]; then
    mkdir result/stat # directory for holding runtime statistics
fi

for i in emb stat; do
	for j in $(cat data/implementation_list.txt); do
		mkdir result/$i/$j
	done
done

echo Done
echo

