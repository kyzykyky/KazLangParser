import glob, os


directory = 'D:\\Documents\\MyCodes\\MyPy\\ParsePjt\\'
print('Exact the path:', end='  ')
folderr = input(directory)
directory += folderr

os.chdir(directory)
for x in os.listdir(directory):
    os.chdir(directory)
    if x != '__pycache__' and x != '.idea' and x != '.git' and os.path.isdir(directory + '\\' + x):
        os.chdir(x)
        for Ufile in glob.glob("*.url"):
            new_url = ''
            with open(Ufile, 'r') as f:
                new_url = f.read().replace('[InternetShortcut]\nURL=', '')
                print(new_url)
            with open(Ufile, 'w') as f:
                f.write(new_url)
print('Action successful!')
