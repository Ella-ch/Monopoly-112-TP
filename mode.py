from cmu_112_graphics import *

from classes import *

from helper import *

import time
##########################################
# Splash Screen Mode
##########################################

def splashScreenMode_redrawAll(app, canvas):
    font = 'Baloo 20'
    canvas.create_text(app.width/2, app.height/3, text='Monopoly!',
                       font='Baloo 60', fill='black')
    #start new game button
    start = Button('start new game', (app.width/2, app.height/1.8))
    coord = start.getCoords(app)
    canvas.create_oval(coord, fill='#FFC125', outline='#FFC125')
    canvas.create_text(app.width/2, app.height/1.8, 
                       text='      Start\nNew Game',
                       font=font, fill='black', anchor='center')
    
    canvas.create_text(app.width*0.89, app.height*0.94, text='15-112 Term Project',
                       font='Times 20', fill='black')
    


def splashScreenMode_mousePressed(app, event):
    start = Button('start a new game', (app.width/2, app.height/1.8))
    x0S, y0S, x1S, y1S = start.getCoords(app)
    if x0S < event.x <= x1S and y0S < event.y <= y1S:
        app.mode = 'playerSettingMode'

# ##########################################
# # Player setting Mode
# ##########################################

def playerSettingMode_redrawAll(app, canvas):
    font = 'Baloo 28'
    
    canvas.create_text(app.width/2, app.height/2, 
                       text=app.message,
                       font=font, fill='black')
    canvas.create_text(app.width/7, app.height/8, 
                       text=f"Player number: {app.playerNum}",
                       font=font, fill='black')
    x0N, y0N, x1N, y1N = app.nextButton.getCoords(app)
    canvas.create_oval(x0N, y0N, x1N, y1N, fill='#FFC125', outline='#FFC125')
    canvas.create_text(app.width * 0.85, app.height * 0.8, text='next',
                       font='Baloo 24', fill='#8B5742')
    

def playerSettingMode_keyPressed(app, event):
    name = app.getUserInput('Please enter your name:)')
    if name == '':
        app.message = 'Please type in a valid name.'
    else:
        if app.playerNum < 4:
            if name != None:
                app.playerNum += 1
                app.message = 'Successfully add a player'
                app.playerNameList.append(name)
        if app.playerNum == 4:
                app.message = '''
                    Has reached the maximum of players. 
                    Let's start the game!
                '''
def playerSettingMode_mousePressed(app, event):
    x0N, y0N, x1N, y1N = app.nextButton.getCoords(app)
    if (x0N < event.x < x1N) and (y0N < event.y < y1N):
        if app.playerNum < 2:
            app.message = "Please add at least\n      two players."
        else:
            app.mode = 'mapChooseMode'
    

# ##########################################
# # Map Choose Mode
# ##########################################

def mapChooseMode_redrawAll(app, canvas):
    font = 'Baloo 28'
    canvas.create_text(app.width/2, app.height/8, 
                    text="Please press left and right key to choose the map",
                    font=font, fill='black')
    mapChooseMode_drawBoard(app, canvas)
    start = Button('start', (app.width*0.89, app.height*0.85))
    coord = start.getCoords(app)
    canvas.create_oval(coord, fill='#FFC125', outline='#FFC125')
    canvas.create_text(app.width*0.89, app.height*0.85, 
                       text='start',
                       font=font, fill='black')
    

def mapChooseMode_mousePressed(app, event):
    start = Button('start', (app.width*0.89, app.height*0.85))
    x0, y0, x1, y1 = start.getCoords(app)
    if x0 < event.x <= x1 and y0 < event.y <= y1:
        # set players
        colors = ['#00a2ff', '#ff004c', '#ffd900', '#8f02fa'] #blue, red, yellow,green
        for playerName in app.playerNameList:
            color = random.choice(colors)
            colors.remove(color)
            player = Player(playerName, color)
            app.playerInfo[player] = dict()

            loc = app.myBoard.getRandomPlace() #returns a tuple
            player.loc = loc
            
            app.playerInfo[player]["loc"] = player.loc
            app.playerInfo[player]["myTurn"] = player.myTurn
            app.playerInfo[player]["color"] = player.color
            ori = player.checkOri(app)
            player.ori = ori
        app.playerInfoKeysList = list(app.playerInfo)
        app.curPlayer = app.playerInfoKeysList[app.curPlayerIndex-1] #app.playerNameList[0]
        app.whoseTurn = app.curPlayer
        app.lastPlayer = app.playerInfoKeysList[0]
        
        # set grids in Board
        makeDetailedInfo(app)

        # modify app mode
        app.mode = 'gameMode'
        
    
    
def mapChooseMode_keyPressed(app, event):

    if event.key == 'Left':
        app.index = max(1, app.index-1)
    elif event.key == 'Right':
        app.index = min(app.index+1, 4)
    
    if app.index == 1:
        app.myBoard = Board(board1)
    elif app.index == 2:
        app.myBoard = Board(board2)
    elif app.index == 3:
        app.myBoard = Board(board3)
    elif app.index == 4:
        app.myBoard = Board(board4)
 


