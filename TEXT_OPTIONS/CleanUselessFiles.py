import glob, os


directory = 'D:\\Documents\\MyCodes\\MyPy\\ParsePjt\\'
print('Exact the path:', end='  ')
folderr = input(directory)
directory += folderr
count = 0

os.chdir(directory)
for x in os.listdir(directory):
	os.chdir(directory)
	if x != '__pycache__' and x != '.idea' and x != '.git' and os.path.isdir(directory + '\\' + x):
		os.chdir(x)
		txt_files = {}
		urls_for_remove = []

		for file in glob.glob("*.txt"):
			txt_files[file[:-4]] = file
			dest = directory + "\\" + x + "\\" + file
			size = os.path.getsize(dest)/1024
			print(file[:-4], size)
			if (size < 2.2):
				os.remove(dest)
				txt_files[file[:-4]] = ''
				urls_for_remove.append(file[:-4])
			if txt_files[file[:-4]] == '':
				os.remove(directory + "\\" + x + "\\" + file[:-4] + '.url')
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
				os.remove(directory + "\\" + x + "\\" + Ufile)
				count += 1

print("Successfully removed " + str(count) + " files.")

