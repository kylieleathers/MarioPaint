""" Mario Paint Application """

#MCS 260 Spring 2021 Project 5
#Kylie Leathers
#Declaration: I, Kylie Leathers, am the sole author of this code, which was developed in accordance with the rules in the course syllabus


import sys
#if not sys.version_info >= (3, 9, 4):
#	raise Exception("Please run Mario Paint in Python version 3.9.4, required for music to run in Mario Paint")

import pygame
from pygame import *
from datetime import datetime
import random

class Tools:
	def __init__(self,screen,backgroundRect):
		self.radius = 10
		self.circle = Rect(172,736,64,64) #pygame.Rect(left, top, width, height) of a rectangle
		self.screen = screen
		self.drawMario = Rect(376,736,65,61)
		self.backgroundRect = backgroundRect #coordinates of the screen the user can draw on 
		self.sticker_mario = image.load("images/marioSticker.png")
		
		#initiate pygame.mixer for music 
		mixer.init()  
		mixer.music.load('./mario.wav')
		mixer.music.set_volume(0.3)
		#music automatically plays 
		self.musicState = True
		mixer.music.play(loops=-1)
		self.musicRect = Rect(888,739,59,55)

		self.saveRect = Rect(70,738, 64,62)
		
		self.color = (255,0,0)
		#dict of RBG color values and the rectangular points of the color buttons 
		self.colors = {                        
			(255,0,0): Rect(104,32,56,52),
			(255,129,0): Rect(164,32,55,52),
			(255,251,0): Rect(223,31,56,52),
			(0,251,0): Rect(283,32,56,52),
			(0,129,66): Rect(343,32,57,54),
			(0,251,255): Rect(401,32,58,53),
			(0,0,255): Rect(460,30, 59,53),
			(197,65,33): Rect(520,32,58,51),
			(132,97,0): Rect(581,30,56,54),
			(255,194,132): Rect(642,32,54,49),
			(197,0, 197): Rect(700,32,57,49),
			(0,0,0): Rect(757,29,60,55),
			(132,129,132): Rect(819,28,57,56),
			(197,194,197): Rect(880,26,55,59),
			(255,251,255): Rect(939,28,58,57)
		}

		self.currentTool = self.drawBrush_S
		#dict of tool functions and the rectangular points of their buttons 
		self.tools = {                             
			self.drawBrush_S: Rect(172,736,64,62),
			self.drawBrush_M: Rect(241,736,63,62),
			self.drawBrush_L: Rect(309,735,63,64),
			self.drawSticker: Rect(377,737,63,62),
			self.drawSprayCan: Rect(445,735,63,63),
			self.drawCircle: Rect(547,736,64,62),
			self.fillTool: Rect(648,735,64,63),
			self.clearTool: Rect(787,735,60,62),
			self.eraserTool : Rect(716,737,64,60),
		}
		#for spray tool, outer radius is the radius of the final circle shape
		self.sprayRadius_outer = 30
		#inner radius is the radius of each indivual circle  
		self.sprayRadius_inner = 1

	#change the color when user clicks on color button      
	def colorHandler(self,mousePos):
		if not self.backgroundRect.collidepoint(mousePos): 
			 #iterates through the dict to update self.color
			for color,rect in self.colors.items():
				#if the user clicks on one of the rect points from the dict, update color
				if rect.collidepoint(mousePos):
					self.color = color
					break
	
	 #change the tool when user clicks on tool button
	def toolHandler(self,mousePos):                          
		if not self.backgroundRect.collidepoint(mousePos):
			 #iterates through dict to update self.currentTool
			for toolFunc,rect in self.tools.items():  
				#if user clicks on a tool from the tool dict, update tool       
				if rect.collidepoint(mousePos):
					self.currentTool = toolFunc
					break

	#pause/unpause music when user clicks music button
	def musicHandler(self,mousePos):                          
		if self.musicRect.collidepoint(mousePos):
			#keep track of pause/unpause by changing state - pause = False, unpause = True
			if self.musicState:
				mixer.music.pause()
				self.musicState = False
			else:
				mixer.music.unpause()
				self.musicState = True
	
	#tool for saving image in .jpeg or .png
	def saveHandler(self,mousePos): 
		if self.saveRect.collidepoint(mousePos):
			#use datetime to save date and time with the image so it doesn't override last image
			pygame.image.save_extended(self.screen, "MarioPaint_{}.png".format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")))

	#single use function for tools that we dont want to keep iterating
	def singleUse(self):                                      
		if self.currentTool.__name__ in ['fillTool']:  #fill tool is only executed once when this is true
			return True
		else:
			return False
	
	#---------------------------------------------------------------------------
	def drawBrush_S(self,mousePos):
		draw.circle(self.screen, self.color, mousePos, 5)
	
	def drawBrush_M(self,mousePos):
		draw.circle(self.screen, self.color, mousePos, 10)
	
	def drawBrush_L(self,mousePos):
		draw.circle(self.screen, self.color, mousePos, 15)
	
	def drawSticker(self, mousePos):
		mario = transform.scale(self.sticker_mario,(70,70))
		#draws the image onto the screen, -35 points away from the where the user is clicking 
		self.screen.blit(mario,(mousePos[0]-35,mousePos[1]-35))
	
	def drawSprayCan(self, mousePos):
		mx,my = mousePos
		for i in range(10):
			#second (x,y) point is a random point between the mouse position and the outer radius 
			randX = mx + random.uniform(-self.sprayRadius_outer,self.sprayRadius_outer)
			randY = my + random.uniform(-self.sprayRadius_outer,self.sprayRadius_outer)
			#use distance formula to find difference between mouse position and Randx + RandY to limit rand ints to circle shape 
			while (((mx-randX)**2) + (my-randY)**2)**0.5 > self.sprayRadius_outer:
				#while distance is less than the legnth of the radius, continue drawing random points
				randX = mx + random.uniform(-self.sprayRadius_outer,self.sprayRadius_outer)
				randY = my + random.uniform(-self.sprayRadius_outer,self.sprayRadius_outer)

			draw.circle(self.screen, self.color, (randX,randY), self.sprayRadius_inner)   

	def eraserTool(self, mousePos):
		draw.circle(self.screen, (255,255,255), mousePos, 15)

	def clearTool(self,*args):
		pygame.Surface.fill(self.screen, (255,255,255))

	def drawCircle(self, mousePos):
		draw.circle(self.screen, self.color, mousePos, 20, width =3)

	def fillTool(self, mousePos):
		if self.backgroundRect.collidepoint(mousePos):
			 #make color mapped int value
			fill_color = self.screen.map_rgb(self.color) 
			#reference pixels in 2d array
			surf_array = pygame.surfarray.pixels2d(self.screen)  
			refColor = surf_array[mousePos]  
			 #list of pixels not checked
			pixels = [mousePos]
			while len(pixels) > 0:
				px, py = pixels.pop()
				try:  
					#if pixel color != same color as previous pixel color, paint it
					if surf_array[px, py] != refColor:  
						continue
				except IndexError:
					continue
				surf_array[px, py] = fill_color
				#recursively check left, right, up and down pixels from previous pixel pos 
				pixels.append((px + 1, py))  
				pixels.append((px - 1, py))  
				pixels.append((px, py + 1))  
				pixels.append((px, py - 1))  

			surfarray.blit_array(self.screen, surf_array)


def main():
	screen = display.set_mode((1094,817))
	background = image.load('./images/marioUI.png')
	bg_barsReset = image.load('./images/marioUI_bars.png')
	screen.blit(background,(0,0))
	backgroundRect = Rect(19,98,1056,612)
	colorBarRect = Rect(172,736,541,64)
		
	running = True
	tool = Tools(screen,backgroundRect)
	while running:  
		mb = mouse.get_pressed()
		mousePos = mouse.get_pos()
		for e in event.get():
			if e.type == QUIT:
				running = False
			if e.type == MOUSEBUTTONDOWN:
				#when mouse is clicked, initate music and saveTool function
				tool.musicHandler(mousePos)
				tool.saveHandler(mousePos)
				if tool.singleUse():
					tool.currentTool(mousePos)
			if e.type == MOUSEBUTTONUP:   
				#after mouse is clicked, initiate color and tool function 
				tool.colorHandler(mousePos)
				tool.toolHandler(mousePos)
			if e.type == KEYDOWN:
				#left and right arrow increase/decrease radius
				if e.key == K_LEFT:
					tool.radius -= 1
				if e.key == K_RIGHT:
					tool.radius += 1

		#if mouse button is clicked on screen, go through tool functions 
		if mb[0]==1 and backgroundRect.collidepoint(mousePos):
			if not tool.singleUse():
				tool.currentTool(mousePos)
				
		#draw rectangle to indicate current color on UI bar
		draw.rect(screen,tool.color,colorBarRect)
		screen.blit(bg_barsReset,(0,0))
		display.flip()

if __name__ == '__main__':
	main()

