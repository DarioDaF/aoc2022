
from utils import readInput

text = readInput()

x = sorted(sum(int(c) for c in elf.split('\n') if c != '') for elf in text.split('\n\n'))
print(f'Top: {x[-1]}')
print(f'Top3: {sum(x[-3:])}')
