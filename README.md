# Euphony
Euphony: a probabilistic model-guided program synthesizer

## Build (tested on Linux)
```
$ ./build
```

## Reproduce the experiments in the paper
```sh
$ ./artifact.py [string | bitvec | circuit] --timeout 3600
```

## Run 
```
$ cd bin
$ ./run_[bv | str | circuit] ../benchmarks/[BV | STR | CrCy]/test/[a SyGuS input file]
```
