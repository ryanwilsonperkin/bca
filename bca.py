#!/usr/bin/python
from subprocess import call
HONEST_FILE = "data/honest"
MALICIOUS_FILE = "data/malicious"
MINER_PROGRAM = "src/miner.py"
VIEW_PROGRAM = "src/view.py"

call(["python", VIEW_PROGRAM, HONEST_FILE, MALICIOUS_FILE, "python " + MINER_PROGRAM])
