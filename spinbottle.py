#!/usr/bin/env python

#Created By Kris Occhipinti
#Wed Aug 24, 2011
#http://FilmsByKris.com
# Project Link: http://filmsbykris.com/wordpress/?p=1099
# GPLv3


import pygame, sys, random
from pygame import *

w = 800
h = 400

screen = pygame.display.set_mode((w,h))

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

    def click(self,x,y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
 #               self.active = random.randint(0, 360)
                self.tork = 6000
                self.speedt = random.randint(25, 75)
                self.speedx = 10
                self.speedy = 10
      
    def update(self):
        if self.x < 0 or self.x + self.width > w:
            self.speedx = -self.speedx

        if self.y < 0 or self.y + self.width > h:
            self.speedy = -self.speedy

        self.x+=self.speedx
        self.y+=self.speedy

        if self.speedx > 0:
            self.speedx-=.05
        if self.speedy > 0:
            self.speedy-=.05

        #print self.speedx, self.speedy


        if self.speedt > 0:
            self.tork-=self.speedt
            self.speedt-=.1
           
        print self.tork 
        self.image2 = pygame.transform.rotate(self.image,self.tork)

        screen.blit(self.image2,(self.x,self.y))
                

clock = pygame.time.Clock()
bottle = Bottle()

while 1:
    x,y = pygame.mouse.get_pos()

    screen.fill((250,250,250))
    clock.tick(60)
    bottle.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            bottle.click(x,y)

    pygame.display.update()    
