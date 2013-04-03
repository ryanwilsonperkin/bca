#!/usr/bin/python
import argparse
import random
import time
import hashlib

DIFFICULTY = 4
RANDOM_LOWERBOUND = 1
RANDOM_UPPERBOUND = 100

def testminer():
	first_hash = "qwerty"
	current_hash = first_hash
	while True:
		next_hash = getHash(current_hash)
		print next_hash
		current_hash = next_hash

def miner(block_chain_file):
	random.seed(time.clock())
	while True:
		block_chain = loadBlockChainFromFile(block_chain_file)
		latest_block = block_chain[-1]
		latest_header = latest_block['header']
		next_header = getHash(latest_header)
		try:
			writeToBlockChain(next_header)
		except exception as e:
			print "debug: collision while writing to [{}]".format(block_chain_file)

def getHash(data):
	nonce = 0
	increment = random.randint(RANDOM_LOWERBOUND,RANDOM_UPPERBOUND)
	while True:
		nonce += increment
		hex_hash = generateHash(data, nonce)
		if validHash(hex_hash):
			return hex_hash

def generateHash(header, nonce):
	data = "{}{}".format(header, nonce)
	return hashlib.sha256(data).hexdigest()

def validHash(hex_hash):
	int_hash = int(hex_hash, 16)
	cutoff = pow(10,75 - DIFFICULTY)
	if int_hash < cutoff:
		return True
	else:
		return False

if __name__ == "__main__":
	# parser = argparse.ArgumentParser(description="Simplified Bitcoin miner program")
	# parser.add_argument("block_chain_file", help="")
	# args = parser.parse_args()
	# miner(args.block_chain_file)
	testminer()

