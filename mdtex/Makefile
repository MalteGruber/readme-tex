
OUTNAME?="error"
DOC_FOLDER="error"
RESOLUTION?="error"


#This files pwd is in the ./mdtex folder!

all: tex png move

tex:
	latex -halt-on-error -output-directory=build formula.tex
png:
	dvipng -T tight  -D $(RESOLUTION) build/formula.dvi -o file.png
move:
	#Move the generated file to the output directory and rename it to match the path in the new readme file.
	
	
	mkdir -p $(DOC_FOLDER)/teximg
	#mkdir -p doc/teximg #Fail -> generates in /home/mg/readme-tex/mdtex
	mv --force file.png $(OUTNAME)
