def compare(x, y):
    if x['height'] < y['height']:
        return -1
    elif x['height'] > y['height']:
        return 1
    elif x['procID'] < y['procID']:
        return -1
    else:
        return 1
