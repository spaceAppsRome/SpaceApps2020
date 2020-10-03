
# Copyright (C) 2020  thatsOven, BboyKatà
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

from pathlib import Path
import os, png, math, pygame
from pyqrcode import create
from random import randint

os.system("mode 100,3")
os.system("title S-APP's 'QR Code Generator' By thatsOven and BboyKatà - SpaceApps 2020")
os.environ["SDL_VIDEODRIVER"] = "dummy"

EcoTips = ["If God made us similar to him, why do we continue to destroy, pollute and kill the environment?","For an ecologist to be elected president, trees have to vote.","Don't pollute - good planets are hard to find.","Sustain all together","Arctic temperatures now are 8 to 10 degrees Celsius warmer than average","Thanks to altimetry missions, we now have a nearly three-decade-long record of sea level change.","Always take with you a water bottle!","Be plastic free!","Replace plastic straws with metal straws!","Tear off the straps on the mask before throwing it away!","NASA Helps Puerto Rico Prepare for Saharan Dust Impacts"]

os.chdir(Path(__file__).resolve().parent)
directory = str(os.getcwd())
if not os.path.isfile(directory+'\\code.txt'):
    with open(directory+'\\code.txt', "w") as txt:
        txt.write("")

def getmax(start):
    global directory
    user_number, maxid = start, start-1 
    with open(directory+'\\code.txt', 'r') as txt:
        for line in txt:
            data = line.strip('\n').split(":")
            if int(data[1], 16) > maxid:
                maxid = int(data[1], 16)
            if int(data[0]) > user_number:
                user_number = int(data[0])
    return maxid, user_number

def progressbar(width, progress, total):
    lines = round((progress*width) / total)
    os.system("cls")
    print("[", end="")
    for _ in range(lines):
        print("█", end="")
    for _ in range(width-lines):
        print("░", end="")
    print("] " + str(round((progress*100)/total)) + "%")

def multiLineSurface(string, font, rect):
    finalLines = []
    requestedLines = string.splitlines()
    for requestedLine in requestedLines:
        if font.size(requestedLine)[0] > rect.width:
            words = requestedLine.split(' ')
            accumulatedLine = ""
            for word in words:
                testLine = accumulatedLine + word + " "
                if font.size(testLine)[0] < rect.width:
                    accumulatedLine = testLine
                else:
                    finalLines.append(accumulatedLine)
                    accumulatedLine = word + " "
            finalLines.append(accumulatedLine)
        else:
            finalLines.append(requestedLine)
    return finalLines

maxid, user_number = getmax(0)

while True:
    os.system("cls")
    NumCods = input("Insert quantity of QR Codes to generate: ")
    try:
        NumCods = int(NumCods)
    except:
        input("\nUnacceptable Input")
    else:
        if NumCods < 1:
            input("\nUnacceptable Input")
        else:
            if NumCods+user_number > 65535:
                base = math.ceil(math.log2(NumCods/4))
            else:
                base = 4
            break

os.system("cls")
pygame.display.init()
pygame.font.init()
pygame.display.set_mode(size=(580,858))
fontused = pygame.font.SysFont("Calibri",30)
logosurface = pygame.image.load(directory+"\\logo.png").convert()

notfirst = False
for i in range(NumCods):
    pygame.event.get()
    if notfirst:
        maxid, user_number = getmax(user_number)
    else:
        notfirst = True
    user_number += 1 
    maxid = hex(maxid + 1).split('x')[-1].zfill(base).upper() 
    with open(directory+'\\code.txt', 'a') as txt: 
        txt.write(str(user_number) + ':' + maxid + '\n') 
    create(maxid).png("temp.png",scale=20)
    imagesurface = pygame.image.load(directory+'\\temp.png')
    finalsurface = pygame.display.get_surface()
    finalsurface.fill((79, 82, 87))
    basesurface = pygame.Rect(2,4,576,60)
    multilinetext = multiLineSurface(EcoTips[randint(0,len(EcoTips)-1)],fontused,basesurface)
    counter = 4
    for line in multilinetext:
        textsurface = fontused.render(bytes(line,"utf-8"),True,(255,255,255), (79, 82, 87))
        finalsurface.blit(textsurface,(2,counter))
        counter += 32
    size = counter + 10
    finalsurface.blit(imagesurface,(0,size))
    size += 584
    finalsurface.blit(logosurface,(0,size))
    pygame.image.save(finalsurface,str(maxid)+".png")   
    progressbar(93, i+1, NumCods)
os.system("del /q temp.png")
input("DONE!")