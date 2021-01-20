#!/bin/bash

echo Setting data...

home_dir=$(dirname $(dirname $(dirname $(realpath $0))))
echo home_dir=$home_dir
cd $home_dir/data/networks

# download and process network data
echo Downloading networks from GenePlexus...
wget https://zenodo.org/record/3352348/files/Supervised-learning%20is%20an%20accurate%20method%20for%20network-based%20gene%20classification%20-%20Data.tar.gz

echo Unpacking data...
tar -xzf "Supervised-learning is an accurate method for network-based gene classification - Data.tar.gz" --strip-components=1
echo Moving BioGRID
mv networks/BioGRID.edg .
echo Moving GIANT-TN
mv networks/GIANT-TN.edg .
echo Moving STRING
mv networks/STRING.edg .
rm -rf "Supervised-learning is an accurate method for network-based gene classification - Data.tar.gz" LICENSE.txt embeddings/ networks/ labels/

echo Construct GIANT-TN-c01 by obtaining edges of GIANT-TN with weights greater than 0.01
awk '{ if ($3 > 0.01) print $1"\t"$2"\t"$3 }' GIANT-TN.edg > GIANT-TN-c01.edg

echo Downloading SSN200 network from Fast Sinksource
wget --no-check-certificate https://bioinformatics.cs.vt.edu/~jeffl/supplements/2019-fastsinksource/downloads/200-species/2018_09-s200-seq-sim-e0_1-net.txt.gz

echo Unpacking data...
gzip -d 2018_09-s200-seq-sim-e0_1-net.txt.gz
echo Moving SSN200
echo
mv 2018_09-s200-seq-sim-e0_1-net.txt SSN200.edg

# making dense networks
echo Converting edgelists to dense matrix files for DenseOTF mode
mkdir dense

source ~/.bashrc
conda activate pecanpy-bench_pecanpy

cd $home_dir/script/init_setup
python make_dense_networks.py

echo Done
echo

