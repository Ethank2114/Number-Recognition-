##Network Training
##Ethan Kerr

from Network import network
from Network import matrix


#testWeights = [matrix([], (16, 1024), "normal"), matrix([], (16,16), "normal"), matrix([], (10,16), "normal")]
#testBiases = [matrix([], (16, 1), "normal"), matrix([], (16,1), "normal"), matrix([], (10,1), "normal")]

for i in range(10):


	testWeights = [matrix([], (16, 1024), "normal"), matrix([], (16,16), "normal"), matrix([], (10,16), "normal")]
	testBiases = [matrix([], (16, 1), "normal"), matrix([], (16,1), "normal"), matrix([], (10,1), "normal")]
	
	testNetwork = network(testWeights, testBiases)  #testWeights, testBiases
	
	print(testNetwork.getAllPredictions())
	print(testNetwork.accuracy())


'''
testNetwork.backPropagate(0)
testNetwork.backPropagate(0)
testNetwork.backPropagate(0)

print(testNetwork.getAllPredictions())
print(testNetwork.accuracy())


input("done")
'''