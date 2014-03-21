import os #for access to system commands
import pydoc #for writing documentation

OUTFOLDER = "generatedDocumentation/"

GHPagesInstructions = """
INSTRUCTIONS FOR UPDATING WEB DOCUMENTATION
-The documentation files were put in @outfolder.
-Move this folder to a location outside the git repository (so it is preserved when switching branches)
-Remember to commit and push important changes in current branch 
-Switch branches to gh-pages using "git checkout gh-pages"
-Move the contents of @outfolder into the documentation folder of gh-pages
-Commit and push the changes
-Make sure it works by checking out http://cssdepaul.github.io/Computerized-Robot-Arena-Program/documentation/
-(You may have to wait 10 minutes before it shows up
""".replace('@outfolder', OUTFOLDER)

def generateDoc(moduleName):
	"""
	@param moduleName is the name of the module to document (example: robot)
	generates the HTML pydoc file for the given module
	then it moves the file to OUTFOLDER 
		(this is necessary because pydoc does not allow user-defined destination path)
	"""
	pydoc.writedoc(moduleName)
	filename = moduleName+'.html'
	destination = OUTFOLDER+filename
	command = "mv %s %s"%(filename, destination)
	os.system(command)
	
def generateDocs():
	"""
	Creates the documentation HTML files for all python files in this directory
	The files are moved to OUTFOLDER (default = documentation/)
	"""
	command = "mkdir -p %s" %(OUTFOLDER) #makes directory OUTFOLDER. the -p means it ignores 'already exists' error
	os.system(command)
	for filename in os.listdir(): #for every file in current directory
		partList = filename.split(".") #a list containing [name, extension]
		if len(partList) != 2: continue #either a directory or some weird file, ignore it.
		moduleName = partList[0]
		extension = partList[1]
		if extension == 'py':
			generateDoc(moduleName)
			
def main():
	print("Note: This program will probably only work on Linux machines.")
	generateDocs()
	print(GHPagesInstructions)

#if run as the main program (as opposed to being imported)
if __name__ == "__main__":
	main()
