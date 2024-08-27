from cmu_graphics import *
import math 
import random
# from math import e


class siphonophore:
    #species, segments, segment length, init hunger, tentacles t/f, 
    #glow t/f, colors (str)
    #Originally planned for more features, that's why some things are commented out
    def __init__(self, siphData):
        self.siphData = siphData
        self.species = self.siphData[0]
        self.segments = int(self.siphData[1])
        #segLength spans x, width spans y axis
        self.segLength = int(self.siphData[2])
        self.segWidth = int(self.siphData[3])
        self.hunger = float(self.siphData[4])
        self.gain = 0
        self.loss = 0
        # self.tentacles = self.siphData[5]
        # self.glow = self.siphData[6]
        #base color in rgb, if we can do this w/o so many variables that would be banger
        self.r = int(self.siphData[7])
        self.g = int(self.siphData[8])
        self.b = int(self.siphData[9])
        #climate requirements
        self.maxDepth = int(self.siphData[10])
        self.spawnDepth = int(self.siphData[11])
        self.minDepth = int(self.siphData[12])
        self.startX = 200
        self.startY = 200
        self.maxY = self.startY+10 
    
    def drawSiph(self, app):
        if self.species == 'Praya Dubia':
            for i in range(self.segments):
                drawRect(app.currSiph.startX+i*2*(self.segLength), 
                         app.currSiph.startY+10*math.sin(i+app.siphPhase), self.segWidth, self.segLength, 
                         fill = rgb(self.r, self.g, self.b), 
                         align = 'top-left')
                

    def moveSiph(self, app, dir):
        tempSpeedModifier = 10*((app.seaTemp-15)/30)

        if dir == 'down' or dir == 's':
            if self.startY >= 550: 
                app.seaDepth += 10
                updateRGB(app, 1)
            else:
                self.startY += 10 + tempSpeedModifier
                self.maxY+= 10 + tempSpeedModifier

        if dir == 'up' or dir == 'w':
            if app.seaDepth <=320: 
                seaLev = 320-app.seaDepth
                if self.startY < seaLev +50:
                    app.seaDepth -= 10 + tempSpeedModifier
                    self.startY = seaLev +50
                else:
                    self.startY -= 10 + tempSpeedModifier
                    self.maxY -= 10 + tempSpeedModifier

            if app.seaDepth>320:
                if self.startY <= 50: 
                    app.seaDepth -= 10 + tempSpeedModifier
                    updateRGB(app, -1)
                else:
                    self.startY -= 10 + tempSpeedModifier
                    self.maxY -= 10 + tempSpeedModifier

        app.seaTemp = pythonRound(30 -31*(app.seaDepth/1600))
        if dir == 'right' or dir == 'd':
            self.startX +=10 + tempSpeedModifier
        if dir == 'left' or dir == 'a':
            self.startX -=10 + tempSpeedModifier
    

    def preyTouchingSiph(self, app, pTopX, pTopY, pSideLength, count):
        preyXrange = (pTopX, pTopX+pSideLength)
        preyYrange = (pTopY, pTopY+pSideLength)
        
        siphX = app.currSiph.startX +(count*2*app.currSiph.segLength)
        siphY = app.currSiph.startY+10*math.sin(count)

        siphXrange = (siphX, siphX+app.currSiph.segWidth)
        siphYrange = (siphY, siphY+app.currSiph.segLength)
        # app.tempMSG = f'prey range{preyXrange} siph range of {siphXrange}'
        #^^for testing
        if (preyXrange[0] <= siphXrange[1] and preyXrange[1] >= siphXrange[0]) and (
            preyYrange[0] <= siphYrange[1] and preyYrange[1] >= siphYrange[0]):
            return True
        else:
            return False

class prey:
    #have a method that randomly generates an x&y, siph uses app variables 
    # b/c really should only be 1 siph on screen at any given time
    def __init__(self, app, species, topx, topy, side):
        self.species = species
        self.topX = topx
        self.topY = topy
        self.side = side #squre hitbox on prey
        ##Vars that are different with each prey/Marine Snow
        self.tempR = random.randint(200,255)
        self.tempG = random.randint(200,255)
        self.tempB = random.randint(200,255)
        #Set a y direction, then randomize x drift down and y falling depth
        self.randDirection = random.randint(0,1)
        if self.randDirection == 0:
            self.randDirection = -1
        self.randXdrift = random.randint(0,3)
        self.randYfall = random.randint(1,4)
        
        
        #fish rand gen
        self.fishType = random.randint(0,9)
        self.fishX = random.randint(0,4)
        self.fishY = random.randint(1,3)

        
        if self.fishType <= 1:
            self.color = 'Green'
        elif self.fishType <= 4:
            self.color = 'Red'
        else:
            self.color = 'goldenrod'

    def drawPrey(self, app):
        if self.species == 'Marine Snow':
            drawCircle(self.topX, self.topY, self.side, fill = rgb(self.tempR,self.tempG,self.tempB))
    def drawFish(self, app):
        if self.species == 'Common Fish':
            phaseStart = -5*3.14/8
            phaseEnd = 5*3.14/4
            phasePeriod = abs(phaseEnd-phaseStart)
            for seg in range(app.fishSegments):
                drawRect(self.topX+(seg*(app.fishSegLength-10)), 
                        self.topY + app.fishRad*math.sin(phaseStart+phasePeriod*(seg/app.fishSegments)), 
                        app.fishSegLength, app.fishSegWidth, fill = self.color, align = 'top-left')
                
                drawRect(self.topX+(seg*(app.fishSegLength-10)), 
                        self.topY + app.fishRad*math.cos(1.57+phaseStart+phasePeriod*(seg/app.fishSegments)), 
                        app.fishSegLength, app.fishSegWidth, fill = self.color, align = 'top-left')
                
    def drawDemoFish(self, app, color):
        if self.species == 'Common Fish':
            phaseStart = -5*3.14/8
            phaseEnd = 5*3.14/4
            phasePeriod = abs(phaseEnd-phaseStart)
            for seg in range(app.fishSegments):
                drawRect(self.topX+(seg*(app.fishSegLength-10)), 
                        self.topY + app.fishRad*math.sin(phaseStart+phasePeriod*(seg/app.fishSegments)), 
                        app.fishSegLength, app.fishSegWidth, fill = color, align = 'top-left')
                
                drawRect(self.topX+(seg*(app.fishSegLength-10)), 
                        self.topY + app.fishRad*math.cos(1.57+phaseStart+phasePeriod*(seg/app.fishSegments)), 
                        app.fishSegLength, app.fishSegWidth, fill = color, align = 'top-left')
 
    def movePrey(self,app):
        if self.species == 'Marine Snow':
            self.topY += self.randYfall
            self.topX += self.randDirection*self.randXdrift
        
        if self.species == 'Common Fish':
            self.topY += self.fishY
            self.topX += self.randXdrift

    def isEaten(self, app):
        if app.currSiph.species == 'Praya Dubia':
            if (self.topY + self.side) >= (app.currSiph.startY) and (
                (self.topY - self.side) <= (app.currSiph.startY + app.currSiph.segWidth)):
                for seg in range(app.currSiph.segments):
                        if app.currSiph.preyTouchingSiph(app, self.topX, self.topY, self.side, seg):
                            return True

