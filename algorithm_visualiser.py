# sorting algorithm visualiser, like the ones you see on youtube
# TODO add sound effects
# TODO highlight blocks at indexes being read/written to
# TODO add lots of different algorithms

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time

from pygame.locals import (
    KEYDOWN,
    QUIT,
    K_b,
    K_i,
    K_r,
    K_q,
    K_ESCAPE,
)

name = "Algorithm Visualiser"
screen_width = 1200
screen_height = 600
running = True
operations = 0
status = "Idle"
automate = False

pygame.init()
pygame.font.init()
pygame.display.set_caption(name + " - " + status + " - " + str(operations) + " Operations")

font = pygame.font.SysFont("Monospace", 16)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

debug = False
block_width = 10
block_height = 1 # TODO implement block height variable
delay = 0
fps = 30

# get command line arguments
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--debug":
        debug = True
        print("Debug mode enabled")
    elif sys.argv[i] == "--automate":
        automate = True
        print("Automate mode enabled")
    elif sys.argv[i].__contains__("-w"):
        try:
            block_width = int(sys.argv[i].strip("-w")) + 1  # we dont want to set to zero
            if (debug):
                print("Block width: " + str(block_width))
        except:
            pass
    elif sys.argv[i].__contains__("-h"):
        try:
            block_height = int(sys.argv[i].strip("-h")) + 1
            if (debug):
                print("Block height: " + str(block_height))
        except:
            pass
    elif sys.argv[i].__contains__("-fps"):
        try:
            fps = int(sys.argv[i].strip("-fps"))
            if (debug):
                print("FPS: " + str(fps))
        except:
            pass

class Block(pygame.sprite.Sprite):  # block object used for rendering
    def __init__(self, pos, size):
        super(Block, self).__init__()
        self.pos = pos
        self.size = size
        
        self.surf = pygame.Surface((block_width, size * block_height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = ((pos + 1) * block_width, (screen_height) - (size * block_height)))

def render(list):
    screen.fill((30, 30, 30))   # background
    positions = [0] # positions to render blocks at (so they dont overlap)
    
    for i in range(1, len(list)):
        positions.append(i * (block_width + 5)) # blocks are 30px wide and we want a 5px gap between each of them
    
    k = 1
    for item in list:
        block = Block(k, item)
        r = pygame.Rect.copy(block.rect)
        r.update(positions[k - 1], block.rect.center[1], block_height * item, block.rect.height)
        screen.blit(block.surf, r)  # actual render
        k += 1
    
    pygame.display.set_caption(name + " - " + status + " - " + str(operations) + " operations")
    
    text = font.render("Operations: " + str(operations), False, (255, 255, 255))
    screen.blit(text, (1, 0))   # render operations counter
    text = font.render("Status: " + status, False, (255, 255, 255))
    screen.blit(text, (1, text.get_height()))   # render status
    
    pygame.display.flip()   # show frame on screen

def randomise():
    global status
    status = "Randomising"
    global operations   # access and set global operations variable to 0
    operations = 0
    
    temp = []
    for i in range(screen_width // (block_width + 5)):
        render(temp)
        temp.append(random.randint(1, screen_height // block_height))
    status = "Idle"
    return temp

def bubbleSort(list):
    global status
    status = "Bubble Sort"
    for i in range(len(list)- 1):
        swapped = False
        for j in range(len(list) - 1):
            if list[j] > list[j + 1]:
                temp = list[j]
                # render, increment operations, print if debug
                render(list)
                time.sleep(delay)
                global operations
                operations += 1
                if (debug): print(list)
                #
                list[j] = list[j + 1]
                list[j + 1] = temp
                swapped = True
        if (swapped == False):
            break
    return list

def insertionSort(list):
    global status
    status = "Insertion Sort"
    pos = 0
    valueToInsert = 0
    for i in range(len(list)):
        valueToInsert = list[i]
        pos = i
        while pos > 0 and list[pos - 1] > valueToInsert:
            # render, increment operations, print if debug
            render(list)
            time.sleep(delay)
            global operations
            operations += 1
            if (debug): print(list)
            #
            list[pos] = list[pos - 1]
            pos = pos - 1
        list[pos] = valueToInsert
    return list



list = randomise()
while running:
    clock = pygame.time.Clock()
    clock.tick(fps)
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    render(list)
    
    if (automate):
        # automate
        time.sleep(1)
        list = randomise()
        time.sleep(1)
        list = bubbleSort(list)
        time.sleep(1)
        list = randomise()
        time.sleep(1)
        list = insertionSort(list)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                pygame.quit()
            elif event.key == K_b:
                list = bubbleSort(list)
            elif event.key == K_i:
                list = insertionSort(list)
            elif event.key == K_r:
                list = randomise()
pygame.quit()
