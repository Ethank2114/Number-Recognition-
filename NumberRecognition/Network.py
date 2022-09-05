##Network
##Ethan Kerr

import math, random, sys, time, tabulate

class matrix:
	#content:2d array # size:(n, m)
	def __init__(self, content, size = None, mode = None, constant = 0):
		self.content = content

		if mode != None:
			self.fill(size, mode, constant)

		#n: depth(y) m:width(x)
		self.n = len(self.content[0])
		self.m = len(self.content)

	#matrix by vector
	def dot(self, vector): #dot product of  a vector and matrix
		out = []
		for i in range(self.n):
			counter = 0
			for j in range(vector.n):
			
				counter += float(self.content[j][i]) * float(vector.content[0][j])
				

			out.append(counter)

		return matrix([out])

	#self is vector // matrix now
	def add(self, vector): #add together similar sized matrixs

		return matrix([[self.content[j][i] + vector.content[j][i] for i in range(self.n)] for j in range(self.m)])


	#self is vector
	def multiply(self, const): #multiply matrix by a constant
		return matrix([[self.content[j][i] * const for i in range(self.n)] for j in range(self.m)])

	#size: (n, m)
	def fill(self, size, mode, constant = 0):
		if mode == "const":
			self.content = [[int(constant) for i in range(size[0])] for i in range(size[1])]

		elif mode == "rand": #random float between -1 and 1
			self.content = [[random.uniform(-3, 3) for i in range(size[0])] for i in range(size[1])]

		elif mode == "randinp": #Either 0 or 1
			self.content = [[random.randint(0, 1) for i in range(size[0])] for i in range(size[1])]

		elif mode == "testData": #all zeros but 1
			self.content = [[0 for i in range(size[0])] for i in range(size[1])]
			self.content[0][random.randint(0,9)] = 1

		elif mode == "label": #all zeros but one which is the constant
			self.content = [[0 for i in range(size[0])] for i in range(size[1])]
			self.content[0][constant] = 1

		elif mode == "randDist": #divide by sqrt of number of inputs for layer
			self.content = [[distributionCurve(random.uniform(-3,3)) for i in range(size[0])] for j in range(size[1])]

		elif mode == "normal": #divide by sqrt of number of inputs for layer
			self.content = [[normalDist(random.uniform(-1,1)) / size[1] for i in range(size[0])] for j in range(size[1])]

	def __str__(self):
		out = []
		for i in range(self.n):
			out2 = []
			for j in range(self.m):
				out2.append(self.content[j][i])
			out.append(out2)

		return tabulate.tabulate(out)

	'''def __str__(self):
		out = ""
		for i in range(self.n):
			for j in range(self.m):
				out += str(self.content[j][i]) + " "
			out += "\n"
		return out'''


	def printArray(self, array):
		for i in range(len(array[0])):
			out = ""
			for j in range(len(array)):
				out += str(array[j][i]) + " "
			#print(out)


### Math Functions: -->



def sigma(x): #regular sigmoid function
	return 1/((math.exp(-1 * x)) + 1)

def sigmaPrime(x): #regular sigmoid derivative function
	return math.exp(-1 * x)/((math.exp(-1*x) + 1)**2)
	
def distributionCurve(x): #normal distribution curve
	return math.exp((-1) * (x ** 2))

def normalDist(x): #returns values based on probability on the normal distribution curve
	if x < 0:
		return (-1 * math.log(x + 1))**0.5
	elif x >= 0:
		return -1* (-1* math.log(-1*(x-1)))**0.5



#	<-- Math Functions ###



'''
def lowerRes(array): #to compress the hilbert curved series's
	counter = 0
	out = []
	for i in range(len(array)):
		counter += array[i]
		if (i + 1) % 4 == 0:
			out.append(counter / 4)
			counter = 0
	return out
'''