class wave:
    def __init__(self, app):
        self.segLength = random.randint(4, 7)
        self.waveAmp = self.segLength
        self.segWidth = 15
        self.startX = random.randint(10, (7/8)*app.width)
        self.startY = random.randint((5/8)*app.height, (7/8)*app.height)
        self.numPeriod = random.randint(1,3)
        self.phase = 1.57075 #pi/2 phase shift
        self.waveSpeed = random.randint(1,4)
        self.color = 'white'

    def drawWave(self, app):
        numBlocs = (10*self.numPeriod)
        for segment in range(numBlocs):
            drawRect(self.startX + segment*self.segWidth, self.startY+self.waveAmp*math.sin(segment+self.phase+app.wavePhase), 
                    self.segWidth, self.segLength, fill = self.color, align = 'top-left')
            
    def moveWave(self):
        self.startX += self.waveSpeed*0.5
                        
class Button:
    def __init__(self, topx, topy, width, height, message, textSize, font, 
                 textColor, bkgColor, opacity, size):
        self.topX = topx
        self.topY = topy
        self.width = width
        self.height = height
        self.message = message
        self.textSize = textSize
        self.font = font
        self.textColor = textColor
        self.bkgColor = bkgColor
        self.opacity = opacity
        self.size = size
    
    def draw(self):
        drawRect(self.topX, self.topY, self.width, self.height, fill = self.bkgColor, 
                 opacity = self.opacity, align = 'top-left')
        drawLabel(f'{self.message}', self.topX + self.width*0.5, self.topY + self.height*0.5, 
                  fill = self.textColor, font = self.font, size = self.size)

class popUp:
    def __init__(self, show, topX, topY, width, height, message, textSize, font, 
                 textColor, bkgColor, opacity, size):
        self.show = show
        self.topX = topX
        self.topY = topY
        self.width = width
        self.height = height
        self.message = message
        self.textSize = textSize
        self.font = font
        self.textColor = textColor
        self.bkgColor = bkgColor
        self.opacity = opacity
        self.size = size
    def drawPopUp(self):
        drawRect(self.topX, self.topY, self.width, self.height, fill = self.bkgColor, 
                 opacity = self.opacity, align = 'top-left')
        
        clipCharas = 52
        if len(self.message) > clipCharas:
            linesNeeded = math.ceil(len(self.message)/clipCharas)
            for val in range(linesNeeded):
                if (val+1)*clipCharas > len(self.message):
                    #All cases
                    wrappedLine = self.message[val*clipCharas:-1]
                else: 
                    #less than 20 charas left in block
                    wrappedLine = self.message[val*clipCharas: (val+1)*clipCharas]
                drawLabel(f'{wrappedLine}', self.topX + 10, (self.topY+10+(val)*20), 
                    fill = self.textColor, font = self.font, size = self.size, italic = True, align = 'top-left')
        else:
            drawLabel(f'{self.message}', self.topX+10, self.topY+10, 
                  fill =self.bkgColor, font = self.font, size = self.size, italic = True, align = 'top-left')
            
class sliderBar:
    def __init__(self, barX, barY, barLength, barHeight, knobY, lowerVal, currVal, maxVal, colr, label):
        self.barX = barX
        self.barY = barY
        self.barLength = barLength
        self.barHeight = barHeight
        self.rad = self.barHeight/2
        self.label = label
        
        # self.knobY = knobY
        self.toggWidth = 10
        self.toggHeight = 20
        self.lowerVal = lowerVal
        self.currVal = currVal
        self.maxVal = maxVal
        self.knobX = self.barX +(self.barLength)*(self.currVal/self.maxVal)
        self.knobY = self.barY - (self.toggHeight/4)

        self.colr = colr

    def draw(self):
        #bar + edges
        drawLabel(f'{self.label}', 150, self.barY, align = 'top-left')
        drawLabel(f'{self.lowerVal}', 350, self.barY, align = 'top-left')
        drawLabel(f'{self.maxVal}', 650, self.barY, align = 'top-left')
        drawRect(self.barX, self.barY, self.barLength+2*self.rad, self.barHeight, fill = self.colr, align = 'top-left')
        drawCircle(self.barX-self.rad, self.barY, self.rad, fill = self.colr, align = 'top-left')
        drawCircle(self.barX+self.barLength+self.rad, self.barY, self.rad, fill = self.colr, align = 'top-left')
        #toggle
        #Toggle x range, (0, self.barLength-self.toggWidth)
        drawRect(self.knobX, self.knobY, self.toggWidth, self.toggHeight, align = 'top-left', fill = self.colr)
        drawRect(self.barX +(self.barLength/2), self.toggHeight+self.knobY+3, 50, 20, fill = 'navy', opacity = 70, align = 'top-left', border = 'midnightBlue')

