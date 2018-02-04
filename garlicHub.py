import pygame,smtplib,ghub.ui as ui
from pygame import *
import subprocess
import sys
from os import system

pygame.init()
## ^ Who really knows about that one lol
## include scalability down here V

disp = pygame.display.set_mode((432,232))
screen = pygame.Surface((640,480))
clock = pygame.time.Clock()

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
        self.buttonsMain=[ui.Button(166,16,100,32,"Start mining!",self.surf),ui.CheckBox(50,160,"eMail Update?",self.surf,size=32)]
        self.buttonsMining=[ui.Button(166,16,100,32,"Stop mining!",self.surf)]
        self.miner=0
        self.drawn=0
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
                    if b.text == "eMail Update?":
                        b.Check()
                    if b.text == "Start mining!":
                        self.miner=subprocess.Popen([sys.executable, 'miner.py'], shell=True)
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

            if self.currentFrame == "main":
                disp.fill((0,0,150))
                for f in self.buttonsMain:
                    f.Update()
            pygame.display.update()
            

#A class to act as the program
class program(object):
    def __init__(self):
        self.go=1
        self.stats={"sharesfound":0}

#eMail function
def sendMail(mailtext,mailusr,mailpass,mailaddrto):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mailusr, mailpass)

    msg = mailtext
    server.sendmail(mailusr, mailaddrto, msg)
    server.quit()

theProgram=program()
theMainFrame=mainFrame(disp,theProgram)


def Main():
    while theProgram.go>0:
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONUP and e.button == 1:
                theMainFrame.buttonCheck(e.pos)
            if e.type == QUIT:
                theProgram.go=-1
            if e.type == KEYUP and e.key == K_SPACE:
                sendMail("ayo","samtubbiscool@gmail.com","","samtubbiscool@gmail.com")
        theMainFrame.doUpdate()
    pygame.display.quit()



#Enter main loop
if(__name__ == "__main__"):
    Main()
