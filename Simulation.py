import pandas as pd
import numpy as np

import time as t
import multiprocessing as mp
import random
import string

from Master import Master
from Master import MasterSlotMode
from Master import TrainNum
from Slave import Slave

class Simulation(object):
	def __init__(self):
		self.master = Master()
		self.slave = Slave()

	def start_simulation(self):
		detections = 0
		numOfDetections = 4000
		timeArray = np.arange(numOfDetections)
		

		masters_clock = 1 # 1 - 16384

		# 15 + 1023 + 16 <- Max case
		# min 4 max 1054

		true_clock = 1
		while(detections < numOfDetections):
			self.master.tic(masters_clock)
			self.slave.tic()

			if masters_clock == 1:
				print true_clock
			#if true_clock >= 2048:
				#print '****************'
				#print 'Clock ' + str(true_clock)
				#print 'F1: ' + str(self.master.freqNumOne) + ' F2: ' + str(self.master.freqNumTwo)
				
			#if true_clock == 4096:
				#break;

			if self.master.slotMode == MasterSlotMode.tx:
				if (self.slave.sendFHS==True):
					print 'Assert: TX & slave sending FHS'
				if ((self.slave.inBackOffZone==False) & (self.slave.inOneSlotTo==False)):
					if ((self.slave.freqNum == self.master.freqNumOne) | (self.slave.freqNum == self.master.freqNumTwo)):
						self.slave.listen("Master_MAC")
						print '>> Hit at ' + str(true_clock)
			else: # in Rx mode
				if (self.slave.sendFHS==True):
					if ((self.slave.freqNum == self.master.freqNumOne) | (self.slave.freqNum == self.master.freqNumTwo)):
						time = true_clock
						timeArray[detections] = time

						# Reset Master & Slave
						self.slave.reset()
						self.master.resetTrain()
						masters_clock = 0 # because it will get increment at the end of while loop
						true_clock = 0

						detections = detections +1
					else:
						print 'Assert: RX & FHS sent, freqs didnt match ' + str(true_clock)
					

			#increment clocks
			true_clock = true_clock + 1
			masters_clock = masters_clock + 1
			if masters_clock > 16384:
				masters_clock = 1
				#self.master.resetTrain()
			
		rand_str = ''.join(random.choice(
                    string.ascii_lowercase
                    + string.ascii_uppercase
                    + string.digits)
               for i in range(5)) + '.csv'
		path = 'temp/'+rand_str
		#print timeArray
		np.savetxt(path, timeArray, delimiter=',', header='Time', fmt='%1.0f')


def multiMethod():
	simulation = Simulation()
	simulation.start_simulation()

if __name__ == '__main__':

	multiMethod()
	'''start_time = t.time()
	
	# Setup a list of processes that we want to run
	processes = [mp.Process(target=multiMethod) for x in range(4)]

	# Run processes
	for p in processes:
		p.start()

    # Exit the completed processes
	for p in processes:
		p.join()

	print("--- %s seconds ---" % (t.time() - start_time))
	'''

	

'''
[19 18 14 28  3  6 25 29 22 15 23  8 24 16  9 11]
[27 29 15 19  4 17 14 16 11  0 13 24 23  8  5 18 10 30  6 20 31 21  3  9  7
 22 28 12  2 25  1 26]
>> Hit at 6145

'''







