import pygame,random,json,os
from pygame.locals import *
pygame.init()

tilesizemultiplier = 2
TILESIZE = int(16*tilesizemultiplier)
wordim = (20,20)
WIN = (wordim[0]*TILESIZE,wordim[1]*TILESIZE)

adjneigh = ((0,-1),(1,0),(0,1),(-1,0))

win = pygame.display.set_mode(WIN)
pygame.display.set_caption("WFC")

worsur = pygame.Surface((wordim[0]*TILESIZE,wordim[1]*TILESIZE))
world = {}
with open("tileset.json",'r')as file:
    pre = json.load(file).values()
    rawtileset = list(pre)
rawspriteset = []
for sp in os.listdir("sprites"):
    pre_img = pygame.transform.scale(pygame.image.load("sprites/"+sp),(TILESIZE,TILESIZE))
    rawspriteset.append(pre_img)

tileset = []
spriteset = []
for count in range(len(rawtileset)):
    t = rawtileset[count]
    tileset.append(t[0])
    spriteset.append(rawspriteset[count])
    if t[1] == 1:
        tileset.append(t[0][1:]+t[0][:1])
        spriteset.append(pygame.transform.rotate(rawspriteset[count],90))
    if t[1] == 2:
        tileset.append(t[0][1:]+t[0][:1])
        tileset.append(t[0][2:]+t[0][:2])
        tileset.append(t[0][3:]+t[0][:3])
        spriteset.append(pygame.transform.rotate(rawspriteset[count],90))
        spriteset.append(pygame.transform.rotate(rawspriteset[count],180))
        spriteset.append(pygame.transform.rotate(rawspriteset[count],270))

def inbound(cord,dim):
    if cord[0] >= 0 and cord[0] < dim[0]:
        if cord[1] >= 0 and cord[1] < dim[1]:
            return True
    
def generateworld():
    global world
    world = {}
    win.fill((50,50,50))
    to_do = [(random.randrange(0,wordim[0]),random.randrange(0,wordim[1]))]
    while len(to_do) > 0:
        cur = to_do[0]
        to_do.pop(0)
        neigh = [(cur[0]+ad[0],cur[1]+ad[1]) for ad in adjneigh]
        t,r,b,l = neigh 
        for n in neigh:
            if not(n in world or n in to_do) and inbound(n,wordim):
                to_do.append(n)
        possible = []
        count = -1
        for i in tileset:
            count += 1
            if t in world:
                if not i[0][-1::-1] == tileset[world[t]][2]:
                    continue
            if r in world:
                if not i[1][-1::-1] == tileset[world[r]][3]:
                    continue
            if b in world:
                if not i[2][-1::-1] == tileset[world[b]][0]:
                    continue
            if l in world:
                if not i[3][-1::-1] == tileset[world[l]][1]:
                    continue
            possible.append(count)
        if len(possible) == 0:
            pass
        selected = random.choice(possible)
        world[cur] = selected
        win.blit(spriteset[selected],(cur[0]*TILESIZE,cur[1]*TILESIZE))
        pygame.display.update()
    #print(world,"\n")
        
generateworld()
run = True
while run:

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == KEYDOWN:
            if event.key == K_r:
                generateworld()
        
        #print(world)
        win.fill((50,50,50))
        for i in world:
            win.blit(spriteset[world[i]],(i[0]*TILESIZE,i[1]*TILESIZE))

        pygame.display.update()

pygame.quit()
