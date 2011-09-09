#!/usr/bin/env python

#Created By Kris Occhipinti
#Wed Aug 24, 2011
#http://FilmsByKris.com
# Project Link: http://filmsbykris.com/wordpress/?p=1099
# GPLv3


import pygame, sys, random
from pygame import *

pygame.mixer.init()

w = 800
h = 400

screen = pygame.display.set_mode((w,h))

#Load Background Image
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg,(w,h))

class Bottle:
    def __init__(self):
        self.width = 200
        self.height = 200
        self.image = pygame.image.load("bottle.png")
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.x = 200
        self.y = 100
#        self.active = 0
        self.speedx = 0
        self.speedy = 0
        self.tork = 0
        self.speedt = 0
        # Create a rect from the loaded image. --Kevin
        self.rect = self.image.get_rect()
        #Load Glass Sound
        self.sound1 = pygame.mixer.Sound("glass.wav") 

    def click(self,x,y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
 #               self.active = random.randint(0, 360)
                #play sound when clicked
                self.sound1.play()
                self.tork = 6000
                self.speedt = random.randint(25, 75)
                self.speedx = 10
                self.speedy = 10
      
    def update(self):
        # Here we're going to prevent the bottle from getting stuck on the edges of the screen. --Kevin
        if self.x < 0:
            self.speedx = -self.speedx
            self.x = 1
        elif self.x + self.width > w:
            self.speedx = -self.speedx
            self.x = w - self.width - 1

        if self.y < 0:
            self.speedy = -self.speedy
            self.y = 1
        elif self.y + self.width > h:
            self.speedy = -self.speedy
            self.y = h - self.width - 1

        self.x+=self.speedx
        self.y+=self.speedy
        
        # Set the rect's position to the object's x and y positon. --Kevin
        self.rect.left, self.rect.top = self.x, self.y

        if self.speedx > 0:
            self.speedx-=.025
        elif self.speedx < 0:
            self.speedx+=.025
                
        if self.speedy > 0:
            self.speedy-=.025
        elif self.speedy < 0:
            self.speedy+=.025
            
        # These lines stop the bottle from sliding by setting the speed to zero if the bottle's speed is almost zero. --Kevin
        if (self.speedx > 0 and self.speedx < 0.5) or (self.speedx < 0 and self.speedx > -0.5):
            self.speedx = 0
        if (self.speedy > 0 and self.speedy < 0.5) or (self.speedy < 0 and self.speedy > -0.5):
            self.speedy = 0

        #print self.speedx, self.speedy


        if self.speedt > 0:
            self.tork-=self.speedt
            self.speedt-=.1
           
        print self.tork 
        self.image2 = pygame.transform.rotate(self.image,self.tork)
        
        # Create a new rect from the rotated image. --Kevin
        self.rect2 = self.image2.get_rect()
        
        # Set the center of the rotated image's rect to be in the same position as the center of the un-rotated image's rect. 
        # This fixes the strange rotation. --Kevin
        self.rect2.center = self.rect.center

        # Now draw the image, using the rotated image's rect as the position. --Kevin
        screen.blit(self.image2, self.rect2)
        
class Music:
    def __init__(self, music):
        self.unmute = pygame.image.load("unmute.png")
        self.mute = pygame.image.load("mute.png")
        self.image = self.unmute
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.playing = True
        self.music = pygame.mixer.Sound(music)
        self.music.play(loops=-1)
        self.x = 0
        self.y = h - self.height
        
    def click(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                if self.playing:
                    self.image = self.mute
                    self.playing = False
                    #self.music.pause()
                    pygame.mixer.pause()
                else:
                    self.image = self.unmute
                    self.playing = True
                    pygame.mixer.unpause()
                

clock = pygame.time.Clock()
bottle = Bottle()
music = Music("music.ogg")

while 1:
    x,y = pygame.mouse.get_pos()

    screen.blit(bg,(0,0))
    clock.tick(60)
    bottle.update()
    screen.blit(music.image, (music.x, music.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            bottle.click(x, y)
            music.click(x, y)

    pygame.display.update()    

