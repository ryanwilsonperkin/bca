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
		self.blockchain_file = open(filename)	
		self.blockchain = [line[:-1] if line.endswith('\n') 
				   else line 
				   for line in self.blockchain_file]
		self.current_block = self.blockchain[-1]

	def reload(self):
		self.load(self.blockchain_file.name)
	
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
				return hex_hash

def handler(signum, frame):
	global miner
	print "Reloading"
	miner.reload()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Simplified Bitcoin miner program")
	parser.add_argument("filename", help="blockchain file")
	args = parser.parse_args()
	signal.signal(signal.SIGUSR1, handler)
	global miner
	miner = Miner()
	miner.load(args.filename)
	while True:
		print miner.mine()
		miner.reload()
