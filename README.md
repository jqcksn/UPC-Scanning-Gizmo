# UPC Scanning Gizmo

A command-line Python utility for searching tab-delimited text files, printing selected columns, and optionally playing success/failure sounds or reading matches aloud with text-to-speech.

## Features

- Searches `.txt` files in the script directory
- Prints selected columns from matching rows
- Lets you change which columns are displayed
- Optional sound effects for match / no match
- Optional text-to-speech for the last printed match
- Optional output logging to a file
- Simple interactive settings menu

## Requirements

- Python 3.10+ recommended
- `pygame`
- `gTTS`

Install dependencies:

```bash
pip install pygame gTTS
```

## Expected project structure

```text
project_folder/
├─ your_script.py
├─ some_data.txt
└─ files/
   ├─ settings.json
   └─ sounds/
      ├─ yes.mp3
      ├─ no.mp3
      └─ temp.mp3   # generated when text-to-speech is used
```

## Input file format

The program expects a **tab-delimited** text file.

Example:

```text
Code	Name	Description
A100	Widget	Blue widget
B200	Gadget	Small gadget
```

- The first line should contain column headers
- Each later line should contain the same number of tab-separated fields

## How it works

When the program starts, it:

1. Loads settings from `files\settings.json`
2. Scans the script directory for `.txt` files
3. Lets you choose a file if more than one is found
4. Repeatedly prompts for commands or search terms

If your query matches a row, the program prints the configured columns for that row.

## Commands

### `help`
Shows the built-in help text.

### `printcols`
Prints available columns.

You can also append `printcols` to a search to print all columns for matching rows.

### `settings`
Opens the settings menu.

Available settings include:

- **Text to speech**
- **Sound**
- **Columns**
- **Max speaking time**
- **Output file**

### `changefile`
Lets you pick a different `.txt` file.

### `clear`
Clears the console.

### `exit`
Exits the program.

### `-c`
If included in a command, clears the console before running the command.

Example:

```text
ABC123 -c
```

## Example session

```text
Please input code or (help): settings
Please input code or (help): printcols
Please input code or (help): A100
Please input code or (help): A100 printcols
Please input code or (help): changefile
Please input code or (help): exit
```

## Settings behavior

### Columns
The `Columns` setting controls which column indexes are printed when a row matches.

Examples in the settings menu:

- `rewrite 0 2 5`
- `add 3`
- `remove 2`

### Output file
If an output file is configured, matches are appended to that file.

### Max speaking time
Used to limit how long the text-to-speech audio is allowed to play.

## Notes

- The script appears to be designed mainly for Windows because it uses paths like `files\settings.json` and console clearing with `cls`.
- Audio playback depends on the system having a working audio device and compatible `pygame` setup.
- `gTTS` requires internet access to generate speech.

## License

MIT
