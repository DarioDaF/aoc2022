
import random, argparse

ap = argparse.ArgumentParser()
ap.add_argument('--seed')
ap.add_argument('--outfile')
args = ap.parse_args()

output = [[*l] for l in '''
________________________________________
####.#..#..###.#..#......#..#..##.##....
#....#..#.#....#.#.......#..#.#..#..#...
###..#..#.#....##........#..#.#.....#...
#....#..#.#....#.#.......#..#..#...#....
#....#..#.#....#.#.......#..#...#.#.....
#.....##...###.#..#.......##.....#......
'''.strip('\n _').split('\n')]
#seed = 'ByxNqReUvv6PwgW' # Seed that generated 1 loop (trial and error)
seed = args.seed

# Cannot unmark this part with X = 1 and 2 clocks for addx
assert output[0][0] == '#' and output[0][1] == '#'
output[0][0] = '.'; output[0][1] = '.'

rows = len(output)
cols = len(output[0])
full_modulo = cols * rows

def iterMass(row):
    row += '.'
    i_col_st = 0
    while True:
        while row[i_col_st] == '.':
            i_col_st += 1
            if i_col_st >= len(row):
                return
        i_col_end = i_col_st
        while row[i_col_end] == '#':
            i_col_end += 1
        yield i_col_st, i_col_end
        i_col_st = i_col_end

if seed == None:
    random.seed()
    seed = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=15))

rng = random.Random(seed)
print(f'# Seed: {seed}')

conditions = []

def gen_block_len(rng):
    x = rng.randint(1, 100)
    if x < 10:
        return 1
    if x < 50:
        return 2
    return 3

for i_row in range(rows):
    row = output[i_row]
    for i_st, i_end in iterMass(row):
        # Handle row of #s
        while i_end > i_st:
            block_len = min(gen_block_len(rng), i_end - i_st)
            # Handle block
            need_clean = False
            if block_len == 1:
                cursor_pos = i_st - 2
            elif block_len == 2:
                if rng.randint(0, 1) == 0:
                    cursor_pos = i_st - 1
                else:
                    cursor_pos = i_st
                    need_clean = True
            elif block_len == 3:
                cursor_pos = i_st
            else:
                raise
            conditions.append((i_st + i_row * cols, block_len, cursor_pos, need_clean))
            i_st += block_len

code = []
t = 0
x = 0

# conditions are sorted by start value
loop_count = 0
while len(conditions) > 0:
    loop_count += 1
    botched_conditions = []
    need_clean = False
    last_row = 0
    for i_st, block_len, cursor_pos, _need_clean in conditions:
        i_st_row = i_st // cols
        if i_st_row > last_row and x >= -2: # if new line and cursor in the way
            # New line passed insure cursor out of position
            i = rng.randint(-20, -3)
            code.append(f'addx {i-x}')
            t += 2
            x = i
            need_clean = False
        last_row = i_st_row

        t0 = i_st - 2
        while t0 > t:
            if need_clean:
                i = rng.randint(-20, -3)
                code.append(f'addx {i}')
                t += 2
                x += i
                need_clean = False
            else:
                code.append('noop')
                t += 1
        if t != t0:
            botched_conditions.append((i_st, block_len, cursor_pos, _need_clean))
            continue
        code.append(f'addx {cursor_pos-x}')
        t += 2
        x = cursor_pos
        assert t == i_st
        if block_len == 3:
            code.append('noop (!)') # Insure still on screen in 3 frames (! this noop is not replacable)
            t += 1
        need_clean = _need_clean
    
    conditions = botched_conditions
    if len(conditions) == 0:
        break # Fast exit
    
    # Align to vsync
    if x >= -2:
        i = rng.randint(-20, -3)
        code.append(f'addx {i-x} (align)')
        t += 2
        x = i
        need_clean = False
    while t < full_modulo:
        if need_clean:
            i = rng.randint(-20, -3)
            code.append(f'addx {i}')
            t += 2
            x += i
            need_clean = False
        else:
            code.append('noop')
            t += 1
    assert t == full_modulo
    t = 0

# Count stuff to free the buffer
i = rng.randint(-20, 20)
if abs(i) < 5:
    i = 5 if i > 0 else -5
code.append(f'addx {i}')
t += 2
x += i

print(f'# Done {loop_count} loops')

# Compact noops
new_code = []
noops_cnt = 0
for line in code:
    if line == 'noop':
        noops_cnt += 1
    else:
        rel_x = 0
        if noops_cnt > 0:
            # Consume noops (always backwards)
            while noops_cnt // 2 > 0:
                rel_target = rng.randint(-20, 0)
                new_code.append(f'addx {rel_target-rel_x}')
                rel_x = rel_target
                noops_cnt -= 2
            if noops_cnt > 0:
                new_code.append('noop')
                noops_cnt -= 1
            assert noops_cnt == 0
        if rel_x != 0:
            parts = line.split(' ')
            parts[1] = str(int(parts[1]) - rel_x)
            new_code.append(' '.join(parts))
        else:
            new_code.append(line)

if args.outfile != None:
    with open(args.outfile, 'w') as fp:
        fp.write('\n'.join(new_code))
else:
    print('\n'.join(new_code))