def onAppStart(app):
    app.siphSubOrder = ['Calycophorae', 'Cystonectae', 'Physonectae']
    app.cleanedSiph = cleanExtract("siphonophoreData.txt")
    # app.cleanedPrey = cleanExtract("preyData.txt")
    app.currSiph = siphonophore(app.cleanedSiph[0])

    # System/enviroment variables
    app.width = 800
    app.height = 600
    app.stepsPerSecond = 20
    app.seaDepth = app.currSiph.spawnDepth
    app.seaTemp = 30 -31*(800/1600)
    app.paused = False
    app.death = False
    app.deathCause = ''
    app.creativeMode = False
    app.controlPanel = False
    app.exInShow = False
    app.userCustomized = False

    app.topGrad = [47,49,67]
    app.bottomGrad = [5,1,24]
    app.seaY = 0
    if app.seaDepth <= 320:
        app.seaY = 320-app.currSiph.startY

    ## Siph motion
    app.siphDirection = 1
    app.siphMessage = []
    app.siphPhase = 0

    ###Prey variables
    app.fishRad = 20
    app.fishSegments = 15
    app.fishSegLength = 15
    app.fishSegWidth = 8

    app.demoFishList = []
    for i in range(3):
        demFish = prey(app, 'Common Fish', 160 + i*170, 360, 10)
        app.demoFishList.append(demFish)


    # app.testFish = prey(app, 'Common Fish', 200, 200, 20)
    app.timeSinceLastPrey = 0
    app.preyList = []
    app.timeSinceFish = 0
    app.fishGen = 0.2
    app.fishList = []

    app.xDisp = 9
    app.amp = 0.1
    app.yDisp = 0.15
    app. disp = app.currSiph.segments - app.xDisp

    if app.yDisp- ((app.amp*app.disp)/(1+app.disp**2)**0.5) == 0:
        app.mSGen = 0.001
    else:
        app.mSGen = pythonRound(app.yDisp- ((app.amp*app.disp)/(1+app.disp**2)**0.5),4)

    app.hungerSlider = sliderBar(app.width/2, 150, 200, 10, 20, 0, app.currSiph.hunger, 100, 'green', 'Hunger')
    app.lengthSlider = sliderBar(app.width/2, 190, 200, 10, 70, 1, app.currSiph.segments, 40, 'green', 'Length')
    app.depthSlider = sliderBar(app.width/2, 230, 200, 10, 20, 0, app.seaDepth, 2000, 'green', 'Sea Depth')
    app.tempSlider = sliderBar(app.width/2, 270, 200, 10, 20, -20, app.seaTemp, 35, 'green', 'Temperature')
    app.mSGenSlider = sliderBar(app.width/2, 310, 200, 10, 20, 0.0001, app.mSGen, 1, 'green', 'Marine Snow Generation')
    app.sliderList= [app.hungerSlider, app.lengthSlider, app.depthSlider, app.tempSlider, app.mSGenSlider]

    #Buttons
    app.startButton = Button(app.width*0.7, app.height*0.75, 60, 40, 
                             'Start>', 18, 'montserrat', 'aliceBlue', 
                             'white', 40, 18)
    app.infoButton = Button(app.width*0.2, app.height*0.75, 60, 40, 
                             '?', 18, 'montserrat', 'aliceBlue', 
                             'white', 40, 18)
    app.nextButton = Button(app.width*0.7, app.height*0.8, 60, 40, 
                             'Next>', 18, 'montserrat', 'aliceBlue', 
                             'white', 40, 18)
    app.backButton = Button(app.width*0.2, app.height*0.8, 60, 40, 
                             '<Back', 18, 'montserrat', 'aliceBlue', 
                             'white', 40, 18)
    
    app.pauseButton = Button(app.width*0.1, 230, 40, 40, 
                             '||', 18, 'montserrat', 'aliceBlue', 
                             'darkGoldenrod', 80, 18)
    app.creativeButton = Button(app.width*0.1 + 45, 230, 40, 40, 
                             'C', 18, 'montserrat', 'aliceBlue', 
                             'darkGoldenrod', 80, 18)
    app.extraInfoButton =Button(app.width*0.1, 290, 90, 40, 
                             'Extra Info', 18, 'montserrat', 'aliceBlue', 
                             'goldenrod', 40, 18)
    app.controlButton =Button(app.width*0.1, 350, 90, 40, 
                             'Controls', 18, 'montserrat', 'aliceBlue', 
                             'goldenrod', 40, 18)
    app.closeButton = Button(app.width*0.8, 90, 60, 40, 
                             'X', 18, 'montserrat', 'aliceBlue', 
                             'darkGoldenrod', 80, 18)
    #PopUps
    app.infoPanel = popUp(False, app.width*0.2, app.height*0.22, 60+app.width*0.5, app.height*0.5, 
                             '''Play as a siphnophore! Utilize the 'WASD' or arrow keys to move up, down right and left to consume prey!! If you maintain a hunger level above 80 you can even grow in length!! However, remember to pay attention to your surroundings. The ocean is a dangerous place, and you must be careful not to venture too far above and below your preffered ocean depth. Keep a close eye on your hunger bar!! When your hunger runs below 40 you will begin the process of starving.''', 
                             8, 'montserrat', 'ivory', 
                             'peru', 40, 18)
    ##highlight
    app.selectionHighlight = False
    app.selectionCoords = []


