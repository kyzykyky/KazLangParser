import os


dir = 'D:\Documents\MyCodes\MyPy\ParsePjt'
tree = os.walk(dir)
print(tree)
x = True
for d in tree:
    if x is True:
        print(d)
        dirs = d[1]
        print(dirs)
        paths = []
        for item in dirs:
            paths.append(dir + '\\' + item)
        print(paths)
        x = False
    for folder in d:
        # print(folder)
        for item in folder:
            if item.endswith('.txt'):
                print(item)
                # f = open()
