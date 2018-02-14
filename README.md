# Euphony
Euphony: a probabilistic model-guided program synthesizer

## Build (tested on Linux)
```
$ ./build
$ . bin/setenv
```

## Reproduce the experiments in the paper
```sh
# Table 4,5,6
$ ./artifact [string | bitvec | circuit] --timeout 3600
# Table 4,5,6 without EUSOLVER
$ ./artifact [string | bitvec | circuit] --timeout 3600 --only_euphony
# Figure 8
$ ./artifact [string | bitvec | circuit] --timeout 3600 --only_euphony --strategy [uniform | pcfg | pcfg_uniform]
```

## Run Euphony on a single SyGus file
```
$ ./bin/run_[string | bitvec | circuit] [a SyGuS input file]
# For example
$ ./bin/run_[string | bitvec | circuit] ../benchmarks/[string | bitvec | circuit]/test/[a SyGuS input file]
```
