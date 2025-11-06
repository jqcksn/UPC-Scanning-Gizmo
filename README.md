# Gizmo Scanner

A minimal Python tool that checks scanned codes against a text file and plays a sound for matches.

## Info

Looks for the first .txt file in the same folder.

Waits for input (Scan the item!).

If the code matches a line in the file → plays sounds/yes.mp3.

If not → plays sounds/no.mp3.

## Notes

Requires pygame.

One item code per line in the .txt file.

Will warn if no .txt files are found.