###CREDIT: Read + Write file from cmu fall23 cs string notes, 12.Basic FileIO
#https://www.cs.cmu.edu/~112/notes/notes-strings.html 
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

#file extraction my own
def cleanExtract(fileName):
    cleanedVers = []
    originalData = readFile(fileName).split('\n')
    for line in originalData:
        cleanedVers += [line.split(',')]
    return cleanedVers

#####START MENU!
#CREDIT: Frame switching adapted from Piazza post @2232_f1 by Hugo Martinez
# https://piazza.com/class/lkq6ivek5cg1bc/post/2232_f1
def start_redrawAll(app):
    drawRect(0,0, app.width, app.height, align = 'top-left', 
             fill = gradient(rgb(47,49,67), rgb(5,1,24), start ='top'))
    
    
    for currPrey in app.preyList:
            currPrey.drawPrey(app)
    drawRect(app.width/2, app.height*0.15, 350, 70,  fill = 'white',
             opacity = 50, border = 'gold', align = 'center')
    drawLabel(f'Siphonophore Simulator', app.width/2, app.height*0.15,
              font='montserrat', fill = 'aliceBlue', size = 30, border = 'black', borderWidth = 1)
    
    app.startButton.draw()
    app.infoButton.draw()
    if app.infoPanel.show == True:
        app.infoPanel.drawPopUp()
    
    drawRect(app.width/2, app.height*0.8, 300, 70,  fill = 'white',
             opacity = 50, border = 'gold', align = 'center')
    drawLabel(f'''Click '?' for basic instructions''', app.width/2, app.height*0.78,
              font='montserrat', fill = 'aliceBlue', size = 18)  
    drawLabel(f'''|| Click 'Start' to begin''', app.width/2, app.height*0.82,
              font='montserrat', fill = 'aliceBlue', size = 18)

def start_onStep(app):
    app.timeSinceLastPrey += app.mSGen 
    if app.timeSinceLastPrey >= 1:
        newPrey = prey(app, 'Marine Snow', random.randint(0, app.width), random.randint(0, int(app.height*0.2)), 
                                random.randint(3, 7))
        app.preyList.append(newPrey)
        app.timeSinceLastPrey = 0
    for currPrey in app.preyList:
        currPrey.movePrey(app)
        if currPrey.topY + currPrey.side >= app.height or currPrey.topX + currPrey.side >= app.width or currPrey.topX+currPrey.side <=0:
            app.preyList.remove(currPrey)

def start_onKeyPress(app, key):
    if key == 'right' or key == 'd':
        setActiveScreen("selectionMenu")

def start_onMousePress(app, mouseX, mouseY):
    if mouseTouchingRect(mouseX, mouseY,app.startButton.topX,app.startButton.topY, 
                    app.startButton.width, app.startButton.height):
        setActiveScreen("selectionMenu")

    if mouseTouchingRect(mouseX, mouseY,app.infoButton.topX,app.infoButton.topY, 
                    app.infoButton.width, app.infoButton.height):
        app.infoPanel.show = not app.infoPanel.show

####'CHARACTER' SELECTION
def selectionMenu_redrawAll(app):
    drawBKG(app)
    
    drawRect(33 + (app.width/3), app.height/6, 
            200, app.height*0.6, align = 'top-left', 
            fill = 'steelBlue', border = 'goldenrod', borderWidth=2)
    for j in range(7):
        drawRect(50 + (app.width/3) +j*2*(app.currSiph.segLength), 
                    app.currSiph.startY+10*math.sin(j), 35, app.currSiph.segLength, 
                    fill = rgb(app.currSiph.r,app.currSiph.g, app.currSiph.b), 
                    align = 'top-left')
    
    for i in range(0,1):
        #horrific dastardly function to wrap text
        # I know this should be written in a more efficient & concise way, I just don't have the time :(
        if len(app.cleanedSiph[i][0]) > 20:
            linesNeeded = math.ceil(len(app.cleanedSiph[i][0])/20)
            for val in range(linesNeeded):
                if (val+1)*20 > len(app.cleanedSiph[i][0]):
                    wrappedLine = app.cleanedSiph[i][0][val*20:-1]
                else: 
                    wrappedLine = app.cleanedSiph[i][0][val*20: (val+1)*20]
                drawLabel(f'{wrappedLine}', 133 + (i+1)*(app.width/3), (430-(linesNeeded-val-2)*20), 
                    fill = rgb(179, 141, 151), size = 18, bold = True, italic = True, align = 'center')
        else:
            drawLabel(f'{app.cleanedSiph[i][0]}', 133 + (i+1)*(app.width/3), 4.3*app.height/6, 
                  fill = rgb(179, 141, 151), size = 18, bold = True, italic = True, align = 'center')
        drawLabel(app.siphSubOrder[i], 133 + (i+1)*(app.width/3), app.height/5, 
                  fill = rgb(179, 141, 151), size = 18, bold = True, italic = True, align = 'center')
    
    drawLabel(f'Character Selection',app.width/2, app.height*0.1, size = 24, fill = 'goldenrod')

    ##Other Siphs
    praya = ['This is you!! :)',
             'A deep sea colonial organism', 
             'that can grow in size to rival', 
             'the blue whale.', 
             '',
             'You would still be loved as a',
             'worm.',
             'You basically are one anyways']
    # physalia = ['Physalia keeps trying to get', 
    #             'you to excersize and meet', 
    #             'the sun.', 
    #             '',
    #             'When will they learn that', 
    #             '''you're simply not built''', 
    #             'for sunlight!!']
    # dromalia = ['Ever since your cousin learned', 
    #             'how to anchor themself to the', 
    #             'sea floor with their tentacles', 
    #             'your mother has NOT stopped', 
    #             'talking about how you should', 
    #             'try to do the same.', 
    #             '', 
    #             'You just want to swim :(']
    # siphBlurbs =[praya, physalia, dromalia]
    siphBlurbs =[praya]
    for siph in range(len(siphBlurbs)):
        for line in range(len(siphBlurbs[siph])):
            drawLabel(siphBlurbs[siph][line], 50+(siph+1)*266, 280+14*(1+line), align = 'top-left', fill = 'linen', size = 13)
            # drawLabel(siphBlurbs[siph][line], 50+siph*266, 300+14*line, align = 'top-left', fill = 'linen', size = 13)

    app.nextButton.draw()
    app.backButton.draw()
    if app.selectionHighlight:
        drawSelection(app.selectionCoords[0], app.selectionCoords[1], app.selectionCoords[2], app.selectionCoords[3], 'pink')
        drawSelection(app.nextButton.topX, app.nextButton.topY,app.nextButton.width,app.nextButton.height, 'goldenrod')

