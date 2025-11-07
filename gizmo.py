try:
    import os
    filepath = os.path.dirname(os.path.abspath(__file__))
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame
    for dirfile in os.listdir(filepath):
        if '.txt' in dirfile:
            jerry = open(f"{filepath}{dirfile}", 'r')
			print(f"Using: {dirfile}")
            break
    try:
        jerry
    except:
        print("There are no txts in your directory!")
    pygame.mixer.init()
    lines = jerry.read()
    jerry.close()
    while True:
        upc = f'{input("Scan the item! ")}\n'
        if upc in lines:
	        pygame.mixer.music.load(f'{filepath}\\sounds\\yes.mp3')
        else:
	        pygame.mixer.music.load(f'{filepath}\\sounds\\no.mp3')
        pygame.mixer.music.play()
except Exception as e:
    print(e)
    input("Press enter to exit:")
