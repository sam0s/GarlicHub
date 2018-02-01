import pygame,smtplib
#import ghub.frames as gFrames
from pygame import *
pygame.init()
## ^ Who really knows about that one lol
## include scalability down here V

disp = pygame.display.set_mode((640,480))
screen = pygame.Surface((640,480))

class mainFrame(object):
    def __init__(self):
        self.currentFrame = gFrames.frame("main")

class program(object):
    def __init__(self):
        self.go=1

def sendMail(mailtext,mailusr,mailpass,mailaddrto):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mailusr, mailpass)

    msg = mailtext
    server.sendmail(mailusr, mailaddrto, msg)
    server.quit()

theProgram=program()

def main():
    while theProgram.go>0:
        for e in pygame.event.get():
            if e.type == QUIT:
                theProgram.go=-1
            if e.type == KEYUP and e.key == K_SPACE:
                sendMail("ayo","samtubbiscool@gmail.com","","samtubbiscool@gmail.com")
        if theProgram.go==2:
            #MINING
            pass
        else:
            #NOT MINING
            pass
    #currentFrame.update()
    pygame.display.flip()

#Enter main loop
if(__name__ == "__main__"):
    main()	