class network:
	#weights and biases lists of matrixs fit to size of network
	def __init__(self, weights = None, biases = None):
		self.input = None

		self.weights = weights
		self.biases = biases
		self.actual = None

		if self.weights == None and self.biases == None:
			self.readWeights()
			self.readBiases()
		
		self.clearCache()

		#self.counter = [0,0,0,0,0,0,0]


	def clearCache(self): #for dynamically calculating the cost gradient
		self.layerCacheSig = [None for i in range(len(self.weights) + 1)]
		self.layerCacheNoSig = [None for i in range(len(self.weights) + 1)]
		self.dC_daL1Cache = [[None for i in range(self.weights[0].n)] for j in range(len(self.weights) + 1)]
		self.dC_daL2Cache = [[None for i in range(self.weights[0].n)] for j in range(len(self.weights) + 1)]

	def __str__(self):
		return "layers: " + str(len(self.biases) + 1)

	def getLayer(self, layer, sigmoid = True): #return layer of network in a vector
		#sigmoid=false: for z in nodes
		if sigmoid:
			
			if self.layerCacheSig[layer] == None:
				#self.counter[1] += 1
				currentLayer = self.input
				for i in range(layer):
					currentLayer = matrix([[sigma(x) for x in self.weights[i].dot(currentLayer).add(self.biases[i]).content[0]]])
		
				self.layerCacheSig[layer] = currentLayer

				return currentLayer
			else:
				#self.counter[2] += 1
				return self.layerCacheSig[layer]

		else:
			
			if self.layerCacheNoSig[layer] == None:
				#self.counter[3] += 1
				currentLayer = self.input
				for i in range(layer):
					if i != layer:
						currentLayer = matrix([[sigma(x) for x in self.weights[i].dot(currentLayer).add(self.biases[i]).content[0]]])
					elif i == layer:
						currentLayer = self.weights[i].dot(currentLayer).add(self.biases[i])

				self.layerCacheNoSig[layer] = currentLayer
		
				return currentLayer
			else:
				#self.counter[4] += 1
				return self.layerCacheNoSig[layer]



	###	Calculus Helper Functions:	-->



	#L: layer of z
	#j: depth of node in layer
	def z(self, L, j): #returns number
		return self.getLayer(L, False).content[0][j]
		
	#L: layer of z
	#k: depth of node in layer L - 1
	def dz_dw(self, L, k): #returns number
		return self.getLayer(L - 1).content[0][k]	

	#z: z
	def da_dz(self, z):
		return sigmaPrime(z)

	#L: #j: 
	def dC_daL(self, L, j):
		#self.counter[2] += 1
		return 2 * (self.getLayer(L).content[0][j] - self.actual.content[0][j])

	def dC_dwL(self, L, j, k): #weights in last layer
		#self.counter[1] += 1

		return self.dz_dw(L, k) * self.da_dz(self.z(L, j)) * self.dC_daL(L, j)

	def dC_dbL(self, L, j): #biases in last layer
		return self.da_dz(self.z(L, j)) * self.dC_daL(L, j)

	#L: layer of z
	def dz_daL1(self, L, j, k):
		return self.weights[L].content[j][k]

	#L: layer of aL1
	def dC_daL1(self, L, k):
		#self.counter[1] += 1
		if self.dC_daL1Cache[L][k] == None:
			count = 0
			for j in range(self.getLayer(L + 1).n):
				#print(i)
				count += self.dz_daL1(L, k, j) * self.da_dz(self.z(L + 1, j)) * self.dC_daL(L + 1, j) 

			self.dC_daL1Cache[L][k] = count

			return count
		else:
			return self.dC_daL1Cache[L][k]

	def dC_daL2(self, L, i):
		#self.counter[0] += 1
		if self.dC_daL2Cache[L][i] == None:
			count = 0
			for k in range(self.getLayer(L + 1).n):
	
				#print(i)
				count += self.dz_daL1(L, k, i) * self.da_dz(self.z(L + 1, k)) * self.dC_daL1(L + 1, k) 
			self.dC_daL2Cache[L][i] = count
			return count
		else:
			return self.dC_daL2Cache[L][i]

	#weights:Matrix #layer:vector #biases:vector #actuals:vector
	def dC_dwL1(self, L, k, i): #weights all but last layer

		#self.counter[2] += 1
		return self.dz_dw(L, i) * self.da_dz(self.z(L, k)) * self.dC_daL1(L, k)

	def dC_dbL1(self, L, k):
		return self.da_dz(self.z(L, k)) * self.dC_daL1(L, k)


	def dC_dwL2(self, L, i, l): #weights all but last layer
		#self.counter[3] += 1
		return self.dz_dw(L, l) * self.da_dz(self.z(L, i)) * self.dC_daL2(L, i)

	def dC_dbL2(self, L, i):
		return self.da_dz(self.z(L, i)) * self.dC_daL1(L + 1, i)

	def delCknot(self):

		gradient = []
		layerIndex = len(self.weights)

		for weights in list(reversed(self.weights)): #for every weight matrix (backward)

			#print("layerIndex: " + str(layerIndex))

			if layerIndex == len(self.weights): #if matrix is weights L

				gradient.append(matrix([[self.dC_dwL(layerIndex, j, k) for j in range(weights.n)] for k in range(weights.m)]))

				#print(gradient[0].content[0][0], "gradient")
				#print(weights.content[0][0], "weight")
				#print(self.getLayer(2).content[0][0], "layer 2")
				#print(self.getLayer(3).content[0][0], "layer 3")
				#print(self.actual.content[0][0], "actual")

				#input("")
			
			elif layerIndex == len(self.weights) - 1:
						
				gradient.append(matrix([[self.dC_dwL1(layerIndex, k, i) for k in range(weights.n)] for i in range(weights.m)]))

			elif layerIndex == len(self.weights) - 2:
	
				gradient.append(matrix([[self.dC_dwL2(layerIndex, i, l) for i in range(weights.n)] for l in range(weights.m)]))

			layerIndex -= 1

			#print("layer: " + str(layerIndex))
		#print("weights done")

		gradient.reverse()

		layerIndex = len(self.biases)

		holder = []
		for biases in list(reversed(self.biases)): #for every weight matrix (backward)
			
			#print("layerIndex: " + str(layerIndex))

			if layerIndex == len(self.biases): #if matrix is biases L
					
					#print(j)

					holder.append(matrix([[self.dC_dbL(layerIndex, j) for j in range(biases.n)]]))
				

			elif layerIndex == len(self.biases) - 1:

					#print(k)

					holder.append(matrix([[self.dC_dbL1(layerIndex, k) for k in range(biases.n)]]))

			elif layerIndex == len(self.biases) - 2:

					#print(i)

					holder.append(matrix([[self.dC_dbL2(layerIndex, i) for i in range(biases.n)]]))

			layerIndex -= 1
			#print("layer: " + str(layerIndex))
		#print("biases done")

		holder.reverse()
		gradient += holder

		return gradient #list of matrixs

			

		#return matrix([[0]])

	def delC(self, subSetLength): #subset is integer size

		delArray = None #array of arrays of matrixs
		gradient = None #output array of matrixes (delArray entrys added up)
		total = 0 #total number of digit strings

		if subSetLength > 0: #a subset of training sets

			total = subSetLength

			for i in range(subSetLength): #get delCKnot for all subSets
	
	
				sys.stdout.write("\r%d" % ((i * 100) / subSetLength)) #print backpropagation progress in flushing manner
				sys.stdout.flush()
	
	
				
				
				randInt = random.randint(0, 9) # 0-9
				randNum = open("numbers/" + str(randInt) + ".txt", "r").readlines()  #all entries from a certain digit file
				randInput = randNum[random.randint(0, len(randNum) - 1)].replace("\n", "") #single line from a digit file
	
				self.input = matrix([[int(i) for i in list(randInput)]])
				self.actual = matrix([], (10, 1), "label", randInt)
	
				''' for debugging: 
	
				doc = open("testData.txt", "r")
				#inp = [int(x) for x in list(i.replace("\n", ""))]
	
				randInput = [int(x) for x in list(doc.readlines()[random.randint(0, 1999)].replace("\n", ""))]
	
				self.input = matrix([randInput])
				self.actual = matrix([randInput[:4]])
				'''
	
				self.clearCache()
	
				setDelCknot = self.delCknot()
	
	
				if gradient == None:
					gradient = setDelCknot
				else:
					for i in range(len(gradient)):
						gradient[i].add(setDelCknot[i])

		elif subSetLength == 0: #all training sets



			for digit in range(10):

				digitFile = open("numbers/" + str(digit) + ".txt", "r")

				progress = 0

				for j in digitFile.readlines(): #j is a single digit in string form

					#print(digit)

					

					sys.stdout.write("\r%d" % progress)
					sys.stdout.flush()

					total += 1

					self.input = matrix([[int(i) for i in list(j.replace("\n", ""))]])
					self.actual = matrix([], (10, 1), "label", digit)

					self.clearCache()

					setDelCknot = self.delCknot()
					

					print(setDelCknot[2])
					input("")
					

					if gradient == None:
						gradient = setDelCknot
					else:
						for i in range(len(gradient)):
							gradient[i].add(setDelCknot[i])

					progress += 1



				digitFile.close()
				print('\n')





		print('\n')

		for i in range(len(gradient)):
			gradient[i] = gradient[i].multiply(1 / total)

		return gradient #list of matrixes



	#	<--	Calculus Helper Functions:	###



	def backPropagate(self, subSetLength = 0): #calculate negative del cost and add to existing weights

		#self.readWeights()
		#self.readBiases()

		gradient = [i.multiply(-1) for i in self.delC(subSetLength)]

		#print(gradient[3])
		#input("grad wait")

		for i in range(len(self.weights)): #add gradient to all weights

			self.weights[i] = self.weights[i].add(gradient[i])


		for i in range(len(self.weights), len(self.weights) + len(self.biases)): #add gradient to all weights

			self.biases[i - len(self.weights)] = self.biases[i - len(self.weights)].add(gradient[i])


		self.writeWeights()
		self.writeBiases()



	###	Quality of life functions -->



	def readWeights(self): #reads weights from saved text

		weightsArray = eval(open("weights.txt", "r").readline())
		self.weights = [None for i in range(len(weightsArray))]

		for i in range(len(weightsArray)):
			self.weights[i] = matrix(weightsArray[i])


	def readBiases(self): #reads biases from saved text

		biasesArray = eval(open("biases.txt", "r").readline())
		self.biases = [None for i in range(len(biasesArray))]

		for i in range(len(biasesArray)):
			self.biases[i] = matrix(biasesArray[i])


	def writeWeights(self): #writes weights to text

		weights = [i.content for i in self.weights] #save new weights
		open("weights.txt", "w").write(str(weights))

	def writeBiases(self): #writes biases to text

		biases = [i.content for i in self.biases] #save new biases
		open("biases.txt", "w").write(str(biases))



	#	<--	Quality of life functions ###

	### Network Accuracy Functions: -->



	def getPrediction(self, inputSet): #finds largest prediction value

		self.input = inputSet


		output = self.getLayer(len(self.weights)).content[0]
		highest = 0 
		highestIndex = 0

		for i in range(len(output) - 1):
			if output[i] > highest:
				highest = output[i]
				highestIndex = i

		return highestIndex


	def accuracy(self): #prints percent of training sets correct

		total = 0
		correct = 0

		for i in range(10):
			for j in open("numbers/" + str(i) + ".txt", "r").readlines():
				if self.getPrediction(matrix([[int(x) for x in list(j.replace("\n", ""))]])) == i:
					correct += 1
				total += 1
			open("numbers/" + str(i) + ".txt", "r").close()

		return str((correct / total) * 100) + "%"

	def getAllPredictions(self): #prints how many of each digit there are and how many correct

		total = [0 for i in range(10)]
		predictions = [0 for i in range(10)]
		finalWeights = matrix([], (10, 1), "const") #[matrix([], (16, 1), "normal")

		for i in range(10):
			for j in open("numbers/" + str(i) + ".txt", "r").readlines():
				total[i] += 1
				predictions[self.getPrediction(matrix([[int(x) for x in list(j.replace("\n", ""))]]))] += 1

				finalWeights = finalWeights.add(self.getLayer(len(self.weights)))

			open("numbers/" + str(i) + ".txt", "r").close()
		return total, predictions, finalWeights.content[0]


	def testNetworkNewDataSet(self): #for debugging
		doc = open("testData.txt", "a")
		for i in range(1000):
			for j in range(8):
				doc.write(str(random.randint(0, 1)))
			doc.write("\n")
		doc.close()

			
	def testNetworkAccuraccy(self): #for debugging

		doc = open("testData.txt", "r")
		correct = 0
		total = 0

		for i in doc.readlines():

			inp = [int(x) for x in list(i.replace("\n", ""))]
			self.input = matrix([inp])

			#print([round(x) for x in self.getLayer(len(self.weights)).content[0]])
			#print(randInput[:4])
		
			#input("")

			if [round(x) for x in self.getLayer(len(self.weights)).content[0]] == inp[:4]:
				correct += 1
			total += 1

		doc.close()

		return correct, total, str((correct / total) * 100) + "%"

	
	#	<-- Network Accuracy Functions: ###



