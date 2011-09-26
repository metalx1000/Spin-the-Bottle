#!/usr/bin/env python

#Created By Kris Occhipinti
#Wed Aug 24, 2011
#http://FilmsByKris.com
# Project Link: http://filmsbykris.com/wordpress/?p=1099
# GPLv3


import pygame, sys, random
from pygame import *

# Calling mixer.pre_init() fixes the lag in playing sound that sometimes occurs.
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

w = 800
h = 400

screen = pygame.display.set_mode((w,h))

#Load Background Image
bg = pygame.image.load("stone-bg.png")
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
        # Create a rect from the loaded image.
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
        # Here we're going to prevent the bottle from getting stuck on the edges of the screen. 
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
        
        # Set the rect's position to the object's x and y positon. 
        self.rect.left, self.rect.top = self.x, self.y

        if self.speedx > 0:
            self.speedx-=.025
        elif self.speedx < 0:
            self.speedx+=.025
                
        if self.speedy > 0:
            self.speedy-=.025
        elif self.speedy < 0:
            self.speedy+=.025
            
        # These lines stop the bottle from sliding by setting the speed to zero if the bottle's speed is almost zero.
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
        
        # Create a new rect from the rotated image.
        self.rect2 = self.image2.get_rect()
        
        # Set the center of the rotated image's rect to be in the same position as the center of the un-rotated image's rect. 
        # This fixes the strange rotation. 
        self.rect2.center = self.rect.center
        
        # Make sure we can still see the bottle even if the options tab is open.
        if tab.expanded and self.x < tab.x:
            self.x += 10

        # Now draw the image, using the rotated image's rect as the position.
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
        self.x = 0 - self.width
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
                
    def update(self, x):
        self.x = x - 300
        screen.blit(self.image, (self.x, self.y))
        
class Background:
    """A class to change the background image."""
    def __init__(self, image, x, y):
        self.bg = pygame.image.load(image)
        self.image = pygame.transform.scale(self.bg, (100, 50))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = [x, y]
        self.x = x
        self.y = y
        
    def click(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                global bg
                bg = pygame.transform.scale(self.bg, (w, h))
                
    def update(self, x):
        self.x = x + (self.pos[0] - 300)
        screen.blit(self.image, (self.x, self.y))
                
class OptionTab:
    """A small tab that expands to show extra options."""
    
    def __init__(self):
        self.icon = pygame.image.load("tab.png")
        self.image = self.icon
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 0
        self.y  = h - self.height
        self.expanded = False
        
        # Options.
        self.music = Music("music.ogg")
        self.red_bg = Background("redwood-bg.png", 5, 5)
        self.stone_bg = Background("stone-bg.png", 110, 5)
        
        self.options = {"music":self.music, "red bg":self.red_bg, "stone bg":self.stone_bg}
        
    def click(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                if not self.expanded:
                    self.expanded = True
                else:
                    self.expanded = False
                   
        if self.expanded:
            for thing in self.options:
                self.options[thing].click(x, y)
                    
    def update(self):
        if self.expanded:
            self.image = pygame.transform.flip(self.icon, 1, 0)
            
            if self.x < 300:
                self.x += 10
                
        else:
            self.image = self.icon
            
            if self.x > 0:
                self.x -= 10
        
        pygame.draw.rect(screen, (86, 152, 119), (0, 0, self.x, h))
        screen.blit(self.music.image, (self.music.x, self.music.y))
        for thing in self.options.keys():
            self.options[thing].update(self.x)
        screen.blit(self.image, (self.x, self.y))

clock = pygame.time.Clock()
bottle = Bottle()
#music = Music("music.ogg")
tab = OptionTab()

while 1:
    x,y = pygame.mouse.get_pos()

    screen.blit(bg,(0,0))
    clock.tick(60)
    bottle.update()
    tab.update()
#    screen.blit(music.image, (music.x, music.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            tab.click(x, y)
            # Make sure that the options tab isn't open before checking to see if the user clicked the bottle.
            if not tab.expanded:
                bottle.click(x, y)
#            music.click(x, y)

    pygame.display.update()    

