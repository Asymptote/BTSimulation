from enum import Enum
import numpy as np

class Slave(object):
	def __init__(self):
		#print 'Slave init'

		self.slave_clock = 1 # 1 65536
		
		# Constants
		self.SLOTS_PER_FREQ = 2048 # No. of slots per freq
		self.FREQUENCIES = 32 # No. of frequencies per train
		self.BACKOFF_TIME_LIMIT = 1024

		np.random.seed()
		self.sTrain = np.random.permutation(self.FREQUENCIES)
		self.freqNum = 0
		self.potentialMasterMAC = ""

		# Backoff Zone
		self.inBackOffZone = False
		self.backOffTime = 0

		# oneSlotTo
		self.inOneSlotTo = False
		self.waitInOneSlotTo = 0

		self.sendFHS = False

	def resetAfterBackoff(self):
		self.slave_clock = 1

		np.random.seed()
		self.sTrain = np.random.permutation(self.FREQUENCIES)
		self.freqNum = 0

		# Backoff Zone
		self.inBackOffZone = False
		self.backOffTime = 0

		# oneSlotTo
		self.inOneSlotTo = False
		self.waitInOneSlotTo = 0

		self.sendFHS = False


	def listen(self, masterMac):
		if self.potentialMasterMAC == masterMac:
			#Got second packet
			#print '2nd Packet'
			self.inOneSlotTo = True
			self.waitInOneSlotTo = 1
		else:
			#print '1st Packet'
			np.random.seed()
			rnd = np.random.randint(self.BACKOFF_TIME_LIMIT,size=1)
			self.backOffTime = rnd[0]
			self.inBackOffZone = True
			self.potentialMasterMAC = masterMac

	def reset(self):
		self.resetAfterBackoff()
		self.potentialMasterMAC = ""

	def tic(self):
		# in oneSlotTo
		if self.inOneSlotTo:
			self.waitInOneSlotTo = self.waitInOneSlotTo - 1
			if self.waitInOneSlotTo == 0:
				self.inOneSlotTo = False
				self.sendFHS = True
				return
			else:
				print 'TX/RX issue'
				return

		# in Backoff
		if self.inBackOffZone:
			self.backOffTime = self.backOffTime - 1
			if self.backOffTime < 0:
				self.inBackOffZone = False
				#Reset Slave
				self.resetAfterBackoff()
			else:
				return

		# Alive
		currentFreqIndex = (self.slave_clock-1)/self.SLOTS_PER_FREQ
		self.freqNum = self.sTrain[currentFreqIndex]

		#increment slave clock
		self.slave_clock = self.slave_clock + 1
		if self.slave_clock > 65536:
			self.reset()