def drawSelection(topX, topY, width, height, bordco):
    drawRect(topX, topY, width, height, fill = None, border = bordco, borderWidth = width/20)
    pass

def selectionMenu_onMousePress(app, mouseX, mouseY):
    if mouseTouchingRect(mouseX, mouseY,app.nextButton.topX,app.nextButton.topY, 
                    app.nextButton.width, app.nextButton.height):
        setActiveScreen("play")
    if mouseTouchingRect(mouseX, mouseY,app.backButton.topX,app.backButton.topY, 
                    app.backButton.width, app.backButton.height):
        setActiveScreen("start")

    ##Used to be full selection menu but scrapped for the sake of completing on time
    for i in range(1,2,1):
        if mouseTouchingRect(mouseX, mouseY, 33 + i*(app.width/3), 100, 
                    200, 360):
            if app.selectionCoords!= [] and app.selectionHighlight == True and app.selectionCoords[4] == i:
                app.selectionHighlight = False
            else:
                app.selectionHighlight = True
                app.selectionCoords = [33 + i*(app.width/3), 100, 200, 360, i]

def selectionMenu_onKeyPress(app,key):
    if key == 'right' or key == 'd':
        setActiveScreen("play")
    if key == 'left' or key == 'a':
        setActiveScreen("start")

### Specialized drawing methods
def drawBKG(app):
    drawRect(0,0, app.width, app.height, align = 'top-left', 
             fill = gradient(rgb(app.topGrad[0], app.topGrad[1], app.topGrad[2]), rgb(app.bottomGrad[0], app.bottomGrad[1], app.bottomGrad[2]), start ='top'))
def drawHorizon(app, siphYPos):
    #draw Sky
    drawRect(0, 0, app.width, (app.height/2)+25, align = 'top-left', 
             fill = gradient(rgb(65, 214, 255), rgb(235, 250, 255), start = 'top'))
    drawCircle(app.width/2, (app.height/2)+25, 140, fill = 'gold')
    #drawing Sea
    #when seaLevel = 0, sea starts at 320
    #thus seaLevel = 10, seastarts at 310etc.
    #sea level = 50, sea stafrts at 270
    #seastarts at ogStart-horizon lineseaYpos
    drawRect(0, 320-app.seaDepth, app.width, (app.height-(320-siphYPos)), align = 'top-left', 
             fill = gradient(rgb(16, 78, 196), rgb(16, 12, 80), start = 'top'))
    
def drawPanel(app):
    drawRect(30, 30, 175, app.height*0.65, align = 'top-left', fill = 'black', opacity = 60)
    drawLabel(f'hunger: {pythonRound(app.currSiph.hunger)}',45, 50, fill = 'white', opacity = 80, align = 'top-left', size = 13)
    drawLabel(f'length: {int(app.currSiph.segLength*app.currSiph.segments/10)}m',45, 70, fill = 'white', opacity = 80, align = 'top-left', size = 13)
    drawLabel(f'base species: {app.currSiph.species}',45, 90, fill = 'white', opacity = 80, align = 'top-left', size = 13)
    drawLabel(f'Sea Depth: {int(app.seaDepth)}m below ',45, 110, fill = 'white', opacity = 80, align = 'top-left', size = 13)
    drawLabel(f'surface',114, 130, fill = 'white', opacity = 80, align = 'top-left', size = 13)
    drawLabel(f'Sea Temp: {app.seaTemp}*C',45, 150, fill = 'white', opacity = 80, align = 'top-left', size = 13)

