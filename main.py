import json
import os
try:
    with open('files\\settings.json', 'r') as settinginit:
        settings = json.load(settinginit)
except:
    with open('files\\settings.json', 'w') as settinginit:
        settinginit.write("""{
    "Text to speech": false,
    "Sound": false,
    "Columns": [
        0
    ],
    "Max speaking time": "10000.0"
}""")
        json.loads("""{"Text to speech": true,"Sound": true,"Columns": [0],"Max speaking time": "10000.0"}""")
filepath = os.path.dirname(os.path.abspath(__file__))
texts = []
for dirfile in os.listdir(filepath):
    if dirfile.endswith('.txt'):
        texts.append(dirfile)
if len(texts) > 1:
    print(*map(lambda t: f"{t[0]+1}: {t[1]}", enumerate(texts)), sep="\n")
    textfile = open(texts[int(input("Which number text file are you using?: "))-1], 'r')
else:
    textfile = open(texts[0], 'r')
print(f"Using: {textfile.name}")
lines = textfile.readlines()
textfile.close()
running = True
columns = lines[0].strip().split('\t')
initted = False
while running:
    allem = False
    command = f'{input("Let me know what you want to let me know: ")}'
    if ' -c' in command:
            os.system('cls')
    match command.split(' ')[0]:
        case 'help':
            print(
"""If you want to search the file for any of the commands, start the query with "^^^"

printcols: Prints column names and numbers for settings. Can also be typed after query to print all columns of query

-c: Clear console. Will still run command if combined with another one.

exit: idk what this one does i'm scared

settings: accesses settings
    Sound: if sound should be enabled
    Text to speech: If text to speech should be enabled
    Columns: Selection of what columns should be printed when an item is found
        
        action examples: 
        remove 10 20

        remove: removes the following columns
        rewrite: deletes all columns except for ones input
        add: adds numbers to printed columns""")
        case 'printcols':
            print(*map(lambda t: f"{t[0]}: {t[1]}", enumerate(columns)), sep="\n")
        case 'clear':
            os.system('cls')
        case 'settings':
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
                        settings['Max speaking time'] = str(float(input("What is your desired maximum speaking time? (seconds): ")))
                    case 'save':
                        adjusting = False
            with open('files\\settings.json', 'w') as settingfile:
                    json.dump(settings, settingfile, indent=4)
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
                    print(printed.rstrip())
                    found = True
            allem = False
            if not found:
                if settings['Sound']:
                    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
                    import pygame
                    if not initted:
                        initted = True
                        pygame.mixer.init()
                    pygame.mixer.music.load(f'{filepath}\\files\\sounds\\no.mp3')
                print(f"\033[31m({command}) not found in file\033[0m")
            else:
                if settings['Sound']:
                    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
                    import time
                    import pygame
                    pygame.mixer.init()
                    if settings['Text to speech']:
                        from gtts import gTTS
                        if not printed:
                            printed = "fuck you"
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
            if settings['Sound']:
                pygame.mixer.music.play()