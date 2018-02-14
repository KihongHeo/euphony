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

def count_example(args, f):
    if args.cmd == "circuit":
        example_count_base_cmd = 'head -1 euphony-out/' + args.cmd + '/'
        example_count_cmd = example_count_base_cmd + f + '.iter'
    else:
        example_count_base_cmd = 'grep \"constraint\" benchmarks/' + args.cmd + '/test/'
        example_count_cmd = example_count_base_cmd + f + ' | wc -l'
    try:
        return int(subprocess.getoutput(example_count_cmd))
    except:
        return -1

def run_euphony(args, f, solver="euphony"):
    cmd = 'timeout ' + str(args.timeout) + ' ./bin/run_' + args.cmd
    if solver == "eusolver":
        cmd += "_eusolver"

    cmd += ' benchmarks/' + args.cmd + '/test/' + f
    start_time = time.time()
    output = subprocess.getoutput(cmd)
    if output is "":
        iters = ""
        output = ""
    else:
        lines = output.split('\n')
        iters = lines[0]
        output = lines[1]
    with open('euphony-out/' + args.cmd + '/' + f + '.' + solver + '.iter', 'w') as out_file:
        out_file.write(iters)
    with open('euphony-out/' + args.cmd + '/' + f + '.' + solver + '.sol', 'w') as out_file:
        out_file.write(output)
    elapsed_time = time.time() - start_time
    return elapsed_time

def count_ast(args, f, solver="euphony"):
    ast_count_base_cmd = './bin/stat euphony-out/' + args.cmd + '/'
    ast_count_cmd = ast_count_base_cmd + f + '.' + solver + '.sol'
    out = subprocess.getoutput(ast_count_cmd)
    try:
        return int(subprocess.getoutput(ast_count_cmd))
    except:
        return -1

def print_header(args):
    if args.cmd == "circuit":
        E = "#Iter"
    else:
        E = "|E|"
    print("-" * 120)
    print("  %54s %18s" % ("EUPHONY", "EUSOLVER"))
    print("  %-30s %8s %8s %8s %8s %8s" %
          (args.cmd.capitalize() + " Benchmarks", E, "|P|", "Time", "|P|", "Time"))
    print("-" * 120)

def run(args, logger):
    os.makedirs('euphony-out/' + args.cmd, 0o755, True)
    inputs = [ f for f in os.listdir('benchmarks/' + args.cmd + '/test') \
               if f.endswith('.sl') and is_valid(f) ]
    inputs = sorted(inputs)

    print_header(args)
    for f in inputs:
        elapsed_time_euphony = run_euphony(args, f)
        elapsed_time_eusolver = run_euphony(args, f, "eusolver")
        E = count_example(args, f)
        P_euphony = count_ast(args, f)
        P_eusolver = count_ast(args, f, "eusolver")
        print("  %-30s %8d %8d %8.1f %8d %8.1f" %
              (f, E, P_euphony, elapsed_time_euphony,
               P_eusolver, elapsed_time_eusolver))

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