def drawExInPanel(app):
    rectWidth = app.width*(0.8)
    rectHeight = app.height*(0.8)
    drawRect(app.width/2, app.height/2, rectWidth, rectHeight, 
             align = 'center', fill = 'linen', border = 'darkGoldenrod', 
             borderWidth = 10, opacity = 80)
    drawLabel(f'Extra Info', app.width/2, (app.height/2)-(rectHeight*0.4), fill = 'darkGoldenrod', align = 'center', size = 25, bold = True)
    
    ##Body text, hardcoded b/c custom
    drawLabel(f'Species: {app.currSiph.species}', 145, 130, fill = 'saddleBrown', align = 'top-left', size = 13, bold = True)
    drawLabel(f'Playable Depth: 0-2000m Below Sea Level', 145, 150, fill = 'saddleBrown', align = 'top-left', size = 13, bold = True)
    drawLabel(f'Real World Depth: 700-1000m Below Sea Level', 145, 170, fill = 'saddleBrown', align = 'top-left', size = 13, bold = True)
    
    drawLine(145,190, 680,190, fill = 'saddleBrown', lineWidth = 2)
    drawLine(145,195, 680,195, fill = 'saddleBrown', lineWidth = 2)

    drawLabel(f'Prey Types:', 145, 210, fill = 'saddleBrown', align = 'top-left', size = 15, bold = True)
    mSColor = ['mistyRose','honeydew','ghostWhite']
    for i in range(0,3):
        dirr = 0
        if i%2 == 1:
            dirr = 1
        drawCircle(160+dirr*15, 240+8*i, 5, fill = mSColor[i], border = 'peru')
    drawLabel(f'Marine Snow:', 220, 230, fill = 'saddleBrown', align = 'top-left', size = 13, bold = True)
    marineSnowBlurb = ['Devoid of sunlight, the ocean depths do not allow for much', 
                       'primary production, as such, in this simulation marine snow',
                        '''will take the role of 'producer'. ''', 
                        '   --> Organic waste and decaying matter from the photic zone, mmm delicious']
    for label in range(len(marineSnowBlurb)):
        drawLabel(marineSnowBlurb[label], 220, 245+label*13, fill = 'saddleBrown', align = 'top-left', size = 12)
    
    drawLabel(f'Fish Types:', 145, 310, fill = 'saddleBrown', align = 'top-left', size = 13, bold = True)
    colors = ['goldenRod', 'Green', 'Red']
    for fish in range(len(app.demoFishList)):
        app.demoFishList[fish].drawDemoFish(app, colors[fish])
        drawLabel(colors[fish], 150 +fish*170, 405, fill = colors[fish], align = 'top-left', size = 14, border ='black', borderWidth = 0.5, bold = True)
    
    ##Fish bios
    yellowBlurb = ['Common Fish, consuming', 
                   'this fish will provide you', 
                   'with sustenance']
    greenBlurb = ['Rare Fish, consuming', 
                  'this fish will provide you',
                  'a bonus amount of', 
                  'sustenance']
    redBlurb = ['Beware of Dog? Wrong.',
                'Beware of Fish. This one bites',
                'Be careful not to get bitten by it']
    fishBios = [yellowBlurb, greenBlurb, redBlurb]
    for color in range(len(fishBios)):
        for line in range(len(fishBios[color])):
            drawLabel(fishBios[color][line], 150 +color*170, 425+line*13, fill = 'saddleBrown', align = 'top-left', size = 12)

    ##Bonus Commands here
    drawLine(145,480, 680,480, fill = 'saddleBrown', lineWidth = 2)
    drawLine(145,485, 680,485, fill = 'saddleBrown', lineWidth = 2)
    drawLabel(f'Bonus Commands:', 145, 490, fill = 'saddleBrown', align = 'top-left', size = 15, bold = True)
    drawLabel('''['p'] --> Quickly pause and unpause, ['c'] --> Quickly enable creative mode''', 200, 505, fill = 'saddleBrown', align = 'top-left', size = 12)

def drawControlPanel(app):
    rectWidth = app.width*(0.8)
    rectHeight = app.height*(0.8)
    drawRect(app.width/2, app.height/2, rectWidth, rectHeight, 
             align = 'center', fill = 'linen', border = 'darkGoldenrod', 
             borderWidth = 10, opacity = 80)
    drawLabel(f'Control Panel', app.width/2, (app.height/2)-(rectHeight*0.4), fill = 'darkGoldenrod', align = 'center', size = 25, bold = True)
    varNum = 0
    for variable in app.sliderList:
        variable.draw()
        if variable.label == 'Hunger':
            var = pythonRound(app.currSiph.hunger)
        if variable.label == 'Length':
            var = (app.currSiph.segments)
        if variable.label == 'Sea Depth':
            var = pythonRound(app.seaDepth)
        if variable.label == 'Temperature':
            var = pythonRound(app.seaTemp)
        if variable.label == 'Marine Snow Generation':
            var = app.mSGen
        drawLabel(var, variable.barX +(variable.barLength/2)+5, variable.toggHeight+variable.knobY+8 + (varNum*40), fill = 'darkGoldenrod', align = 'top-left', size = 14, bold = True)


def drawPauseMenu(app):
    drawRect(0, app.height*0.25, app.width, app.height*0.5, align = 'top-left', fill = 'black', opacity = 60)
    drawLabel(f'Game Paused', app.width/2, app.height/2, fill = 'yellow', size = 30)

def drawDeathMenu(app):
    drawRect(0, app.height*0.3, app.width, app.height*0.65, align = 'top-left', fill = 'black', opacity = 60)
    drawLabel(f'You Died', app.width/2, app.height/2, fill = 'yellow', size = 30)
    drawLabel(f'Cause of Death: {app.deathCause}', app.width/2, app.height/2+30, fill = 'yellow', size = 30)

def drawCreativeBanner(app):
    drawLabel(f'Creative mode enabled', app.width*0.8, 30, fill = 'yellow', size = 18)
    drawLabel(f'Now unable to be harmed', app.width*0.8, 50, fill = 'yellow', size = 14)
def drawUserCustomized(app):
    drawLabel(f'**Enviroment has previously', app.width*0.5, 30, fill = 'yellow', size = 18)
    drawLabel(f'been customized', app.width*0.5, 50, fill = 'yellow', size = 14)

def drawHunger(app):  
    int(87*app.currSiph.hunger/100)<=0 
    if int(87*app.currSiph.hunger/100)<=0 or app.currSiph.hunger <=0:
        drawRect(20, 20, 1, 20, align = 'top-left', fill = 'goldenrod')
    elif int(87*app.currSiph.hunger/100) >=100:
        drawRect(20, 20, 87, 20, align = 'top-left', fill = 'goldenrod')
    else:
        drawRect(20, 20, int(87*app.currSiph.hunger/100), 20, align = 'top-left', fill = 'goldenrod')

    drawRect(20, 20, 87, 20, align = 'top-left', border = 'white', fill = None)
    for i in range(5):
        drawLine(20+i*17.4, 20, 20+i*17.4, 40, fill = 'white')
    drawLabel(f'Hunger: {pythonRound(app.currSiph.hunger)}', 115, 25, fill = 'goldenrod', align = 'top-left')

