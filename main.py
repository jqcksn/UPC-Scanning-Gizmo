import json
import os
import time

# -----------------------------
# Settings & File Handling
# -----------------------------

def load_settings(path):
    with open(path, "r") as f:
        return json.load(f)

def save_settings(path, settings):
    with open(path, "w") as f:
        json.dump(settings, f, indent=4)

def list_text_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".txt")]

def choose_text_file(files):
    if len(files) == 1:
        return files[0]

    print("\nAvailable text files:")
    for i, filename in enumerate(files, start=1):
        print(f"{i}: {filename}")

    while True:
        choice = input("Which number text file are you using?: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(files):
                return files[idx - 1]
        print("Invalid selection. Try again.")


# -----------------------------
# Search Logic
# -----------------------------

def search_lines(lines, query, columns, settings, print_all):
    query = query.lower()
    found_any = False

    for line in lines:
        if query in line.lower():
            found_any = True
            parts = line.rstrip("\n").split("\t")

            # Build output
            output = []
            for i, col_name in enumerate(columns):
                if print_all or i in settings["Columns"]:
                    if i < len(parts):
                        output.append(f"{col_name}: {parts[i]}")

            result = "\n".join(output)
            print(result + "\n")
            last_output = result

    if found_any and settings["Sound"]:
        play_audio_feedback(last_output, settings)

    return found_any



# -----------------------------
# Audio/TTS
# -----------------------------

pygame_initialized = False

def ensure_pygame():
    global pygame_initialized
    if pygame_initialized:
        return
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame
    pygame.mixer.init()
    pygame_initialized = True

def play_audio_feedback(text, settings):
    ensure_pygame()
    import pygame

    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", "sounds")

    # TTS first
    if settings["Text to speech"]:
        from gtts import gTTS

        if not text:
            text = "fuck you"

        tts_path = os.path.join(base, "temp.mp3")
        gTTS(text).save(tts_path)

        pygame.mixer.music.load(tts_path)
        pygame.mixer.music.play()

        start = time.time()
        while pygame.mixer.music.get_busy():
            if time.time() - start >= float(settings["Max speaking time"]):
                break
            time.sleep(0.05)

    # Success sound
    pygame.mixer.music.load(os.path.join(base, "yes.mp3"))
    pygame.mixer.music.play()


def play_not_found_sound(settings):
    if not settings["Sound"]:
        return
    ensure_pygame()
    import pygame

    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", "sounds")
    pygame.mixer.music.load(os.path.join(base, "no.mp3"))
    pygame.mixer.music.play()


# -----------------------------
# Settings Menu
# -----------------------------

def settings_menu(settings, columns, settings_path):
    while True:
        print("\nSettings:")
        for i, (key, value) in enumerate(settings.items(), start=1):
            if isinstance(value, bool):
                print(f"{i}: {key} is {'on' if value else 'off'}")
            elif isinstance(value, list):
                print(f"{i}: Columns printed: {' '.join(map(str, value))}")
            else:
                print(f"{i}: {key}: {value}")
        print("save: Save settings and exit")

        cmd = input("Enter the index of your change: ").strip()

        if cmd == "save":
            save_settings(settings_path, settings)
            break

        if not cmd.isdigit():
            print("Invalid input.")
            continue

        cmd = int(cmd)

        if cmd == 1:
            settings["Text to speech"] = not settings["Text to speech"]
        elif cmd == 2:
            settings["Sound"] = not settings["Sound"]
        elif cmd == 3:
            print("\nColumns:")
            for i, col in enumerate(columns):
                print(f"{i}: {col}")

            action = input("Action (add/remove/rewrite) and column index(es): ").split()
            if not action:
                continue

            mode = action[0]
            nums = [int(x) for x in action[1:] if x.isdigit()]

            if mode == "add":
                settings["Columns"].extend(nums)
            elif mode == "remove":
                settings["Columns"] = [c for c in settings["Columns"] if c not in nums]
            elif mode == "rewrite":
                settings["Columns"] = nums

            settings["Columns"] = sorted(set(settings["Columns"]))

        elif cmd == 4:
            val = input("Max speaking time (seconds): ").strip()
            try:
                settings["Max speaking time"] = str(float(val))
            except ValueError:
                print("Invalid number.")

        else:
            print("Unknown index.")


# -----------------------------
# Main Loop
# -----------------------------

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(base_path, "files", "settings.json")

    settings = load_settings(settings_path)
    text_files = list_text_files(base_path)
    chosen_file = choose_text_file(text_files)

    with open(os.path.join(base_path, chosen_file), "r") as f:
        lines = f.readlines()

    columns = lines[0].strip().split("\t")
    print(f"\nUsing: {chosen_file}\n")

    while True:
        cmd = input("Let me know what you want to let me know: ").strip()

        if " -c" in cmd:
            os.system("cls")
            cmd = cmd.replace(" -c", "").strip()

        if not cmd:
            continue

        if cmd == "exit":
            break

        if cmd == "help":
            print("""Commands:
printcols — Print column names
settings — Adjust settings
exit — Quit
^^^query — Search file
""")
            continue

        if cmd == "printcols":
            for i, col in enumerate(columns):
                print(f"{i}: {col}")
            continue

        if cmd == "settings":
            settings_menu(settings, columns, settings_path)
            continue

        # Searching
        print_all = "printcols" in cmd
        query = cmd.replace("^^^", "").replace("printcols", "").strip()

        found = search_lines(lines, query, columns, settings, print_all)

        if not found:
            print(f"\033[31m({query}) not found in file\033[0m")
            play_not_found_sound(settings)


if __name__ == "__main__":
    main()