testWeights = [matrix([], (16, 1024), "normal"), matrix([], (16,16), "normal"), matrix([], (10,16), "normal")]
testBiases = [matrix([], (16, 1), "normal"), matrix([], (16,1), "normal"), matrix([], (10,1), "normal")]

'''
testWeights = [matrix([], (8, 8), "normal"), matrix([], (8,8), "normal"), matrix([], (4,8), "normal")]
testBiases = [matrix([], (8, 1), "const"), matrix([], (8,1), "const"), matrix([], (4,1), "const")]
'''
testNetwork = network()  #testWeights, testBiases

#testNetwork.weights = [matrix([], (16, 1024), "randDist"), matrix([], (16,16), "randDist"), matrix([], (10,16), "randDist")]
#testBiases = [matrix([], (16, 1), "randDist"), matrix([], (16,1), "randDist"), matrix([], (10,1), "randDist")]
#
#testNetwork.writeWeights()
#testNetwork.writeBiases()

#testEntry = [int(x) for x in list(open("numbers/7.txt").readlines()[0].replace("\n", ""))]
#print(len(testEntry))
#print(len(lowerRes(testEntry)))

#testNetwork.testNetworkNewDataSet()
#input()

#input("") input("continue") != "n"

'''
while True:
	print(testNetwork.testNetworkAccuraccy())
	
	for i in range(25):
		testNetwork.backPropagate(100)
	
	print(testNetwork.testNetworkAccuraccy())
'''

	#print(testNetwork.weights[0])
	#print(testNetwork.weights[1])
	#print(testNetwork.weights[2])

#print(testNetwork.weights[2])


'''

testNetwork.backPropagate(0)

print(testNetwork.getAllPredictions())
print(testNetwork.accuracy())



input("done")
'''