### PLAY FRAME
def play_redrawAll(app):
    drawBKG(app)
    if app.seaDepth<=320:
        drawHorizon(app, app.seaDepth)
    drawPanel(app)
    app.controlButton.draw()
    app.extraInfoButton.draw()
    app.creativeButton.draw()
    app.pauseButton.draw()
    

    for currPrey in app.preyList:
            currPrey.drawPrey(app)
    for fish in app.fishList:
        fish.drawFish(app)

    app.currSiph.drawSiph(app)
    drawHunger(app)
    app.backButton.draw()

    if app.paused == True:
        drawPauseMenu(app)
    if app.creativeMode == True:
        drawCreativeBanner(app)
    if app.userCustomized:
        drawUserCustomized(app)
    if app.controlPanel:
        drawControlPanel(app)
        app.closeButton.draw()
    if app.exInShow:
        drawExInPanel(app)
        app.closeButton.draw()
    if app.death == True:
        drawDeathMenu(app)

##Death Functions
def inSeaBounds(app):
    if app.seaDepth <= 0 or app.seaDepth >=2000:
        app.deathCause = 'Out of natural habitat'
        app.death = True

def mouseTouchingRect(mouseX, mouseY, rectX, rectY, rectWidth, rectHeight):
    if mouseX < rectX or mouseX > rectX + rectWidth or (
        mouseY < rectY) or mouseY > mouseY+rectHeight:
        return False
    return True 

###BKG color shifting methods
def updateRGB(app, dirr):
    # app.topGrad = [47,49,67] @800 m
    # app.bottomGrad = [5,1,24]
    #top rgb(16, 78, 196) bottom = rgb(16, 12, 80)
    bR =app.bottomGrad[0]
    bG = app.bottomGrad[1]
    bB = app.bottomGrad[2]

    tR =app.topGrad[0]
    tG = app.topGrad[1]
    tB = app.topGrad[2]  

    if app.seaDepth <= 800:
        #move towards top rgb of(16, 78, 196) || or bottom rgb of = rgb(16, 12, 80)
        #fT = goal top, gB = goal bottom, aka the rgb we're transitioning to
        gT = [16, 78, 196]
        gB = [16, 12, 80]
        # print(gT, gT[0], gT[1], gT[2])
        app.topGrad = [closerColor(app, tR,gT[0],dirr), closerColor(app, tG,gT[1],dirr), closerColor(app,tB,gT[2],dirr)]
        app.bottomGrad = [closerColor(app, bR,gB[0],dirr), closerColor(app, bG,gB[1],dirr), closerColor(app,bB,gB[2],dirr)]
        #0->800m
        
    elif app.seaDepth > 800:
        #move towards top of 240, 42, 18 || or bottom of: 12, 15, 23
        #800 ->1600m
        gT = [240, 42, 18]
        gB = [12, 15, 23]
        
        app.topGrad = [closerColor(app, tR,gT[0],dirr), closerColor(app, tG,gT[1],dirr), closerColor(app,tB,gT[2],dirr)]
        app.bottomGrad = [closerColor(app, bR,gB[0],dirr), closerColor(app, bG,gB[1],dirr), closerColor(app,bB,gB[2],dirr)]
        
def closerColor(app, curr, goal, dirr):
    #ex: given a sea depth, go from 47 -> 16 slowly
    #there is a val of 31 to bridge 
    #if at m400 -> should be 47-(31)*1/2
    #ratio = 400/800
    ##-> return current -(difference)*(ratio)
    diff = abs(curr-goal)
    ratio = abs((app.seaDepth-800)/800)
    if dirr < 0 and curr <= goal:
        return goal
    elif dirr > 0 and curr >= goal:
        return goal
    else:
        return curr + int(diff*ratio*dirr)

def drawTestCol(app):
    drawRect(app.tempPX, app.tempPY, 10, 10, fill = 'green', visible = app.vis)
    drawRect(app.tempSX, app.tempSY, 20, 20, fill = 'purple', visible = app.vis)
    drawLabel(app.tempMSG, app.width/2, app.height/2, fill = 'yellow', size = 20)

