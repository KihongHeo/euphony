# Euphony
Euphony: a probabilistic model-guided program synthesizer

## Build (tested on Linux)
```
$ ./build
$ . bin/setenv
```

## Reproduce the experiments in the paper
```sh
$ ./artifact [string | bitvec | circuit] --timeout 3600
```

## Run 
```
$ cd bin
$ ./run_[string | bitvec | circuit] ../benchmarks/[string | bitvec | circuit]/test/[a SyGuS input file]
```