def makeDetailedInfo(app): #modify app.boardDetailedInfo

    nameList = ['Peak District', 'Lake District', 'Snowdonia', 'Dartmoor',
                'Pembrokeshire Coast', 'North York Moors','Yorkshire Dales',
                'Exmoor', 'Northumberland', 'Brecon Beacons', 'The Broads',
                'Cairngorms', 'New Forest', 'South Downs',
                'Royal Gorge Park', 'Falls Park', 'Scioto Audubon',
                'Rifle Mountain Park', 'Fairmount Park', 'City Park',
                'Zilker Park', 'The Gathering Place', 'Papago Park']
    events = ['Market Crash', 'Go to Jail', 'Get out of Jail Free',
            'Chairman', 'competition', 'poor tax', 'parking fee']
    index = 0
    app.boardDetailedInfo = dict()
    rows, cols = app.myBoard.getDims()
    for row in range(rows):
        for col in range(cols):
            coord = (row, col)

            if app.myBoard.map[row][col] != 0:

                if index == 7:
                    gridName = 'jail'
                    app.boardDetailedInfo[coord] = gridName
                    app.myBoard.map[row][col] = Grid(gridName, 0)
                    app.jailLoc = coord

                elif 0 < index % 8 % 4 <= 4:

                    if index % 8 % 4 == 1:
                        gridName = random.choice(events)
                        grid = app.myBoard.map[row][col] = chanceCards(gridName)
                        app.boardDetailedInfo[coord] = dict()
                        app.boardDetailedInfo[coord]['property name'] = 'chance'
                        app.boardDetailedInfo[coord]['event name'] = gridName
                        app.boardDetailedInfo[coord]['description'] = (
                                                                grid.description)
                    else:
                        gridName = None
                        gridPriceToBuy = 0
                        app.boardDetailedInfo[coord] = None

                else:
                    gridName = random.choice(nameList)
                    gridPriceToBuy = random.randint(3000, 6000)
                    app.boardDetailedInfo[coord] = dict()
                    app.myBoard.map[row][col] = Grid(gridName, gridPriceToBuy) #####
                    grid = app.myBoard.map[row][col]

                if ((gridName != None) and (gridName != 'jail') and 
                    (gridName not in events)):
                        nameList.remove(gridName)
                        app.boardDetailedInfo[coord]['property name'] = gridName
                        app.boardDetailedInfo[coord]['price to buy'] = (
                                                                gridPriceToBuy)
                        app.boardDetailedInfo[coord]['owner'] = 'No Owner'
                        app.boardDetailedInfo[coord]['level'] = grid.level
                        if grid.owner != None:
                            app.boardDetailedInfo[coord]['owner'] = grid.owner
                            app.boardDetailedInfo[coord]['cost to upgrade'] = (
                                                            grid.priceToUpgrade)
                            app.boardDetailedInfo[coord]['toll'] = (grid.toll)
                index += 1

def mapChooseMode_drawBoard(app, canvas):
    rows, cols = app.myBoard.getDims()
    for row in range(rows):
        for col in range(cols):
            if app.myBoard.map[row][col] != 0:
                cx = app.gridWidth * col + app.width * 0.4
                cy = app.gridHeight * row
                placeGrid(app, canvas, cx, cy)


##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):
    
    gameMode_drawButtons(app, canvas)
    gameMode_drawBoard(app, canvas)
    gameMode_drawPlayer(app, canvas)
    
    # msg of rolling dice
    if type(app.dice) != str:
        canvas.create_text(app.width*0.87 - app.width*0.015, 
                           app.height*0.85 - app.width*0.1, 
                           text=f"{app.lastPlayer} rolled {app.dice}.",
                           font='Baloo 24', fill='#50961b')
        
    if app.clickGrid:
        gameMode_drawGridInfo(app, canvas)
    
    if app.askBuy:
        gameMode_askBuy(app, canvas)
    elif app.askUpgrade:
        gameMode_askUpgrade(app, canvas)
    elif app.askToPayToll:
        gameMode_askToPayToll(app, canvas)
    elif app.displayChanceCards:
        gameMode_displayChanceCards(app, canvas)
    if app.askToUseJailCard:
        gameMode_askToUseJailCard(app, canvas)
    if app.askNewGame:
        gameMode_askNewGame(app, canvas)

    gameMode_drawMoneyAndPropertyCoin(app, canvas)
    gameMode_drawDice(app, canvas)

    if app.instructionButton.enabled:
        gameMode_drawInstruction(app, canvas)
    elif app.cardsButton.enabled:
        gameMode_drawCards(app, canvas)
    elif app.propertiesButton.enabled:
        gameMode_drawProperties(app, canvas)
    
    if app.bankrupcy:
        gameMode_displayBankrupcyMsg(app, canvas)
    
    if app.displayWinnerMsg:
        gameMode_drawWinnerMsg(app, canvas)

    if app.showSellButton:
        gameMode_showSellButton(app, canvas)
    if app.sellProperty:
        coord = app.row, app.col
        money = app.boardDetailedInfo[coord]['price to sell']
        text = f'You sold the land and got ${money}'
        font = 'Baloo 15'
        canvas.create_text(app.width/2, app.height/3, text=text, font=font)

