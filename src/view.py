#!/usr/bin/python
import signal, subprocess, argparse
from Tkinter import Tk, Canvas, Frame, BOTH, NW

WINDOW_W = 640
WINDOW_H = 150
WINDOW_OFFSET_X = 100
WINDOW_OFFSET_Y = 100

class BCAView(Frame):
	TITLE = "Block Chain Attack"
	BLOCK_W = 30
	BLOCK_H = 30
	BLOCK_PADDING = 15
	ORIGIN_X = 10
	ORIGIN_Y = 60
	ORIGIN_FILL = "#000"
	HONEST_FILL = "#000"
	MALICIOUS_FILL = "#ff0000"
	COUNTER_X = 10
	COUNTER_Y = 10
	DELAY = 500
	MAX_HONEST_MINERS = 10
	MAX_MALICIOUS_MINERS = 10
	MAX_NODES = 13

	def __init__(self, parent, honest_file, malicious_file, miner_program):
		Frame.__init__(self, parent)
		self.parent = parent
		self.honest_file = honest_file
		self.malicious_file = malicious_file
		self.miner_program = miner_program.split()
		self.honest_miners = []
		self.malicious_miners = []
		self.honest_node_count = 0
		self.malicious_node_count = 0
		self.honest_block = self.getBlock(self.honest_file)
		self.malicious_block = self.getBlock(self.malicious_file)
		self.setup()

	def setup(self):
		self.parent.title(self.TITLE)
		self.pack(fill=BOTH, expand=1)
		canvas = Canvas(self)
		canvas.create_rectangle(self.ORIGIN_X, self.ORIGIN_Y, 
			self.ORIGIN_X + self.BLOCK_W, 
			self.ORIGIN_Y + self.BLOCK_H,
			fill=self.ORIGIN_FILL)
		canvas.create_line(0, self.ORIGIN_Y + (self.BLOCK_H/2),
			self.ORIGIN_X, self.ORIGIN_Y + (self.BLOCK_H/2),
			fill=self.ORIGIN_FILL,
			width=3.0)
		self.counter = canvas.create_text(
			self.COUNTER_X, 
			self.COUNTER_Y,
			anchor=NW)
		canvas.pack(fill=BOTH, expand=1)
		self.canvas = canvas
		self.addHonestNode()
		self.after(self.DELAY, self.update)

	def update(self):
		new_honest_block = self.getBlock(self.honest_file)
		new_malicious_block = self.getBlock(self.malicious_file)
		if self.honest_block != new_honest_block:
			self.honest_block = new_honest_block
			self.addHonestNode()
			for miner in self.honest_miners:
				self.notifyMiner(miner)

		if self.malicious_block != new_malicious_block:
			self.malicious_block = new_malicious_block
			self.addMaliciousNode()
			for miner in self.malicious_miners:
				self.notifyMiner(miner)
		self.updateCounter()
		if self.malicious_node_count < self.MAX_NODES \
			and self.honest_node_count < self.MAX_NODES:
			self.after(self.DELAY, self.update)
		else:
			self.finish()
	
	def finish(self):
		pass

	def getBlock(self, filename):
		with open(filename, 'r') as f:
			blockchain = [line[:-1] if line.endswith('\n')
				else line 
				for line in f]
			return blockchain[-1]

	def addHonestNode(self):
		self.honest_node_count += 1
		x1 = self.ORIGIN_X \
			+ self.honest_node_count \
			* (self.BLOCK_W + self.BLOCK_PADDING)
		x2 = x1 + self.BLOCK_W
		y1 = self.ORIGIN_Y
		y2 = y1 + self.BLOCK_H
		self.canvas.create_rectangle(x1, y1, x2, y2,
			fill=self.HONEST_FILL)
		lx1 = x1 - self.BLOCK_PADDING
		ly1 = y1 + (self.BLOCK_H/2)
		lx2 = x1
		ly2 = ly1
		self.canvas.create_line(lx1, ly1, lx2, ly2,
			fill=self.HONEST_FILL,
			width=3.0)

	def addMaliciousNode(self):
		self.malicious_node_count += 1
		x1 = self.ORIGIN_X \
			+ self.malicious_node_count \
			* (self.BLOCK_W + self.BLOCK_PADDING)
		x2 = x1 + self.BLOCK_W
		y1 = self.ORIGIN_Y + self.BLOCK_H + self.BLOCK_PADDING
		y2 = y1 + self.BLOCK_H
		self.canvas.create_rectangle(x1, y1, x2, y2,
			fill=self.MALICIOUS_FILL)
		if self.malicious_node_count == 1:
			lx1 = self.ORIGIN_X + (self.BLOCK_W/2)
			ly1 = self.ORIGIN_Y + self.BLOCK_H
		else:
			lx1 = x1 - self.BLOCK_PADDING
			ly1 = y1 + (self.BLOCK_H/2)
		lx2 = x1
		ly2 = y1 + (self.BLOCK_H/2)
		self.canvas.create_line(lx1, ly1, lx2, ly2,
			fill=self.MALICIOUS_FILL,
			width=3.0)
	
	def updateCounter(self):
		text = ("Honest Miners:\t{honest}\n" 
			"Malicious Miners:\t{malicious}").format(
			honest=len(self.honest_miners),
			malicious=len(self.malicious_miners))
		self.canvas.itemconfig(self.counter, text=text)

	def addHonestMiner(self):
		if len(self.honest_miners) < self.MAX_HONEST_MINERS:
			new_miner = subprocess.Popen(
				self.miner_program + [self.honest_file])
			self.honest_miners.append(new_miner)

	def addMaliciousMiner(self):
		if len(self.malicious_miners) < self.MAX_MALICIOUS_MINERS:
			new_miner = subprocess.Popen(
				self.miner_program + [self.malicious_file])
			self.malicious_miners.append(new_miner)

	def killHonestMiner(self):
		if self.honest_miners:
			self.honest_miners.pop().kill()

	def killMaliciousMiner(self):
		if self.malicious_miners:
			self.malicious_miners.pop().kill()

	def killHonestMiners(self):
		while self.honest_miners:
			self.killHonestMiner()
	
	def killMaliciousMiners(self):
		while self.malicious_miners:
			self.killMaliciousMiner()

	def notifyMiner(self, miner):
		miner.send_signal(signal.SIGUSR1)


def cleanup():
	bcaview.killHonestMiners()
	bcaview.killMaliciousMiners()
	exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Block Chain Attack")
	parser.add_argument("honest_file", 
		help="location of the honest block chain file")
	parser.add_argument("malicious_file",
		help="location of the malicious block chain file")
	parser.add_argument("miner_program",
		help="the miner program to invoke on the block chains")
	args = parser.parse_args()
	root = Tk()
	bcaview = BCAView(root, 
		args.honest_file, 
		args.malicious_file,
		args.miner_program)
	signal.signal(signal.SIGINT, lambda signum, frame: cleanup())
	root.bind("h", lambda event: bcaview.addHonestMiner())
	root.bind("m", lambda event: bcaview.addMaliciousMiner())
	root.bind("H", lambda event: bcaview.killHonestMiner())
	root.bind("M", lambda event: bcaview.killMaliciousMiner())
	root.protocol("WM_DELETE_WINDOW", cleanup)
	root.geometry("%dx%d+%d+%d" % (WINDOW_W, WINDOW_H, 
		WINDOW_OFFSET_X, WINDOW_OFFSET_Y))
	root.resizable(0,0)
	root.mainloop()
