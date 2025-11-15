import json
import os
with open('files\\settings.json', 'r') as settinginit:
    settings = json.load(settinginit)
print(settings)
if not settings['Muted']:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame
    import time
    if settings['Text to speech']:
        from gtts import gTTS
filepath = os.path.dirname(os.path.abspath(__file__))
texts = []
for dirfile in os.listdir(filepath):
    if '.txt' in dirfile:
        texts.append(dirfile)
if len(texts) > 1:
    print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(texts)), sep="\n")
    textfile = open(texts[int(input("Which number text file are you using?: "))], 'r')
else:
    textfile = open(texts[0], 'r')
print(f"Using: {textfile.name}")
lines = textfile.readlines()
textfile.close()

pygame.mixer.init()
running = True

while running:
    allem = False
    command = f'{input("Let me know what you want to let me know: ")}'
    if ' -c' in command:
            os.system('cls')
    columns = lines[0].strip().split('\t')
    columns = {k: v for k, v in enumerate(columns)}
    match command.split(' ')[0]:
        case 'help':
            print(
                """If you want to search the file for any of the commands, start the query with "^^^"

printcols: Prints column names and numbers for settings. Can also be typed after query to print all columns of query

-c: Clear console. Will still run command if combined with another one.

exit: idk what this one does i'm scared

settings: accesses settings
    Text to speech: Toggles text to speech
    Mute: Toggles sounds
    Columns: Selection of what columns should be printed when an item is found""")
        case 'printcols':
            print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(columns.values())), sep="\n")
        case 'clear':
            os.system('cls')
        case 'settings':
            with open('files\\settings.json', 'w') as settingfile:
                adjusting = True
                while adjusting:
                    print(settings)
                    setcond = input("What would you like to change?: ")

                        
                json.dump(settings, settingfile)
        case 'exit':
            running = False
        case _:
            if 'printcols' in command:
                allem = True
            command = command.replace('^^^', '').strip().replace('printcols','').strip()
            found = False
            for line in lines:
                if command.lower() in line.lower():
                    printed = ""
                    for num in range(len(columns)):
                        if num in settings['Columns'] or allem:
                            printed += f"{columns[num]}: {line.split('\t')[num]}\n"
                    allem = False
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