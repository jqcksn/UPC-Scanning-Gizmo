try:
    import os
    filepath = os.path.abspath(__file__).replace('gizmo.py', '')
    print(filepath)
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame
    for dirfile in os.listdir(filepath):
        if '.txt' in dirfile:
            jerry = open(f"{filepath}{dirfile}", 'r')
            break
    try:
        jerry
    except:
        print("There are no txts in your directory!")
    pygame.mixer.init()
    lines = jerry.readlines()
    jerry.close()
    while True:
        upc = f'{input("Scan the item! ")}\n'
        found = False
        for line in lines:
            if upc == line:
                pygame.mixer.music.load(f'{filepath}\\sounds\\yes.mp3')
                found = True
        if not found:
            pygame.mixer.music.load(f'{filepath}\\sounds\\no.mp3')
        pygame.mixer.music.play()
except Exception as e:
    print(e)
    while True:
        pass