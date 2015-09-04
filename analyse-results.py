import numpy as np
import matplotlib.pyplot as plt

def analyse():
	print 'analyse'
	final = np.genfromtxt('temp/1.csv', delimiter='\n')
	'''for i in range(2,5):
		data = np.genfromtxt('temp/'+str(i)+'.csv', delimiter='\n')
		final = np.concatenate([final,data])
	'''
	final = final.astype(int)
	print final.size

	#plt.hist(final, bins=(max(final)/16.0), color='b')
	plt.hist(final,bins=range(min(final), max(final) + 1, 1))
	plt.title("First Detection (in cycles) Histogram")
	plt.xlabel("Value")
	plt.xlim(-5000, 50000)
	plt.ylabel("Frequency")
	plt.show()





if __name__ == '__main__':
	analyse()