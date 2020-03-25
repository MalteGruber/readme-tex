
OUTNAME?="error"


all: tex png move

tex:
	latex -halt-on-error -output-directory=build formula.tex
png:
	dvipng -T tight -x 1200 -z 9 build/formula.dvi -o file.png
move:
	mv file.png $(OUTNAME)
clean:
