#!/usr/bin/env python3

import argparse
import logging
import logging.handlers
import os
import subprocess
import time

# test benchmarks for Table 4, 5, 6 in the paper
bitvec_test = [
    "100_1000.sl", "108_1000.sl", "111_1000.sl", "146_1000.sl", "40_100.sl",
    "icfp_gen_10.3.sl", "icfp_gen_15.13.sl", "icfp_gen_15.2.sl",
    "icfp_gen_2.20.sl", "icfp_gen_3.18.sl"
]

circuit_test = [
    "CrCy_10-sbox2-D5-sIn104.sl", "CrCy_10-sbox2-D5-sIn14.sl",
    "CrCy_10-sbox2-D5-sIn15.sl", "CrCy_10-sbox2-D5-sIn80.sl",
    "CrCy_10-sbox2-D5-sIn92.sl", "CrCy_6-P10-D5-sIn.sl",
    "CrCy_6-P10-D5-sIn3.sl", "CrCy_6-P10-D7-sIn.sl",
    "CrCy_6-P10-D7-sIn3.sl", "CrCy_6-P10-D7-sIn5.sl",
    "CrCy_6-P10-D9-sIn.sl", "CrCy_6-P10-D9-sIn3.sl",
    "CrCy_6-P10-D9-sIn5.sl", "CrCy_8-P12-D5-sIn1.sl",
    "CrCy_8-P12-D5-sIn3.sl", "CrCy_8-P12-D7-sIn1.sl",
    "CrCy_8-P12-D7-sIn5.sl", "CrCy_8-P12-D9-sIn1.sl"
]

def is_valid(f):
    return \
        f.startswith('exceljet') \
        or f.startswith('stackoverflow') \
        or f.startswith('phone') \
        or (f in bitvec_test) \
        or (f in circuit_test)

def run(args, logger):
    os.makedirs('euphony-out/' + args.cmd, 0o755, True)
    inputs = [ f for f in os.listdir('benchmarks/' + args.cmd + '/test') \
               if f.endswith('.sl') and is_valid(f) ]
    inputs = sorted(inputs)
    print("-" * 120)
    print("%-25s %8s %8s %8s" %
          (args.cmd + " Benchmarks", "|E|", "|P|", "Time"))
    print("-" * 120)
    euphony_base_cmd = 'timeout ' + str(args.timeout) \
            + ' ./bin/run_' + args.cmd + ' benchmarks/' + args.cmd + '/test/'
    example_count_base_cmd = 'grep \"constraint\" benchmarks/' + args.cmd + '/test/'
    ast_count_base_cmd = './bin/stat euphony-out/' + args.cmd + '/'
    for f in inputs:
        example_count_cmd = example_count_base_cmd + f + ' | wc -l'
        E = int(subprocess.getoutput(example_count_cmd))
        euphony_cmd = euphony_base_cmd + f
        start_time = time.time()
        output = subprocess.getoutput(euphony_cmd)
        with open('euphony-out/' + args.cmd + '/' + f + '.sol', 'w') as out_file:
            out_file.write(output)
        elapsed_time = time.time() - start_time
        ast_count_cmd = ast_count_base_cmd + f + '.sol'
        out = subprocess.getoutput(ast_count_cmd)
        try:
            P = int(subprocess.getoutput(ast_count_cmd))
        except:
            P = -1
        print("%-25s %8d %8s %8.1f" %
              (f, E, P, elapsed_time))

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    subparser = subparsers.add_parser("string", help="Run the String Benchmark Programs")
    subparser.add_argument("--timeout", type = int, default = 3600)
    subparser = subparsers.add_parser("bitvec", help="Run the Bitvec Benchmark Programs")
    subparser.add_argument("--timeout", type = int, default = 3600)
    subparser = subparsers.add_parser("circuit", help="Run the Circuit Benchmark Programs")
    subparser.add_argument("--timeout", type = int, default = 3600)
    return parser.parse_args()

def main():
    args = parse_args()
    logger = logging.getLogger('logger')
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler('./euphony.log')
    streamHandler = logging.StreamHandler()
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    if args.cmd in [ "string", "bitvec", "circuit" ]:
        run(args, logger)
    else:
        print("Invalid Argument")

if __name__ == "__main__":
    main()
