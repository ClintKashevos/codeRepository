import math
import random
import pygame
import sys
pygame.init()

xSound = '/Users/ckashevos/Documents/Automation/beautifulConnect4/boop.mp3'
trumpet = '/Users/ckashevos/Documents/Automation/BeautifulConnect4/trumpet.mp3'
#xSound = 'C:/Users/ckashevos/Documents/Automation/New folder/boop.mp3'
#trumpet = 'C:/Users/ckashevos/Documents/Automation/New folder/trumpet.mp3'
pygame.mixer.init()



def getScreenWidth():
	return 900

def getScreenHeight():
	return 600

class Game:
	def __init__ (self, pygame, screen):
		self.PlayerOneScore = 0
		self.PlayerTwoScore = 0

		self.playerOne = Rectangle(0, 0, 50, 100, 0)
		self.playerTwo = Rectangle(getScreenWidth() - 50, getScreenHeight() - 100, 50, 100, 0)
		self.ball = Circle(300, 300, 10)
		self.pygame = pygame
		self.screen = screen

	def isGameOver(self):
		winner = self.PlayerOneScore >= 10 or self.PlayerTwoScore >= 10
		if winner:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.queue(trumpet)
			else:
				pygame.mixer.music.load(trumpet)
				pygame.mixer.music.play()
		return winner


	def oneUp(self):
		self.playerOne.moveUp()
	def oneDown(self):
		self.playerOne.moveDown()
	def twoUp(self):
		self.playerTwo.moveUp()
	def twoDown(self):
		self.playerTwo.moveDown()

	def draw(self):
		self.playerOne.drawSomething(self.pygame, self.screen)
		self.playerTwo.drawSomething(self.pygame, self.screen)
		wasTouchingVerticalP1 = isCollidingVertical(self.pygame, self.screen, self.ball, self.playerOne)
		wasTouchingHorizontalP1 = isCollidingHorizontal(self.pygame, self.screen, self.ball, self.playerOne)
		wasTouchingVerticalP2 = isCollidingVertical(self.pygame, self.screen, self.ball, self.playerTwo)
		wasTouchingHorizontalP2 = isCollidingHorizontal(self.pygame, self.screen, self.ball, self.playerTwo)
		self.ball.updateBall(self, self.pygame, self.screen)
		isBallCollidingWithRectangle(self.pygame, self.screen, self.ball, self.playerOne, wasTouchingHorizontalP1, wasTouchingVerticalP1)
		isBallCollidingWithRectangle(self.pygame, self.screen, self.ball, self.playerTwo, wasTouchingHorizontalP2, wasTouchingVerticalP2)
		self.ball.drawBall(self.screen)

	def playerOneScored(self):
		self.PlayerOneScore += 1
		print ('Player One: ' + str(self.PlayerOneScore))
		if self.PlayerOneScore >= 10:
			print ('Clint is master of the known universe')

	def playerTwoScored(self):
		self.PlayerTwoScore += 1
		print ('Player Two: ' + str(self.PlayerTwoScore))
		if self.PlayerTwoScore >= 10:
			print ('Joshua is master of the known universe')


class Point:
	def __init__ (self, xRec, yRec):
		self.x = xRec
		self.y = yRec

class Rectangle:
	def __init__ (self, xRec, yRec, wRec, hRec, thickness):
		self.center = Point(xRec, yRec)
		self.wRec = wRec
		self.hRec = hRec
		self.thickness = thickness
		self.updateColor()

	def updateColor(self):
		x = random.randint(0, 255)
		y = random.randint(0, 255)
		z = random.randint(0, 255)
		self.color = (x, y, z)

	def drawSomething(self, pygame, screen):
		pygame.draw.rect(screen, self.color, (self.center.x, self.center.y, self.wRec, self.hRec), 0)

	def moveUp(self):
		self.center.y -= 20
	def moveDown(self):
		self.center.y += 20

