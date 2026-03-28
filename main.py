import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import pygame
pygame.mixer.init()
from gtts import gTTS
import json
import math

def loadSettings() -> dict:
    '''
    Loads settings, initializes to default settings if settings file doesn't exist
    
    :return: Dictionary of settings
    :rtype: dict
    '''
    try: # If file exists load it, otherwise load and write default settings
        with open('files\\settings.json', 'r') as settinginit:
            return json.load(settinginit)
    except:
        with open('files\\settings.json', 'w') as settinginit:
            defaults = '{"Text to speech": false, "Sound": true, "Columns": [0, 7], "Max speaking time": 10000.0, "Output file": ""}'
            settinginit.write(defaults)
            return json.loads(defaults)

def printHelp():
    '''
    Help printer
    '''
    print(
"""printcols: Prints column names and numbers. Can also be typed after query to print all columns of query

-c: Clear console. Will still run command if combined with another one.

changefile: Prompts to change file

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
    '''
    Integer input validation
    
    :param prompt: User input prompt
    :type prompt: str
    :param minimum: Minimum valid input value
    :type minimum: float
    :param maximum: Maximum valid input value
    :type maximum: float
    :return: The first valid integer input by the user
    :rtype: int
    '''
    running = True
    while running:
        try:
            response = int(input(prompt))
            running = not minimum <= response <= maximum
        except:
            print("Invalid input. Please try again.")
    return response

def getFloat(prompt:str, minimum:float=-math.inf, maximum:float=math.inf) -> float:
    '''
    Float input validation
    
    :param prompt: User input prompt
    :type prompt: str
    :param minimum: The lowest valid value
    :type minimum: float
    :param maximum: The highest valid value
    :type maximum: float
    :return: The first value input by the user which is valid
    :rtype: float
    '''
    running = True
    while running:
        try:
            response = float(input(prompt))
            running = not minimum <= response <= maximum
        except:
            print("Invalid input. Please try again.")
    return response

def fileToLines(filename:str) -> list[str]:
    '''
    Takes in a filename and outputs list of lines
    
    :param filename: Name of file
    :type filename: str
    :return: List of lines of file
    :rtype: list[str]
    '''
    with open(filename, 'r') as file:
        return file.readlines()

def getFile() -> list[str]:
    '''
    Prompts user to ask which text file they are using
    
    :return: List of strings which are lines from the file
    :rtype: list[str]
    '''
    filepath = os.path.dirname(os.path.abspath(__file__))
    texts = []
    for dirfile in os.listdir(filepath):
        if dirfile.endswith('.txt'):
            texts.append(dirfile)
    if len(texts) > 1:
        print(*map(lambda t: f"{t[0]+1}: {t[1]}", enumerate(texts)), sep="\n")
        textfile = fileToLines(texts[getInt("Which number text file are you using?: ", 1, len(texts))-1])
    elif len(texts) == 1:
        textfile = fileToLines(texts[0])
    else:
        print("There are no text files in your directory!")
        textfile = ("Hi, I'm nothing")
    return textfile

def optionValidate(prompt:str, *args, invalid="Invalid input. Please try again.") -> str:
    '''
    Validates that a user-input string is in the list `args`
    
    :param prompt: Printed to prompt user for input
    :type prompt: str
    :param args: List of valid inputs
    :param invalid: Printed when input invalid
    :return: A valid string input by user
    :rtype: str
    '''
    while True:
        answer = input(prompt)
        if answer.split()[0] in args:
            return answer
        print(invalid)


def settingsMenu(settings:dict, columns:list[str]):
    '''
    Menu for settings
    
    :param settings: The dictionary of current settings the user has
    :type settings: str
    :param columns: The columns in the text file currently used
    :type columns: list[str]
    '''
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
            elif setting == "Output file":
                print(f"{index + 1}: {setting} is {values if values else 'off'}")
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
                print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(columns.split())), sep="\n")
                settingCommand = optionValidate("Type your action (add/remove/rewrite) and column number(s): ", 'add', 'remove', 'rewrite')
                temp = settingCommand.split()
                settingCommand = []
                for ind, col in enumerate(temp):
                    try:
                        settingCommand.append(int(col) if ind > 0 else col)
                    except:
                        continue
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
                settings['Max speaking time'] = str(getFloat("What is your desired maximum speaking time? (seconds): ", 0))
            case '5':
                settings['Output file'] = input('What file should output be appended to? (filename): ')
            case 'save':
                with open(r'files\settings.json', 'w') as file:
                    json.dump(settings, file)
                adjusting = False

def logicLoop(textfile:list[str], filepath:str, command:str, settings:dict, allem:bool):
    '''
    The core functionality of the program. Takes user input, searches for valid lines, converts to text to speech, plays success/fail sound.
    
    :param textfile: The list of lines of the selected text file
    :type textfile: list[str]
    :param filepath: The directory that the program is in
    :type filepath: str
    :param command: The user's command, what they want to find in the file lines
    :type command: str
    :param settings: Dictionary of user settings
    :type settings: dict
    :param allem: Whether or not to print all lines
    :type allem: bool
    '''
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
            if settings['Output file']:
                with open(settings['Output file'], 'a') as file:
                    file.write(printed.rstrip().replace('\n', '\t')+'\n')

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
            case "changefile":
                textfile = getFile()
            case _:
                logicLoop(textfile, os.path.dirname(os.path.abspath(__file__)), command.replace("printcols", '').strip(), settings, 'printcols' in command)
                
if __name__ == "__main__":
    main()