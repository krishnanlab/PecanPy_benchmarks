# PecanPy_benchmarks

Benchmarking results and scripts for reproducing benchmarks of several implementations of node2vec 
including the newly developed [PecanPy](https://github.com/krishnanlab/PecanPy).  

Note: all test scripts provided use SLURM workload manager

## Setting up

This section contains instruction to setup the repo for benchmarking, which includes setting up 
* Environments for different implementataions (and building if necessary)
* Downloading and processing data
* Setting up directory structure for saving results

## Data

Run to following command to setup data and result directories (TODO).  

```bash
cd script/init_setup
sh setup_data.sh
```

### Networks

Various networks with wide range of sizes and densities are used for benchmarking different implementations. 
The relatively small networks (BlogCatalog, PPI, Wikipedia) are provided in this repository. 
They are originally downloaded from the [node2vec](https://snap.stanford.edu/node2vec/) webpage, and converted 
to edgelist files. The rest of the netowrks will need to be downloaded from other repositories, which will be 
automatically done by the `setup_data.sh` script.

|Network|Weighted|# nodes|# edges|Density (unweighted)|File size|
|:-|:-|-:|-:|-:|-:|
|BioGRID|No|20,558|238,474|1.13E-03|2.5M|
|STRING|Yes|17,352|3,640,737|2.42E-02|60M|
|GIANT-TN-c01|Yes|25,689|38,904,929|1.18E-01|1.1G|
|GIANT-TN|Yes|25,825|333,452,400|1.00E+00|7.2G|
|SSN200|Yes|814,731|72,618,574|2.19E-04|2.0G|
|BlogCatalog|No|10,312|333,983|6.28E-03|3.2M|
|PPI|No|3,852|38,273|5.16E-03|707K|
|Wikipedia|Yes|4,777|92,406|8.10E-03|2.0M|

## List of implementations

* Original node2vec (Python)
* Original node2vec (C++)
* PecanPy
  * PreComp
  * SparseOTF
  * DenseOTF
* nodevectors

## Submitting benchmark jobs

Each implementation will be tested using two different recourse configurations (*multi* and *single*). 
The *multi* setup aims to test the capability of implementation to make use of high computational resource, 
while the *single* setup tests the ability of implementation to be run on less capable resource such as a 
personal computer. The configuration details are the following  

|Configuration|Core count|Memory (GB)|Time limit (hr)|
|:-|:-|:-|:-|
|Multi|28|200|24|
|Single|1|32|8|

*To run all tests, execute the following command (TODO).*  

After all test jobs are finished, the following Python script `~/script get_test_info.py` will be executed 
to extract test information from logging files and summarize into a single table to `~/result/stat_summary/summary.txt`. 
The summary file can be renamed to specify specific benchmark conditions if needed. 
The table consists of the following columns: 
* **Network** - name of the network embedded
* **Method** - name of the implementation of node2vec
* **Setup** - computational resource setting of the test
* **Loading time** - (stage1) time used to load network into memory in desired format
* **Preprocessing time** - (stage2) time used to pre-compute transition probability table
* **Walking time** - (stage3) time used to generate random walks
* **Training time** - (stage4) time used to train word2vec model using the random walks
* **Total time** - total run time of the program (from startup)
* **Total time in second** - same as total time, but converted to seconds
* **Maximum resident size** - maximum physical memory used

# TODO
- [ ] Setup script for result directories
- [ ] Setup script for data retriving
- [ ] Script for converting `.edg` to `.npz`
- [x] Job submision script for all tests
- [ ] Script for extracting results from stat files (execute automatically after all jobs finished, setup with SLURM)
- [ ] Embedding quality evaluation script
