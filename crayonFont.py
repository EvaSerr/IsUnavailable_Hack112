import string
from cmu_112_graphics import *
from tkinter import *
from PIL import *
from crayonify import *

def appStarted(app):
    app.inputText = ""
    app.inputLength = 0
    app.crayon = False
    app.inputTextList = []
    app.translatedList = []
    app.cx = app.width/2
    app.cy = app.height/2
    app.xMargin = app.width/10
    app.yMargin = app.height/10
    app.charactersLeft = 280 #based on Twitter
    app.specialCases = {" ":"space", "*":"asterisk", ")":"cparen", 
                        "\\":"bslash",":":"colon", "/":"fslash", 
                        ">":"greaterthan", "<":"lessthan", "(":"oparen",
                        "?":"qmark", "'":"singlequote", '"':"quote",
                        "#":"pound", ".":"period", "~":"tilde"}
    
    app.rows = 20  
    app.cols = 20 
    app.imageName = ''
    app.angle = 0

    app.gridWidth  = app.width - 2*app.xMargin
    app.gridHeight = app.height - 2*app.yMargin
    app.cellWidth = int(app.gridWidth / app.cols)
    app.cellHeight = int(app.gridHeight / app.rows)

    app.enterCount = 0
    app.carpeDiem = False

def keyPressed(app, event):
    if event.key == 'Enter':
        translatedText = crayonify(app.inputText)
        translatedText = adjustText(app, translatedText)
        app.translatedList = stringtoList(app, translatedText)
        while (len(app.translatedList)<app.rows*app.cols):
            app.translatedList.append("space")
        app.crayon = True
        app.enterCount += 1
        if app.enterCount > 1:
            app.carpeDiem = True
        #move on from input page to crayon text page
    
    if not app.crayon:
        if event.key == 'Space':
            app.inputText += ' '
            app.inputTextList.append('space')
            app.charactersLeft -= 1
        elif event.key == 'Tab':
            app.inputText += '\t'
            app.charactersLeft -= 8 #or 4 I am not sure how much for Twitter
        elif event.key == 'Backspace':
            app.inputText = app.inputText[:-1]
            if(len(app.inputTextList)>0):
                app.inputTextList.pop()
            if app.charactersLeft < 280:
                app.charactersLeft += 1
        elif (event.key in string.ascii_letters or 
             event.key in string.punctuation): 
                if event.key in app.specialCases:
                    app.inputTextList.append(app.specialCases[event.key])
                elif event.key == 'a' or event.key == 'A':
                    app.translatedList.append('A')
                else:
                    app.inputTextList.append(event.key)
                    app.charactersLeft -= 1
                app.imageName = event.key
                app.inputText += event.key
                  
def getCellBounds(app, row, col):
    #From https://tinyurl.com/y33txaud
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    x0 = app.xMargin + col * app.cellWidth
    x1 = app.xMargin + (col+1) * app.cellWidth
    y0 = app.yMargin + row * app.cellHeight
    y1 = app.yMargin + (row+1) * app.cellHeight
    return (x0, y0, x1, y1)

def stringtoList(app, text):
    textList = list(text)
    for i in range(len(textList)):
        if textList[i] in app.specialCases:
            textList[i] = app.specialCases[textList[i]]
        elif textList[i] == 'a':
            textList[i] = "A"
    return textList

#makes words wraparound!
def adjustText(app, text):
    for i in range(0, len(text), app.cols):
        if (text[i]!=" " or text[i+1]!=" "): 
            
            leftCount = 1
            #add spaces until word is on next line
            while (text[i]!=" "):
                leftCount += 1
                i -= 1
            
            text = text[:i]+" "*leftCount+text[i:]
    return text

def timerFired(app):
    app.gridWidth  = app.width - 2*app.xMargin
    app.gridHeight = app.height - 2*app.yMargin
    app.cellWidth = int(app.gridWidth / app.cols)
    app.cellHeight = int(app.gridHeight / app.rows)
    app.angle += 10
 
def getGridIndex(app, row, col):
    stringIndex = row*app.cols+col
    return stringIndex

def drawTitle(app, canvas):
    offset = app.height/20
    canvas.create_text(app.width/2, offset, text = "C R A Y O N I F Y (not ©)",
                        font = f'Lohit_Punjabi 50 bold underline', 
                        fill = 'red')

def drawInputPage(app, canvas):
    # type out input text on screen
    offset = app.height/20
    canvas.create_text(app.width/2, app.height/2-offset-10, 
                            text='Enter your text below:',
                            font = f'Lohit_Punjabi 50 bold')
    canvas.create_text(app.width/2, app.height/2, text=app.inputText,
                       font=f"Lohit_Punjabi 50 bold italic")
    canvas.create_text(app.width, app.height-offset, 
        text = f'Characters left: {app.charactersLeft}', 
        font = f'Lohit_Punjabi 30 bold', anchor = 'e')
    
def drawCrayonPage(app, canvas): # adding images
    for row in range(app.rows):
        for col in range(app.cols):
            index = getGridIndex(app, row, col)
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            extension = '.jpg'
            if (app.translatedList[index].isalpha() and 
                app.translatedList[index] in string.ascii_uppercase):
                extension = '.jpeg'
            img = Image.open(f'{app.translatedList[index]}{extension}')
            image = img.resize((app.cellWidth, app.cellHeight), Image.ANTIALIAS)  
            myImg = ImageTk.PhotoImage(image)
            canvas.create_image(x0, y0, anchor=NW, image=myImg)
                   
def redrawAll(app, canvas):
    if not app.carpeDiem:
        drawTitle(app, canvas)
        if app.crayon == False:
            drawInputPage(app, canvas)
        else:
            drawCrayonPage(app, canvas)
    else:
        img2 = Image.open('eserre.jpg')
        image = img2.resize((app.width, app.height), Image.ANTIALIAS)  
        myImg2 = ImageTk.PhotoImage(image.rotate(app.angle))
        canvas.create_image(0, 0, anchor=NW, image=myImg2)

        canvas.create_image(0, 0, anchor=NW, image=myImg2)

        canvas.create_image(0, 0, anchor=NW, image=myImg2)

        canvas.create_image(0, 0, anchor=NW, image=myImg2)

        canvas.create_image(0, 0, anchor=NW, image=myImg2)


def crayonFont():
    runApp(width=1000, height=1000) #can change borders later

crayonFont()