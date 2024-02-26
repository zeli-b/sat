font = fontforge.fonts()[0]

consonants = ['', 'g', 'k', 'n', 'd', 't', 'l', 'r', 'm', 'b', 'p', 's', 'x', 'z', 'c', 'f', 'h']
vowels = ['a', 'eo', 'e', 'o', 'u', 'w', 'i', 'ya', 'yeo', 'ye', 'yo', 'yu', 'wa', 'weo', 'we', 'wo', 'wi']

offset = 0xe100
for consonant in consonants:
    for vowel in vowels:
        glyph = font.createChar(offset)

        glyph.importOutlines(f'Desktop/SVG/{consonant}{vowel}.svg')

        offset += 1
