import pygame,smtplib,ghub.ui as ui
from pygame import *

pygame.init()
## ^ Who really knows about that one lol
## include scalability down here V

disp = pygame.display.set_mode((640,480))
screen = pygame.Surface((640,480))

#The main window (or only probably)
class mainFrame(object):
    def __init__(self,surf,program):
        self.currentFrame = "main"
        self.surf=surf
        self.program=program
        self.buttons=[ui.Button(32,32,100,32,"Start mining!",self.surf)]
    def buttonCheck(self,evepos):
        for b in self.buttons:
            if b.rect.collidepoint(evepos):
                if b.text == "Start mining!":
                    print "sh"    
                    #self.program.mt.startMining('dep\\ccminer-x64 --algo=scrypt:10 -o stratum+tcp://pool.grlc-bakery.fun:3333 -u GcvJyCUMgEAtLyPrEHm4qZ6avJEc674Via --max-temp=85')
    def doUpdate(self):
        if self.currentFrame == "main":
            disp.fill((200,0,0))
            for f in self.buttons:
                f.Update()
                
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
        pygame.display.update()
    pygame.display.quit()



#Enter main loop
if(__name__ == "__main__"):
    Main()
