import clipboard

string = clipboard.paste()

latin_characters = 'gnmsdvzlhkqtpcrfaúouieéx'
braille_characters = '⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿'

latin, braille = 0,0 

for letter in string:
    if letter in latin_characters:
        latin += 1
    if letter in braille_characters:
        braille += 1

mode_latin = latin >= braille 

convert_table = {
    'sh': '⠯', 'qu': '⠟',
    'à': '⠺⠁', 'è': '⠕⠁', 'ì': '⠱⠁', 'ò': '⠹⠁', 'ù': '⠧⠁',
    'â': '⠺⠉', 'ê': '⠕⠉', 'î': '⠱⠉', 'ô': '⠹⠉', 'û': '⠧⠉',
    'ā': '⠺⠉', 'ē': '⠕⠉', 'ī': '⠱⠉', 'ō': '⠹⠉', 'ū': '⠧⠉',
    'ä': '⠺⠃', 'ë': '⠕⠃', 'ï': '⠕⠃', 'ö': '⠹⠃', 'ü': '⠧⠃',
    '‘': '⠋', '“': '⠋⠋', '’': '⠙', '”': '⠙⠙', '!': '⠣', '?': '⠩', '.': '⠄', ',': '⠤', ' ': '⠀',
    'g': '⠲', 'n': '⠦', 'm': '⠴', 's': '⠖', 'd': '⠮', 'v': '⠵', 'z': '⠫', 'l': '⠶',
    'k': '⠟', 'q': '⠟', 't': '⠾', 'p': '⠷', 'c': '⠻', 'h': '⠜', 'r': '⠭', 'f': '⠳',
    'a': '⠺', 'ú': '⠗', 'o': '⠹', 'u': '⠧', 'y': '⠱', 'i': '⠱', 'e': '⠕', 'é': '⠽', 'x': '⠂'
}

if not mode_latin:
    convert_table = {v: k for k, v in convert_table.items()}

result = ''

while string:
    no = True
    for key, value in convert_table.items():
        if string[:len(key)].lower() == key:
            string = string[len(key):]
            result += value
            no = False
            break
    if no:
        result += string[0]
        string = string[1:]

print(result)
clipboard.copy(result)
