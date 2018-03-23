for i in range(180):
    with open('../data/rand' + f'{i:04d}' + '.txt') as fin:
        lines = fin.readlines()
    lines[0] = lines[0].replace('2', '4')  # replace these values

    with open('../data/rand' + f'{i:04d}' + '.txt', 'w') as fout:
        for line in lines:
            fout.write(line)
