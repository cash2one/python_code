#ecoding:utf-8
def open(filename, mode='r'):
    import __builtin__
    file = __builtin__.open(filename, mode)

    if file.read(5) not in ("GIF87", "GIF89"):
        raise IOError, "not a GIF"
    #否则回到文件开头
    file.seek(0)
    return  file

fr =  open('/Users/bjhl/Documents/ciku.txt')

