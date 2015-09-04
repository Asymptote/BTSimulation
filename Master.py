from enum import Enum
import numpy as np


class MasterSlotMode(Enum):
	tx = 1 # Transmission
	rx = 2 # Reception

class TrainNum(Enum):
	a = 1 # Using train A
	b = 2 # Using train B


class Master(object):
	def __init__(self):
		# Constants
		self.FREQUENCIES_PER_TRAIN = 16 # No. of frequencies per train
		self.SLOTS_PER_TRAIN = 4096 # No. of repetitions per train

		#np.random.seed()
		arr = np.random.permutation(32)
		self.aTrain = arr[0:16]
		#self.aTrain = np.array([19, 18, 14, 28,  3,  6, 25, 29, 22, 15, 23, 8, 24, 16, 9, 11])
		self.bTrain = arr[16:32]
		
		# Current State
		self.train = TrainNum.a
		self.slotMode = MasterSlotMode.tx

		self.freqNumOne = 0
		self.freqNumTwo = 0

	def resetTrain(self):
		#np.random.seed()
		arr = np.random.permutation(32)
		self.aTrain = arr[0:16]
		self.bTrain = arr[16:32]
		
		# Current State
		self.train = TrainNum.a
		self.slotMode = MasterSlotMode.tx

	def tic(self, clk):

		numSwitches = ((clk-1)/self.SLOTS_PER_TRAIN)

		if numSwitches >= 4:
			print 'Assert: Wrong Clock in Master i.e. > 4096*4'
		if ((numSwitches%2) == 0):
			self.train = TrainNum.a
		else:
			self.train = TrainNum.b

		if ((clk%2) == 1):#if clk is odd -> tx
			self.slotMode = MasterSlotMode.tx
		else:
			self.slotMode = MasterSlotMode.rx

		#Update transmitting/receiving frequencies
		if self.slotMode == MasterSlotMode.tx:
			temp_num = (clk%self.FREQUENCIES_PER_TRAIN)
			if temp_num == 0:
				temp_num = self.FREQUENCIES_PER_TRAIN
			freqIndex = temp_num-1

			if self.train == TrainNum.a:
				self.freqNumOne = self.aTrain[freqIndex]
				self.freqNumTwo = self.aTrain[freqIndex+1]
			elif self.train == TrainNum.b:
				self.freqNumOne = self.bTrain[freqIndex]
				self.freqNumTwo = self.bTrain[freqIndex+1]