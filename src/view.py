import signal, subprocess
from Tkinter import Tk, Canvas, Frame, BOTH

WINDOW_W = 640
WINDOW_H = 480
WINDOW_OFFSET_X = 100
WINDOW_OFFSET_Y = 100
HONEST_FILE="../data/honest"
MALICIOUS_FILE = "../data/malicious"

class BCAView(Frame):
	ORIGIN_X = 10
	ORIGIN_Y = 150
	ORIGIN_FILL = "#000"
	MALICIOUS_FILL = "#ff0000"
	HONEST_FILL = "#000"
	BLOCK_W = 30
	BLOCK_H = 30
	BLOCK_PADDING = 15
	BLOCK_OUTLINE = "#000"
	DELAY = 1000
	MINER_PROGRAM = ["python","miner.py"]

	def __init__(self, parent, honest_file, malicious_file):
		Frame.__init__(self, parent)
		self.parent = parent
		self.honest_file = honest_file
		self.malicious_file = malicious_file
		self.honest_miners = []
		self.malicious_miners = []
		self.honest_count = 0
		self.malicious_count = 0
		self.honest_block = self.getBlock(self.honest_file)
		self.malicious_block = self.getBlock(self.malicious_file)
		self.setup()

	def setup(self):
		self.parent.title("Block Chain Attack")
		self.pack(fill=BOTH, expand=1)
		canvas = Canvas(self)
		# Create origin node
		canvas.create_rectangle(self.ORIGIN_X, self.ORIGIN_Y, 
						self.ORIGIN_X + self.BLOCK_W, 
						self.ORIGIN_Y + self.BLOCK_H,
						outline=self.BLOCK_OUTLINE,
						fill=self.ORIGIN_FILL)
		canvas.pack(fill=BOTH, expand=1)
		self.canvas = canvas
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
		self.after(self.DELAY, self.update)
	
	def addHonestMiner(self):
		print "debug: adding honest miner"
		new_miner = subprocess.Popen(
			self.MINER_PROGRAM + [self.honest_file])
		self.honest_miners.append(new_miner)

	def addMaliciousMiner(self):
		print "debug: adding malicious miner"
		new_miner = subprocess.Popen(
			self.MINER_PROGRAM + [self.malicious_file])
		self.malicious_miners.append(new_miner)

	def killHonestMiners(self):
		for miner in self.honest_miners:
			miner.kill()
	
	def killMaliciousMiners(self):
		for miner in self.malicious_miners:
			miner.kill()
	
	def notifyMiner(self, miner):
		miner.send_signal(signal.SIGUSR1)

	def getBlock(self, filename):
		with open(filename, 'r') as f:
			blockchain = [line[:-1] if line.endswith('\n')
							else line 
							for line in f]
			return blockchain[-1]

	def addHonestNode(self):
		self.honest_count += 1
		x1 = self.ORIGIN_X \
			+ self.honest_count \
			* (self.BLOCK_W + self.BLOCK_PADDING)
		x2 = x1 + self.BLOCK_W
		y1 = self.ORIGIN_Y
		y2 = y1 + self.BLOCK_H
		self.canvas.create_rectangle(x1, y1, x2, y2,
						outline=self.BLOCK_OUTLINE,
						fill=self.HONEST_FILL)

	def addMaliciousNode(self):
		self.malicious_count += 1
		x1 = self.ORIGIN_X \
			+ self.malicious_count \
			* (self.BLOCK_W + self.BLOCK_PADDING)
		x2 = x1 + self.BLOCK_W
		y1 = self.ORIGIN_Y + self.BLOCK_H + self.BLOCK_PADDING
		y2 = y1 + self.BLOCK_H
		self.canvas.create_rectangle(x1, y1, x2, y2,
						outline=self.BLOCK_OUTLINE,
						fill=self.MALICIOUS_FILL)

def h(event):
	bcaview.addHonestMiner()

def m(event):
	bcaview.addMaliciousMiner()


def cleanup():
	bcaview.killHonestMiners()
	bcaview.killMaliciousMiners()
	exit(0)

if __name__ == "__main__":
	root = Tk()
	bcaview = BCAView(root, HONEST_FILE, MALICIOUS_FILE)
	signal.signal(signal.SIGINT, lambda signum, frame: cleanup())
	root.protocol("WM_DELETE_WINDOW", cleanup)
	root.bind("h", h)
	root.bind("m", m)
	root.geometry("%dx%d+%d+%d" % (WINDOW_W, WINDOW_H, 
					WINDOW_OFFSET_X, WINDOW_OFFSET_Y))
	root.mainloop()
