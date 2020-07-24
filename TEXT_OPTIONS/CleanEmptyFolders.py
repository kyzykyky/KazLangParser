import os
import shutil


directory = 'D:\\Documents\\MyCodes\\MyPy\\ParsePjt\\'
print('Exact the path:', end='  ')
folderr = input(directory)
directory += folderr
count = 0

for dirr in os.listdir(directory):
    dest = os.path.join(directory, dirr)
    if os.path.isdir(dest) and len(os.listdir(dest)) == 0:
        shutil.rmtree(dest)
        count += 1

print(count, 'empty folders removed')
