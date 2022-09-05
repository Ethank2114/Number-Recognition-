##Digit Recognition Ui
##Ethan Kerr

import pygame, sys

from Network import network
from Network import matrix
#from HilbertCurve import hilbert

pygame.init()

res = 5

class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.display = pygame.display.set_mode((width, height + 128))
		self.contents = []
		self.prediction = None

		self.clearContents()

	def clearContents(self):
		self.contents = ([[0 for j in range(2**res)] for i in range(2**res)])

	def submit(self):

		self.prediction = network().getPrediction(matrix(self.contents))

	'''
	def writeImage(self):
		out = [0 for i in range((2**res)**2)]

		for i in range(2**res):
			for j in range(2**res):
				out[curve[i][j] - 1] = self.contents[i][j]

		outStr = ""
		for i in out:
			outStr += str(i)

		open("numbers/" + str(number) + ".txt", "a").write(outStr + "\n")
		open("numbers/" + str(number) + ".txt", "a").close()
	'''


window = window(512, 512)
pygame.display.set_caption("Number Recognition") 

class colors:
	def __init__(self):
		self.white = (255, 255, 255)
		self.grey = (166, 173, 173)
		self.black = (0, 0, 0)
		self.green = (50, 168, 58)
		self.blue = (44, 207, 222)

colors = colors()

class mouse:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		self.down = False

	def click(self, xy):
		self.x, self.y = xy
		 

		if self.x > window.width / 2 and self.y > window.height - 64:
			hasStuff = False
			for i in window.contents:
				for j in i:
					if j == 1:
						hasStuff = True
						break
			if hasStuff:
				window.submit()
				window.clearContents()

		elif self.x < window.width / 2 and self.y > window.height - 64:
			window.clearContents()

		else:
			window.contents[self.x // (window.width // 2**res)][self.y // (window.height // 2**res)] = 1


pointer = mouse()



font = pygame.font.Font('freesansbold.ttf', 32) 

clearButton = font.render('Clear', True, colors.black)
clearButtonRect = clearButton.get_rect()
clearButtonRect.center = (window.width / 4, window.height + 32) 

doneButton = font.render('Submit', True, colors.black)
doneButtonRect = doneButton.get_rect()
doneButtonRect.center = ((window.width / 4) * 3, window.height + 32) 

preDict = font.render('Prediction:', True, colors.black)
preDictRect = preDict.get_rect()
preDictRect.center = ((window.width / 4), window.height + 96) 


while True:

	window.display.fill(colors.white)

	if pointer.down:
		pointer.click(pygame.mouse.get_pos())

	for i in range(2**res):
		for j in range(2**res):
			if window.contents[i][j] == 1:
				pygame.draw.rect(window.display, colors.grey, (i * window.width / (2**res), j * window.height / (2**res), window.width / (2**res), window.height / (2**res)))
			

	for i in range(2**res + 1): #draw horizontal lines
		pygame.draw.line(window.display, colors.black, (i * window.width / (2**res), 0), (i * window.width / (2**res), window.height))

	for i in range(2**res + 1): #draw vertical lines
		pygame.draw.line(window.display, colors.black, (0, i * window.height / (2**res)), (window.width, i * window.height / (2**res)))

	pygame.draw.line(window.display, colors.black, (window.width / 2, window.height), (window.width / 2, window.height + 64))
	pygame.draw.line(window.display, colors.black, (0, window.height + 64), (window.width, window.height + 64))

	

	preDictTxt = font.render(str(window.prediction), True, colors.black)
	preDictTxtRect = preDictTxt.get_rect()
	preDictTxtRect.center = ((window.width / 4) * 3, window.height + 96) 


	window.display.blit(clearButton, clearButtonRect) 
	window.display.blit(doneButton, doneButtonRect)
	window.display.blit(preDict, preDictRect)
	window.display.blit(preDictTxt, preDictTxtRect)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			break

		if event.type == pygame.MOUSEBUTTONDOWN:
			pointer.down = True

		if event.type == pygame.MOUSEBUTTONUP:
			pointer.down = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				window.submit()
				window.clearContents()

	pygame.display.update()