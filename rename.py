import os
path = 'c:\\Users\\tylerzhu\\Desktop\\icon'
for file in os.listdir(path):
	if os.path.isfile(os.path.join(path,file)) == True:
		newname = file.replace("scroll_1","scroll_00")
		os.rename(os.path.join(path,file),os.path.join(path,newname))
		print(file)

		