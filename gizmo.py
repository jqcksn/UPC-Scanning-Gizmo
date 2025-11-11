try:
    import os
    filepath = os.path.dirname(os.path.abspath(__file__))
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame
    for dirfile in os.listdir(filepath):
        if '.txt' in dirfile:
            jerry = open(f"{filepath}\\{dirfile}", 'r')
            print(f"Using: {dirfile}")
            break
    try:
        jerry
    except:
        print("There are no txts in your directory!")
    pygame.mixer.init()
    lines = jerry.readlines()
    jerry.close()
    while True:
        upc = f'{input("Scan the item! ")}'
        foundit = False
        for line in lines:
            if upc.lower() in line.lower():
                pygame.mixer.music.load(f'{filepath}\\sounds\\yes.mp3')
                print(f"Name: {line.split('\t')[0]}\nCondition: {line.split('\t')[7]}")
                foundit = True
        if not foundit:
            pygame.mixer.music.load(f'{filepath}\\sounds\\no.mp3')
            print(f"\033[31mDENIED. ({upc}) thing fucking SUCKS!!!!\033[0m")
        pygame.mixer.music.play()
except Exception as e:
    print(e)
    input("Press enter to exit:")
