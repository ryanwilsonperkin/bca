#!/usr/bin/python
import argparse
import random
import time
import hashlib
import signal

DIFFICULTY = 4
RANDOM_LOWERBOUND = 1
RANDOM_UPPERBOUND = 100

class Miner:
	def __init__(self):
		pass

	def load(self, filename):
		self.blockchain_file = filename
		with open(filename, 'r') as f:
			self.blockchain = [line[:-1] if line.endswith('\n') 
					   else line 
					   for line in f]
			self.current_block = self.blockchain[-1]

	def reload(self):
		self.load(self.blockchain_file)
	
	def mine(self):
		random.seed(time.clock())
		increment = random.randint(RANDOM_LOWERBOUND,
					   RANDOM_UPPERBOUND)
		nonce = 0
		maximum = pow(10, 75 - DIFFICULTY)
		while True:
			nonce += increment
			data = "{}{}".format(self.current_block, nonce)
			hex_hash = hashlib.sha256(data).hexdigest()
			if int(hex_hash, 16) <= maximum:
				with open(self.blockchain_file, 'a') as f:
					f.write(hex_hash)
					f.write('\n')
				return

def handler(signum, frame):
	global miner
	miner.reload()
	
def finish(signum, frame):
	exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Simplified Bitcoin miner program")
	parser.add_argument("filename", help="blockchain file")
	args = parser.parse_args()
	global miner
	miner = Miner()
	miner.load(args.filename)
	signal.signal(signal.SIGINT, finish)
	signal.signal(signal.SIGUSR1, handler)
	while True:
		miner.mine()
		miner.reload()