def gameMode_askToUseJailCard(app, canvas):
    text = '''\
One of your Jail Cards is automatically used. You're exempt from the accusation'''
    font = 'Baloo 15'
    canvas.create_text(app.width/2, app.height/3, text=text, font=font)

def gameMode_drawWinnerMsg(app, canvas):
    text = f'Congrats! {app.curPlayer} is the last player.'
    font = 'Baloo 20'
    canvas.create_text(app.width/2, app.height/2.5, text=text, font=font)

def gameMode_displayBankrupcyMsg(app, canvas):
    text = f'{app.bankrupt} is declared bankrupt.'
    canvas.create_text(app.width*0.5, app.height*0.25, 
                       font='baloo 15', text=text)


def gameMode_drawButtons(app, canvas):
    font = 'Baloo 24'
    canvas.create_text(app.width/2, 20, text='Game',
                       font=font, fill='black')
    x0Ins, x1Ins = app.width * 0.85, app.width * 0.95
    y0Ins, y1Ins = app.height * 0.2, app.height * 0.3    
    canvas.create_oval(x0Ins, y0Ins, x1Ins, y1Ins,
                       fill='#FFC125', outline='#FFC125') # Instruction
    canvas.create_text(app.width * 0.83, app.height * 0.28, 
                       text="Instruction", anchor='sw',
                       fill='#8B5742', font=font)

    x0Card, x1Card = x0Ins, x1Ins
    y0Card, y1Card = app.height * 0.35, app.height * 0.45
    canvas.create_oval(x0Card, y0Card, x1Card, y1Card, 
                       fill='#FFC125', outline='#FFC125') # Special cards
    canvas.create_text(app.width * 0.865, app.height * 0.43, text="Cards",
                       anchor='sw', fill='#8B5742', font=font)
    
    x0P, x1P = x0Ins, x1Ins
    y0P, y1P = app.height * 0.5, app.height * 0.6
    canvas.create_oval(x0P, y0P, x1P, y1P, 
                       fill='#FFC125', outline='#FFC125') # Properties
    canvas.create_text(app.width * 0.833, app.height * 0.58, text="Properties",
                       anchor='sw', fill='#8B5742', font=font)


def gameMode_askNewGame(app, canvas):
    text = "Press 'y' to start a new game!"
    font = 'Baloo 30'
    canvas.create_text(app.width/2, app.height/2, text=text, 
                       font=font, fill='blue')


def gameMode_askBuy(app, canvas):
    text = 'Do you want to buy the land? y/n'
    font = 'Baloo 15'
    canvas.create_text(app.width/2, app.height/3, text=text, font=font)


def gameMode_askUpgrade(app, canvas):
    text = 'Do you want to upgrade the land? y/n'
    font = 'Baloo 15'
    canvas.create_text(app.width/2, app.height/3, text=text, font=font)


