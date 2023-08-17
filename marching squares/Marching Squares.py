import pygame
from pygame.locals import *
from perlin_noise import PerlinNoise as pn
import matplotlib.pyplot as plt
pygame.init()

noise = pn(octaves=10, seed=1104)
dim = (100,100)
tilesize = 6
pic = [[noise([i/dim[0],j/dim[1]])for j in range(dim[1])]for i in range(dim[0])]
threshold = 0

win = pygame.Surface((dim[0]*tilesize,dim[1]*tilesize))
WIN = pygame.display.set_mode((800,800))
pygame.display.set_caption("Marching Squares")

img = []
for i in range(16):
    img.append(pygame.transform.scale(pygame.image.load("./sprites/"+str(i+1)+".png"),(tilesize,tilesize)))
def get_dec(binary):
    power = 0
    dec = 0
    for i in binary[-1::-1]:
        dec += int(i)*2**power
        power += 1
    return dec
def tile(x,y):
    if pic[y][x] > threshold:
        return 1
    else:
        return 0

def redraw():
    global do_show
    win.fill((0,0,0))

    for y in range(0,dim[1]+1):
        for x in range(0,dim[0]+1):
            if x>0 and x<dim[0] and y>0 and y<dim[1]:
                a,b,c,d = tile(x-1,y-1),tile(x,y-1),tile(x,y),tile(x-1,y)
                imgno = get_dec(str(d)+str(c)+str(b)+str(a))
                win.blit(img[imgno],(x*tilesize-tilesize//2,y*tilesize-tilesize//2))
    if show_grid:
        for y in range(dim[1]):
            pygame.draw.line(win, (255,255,255), (0,y*tilesize),(dim[0]*tilesize,y*tilesize))
        for x in range(dim[0]):
            pygame.draw.line(win, (255,255,255), (x*tilesize,0),(x*tilesize,dim[1]*tilesize))    

    pygame.transform.scale(win,(800,800))
    WIN.blit(win,(0,0))

    pygame.display.update()

show_grid = False

run = True
while run:

    mpos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_o:
                threshold -= 0.05
            if event.key == K_p:
                threshold += 0.05
            if event.key == K_l:
                show_grid = not show_grid

        if event.type == MOUSEBUTTONDOWN:
            mtile = (mpos[0]//tilesize,mpos[1]//tilesize)
            if event.button == 1:
                pic[mtile[1]][mtile[0]] = 1
            if event.button == 3:
                pic[mtile[1]][mtile[0]] = 0

    redraw()

pygame.quit()
