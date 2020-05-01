import glob, os


directory = 'D:\\Documents\\MyCodes\\MyPy\\ParsePjt\\Zharar_com\\Әңгімелер жинағы'
os.chdir(directory)
txt_files = {}
urls_for_remove = []
count = 0
for file in glob.glob("*.txt"):
	txt_files[file[:-4]] = file
	dest = directory + "\\" + file
	size = os.path.getsize(dest)/1024
	print(file[:-4], size)
	if (size < 3.1):
		os.remove(dest)
		txt_files[file[:-4]] = ''
		urls_for_remove.append(file[:-4])
	if txt_files[file[:-4]] == '':
		os.remove(directory + '\\' + file[:-4] + '.url')
		count += 1

# Checking links without file
for Ufile in glob.glob("*.url"):
	check = True
	for Tfile in glob.glob("*.txt"):
		if Ufile[:-4] == Tfile[:-4]:
			check = True
			break
		else:
			check = False
	if not check:
		os.remove(directory + '\\' + Ufile)
		count += 1

print("Successfully removed " + str(count) + " files.")

