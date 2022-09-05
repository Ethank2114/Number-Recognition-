##Network Input
##Ethan Kerr

import pygame, sys
from HilbertCurve import hilbert

number = int(input("Number to be drawn: (0-9) "))

pygame.init()

res = 5
curve = hilbert().getGrid(res)

class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.display = pygame.display.set_mode((width, height + 64))
		self.contents = []

		self.clearContents()

	def clearContents(self):
		self.contents = ([[0 for j in range(2**res)] for i in range(2**res)])

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


window = window(512, 512)
pygame.display.set_caption('Draw a: ' + str(number)) 

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
				window.writeImage()
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

doneButton = font.render('Done', True, colors.black)
doneButtonRect = doneButton.get_rect()
doneButtonRect.center = ((window.width / 4) * 3, window.height + 32) 


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

	

	window.display.blit(clearButton, clearButtonRect) 
	window.display.blit(doneButton, doneButtonRect)

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
				window.writeImage()
				window.clearContents()

			for i in range(10):
				if event.key == eval("pygame.K_" + str(i)):
					number = i
					pygame.display.set_caption('Draw a: ' + str(number)) 

	pygame.display.update()