import json

import os
from gtts import gTTS
import time
with open('files\\settings.json', 'r') as settinginit:
    settings = json.load(settinginit)
print(settings)
filepath = os.path.dirname(os.path.abspath(__file__))
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
texts = []
for dirfile in os.listdir(filepath):
    if '.txt' in dirfile:
        texts.append(dirfile)
if len(texts) > 1:
    print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(texts)), sep="\n")
    jerry = open(texts[int(input("Which number text file are you using?: "))], 'r')
else:
    jerry = open(texts[0], 'r')
print(f"Using: {jerry.name}")
lines = jerry.readlines()
jerry.close()

pygame.mixer.init()
running = True

while running:
    command = f'{input("Let me know what you want to let me know: ")}'
    columns = lines[0].strip().split('\t')
    columns = {k: v for k, v in enumerate(columns)}
    match command.split(' ')[0]:
        case 'help':
            print(
                """If you want to search the file for any of the commands, start the query with "^^^"

printcols: prints column names and numbers for settings.
    -c: Clear right before, use if lines are truncated

clear: clears console log

exit: idk what this one does i'm scared

settings: accesses settings
    Text to speech: Toggles text to speech
    Mute: Toggles sounds
    Columns: Selection of what columns should be printed when an item is found
        -a: Append
        -w: Rewrite
        -r: Until "exit" typed
            (sorry lmao)""")
        case 'printcols':
            if '-c' in command:
                os.system('cls')
            print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(columns.values())), sep="\n")
        case 'clear':
            os.system('cls')
        case 'settings':
            with open('files\\settings.json', 'w') as settingfile:
                adjusting = True
                while adjusting:
                    print(settings)
                    setcond = input("What would you ")
        case 'exit':
            running = False
        case _:
            command.replace('^^^', '').strip()
            found = False
            for line in lines:
                if command.lower() in line.lower():
                    printed = ""
                    for num in range(len(columns)):
                        if num in settings['Columns']:
                            printed += f"{columns[num]}: {line.split('\t')[num]}\n"
                    print(printed.rstrip())
                    found = True
            if not found:
                if settings['Muted']:
                    pygame.mixer.music.load(f'{filepath}\\files\\sounds\\no.mp3')
                print(f"\033[31m({command}) not found in file\033[0m")
            else:
                    if settings['Muted']:
                        if settings['Text to speech']:
                            readFile = gTTS(printed)
                            readFile.save('sounds\\temp.mp3')
                            pygame.mixer.music.load(f'{filepath}\\files\\sounds\\temp.mp3')
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                time.sleep(0.1)
                        pygame.mixer.music.load(f'{filepath}\\files\\sounds\\yes.mp3')
            if settings['Muted']:
                pygame.mixer.music.play()