class Circle:
	def __init__ (self, xCenter, yCenter, radius):
		self.center = Point(xCenter, yCenter)
		self.radius = radius
		self.deltaX = 11
		self.deltaY = 8
		self.updateColor()

	def updateColor(self):
		x = random.randint(0, 255)
		y = random.randint(0, 255)
		z = random.randint(0, 255)
		self.color = (x, y, z)

	def changeXDirection(self):
		self.deltaX *= -1
	def changeYDirection(self):
		self.deltaY *= -1

	def collide(self, collidedFront):
		if collidedFront == True:
			self.changeXDirection()
		else:
			self.changeYDirection()

		if pygame.mixer.music.get_busy():
			pygame.mixer.music.queue(xSound)
		else:
			pygame.mixer.music.load(xSound)
			pygame.mixer.music.play()

	def updateBall(self, game, pygame, screen):
		self.center.x += self.deltaX
		self.center.y += self.deltaY
		if self.center.x >= getScreenWidth() - self.radius:
			# went off right side
			game.playerOneScored()
			self.center.x = getScreenWidth() // 2
			self.center.y = getScreenHeight() // 2
		if self.center.x <= 0 + self.radius:
			# went off left side
			game.playerTwoScored()
			self.center.x = getScreenWidth() // 2
			self.center.y = getScreenHeight() // 2
		elif self.center.y >= getScreenHeight() - self.radius:
			self.changeYDirection()
		elif self.center.y <= 0 + self.radius:
			self.changeYDirection()

	def drawBall(self, screen):
		pygame.draw.circle(screen, self.color, (self.center.x, self.center.y), self.radius, 0)


def isVerticalLineInRectangle(line, rectangle):
	if line > rectangle.center.x and line < rectangle.center.x + rectangle.wRec:
		return True
	else:
		return False

def isHorizontalLineInRectangle(line, rectangle):
	if line > rectangle.center.y and line < rectangle.center.y + rectangle .hRec:
		return True
	else:
		return False

def isCollidingHorizontal(pygame, screen, circle, rectangle):
	topLine = circle.center.y - circle.radius
	bottomLine = circle.center.y + circle.radius
	return isHorizontalLineInRectangle(topLine, rectangle) or isHorizontalLineInRectangle(bottomLine, rectangle)

def isCollidingVertical(pygame, screen, circle, rectangle):
	leftLine = circle.center.x - circle.radius
	rightLine = circle.center.x + circle.radius
	return isVerticalLineInRectangle(leftLine, rectangle) or isVerticalLineInRectangle(rightLine, rectangle)

def isBallCollidingWithRectangle(pygame, screen, circle, rectangle, wasCollidingHorizontal, wasCollidingVertical):
	# leftLine = circle.center.x - circle.radius
	# rightLine = circle.center.x + circle.radius
	# topLine = circle.center.y - circle.radius
	# bottomLine = circle.center.y + circle.radius
	horizontal = isCollidingHorizontal(pygame, screen, circle, rectangle)
	vertical = isCollidingVertical(pygame, screen, circle, rectangle)
	if vertical and horizontal == True:
		circle.collide(wasCollidingHorizontal)

	# pygame.draw.line(screen, (255,255,0), (0,topLine), (getScreenWidth(), topLine))
	# pygame.draw.line(screen, (0,255,255), (0,bottomLine), (getScreenWidth(), bottomLine))
	# pygame.draw.line(screen, (255,0, 255), (leftLine ,0), (leftLine, getScreenHeight()))
	# pygame.draw.line(screen, (255,0, 255), (rightLine ,0), (rightLine, getScreenHeight()))


clock = pygame.time.Clock()
size = (getScreenWidth(), getScreenHeight())
screen = pygame.display.set_mode(size)
pygame.display.set_caption('I am PONG!')
pong = Game(pygame, screen)


carryOn = True
while carryOn:
	screen.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			carryOn = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				carryOn = False
				break

	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		pong.oneUp()
	if keys[pygame.K_s]:
	 	pong.oneDown()
	if keys[pygame.K_i]:
		pong.twoUp()
	if keys[pygame.K_k]:
		pong.twoDown()

	pong.draw()
	if (pong.isGameOver()):
		pong = Game(pygame, screen)

	pygame.display.update()
	clock.tick(90)