def gameMode_askToPayToll(app, canvas):    
    row, col = app.lastPlayer.loc
    grid = app.myBoard.map[row][col]
    pOwner = grid.owner
    text = f'''
Bad luck:(
You visited {pOwner}'s {grid.name} and have to 
pay a ${grid.toll} toll.
    '''
    font = 'Baloo 15'
    canvas.create_text(app.width/2, app.height/3, text=text, font=font)

    tollText = f'-         {grid.toll}'
    cx = app.width*0.64
    cy = app.height*0.283
    rCoin = app.width * 0.009
    x0, x1 = cx - rCoin, cx + rCoin
    y0, y1 = cy - rCoin, cy + rCoin
    canvas.create_oval(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
    canvas.create_text(cx, cy, text='$', fill='#8B5742', font=font)
    canvas.create_text(app.width*0.66, cy, 
                       text=tollText, font='Arial 13 bold', fill='#8B5742')


def gameMode_displayChanceCards(app, canvas):
    coord = app.row, app.col
    x0, y0 = app.width * 0.35, app.height * 0.35
    x1, y1 = app.width * 0.65, app.height * 0.65
    canvas.create_rectangle(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')

    title = 'Chance Card'
    canvas.create_text(app.width*0.5, app.height*0.5*0.9, 
                       font='baloo 15', text=title)
    text = f"{app.boardDetailedInfo[coord]['description']}"
    canvas.create_text(app.width*0.5, app.height*0.5, 
                       font='Arial 15', text=text)


def gameMode_drawMoneyAndPropertyCoin(app, canvas):
    # money coin
    for indexOfPlayer in range(len(app.playerInfoKeysList)):
        text = '$'
        font = 'Arial 10'
        cx = app.width*(indexOfPlayer+1)/4 - app.width/4*0.5
        cy = app.height*0.25*0.4*0.5
        rCoin = app.width * 0.009
        x0, x1 = cx - rCoin, cx + rCoin
        y0, y1 = cy - rCoin, cy + rCoin
        canvas.create_oval(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
        canvas.create_text(cx, cy, text=text, fill='#8B5742', font=font)

        money = app.playerInfoKeysList[indexOfPlayer].money
        cxM = cx + rCoin * 4
        cyM = cy
        canvas.create_text(cxM, cyM, text=money, font=font)
    
    # property coin
    for indexOfPlayer in range(len(app.playerInfoKeysList)):
        text = 'P'
        font = 'Arial 10'
        cx = app.width*(indexOfPlayer+1)/4 - app.width/4*0.5
        cy = (app.height*0.25*0.4*0.5)*1.8
        rCoin = app.width * 0.009
        x0, x1 = cx - rCoin, cx + rCoin
        y0, y1 = cy - rCoin, cy + rCoin
        canvas.create_oval(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
        canvas.create_text(cx, cy, text=text, fill='#8B5742', font=font)

        cxP = cx + rCoin * 4
        cyP = cy 
        property = len(app.playerInfoKeysList[indexOfPlayer].myProperties)
        canvas.create_text(cxP, cyP, text=property, font=font)
    
    # playerName
    for indexOfPlayer in range(len(app.playerInfoKeysList)):
        font = 'Arial 15'
        player = app.playerInfoKeysList[indexOfPlayer]
        cx = app.width*(indexOfPlayer+1)/4 - app.width*0.18
        cy = (app.height*0.25*0.4*0.5)*1.3
        if player == app.curPlayer:
            canvas.create_text(cx, cy, text=player, font=font, fill='#fa0217')
        else:
            canvas.create_text(cx, cy, text=player, font=font,  
                            fill='black')
        canvas.create_oval(cx-rCoin, cy*1.6-rCoin, cx+rCoin, cy*1.6+rCoin, 
                           fill=player.color, outline=player.color)
        if not player.activated:
            canvas.create_text(cx, cy*1.6, text='bankrupt', fill='black')
        

def gameMode_drawDice(app, canvas):
    x0S, x1S = app.width*0.87 - app.width*0.03, app.width*0.87 + app.width*0.03
    y0S, y1S = app.height*0.85 - app.width*0.03, app.height*0.85 + app.width*0.03
    canvas.create_rectangle(x0S, y0S, x1S, y1S, outline='#4f2f22', 
                            fill='#7d4d3b', width=4.5)

    p01 = x0S, y0S
    p02 = x1S, y0S
    p03 = x0S + app.width*0.0182, y0S - app.width*0.0182
    p04 = x1S + app.width*0.0182, y0S - app.width*0.0182
    canvas.create_polygon(p01, p02, p04, p03, 
                          outline='#4f2f22', fill='#5e3a2c', width=4.5)
    
    p11 = p04
    p12 = p02
    p13 = x1S, y1S
    p14 = x1S + app.width*0.0182, y1S - + app.width*0.0182
    canvas.create_polygon(p11, p12, p13, p14,
                          outline='#4f2f22', fill='#663f30', width=4.5)
    
    x0D, y0D, x1D, y1D = app.dieButton.getCoords(app)
    canvas.create_oval(x0D, y0D, x1D, y1D, fill='#FFC125', 
                            outline='#FFC125')
    canvas.create_text((x0D+x1D)/2, (y0D+y1D)/2, text='Roll', 
                       fill='#8B5742', font='Baloo 32')
    
    
def gameMode_mousePressed(app, event):
    if not app.isGameOver:
        # instruction page and special cards mode
        x0Ins, y0Ins, x1Ins, y1Ins = app.instructionButton.getCoords(app)
        x0Cards, y0Cards, x1Cards, y1Cards = app.cardsButton.getCoords(app)
        x0P, y0P, x1P, y1P = app.propertiesButton.getCoords(app)
        x0S, y0S, x1S, y1S = app.sellButton.getCoords(app)
        if ((not app.instructionButton.enabled) and 
            (x0Ins < event.x < x1Ins) and 
            (y0Ins < event.y < y1Ins)):
            app.instructionButton.enabled = True
        elif ((not app.cardsButton.enabled) and
            (x0Cards < event.x < x1Cards) and 
            (y0Cards < event.y < y1Cards)):
            app.cardsButton.enabled = True
        elif ((not app.propertiesButton.enabled) and
            (x0P < event.x < x1P) and
            (y0P < event.y < y1P)):
            app.propertiesButton.enabled = True
        elif ((x0S < event.x < x1S) and
              (y0S < event.y < y1S)):
              app.sellProperty = True
              app.displaySellPMsg = time.time()
              app.curPlayer.sellProperty(app)
              app.askUpgrade = False
              app.showSellButton = False

        

        # click grids
        Isox, Isoy = event.x, event.y
        twoDx, twoDy = isoToTwoD(Isox, Isoy)
        col = roundHalfUp((twoDx - app.width * 0.4) / app.gridWidth)
        row = roundHalfUp(twoDy / app.gridHeight)
        app.clickTime = time.time()

        if (((row, col) in app.boardDetailedInfo) and 
            (app.boardDetailedInfo[(row, col)] != None)):
            app.clickGrid = True
            app.gridInfo = app.boardDetailedInfo[(row, col)]
            app.gridClicked = (row, col)
        
        # roll a die
        x0R, y0R, x1R, y1R = app.dieButton.getCoords(app)
        if ((not app.payToll) and
            (not app.askBuy) and 
            (not app.askUpgrade) and 
            (not app.instructionButton.enabled) and
            (not app.cardsButton.enabled) and 
            (not app.propertiesButton.enabled) and
            (not app.askToUseJailCard)):
            if app.displayChanceCards or app.askToPayToll:
                app.displayChanceCards = False
                app.askToPayToll = False

            while (app.curPlayerIndex in app.bannedPlayerIndex):
                gameMode_changeTurn(app)

            if (((app.curPlayer in app.criminals) and 
                (app.criminals[app.curPlayer] > 0))):
                gameMode_changeTurn(app)
                while (app.curPlayerIndex in app.bannedPlayerIndex):
                    gameMode_changeTurn(app)

            if (x0R < event.x <= x1R) and (y0R < event.y <= y1R): # A player rolled the dice
                # after A rolled the dice, current turn changes
                for criminal in app.criminals:
                    app.criminals[criminal] -= 1
                app.dice = app.curPlayer.playDice()
                app.dieMsgTime = time.time()
                app.curPlayer.move(app, app.dice)
                
                row, col = app.curPlayer.loc
                app.row, app.col = row, col
                
                if ((app.boardDetailedInfo[(row, col)] != None) and
                    (app.myBoard.map[row][col].name != 'jail') and 
                    (app.boardDetailedInfo[(row, col)]['property name'] != 'chance')):
                    app.showSellButton = False
                    if app.boardDetailedInfo[(row, col)]['owner'] == None:
                        app.askBuy = True
                    elif app.boardDetailedInfo[(row, col)]['owner'] == app.curPlayer:
                        app.askUpgrade = True
                        app.showSellButton = True
                    elif app.boardDetailedInfo[(row, col)]['owner'] != app.curPlayer:
                        app.startToAskForToll = time.time()
                        app.askToPayToll = True
                        app.payToll = True  
                elif (app.boardDetailedInfo[(row, col)] != None and
                    app.myBoard.map[row][col].name == 'chance'):
                    app.displayCCtime = time.time()
                    app.displayChanceCards = True
                    app.playChanceCards = True

                app.lastPlayer = app.curPlayer
        
                if ((not app.askBuy) and 
                    (not app.askUpgrade) and
                    (not app.askToUseJailCard)):
                    gameMode_changeTurn(app)
                    while not app.curPlayer.activated:
                        gameMode_changeTurn(app)

def gameMode_changeTurn(app):
    app.curPlayerIndex = (app.curPlayerIndex + 1) % app.playerNum
    app.curPlayer.myTurn = 'False'
    nextPlayer = app.playerInfoKeysList[app.curPlayerIndex-1]
    app.curPlayer = nextPlayer
    app.curPlayer.myTurn = 'True'
    app.whoseTurn = nextPlayer
    
    
def gameMode_timerFired(app):
    if (app.clickGrid == True) and (time.time() - app.clickTime > 2):
        app.clickGrid = False
    updateDetailedInfoDict(app)
    if app.payToll:
        app.lastPlayer.payToll(app)
        app.payToll = False

    if (app.askToPayToll) and (time.time() - app.startToAskForToll > 3.7):
        app.askToPayToll = False
    
    if ((type(app.dice) != str) and (time.time() - app.dieMsgTime > 2.5)):
        app.dice = ''
    
    if app.playChanceCards:
        gameMode_playChanceCards(app)
        app.playChanceCards = False
    if (app.displayChanceCards) and (time.time() - app.displayCCtime > 2.2):
        app.displayChanceCards = False

    if app.bankrupcy and (time.time() - app.bankrupcyTime > 2):
        app.bankrupcy = False
    
    if app.lastPlayer.money <= 0:
        app.bankrupcy = True
        app.bankrupcyTime = time.time()
        app.bankrupt = f'{app.lastPlayer.playerName}'
        app.lastPlayer.activated = False
        app.bannedPlayerIndex.add((app.curPlayerIndex - 1 + app.playerNum) % 
                                  app.playerNum)
        for eachProperty in app.lastPlayer.myProperties:
            eachProperty.selling()  

    if len(app.bannedPlayerIndex) + 1 == app.playerNum:
        app.winnerMsgTime = time.time()
        app.winner = True
        while (app.curPlayerIndex in app.bannedPlayerIndex):
            gameMode_changeTurn(app)
        app.askBuy = app.askUpgrade = app.askToUseJailCard = False
        app.askNewGame = True

    if app.winner:
        app.displayWinnerMsg = True
        app.bankrupcy = False
        app.isGameOver = True

    if app.askToUseJailCard and (time.time() - app.displayJailCardMsg > 1.7):
        app.askToUseJailCard = False
    if app.sellProperty and (time.time() - app.displaySellPMsg > 1.7):
        app.sellProperty = False
 
def gameMode_playChanceCards(app): #need to improve
    row, col = app.row, app.col
    coord = row, col
    event = app.boardDetailedInfo[coord]['event name']
    if event == 'Market Crash':
        for eachPlayer in app.playerInfo:
            eachPlayer.money -= 2000
    elif event == 'Go to Jail':
        if 'Get out of Jail Free' in app.lastPlayer.cards:
            app.askToUseJailCard = True
            app.displayJailCardMsg = time.time()
            app.lastPlayer.cards.remove('Get out of Jail Free')
        else:
            app.lastPlayer.loc = app.jailLoc
            app.playerInfo[app.lastPlayer]['loc'] = app.jailLoc
            app.criminals[app.lastPlayer] = 3 * (len(app.playerInfoKeysList)-1)
    elif event == 'Get out of Jail Free':
        app.lastPlayer.cards += ['Get out of Jail Free']
    elif event == 'Chairman':
        restPlayers = copy.copy(app.playerInfoKeysList)
        restPlayers.remove(app.lastPlayer)
        for eachPlayer in restPlayers:
            eachPlayer.money += 500
            app.lastPlayer.money -= 500
    elif event == 'competition':
        app.lastPlayer.money += 900
    elif event == 'poor tax':
        app.lastPlayer.money -= 120
    elif event == 'parking fee':
        app.lastPlayer.money -= 500

        
def gameMode_drawGridInfo(app, canvas):
    row, col = app.gridClicked
    gridcx, gridcy = app.gridWidth * col + app.width * 0.4, app.gridHeight * row
    gridIsocx, gridIsocy = twoDToIso(gridcx, gridcy)
    x0, y0 = gridIsocx - app.width * 0.07, gridIsocy - app.height * 0.14
    x1, y1 = gridIsocx + app.width * 0.07, gridIsocy - app.height * 0.02
    canvas.create_rectangle(x0, y0, x1, y1, fill = '#FFEC8B')

    if app.gridInfo == 'jail':
        text = 'Jail'
        font = 'Baloo 14'
        canvas.create_text(gridIsocx, (y1+y0)/2, 
                           text=text, font=font, fill='black')
    elif app.gridInfo['property name'] == 'chance':
        text = 'Chance Cards'
        font = 'Baloo 14'
        canvas.create_text(gridIsocx, (y1+y0)/2, 
                           text=text, font=font, fill='black')
    else:
        text = ''
        font = 'Arial 9'
        for key in app.gridInfo:
            if key == 'property name':
                text += f'{key} :\n{app.gridInfo[key]}\n'
            else:
                if app.myBoard.map[row][col].owner == None:
                    if key == 'cost to upgrade':
                        continue
                elif app.myBoard.map[row][col].owner != None:
                    if key == 'price to buy':
                        continue
                text += f'{key} : {app.gridInfo[key]}\n'
        canvas.create_text(gridIsocx, (y1+y0)/2, 
                            text=text, font=font, fill='black')


def gameMode_drawPlayer(app, canvas):
    
    for eachPlayer in app.playerInfo:  
        if eachPlayer.activated:   
            loc = app.playerInfo[eachPlayer]['loc'] #returns a tuple
            twoDRow, twoDCol = loc[0], loc[1]
            cx = app.gridWidth * twoDCol + app.width * 0.4
            cy = app.gridHeight * twoDRow
            isoX, isoY = twoDToIso(cx, cy)
            playerRadius = 9
            x0 = isoX - playerRadius
            y0 = isoY - playerRadius
            x1 = isoX + playerRadius
            y1 = isoY + playerRadius
            canvas.create_oval(x0, y0, x1, y1, fill=eachPlayer.color)


def updateDetailedInfoDict(app):
    rows, cols = app.myBoard.getDims()
    for row in range(rows):
        for col in range(cols):
            if (isinstance(app.myBoard.map[row][col], Grid) and 
                app.myBoard.map[row][col] != 1 and 
                app.myBoard.map[row][col].name != 'jail'):

                grid = app.myBoard.map[row][col]
                coord = (row, col)
                app.boardDetailedInfo[coord]['price to buy'] = grid.priceToBuy
                app.boardDetailedInfo[coord]['owner'] = grid.owner
                app.boardDetailedInfo[coord]['cost to upgrade'] = (
                grid.priceToUpgrade)
                app.boardDetailedInfo[coord]['toll'] = grid.toll
                app.boardDetailedInfo[coord]['level'] = grid.level
                app.boardDetailedInfo[coord]['price to sell'] = grid.priceToSell



###########
#draw map
###########

def gameMode_drawBoard(app, canvas):
    rows, cols = app.myBoard.getDims()
    for row in range(rows):
        for col in range(cols):
            if app.myBoard.map[row][col] != 0:
                cx = app.gridWidth * col + app.width * 0.4
                cy = app.gridHeight * row
                
                if app.boardDetailedInfo[(row, col)] == 'jail':
                    placeJailGrid(app, canvas, cx, cy)
                elif app.boardDetailedInfo[(row, col)] == None:
                    placeNoneGrid(app, canvas, cx, cy)
                elif (app.boardDetailedInfo[(row, col)]['property name'] == 
                                                            'chance'):
                    placeChanceCards(app, canvas, cx, cy)
                else:
                    if app.myBoard.map[row][col].owner != None:
                        placeOccupiedGrid(app, canvas, cx, cy, row, col)
                    else:
                        placeGrid(app, canvas, cx, cy)

def placeGrid(app, canvas, cx, cy):
    coordCenterS = getGridCenterSquareCoord(app, cx, cy)
    coordLeftSide = getGridLeftSideCoord(app, cx, cy)
    coordRightSide = getGridRightSideCoord(app, cx, cy)
    canvas.create_polygon(coordLeftSide, fill='#50961b', outline='#438710')
    canvas.create_polygon(coordRightSide, fill='#316e03', outline='#214a01')
    canvas.create_polygon(coordCenterS, fill='#64b02a', outline='#50941c')


def placeOccupiedGrid(app, canvas, cx, cy, row, col):
    color = app.myBoard.map[row][col].owner.color
    coordCenterS = getGridCenterSquareCoord(app, cx, cy)
    coordLeftSide = getGridLeftSideCoord(app, cx, cy)
    coordRightSide = getGridRightSideCoord(app, cx, cy)
    if color == '#00a2ff':
        color2 = '#0287d4'
        color3 = '#0273b5'
    elif color == '#ff004c':
        color2 = '#e30245'
        color3 = '#bf023a'
    elif color == '#ffd900':
        color2 = '#e0bf02'
        color3 = '#bfa302'
    elif color == '#8f02fa':
        color2 = '#7c02d9'
        color3 = '#5c02a1'
    canvas.create_polygon(coordLeftSide, fill=color2, outline=color2)
    canvas.create_polygon(coordRightSide, fill=color3, outline=color3)
    canvas.create_polygon(coordCenterS, fill=color, outline=color2)


def placeJailGrid(app, canvas, cx, cy):
    coordCenterS = getGridCenterSquareCoord(app, cx, cy)
    coordLeftSide = getGridLeftSideCoord(app, cx, cy)
    coordRightSide = getGridRightSideCoord(app, cx, cy)
    canvas.create_polygon(coordLeftSide, fill='#f7b60f', outline='#f7b302')
    canvas.create_polygon(coordRightSide, fill='#e6a602', outline='#e6a602')
    canvas.create_polygon(coordCenterS, fill='#FFC125', outline='#fcb80a')


def placeNoneGrid(app, canvas, cx, cy):
    coordCenterS = getGridCenterSquareCoord(app, cx, cy)
    coordLeftSide = getGridLeftSideCoord(app, cx, cy)
    coordRightSide = getGridRightSideCoord(app, cx, cy)
    canvas.create_polygon(coordLeftSide, fill='#7d4d3b', outline='#61392b')
    canvas.create_polygon(coordRightSide, fill='#663f30', outline='#4f2f22')
    canvas.create_polygon(coordCenterS, fill='#8B5742', outline='#5e3a2c')


def placeChanceCards(app, canvas, cx, cy):
    coordCenterS = getGridCenterSquareCoord(app, cx, cy)
    coordLeftSide = getGridLeftSideCoord(app, cx, cy)
    coordRightSide = getGridRightSideCoord(app, cx, cy)
    canvas.create_polygon(coordLeftSide, fill='#98def5', outline='#6ed4f5')
    canvas.create_polygon(coordRightSide, fill='#39c8f7', outline='#1dc0f5')
    canvas.create_polygon(coordCenterS, fill='#BFEFFF', outline='#9AC0CD')


def getGridCenterSquareCoord(app, twoDcx, twoDcy):
    Isocx, Isocy = twoDToIso(twoDcx, twoDcy)
    isox00, isoy00 = Isocx, Isocy - app.gridHeight/2
    isox01, isoy01 = Isocx + app.gridWidth, Isocy
    isox02, isoy02 = Isocx, Isocy + app.gridHeight/2
    isox03, isoy03 = Isocx - app.gridWidth, Isocy
    coordCenterS = (isox00, isoy00, isox01, isoy01, isox02, isoy02, 
                    isox03, isoy03)
    return coordCenterS


def getGridLeftSideCoord(app, twoDcx, twoDcy):
    Isocx, Isocy = twoDToIso(twoDcx, twoDcy)
    isox10, isoy10 = Isocx - app.gridWidth, Isocy
    isox11, isoy11 = Isocx, Isocy + app.gridHeight/2
    isox13, isoy13 = isox11, isoy11 + app.gridThickness
    isox12, isoy12 = isox10, isoy10 + app.gridThickness
    coordLeftSide = (isox10, isoy10, isox11, isoy11, isox13, isoy13,
                     isox12, isoy12)
    return coordLeftSide


def getGridRightSideCoord(app, twoDcx, twoDcy):
    Isocx, Isocy = twoDToIso(twoDcx, twoDcy)
    isox20, isoy20 = Isocx, Isocy + app.gridHeight/2
    isox21, isoy21 = Isocx + app.gridWidth, Isocy
    isox22, isoy22 = Isocx + app.gridWidth, Isocy + app.gridThickness
    isox23, isoy23 = Isocx, Isocy + app.gridHeight/2 + app.gridThickness
    coordRightSide = (isox20, isoy20, isox21, isoy21, isox22, isoy22,
                      isox23, isoy23)
    return coordRightSide


##################
# Instruction and Cards Canvas
##################

def gameMode_drawInstruction(app, canvas):
    x0, y0 = app.width * 0.2, app.height * 0.2
    x1, y1 = app.width * 0.8, app.height * 0.8
    canvas.create_rectangle(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
    font = 'Baloo 23'
    text = 'Instruction'
    command = "press 'esc' to return"
    brown = '#8B5742'
    canvas.create_rectangle(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
    canvas.create_text((x0+x1)/2, (y0+y1)*0.25, text=text, fill=brown, font=font)
    canvas.create_text((x0+x1)/2, (y0+y1)*0.75, text=command, font='Times 15')

    text1 = 'As you walk on the map, you will see grids of various colors.'
    canvas.create_text((x0+x1)/2, (y0+y1)*0.36, text=text1, font='Baloo 17')
    cx0, cy0 = (x0+x1)*0.44, (y0+y1)*0.23
    cx1, cy1 = (x0+x1)*0.48, (y0+y1)*0.23
    cx2, cy2 = (x0+x1)*0.52, (y0+y1)*0.23
    cx3, cy3 = (x0+x1)*0.56, (y0+y1)*0.23
    
    font2 = 'Times 14'
    placeGrid(app, canvas, cx0, cy0)
    textG = '''\
Properties. Click them on the map to see detials.\
'''
    canvas.create_text((x0+x1)*0.5, (y0+y1)*0.42, text=textG, font=font2)
    placeJailGrid(app, canvas, cx1, cy1)
    textY = "Jail. People in jail are forbidden to walk."
    canvas.create_text((x0+x1)*0.53, (y0+y1)*0.457, text=textY, font=font2)
    placeNoneGrid(app, canvas, cx2, cy2)
    textBrown = 'Land. You cannot purchase them.'
    canvas.create_text((x0+x1)*0.53, (y0+y1)*0.49, text=textBrown, font=font2)
    placeChanceCards(app, canvas, cx3, cy3)
    textBlue = 'Chance cards. You may lose or get.'
    canvas.create_text((x0+x1)*0.58, (y0+y1)*0.525, text=textBlue, font=font2)
    font3='Baloo 15'
    text2 = '''The bar at the top of the page displays the total amount of money
and the number of properties owned by each player.
'''
    canvas.create_text((x0+x1)/2, (y0+y1)*0.635, text=text2, font=font3)

    text3 = '''If your name is in red in the bar, it's your turn to throw a dice
and move. Press y/n to make decisions.
'''
    canvas.create_text((x0+x1)/2, (y0+y1)*0.72, text=text3, font=font3)


def gameMode_drawCards(app, canvas):
    x0, y0 = app.width * 0.2, app.height * 0.2
    x1, y1 = app.width * 0.8, app.height * 0.8
    font = 'Baloo 20'
    title = 'Cards you have'
    cards = ''
    brown = '#8B5742'
    for eachCard in app.curPlayer.cards:
        cards += eachCard
    command = "press 'esc' to return"
    canvas.create_rectangle(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
    canvas.create_text((x0+x1)/2, (y0+y1)*0.3, text=title, fill=brown, font='Baloo 23')
    canvas.create_text((x0+x1)/2, (y0+y1)*0.55, text=cards, font=font)
    canvas.create_text((x0+x1)/2, (y0+y1)*0.75, text=command, font='Times 15')

def gameMode_drawProperties(app, canvas):
    x0, y0 = app.width * 0.2, app.height * 0.2
    x1, y1 = app.width * 0.8, app.height * 0.8
    font = 'Baloo 20'
    title = 'Properties you have'
    properties = ''
    brown = '#8B5742'
    for eachP in app.curPlayer.myProperties:
        properties += f'{eachP}   '
    command = "press 'esc' to return"
    canvas.create_rectangle(x0, y0, x1, y1, fill='#FFC125', outline='#FFC125')
    canvas.create_text((x0+x1)/2, (y0+y1)*0.3, text=title, 
                       fill=brown, font='Baloo 23')
    canvas.create_text((x0+x1)/2, (y0+y1)*0.45, text=properties, 
                       fill=brown, font=font)
    canvas.create_text((x0+x1)/2, (y0+y1)*0.75, text=command, font='Times 15')

def gameMode_showSellButton(app, canvas):
    font = 'Baloo 24'
    x0, x1 = app.width * 0.85, app.width * 0.95
    y0, y1 = app.height * 0.65, app.height * 0.75
    canvas.create_oval(x0, y0, x1, y1, 
                       fill='#FFC125', outline='#FFC125') # Properties
    canvas.create_text(app.width * 0.88, app.height * 0.73, text="Sell",
                       anchor='sw', fill='#8B5742', font=font)



