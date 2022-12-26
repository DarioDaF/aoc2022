
from utils import readInput, defaultdict

text = readInput()

def moveDir(base, part):
    spart = part.split('/')
    if spart[0] == '':
        if spart[1] == '':
            return [] # Empty abs path
        else:
            return spart[1:] # Abs path
    for x in spart:
        if x == '..':
            base.pop()
        else:
            base.append(x)
    return base

isListing = False
cwd = []
files = []
for line in text.strip().split('\n'):
    parts = line.split(' ')
    if parts[0] == '$':
        isListing = False
        # Command
        if parts[1] == 'cd':
            cwd = moveDir(cwd, parts[2])
        elif parts[1] == 'ls':
            isListing = True
        else:
            print(f'Unknownw command {parts[1]}')
    else:
        # Data
        if isListing:
            if parts[0] == 'dir':
                pass
            else:
                # File
                size = int(parts[0])
                name = parts[1]
                files.append(((*cwd, name), size))

#rootDirSizes = defaultdict(int)
#for file in files:
#    if len(file[0]) > 1:
#        rootDirSizes[file[0][0]] = file[1]

dirSizes = defaultdict(int)
for file in files:
    n = ''
    for x in file[0][:-1]:
        n += '/' + x
        dirSizes[n] += file[1]

t = 0
for n, s in dirSizes.items():
    if s <= 100000:
        t += s

print(f'Redundant: {t}')

MAX_USED_SPACE = 70000000 - 30000000

# Get root size
root_size = sum(f[1] for f in files)

to_free = root_size - MAX_USED_SPACE

x = sorted(((n, s) for n, s in dirSizes.items() if s >= to_free), key=lambda x: x[1])

print(x[0])
