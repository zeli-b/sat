from datetime import datetime
from os import mkdir
from os.path import isdir, join
from sys import argv
from io import BytesIO
import argparse
import win32clipboard

from PIL import Image
import pygame

pygame.init()


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def get_filename():
    return str(datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '') + '.png'


parser = argparse.ArgumentParser(description='A YJemin renderer.')
parser.add_argument('message', type=str, help='content of the image')
parser.add_argument('--color', '-c', type=int, nargs='+', help='color of the text')
parser.add_argument('--size', '-s', type=int, help='size of the text')
args = parser.parse_args()

if args.size is None: args.size = 12
if args.color is None: args.color = (0, 0, 0)

font = pygame.font.Font(r'H:\자소크\yjemin\YJemin8.ttf', args.size)
surface = font.render(args.message, True, args.color)
image = Image.frombytes('RGBA', surface.get_size(), pygame.image.tostring(surface, 'RGBA', False))

output = BytesIO()
image.save(output, 'BMP')
data = output.getvalue()[14:]
output.close()

if not isdir('./output'):
    mkdir('./output')

pygame.image.save(surface, join('./output', get_filename()))

send_to_clipboard(win32clipboard.CF_DIB, data)