def play_onStep(app):
    if app.paused == False and app.death == False:
        #Siphonophore motions
        #6.283 is 2pi
        if app.siphPhase >= 6.283: 
            app.siphPhase = 0
        app.siphPhase += 0.1
        tempMult = 0.03
        tempGainMult = 1

        if app.currSiph.segments <=10:
            tempMult = 0.05
            tempGainMult = 3
        if app.currSiph.segments <=3:
            tempMult = 0.075
            tempGainMult = 4
        if app.currSiph.segments >=15:
            tempMult = 0.01

        if app.creativeMode == False:
            app.currSiph.loss += app.currSiph.segments*0.1
            if app.currSiph.segments == 1 or app.currSiph.hunger > 40:
                if app.currSiph.hunger - app.currSiph.segments*tempMult == 0:
                    app.currSiph.hugner = 0
                else: 
                    app.currSiph.hunger -= app.currSiph.segments*tempMult

            elif app.currSiph.hunger <=40 and app.currSiph.loss >= app.currSiph.segLength:
                app.currSiph.segments -= 1
                app.currSiph.loss = 0

        if app.currSiph.hunger - app.currSiph.segments*tempMult <=0 or app.currSiph.segments <=0:
            app.death = True
            app.deathCause = 'Hunger'

        #Prey functions
        app.timeSinceLastPrey += app.mSGen 
        if app.timeSinceLastPrey >= 1:
            ystart = random.randint(0, int(app.width*0.1))
            if app.seaDepth <=320:
                ystart = 350 - app.seaDepth
            newPrey = prey(app, 'Marine Snow', random.randint(0, int(app.width*0.7)), ystart, 
                                 random.randint(3, 7))
            app.preyList.append(newPrey)
            if len(app.preyList) %10 == 0: 
                if len(app.fishList)<=3:
                    newFish = prey(app, 'Common Fish', 
                                random.randint(0, int(app.width*0.7)), ystart, 
                                random.randint(3, 7))
                    app.fishList.append(newFish)
            app.timeSinceLastPrey = 0

        for fish in app.fishList:
            fish.movePrey(app)
            if fish.topX> app.width or fish.topY+40 >= app.height or fish.topX  + 200 <=0:
                app.fishList.remove(fish)

            if fish.isEaten(app):
                app.fishList.remove(fish)
                if fish.color == 'Green':
                    app.currSiph.segments +=8
                if fish.color == 'Red':
                    app.currSiph.segments -=5
                    app.currSiph.hunger = 30
                    if app.currSiph.segments <= 0 or app.currSiph.hunger <=0:
                        app.death = True
                        app.deathCause = 'Eaten by fish'
                if fish.color == 'goldenrod':
                    app.currSiph.hunger = 80
                    app.currSiph.segments +=1

        for currPrey in app.preyList:
            ##only checking if prey touches first segment of siph!
            currPrey.movePrey(app)
            if currPrey.topY + currPrey.side >= app.height or currPrey.topX + currPrey.side >= app.width or currPrey.topX+currPrey.side <=0:
                app.preyList.remove(currPrey)
            if app.fishList != []:
                for fish in app.fishList:
                    if currPrey.topY + currPrey.side>= fish.topY+app.fishRad and (
                        currPrey.topY+currPrey.side<=fish.topY and currPrey.topX<=fish.topX+120 and
                        currPrey.topX +currPrey.side>=fish.topX):
                        app.fishList.remove(fish)
            if currPrey.isEaten(app):
                app.preyList.remove(currPrey)
                app.currSiph.gain += currPrey.side*tempGainMult

                if app.currSiph.hunger + currPrey.side*tempGainMult >=100:
                    app.currSiph.hunger = 100
                else:
                    app.currSiph.hunger += currPrey.side*tempGainMult

                if app.currSiph.hunger >=80 and app.currSiph.gain*tempGainMult >= app.currSiph.segLength:
                    app.currSiph.segments +=1
                    app.currSiph.gain = 0
            
        
def play_onKeyPress(app, key):
    ##Control
    if app.death == False:
        if key == 'p':
            app.paused = not app.paused
        if key == 'c':
            app.creativeMode = not app.creativeMode
            app.userCustomized = True
                    
def play_onMousePress(app, mouseX, mouseY):
    if mouseTouchingRect(mouseX, mouseY,app.backButton.topX,app.backButton.topY, 
                    app.backButton.width, app.backButton.height):
        setActiveScreen("selectionMenu")
    
    elif mouseTouchingRect(mouseX, mouseY,app.controlButton.topX,app.controlButton.topY, 
                    app.controlButton.width, app.controlButton.height):
        app.controlPanel = True
    
    elif mouseTouchingRect(mouseX, mouseY,app.extraInfoButton.topX,app.extraInfoButton.topY, 
                    app.extraInfoButton.width, app.extraInfoButton.height):
        app.exInShow = True
    elif mouseTouchingRect(mouseX, mouseY,app.closeButton.topX,app.closeButton.topY, 
                    app.closeButton.width, app.closeButton.height):
        app.controlPanel = False
        app.exInShow = False
    
    elif mouseTouchingRect(mouseX, mouseY,app.pauseButton.topX,app.pauseButton.topY, 
                    app.pauseButton.width, app.pauseButton.height):
        app.paused = not app.paused
    elif mouseTouchingRect(mouseX, mouseY,app.creativeButton.topX,app.creativeButton.topY, 
                    app.creativeButton.width, app.creativeButton.height):
        app.creativeMode = not app.creativeMode
        app.userCustomized = True


def play_onMouseDrag(app, mouseX, mouseY):
    
    for var in app.sliderList:
        var.specialVal = 0
        if mouseY >= var.knobY and mouseY <= var.knobY+var.toggHeight:
            if mouseX <= var.barX + var.barLength+var.toggWidth-var.rad and(
                mouseX >= var.barX-var.rad):
                var.knobX = mouseX
                var.currVal = pythonRound(var.lowerVal + (var.maxVal*(mouseX-var.barX)/var.barLength))
                var.specialVal = pythonRound((var.lowerVal + (var.maxVal*(mouseX-var.barX)/var.barLength)), 4)
                if app.userCustomized == False:
                    app.userCustomized = True

        if var.label == 'Hunger':
            app.currSiph.hunger = var.currVal
        elif var.label == 'Length':
            if var.currVal <= 0:
                app.currSiph.segments = 0
            app.currSiph.segments = var.currVal
            
        elif var.label == 'Sea Depth':
            app.seaDepth = var.currVal
        elif var.label == 'Temperature':
            app.seaTemp = var.currVal
        elif var.label == 'Marine Snow Generation':
            if var.specialVal <= 0:
                app.mSGen = 0.001
            elif var.specialVal >=1:
                app.mSGen = 1
            else:
                app.mSGen = pythonRound(var.specialVal,4)

def play_onKeyHold(app, key):
    #control
    #No actions possible if dead
    if app.death == False:
        if key == 'p':
            app.paused = not app.paused

        if key == 'c':
            app.creativeMode = not app.creativeMode

        ##Motion, can't move if paused
        if app.paused == False:
            if len(app.siphMessage) != 1:
                app.message = key[0]
                app.currSiph.moveSiph(app, app.message)
                inSeaBounds(app)

def play_onKeyRelease(app, keys):
    if keys != 'p' and keys != 'c':
        app.siphMessage = []
        
def main():
    runAppWithScreens("start")

main()