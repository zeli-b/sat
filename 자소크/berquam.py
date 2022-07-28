from random import choice, randint

initial = [' ', 'b', 'c', 'ch', 'd', 'f', 'g', 'gh', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'qu', 'r', 'r', 's', 'sh',
           'sch', 'sci', 't', 'v', 'w', 'x', 'y', 'z']
final = ['a', 'ae', 'al', 'am', 'an', 'ar', 'ard', 'as',
         'e', 'ee', 'ees', 'ei', 'el', 'em', 'en', 'er', 'erd', 'es', 'ess',
         'i', 'ie', 'il', 'im', 'in', 'ing', 'ir', 'irs', 'is',
         'o', 'oe', 'oo', 'ol', 'om', 'on', 'or', 'org', 'os', 'ou', 'ous',
         'u', 'ul', 'um', 'un', 'ur', 'us']

banneds = ['mg', 'xu', 'lya', 'ji', 'nl', 'yi', 'wu', 'mw', 'jae', 'nr', 'lr', 'lw', 'mr', 'sy', 'ngr', 'lx', 'mg',
           'mc', 'nc', 'nb', 'mr', 'ln', 'lol', 'mr', 'lil', 'lj', 'ghu', 'nw', 'gy', 'dc', 'sss']


def get_initial():
    while True:
        sound = choice(initial)
        if randint(0, 'eari otnslcqudpmhgbfywkvxzj'.index(sound[0])) == 0:
            return sound


def get_final(initial_sound) -> str:
    while True:
        sound = choice(final)
        if sound[0] != initial_sound[-1]:
            if initial_sound[-1] == 'c' and sound[0] not in ('i', 'e'):
                continue
            return sound


def syllable() -> str:
    initial_sound = get_initial()
    final_sound = get_final(initial_sound)
    result = (initial_sound + final_sound).replace(' ', '')
    return result


def word(syllables: int = 3) -> str:
    while True:
        result = ''.join(syllable() for _ in range(syllables))
        yes = True
        for banned in banneds:
            if banned in result:
                yes = False
                break
        if yes:
            result = result.replace('yu', 'you')
            if result.endswith('i') or result.endswith('u') or result.endswith('o'):
                return result + 'e'
            return result


if __name__ == '__main__':
    from sys import argv

    for i in range(25):
        print(25-i, word(int(argv[1]) if len(argv) >= 2 else 1), sep='\t')
    # print(word(2))

    # scus
