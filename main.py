import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import pygame
pygame.mixer.init()
from gtts import gTTS
import json
import math

def loadSettings() -> dict:
    '''Settings loader'''
    try: # If file exists load it, otherwise load and write default settings
        with open('files\\settings.json', 'r') as settinginit:
            return json.load(settinginit)
    except:
        with open('files\\settings.json', 'w') as settinginit:
            defaults = """{
        "Text to speech": true,
        "Sound": true,
        "Columns": [
            0,
            7
        ],
        "Max speaking time": 10000.0
    }"""
            settinginit.write(defaults)
            return json.loads(defaults)

def printHelp():
    print(
"""printcols: Prints column names and numbers. Can also be typed after query to print all columns of query

-c: Clear console. Will still run command if combined with another one.

filechange: Prompts to change file

exit: exits

settings: accesses settings
    Sound: if sound should be enabled
    Text to speech: If text to speech should be enabled
    Columns: Selection of what columns should be printed when an item is found
        
        action examples: 
        rewrite 0 7 10 20
        remove 10 20
        add 5
        result: 0 5 7

        remove: removes the following columns
        rewrite: deletes all columns except for ones input
        add: adds numbers to printed columns""")

def getInt(prompt:str, minimum:float=-math.inf, maximum:float=math.inf) -> int:
    '''Input validation for ints'''
    running = True
    while running:
        try:
            response = int(input(prompt))
            running = not minimum <= response <= maximum
        except:
            print("Invalid input. Please try again.")
    return response

def getFloat(prompt:str, minimum:float=-math.inf, maximum:float=math.inf) -> float:
    '''Input validation for floats'''
    running = True
    while running:
        try:
            response = float(input(prompt))
            running = not minimum <= response <= maximum
        except:
            print("Invalid input. Please try again.")
    return response

def fileToLines(filename:str) -> list[str]:
    '''Takes in string filename and returns a list of strings which are the file's lines'''
    with open(filename, 'r') as file:
        return file.readlines()

def getFile() -> list[str]:
    filepath = os.path.dirname(os.path.abspath(__file__))
    texts = []
    for dirfile in os.listdir(filepath):
        if dirfile.endswith('.txt'):
            texts.append(dirfile)
    if len(texts) > 1:
        print(*map(lambda t: f"{t[0]+1}: {t[1]}", enumerate(texts)), sep="\n")
        textfile = fileToLines(texts[getInt("Which number text file are you using?: ", 1, len(texts))-1])
    else:
        textfile = fileToLines(texts[0])
    return textfile

def settingsMenu(settings, columns):
    adjusting = True
    while adjusting:
        for index, [setting, values] in enumerate(settings.items()):
            if type(values) == type(True):
                print(f"{index + 1}: {setting} is {'on' if values else 'off'}")
            elif type(values) == type([]):
                print(f"{index + 1}: Columns printed: ", end="")
                for column in values:
                    print(column, end=' ')
                print()
            else:
                print(f"{index + 1}: {setting} is {values}")
        print("save: Save settings and exit")
        settingCommand = input("Enter the index of your change: ")
        match settingCommand:
            case '1':
                settings['Text to speech'] = not settings['Text to speech']
                print(f"Text to speech is now {'on' if settings['Text to speech'] else 'off'}")
            case '2':
                settings['Sound'] = not settings['Sound']
                print(f"Sound is now {'on' if settings['Sound'] else 'off'}")
            case '3':
                print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(columns)), sep="\n")
                settingCommand = input("Type your action (add/remove/rewrite) and column number(s): ")
                settingCommand = settingCommand.split()
                settingCommand = [int(col) if ind > 0 else col for ind, col in enumerate(settingCommand)]
                match settingCommand[0]:
                    case 'add':
                        for column in settingCommand[1:]:
                            settings['Columns'].append(column)
                    case 'remove':
                        settings['Columns'] = [column for column in settings['Columns'] if column not in settingCommand[1:]]
                    case 'rewrite':
                        settings['Columns'] = settingCommand[1:]
                settings['Columns'] = list(set(settings['Columns']))
            case '4':
                settings['Max speaking time'] = str(getFloat("What is your desired maximum speaking time? (seconds): "))
            case 'save':
                adjusting = False

def logicLoop(textfile, filepath, command, settings, allem):
    '''The main logic of find -> play sound'''
    found = False
    for line in textfile:
        if command.lower() in line.lower():
            printed = ""
            for num in range(len(textfile[0])):
                if num in settings['Columns'] or allem:
                    printed += f"{textfile[0].split('\t')[num]}: {line.split('\t')[num]}\n"
            print(printed.rstrip())
            found = True
    if not found:
        if settings['Sound']:
            pygame.mixer.music.load(f'{filepath}\\files\\sounds\\no.mp3')
            pygame.mixer.music.play()
        print(f"\033[31m({command}) not found in file\033[0m")
    else:
        if settings['Sound']:
            if settings['Text to speech']:
                readFile = gTTS(printed)
                readFile.save('files\\sounds\\temp.mp3')
                pygame.mixer.music.load(f'{filepath}\\files\\sounds\\temp.mp3')
                pygame.mixer.music.play()
                start = time.time()
                while True:
                    if not pygame.mixer.music.get_busy():
                        break
                    if time.time() - start >= float(settings['Max speaking time']):
                        break
                    time.sleep(0.05)
            pygame.mixer.music.load(f'{filepath}\\files\\sounds\\yes.mp3')
            pygame.mixer.music.play()

def main():
    settings = loadSettings()
    textfile = getFile()
    running = True
    while running:
        command = input("Please input code or (help): ")
        if ' -c' in command:
            os.system('cls')
        match command:
            case "help":
                printHelp()
            case 'printcols':
                print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(textfile[0])), sep="\n")
            case 'clear':
                os.system('cls')
            case 'settings':
                settingsMenu(settings, textfile[0])
            case 'exit':
                running = False
            case "filechange":
                textfile = getFile()
            case _:
                logicLoop(textfile, os.path.dirname(os.path.abspath(__file__)), command.replace("printcols", '').strip(), settings, 'printcols' in command)
                
if __name__ == "__main__":
    main()