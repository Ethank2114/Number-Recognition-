##Hilbert Curve
##Ethan Kerr

import tabulate

class hilbert:
	#array: list
	def printArray(self, array):
		'''
		for i in range(len(array[0])):
			out = ""
			for j in range(len(array)):
				out += str(array[j][i]) + " "
			print(out)'''

		print(tabulate.tabulate(array))
	
	#array: square array
	def mirror(self, array, xyAxis = True):
		out = []
	
		if xyAxis:
	
			for i in range(len(array)):
				aout = []
				for j in range(len(array) - 1, -1, -1):
					aout.append(array[j][i])
				out.append(aout)
			out.reverse()
		else:
			for i in range(len(array)):
				aout = []
				for j in range(len(array)):
					aout.append(array[j][i])
				out.append(aout)
	
		return out
	
	#array1 on left
	def combineHorizontal(self, array1, array2):
		return array1 + array2
	
	#array1 on top
	def combineVertical(self, array1, array2):
		outArray = []
		for i in range(len(array1)):
			outArray.append(array1[i] + array2[i])
		return outArray
	
	def arrayMultiply(self, temp, num):
		outArray = temp
		for i in range(len(outArray)):
			for j in range(len(outArray)):
				outArray[i][j] += num
	
		return outArray
	
	def scaleUp(self,array):
		length = len(array)
		#q2 q3
		#q1 q4
	
		q1 = self.mirror(array)
		q2 = array
		q3 = array
		q4 = self.mirror(array, False)
	
		return self.combineHorizontal(self.combineVertical(self.arrayMultiply(q2, length**2), q1), self.combineVertical(self.arrayMultiply(q3, length**2), self.arrayMultiply(q4, 3*length**2)))
	
	def getGrid(self, level):
		out = [[1]]
		for i in range(level):
			out = self.scaleUp(out)
		return out

hilbert().printArray(hilbert().getGrid(2))

print("1  2   3  4")
print("8  7   6  5")
print("9  10 11 12")
print("16 15 14 13")