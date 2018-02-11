import pygame,ghub.ui as ui
from pygame import *
import subprocess
import sys
from os import system
import json

pygame.init()
## ^ Who really knows about that one lol
## include scalability down here V

disp = pygame.display.set_mode((432,232))
screen = pygame.Surface((640,480))
clock = pygame.time.Clock()
font = ui.LoadFont(24)
pygame.display.set_caption("GarlicHub by u/sam0s")
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)



#The main window (or only probably)
class mainFrame(object):
    def __init__(self,surf,program):
        self.currentFrame = "main"
        self.surf=surf
        self.program=program
        self.buttonsMain=[ui.Button(166,16,100,32,"Start mining!",self.surf),ui.CheckBox(50,160,"eMail Update?",self.surf,size=32),ui.CheckBox(200,160,"draw Stats?",self.surf,size=32)]
        self.buttonsMining=[ui.Button(166,16,100,32,"Stop mining!",self.surf)]
        self.miner=0
        self.drawn=0
        self.statsUT=0
        self.drawSU=0
    def statsUpdate(self):
        with open('currentStats.json') as json_data:
            d = json.load(json_data)
            statslist=[d['stats'][0]['sharesfound'],d['stats'][1]['sharesfailed'],d['stats'][2]['hash']]
            for f in statslist:
                a=font.render("share finds: "+str(statslist[0]),0,(0,235,0))
                b=font.render("share fails: "+str(statslist[1]),0,(235,0,0))
                c=font.render("hashrate: "+str(statslist[2]),0,(255,255,255))
                self.surf.blit(a,(100,100))
                self.surf.blit(b,(100,150))
                self.surf.blit(c,(100,200))
    def buttonCheck(self,evepos):
        self.drawn=0
        mineFlag=0
        if self.currentFrame=="mining":
            for b in self.buttonsMining:
                if b.rect.collidepoint(evepos):
                    if b.text == "Stop mining!":
                        try:
                            self.miner.kill()
                            system('taskkill /f /im ccminer-x64.exe')

                        except AttributeError:
                            print "Try again brotha."
                        self.currentFrame="main"
                        mineFlag=1
        if self.currentFrame=="main" and mineFlag==0:
            for b in self.buttonsMain:
                if b.rect.collidepoint(evepos):
                    if b.text == "eMail Update?" or b.text=="draw Stats?":
                        b.Check()
                    if b.text == "Start mining!":
                        if self.buttonsMain[1].active==False:
                            self.miner=subprocess.Popen([sys.executable, 'miner.py'], shell=True)
                        else:
                            self.miner=subprocess.Popen([sys.executable, 'minerEmail.py'], shell=True)
                        self.currentFrame="mining"
                        #self.program.mt.startMining('dep\\ccminer-x64 --algo=scrypt:10 -o stratum+tcp://pool.grlc-bakery.fun:3333 -u GcvJyCUMgEAtLyPrEHm4qZ6avJEc674Via --max-temp=85')
    def doUpdate(self):
        
        if self.drawn==0:
            print "efe"
            self.drawn=1
            if self.currentFrame == "mining":
                disp.fill((0,0,100))

                for f in self.buttonsMining:
                    f.Update()
                if self.drawSU==1:
                    self.drawSU=0
                    self.statsUpdate()

            if self.currentFrame == "main":
                disp.fill((0,0,150))
                for f in self.buttonsMain:
                    f.Update()
            pygame.display.update()
        if self.currentFrame=="mining" and self.buttonsMain[2].active==True:
            self.statsUT+=1
            if self.statsUT>5000000:
                self.drawSU=1
                self.drawn=0
                self.statsUT=0




#A class to act as the program
class program(object):
    def __init__(self):
        self.go=1
        self.stats={"sharesfound":0}



theProgram=program()
theMainFrame=mainFrame(disp,theProgram)


def Main():
    while theProgram.go>0:
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONUP and e.button == 1:
                theMainFrame.buttonCheck(e.pos)
            if e.type == QUIT:
                theProgram.go=-1
        theMainFrame.doUpdate()
    pygame.display.quit()



#Enter main loop
if(__name__ == "__main__"):
    Main()
