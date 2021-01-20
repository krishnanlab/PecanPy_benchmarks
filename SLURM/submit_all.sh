#!/bin/bash
cd $(dirname $(realpath $0))

for i in $(cat ../data/implementation_list.txt); do
    echo Submitting test job for $i...
    sbatch test_$i\.sb
    sbatch test_$i\_single.sb
done
