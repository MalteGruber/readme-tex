import argparse
import os.path

def get_text_of_file(file_path):
	file = open(file_path, 'r')
	text = file.read()
	file.close()
	return text

def save_text_to_file(file_path,text):
	text_file = open(file_path, "w")
	text_file.write(text)
	text_file.close()
def file_append_to_path(path,filename):
	if(path[-1]=="/"):
		path+=filename
	else:
		path+="/"+filename
	return path
def test_path_validity(path):
	if not os.path.exists(path):
		print "ERROR: Could not find the location",path
		exit(-1)
def test_if_path_has_file(path,filename):
	path=file_append_to_path(path,filename)
	if not os.path.isfile(path):
		print "ERROR: Could not find the file",path
		exit(-1)


parser = argparse.ArgumentParser(description='Add latex to README files.')


parser.add_argument('source',  type=str, 
                    help='location of source file')

parser.add_argument('target',  type=str, 
                    help='location of target file')

from subprocess import call
img_cnt=0

def get_github_img_tag(path,desc):
	return "![{}]({})".format(desc,path)
def generate_png_from_tex(tex):


	global img_cnt
	
	template=get_text_of_file("template.tex")
	template=template.replace("FORMULA_PLACED_HERE",tex);
	print("TEMPLATE:",template)
	save_text_to_file("formula.tex",template)
	relative_name="doc/teximg/tex_img_"+str(img_cnt)+".png"
	outname=file_append_to_path(target_dir,relative_name)
	img_cnt+=1
	call(["make", "all","OUTNAME="+outname])


	return get_github_img_tag(relative_name,tex.replace("\n",""))

def handle_tex(tex):
	print("found tex",tex)
	ret=generate_png_from_tex(tex)
	return ret

def run_latexifyer(text):
	text=text.split("$$")
	ret=""
	for i in range(len(text)):
		if(i%2==0 ):
			print("normal:"+text[i].replace("\n"," "))
			ret+=text[i]
		else:
			ret+=handle_tex(text[i])
	return ret
	


args = parser.parse_args()

source_dir=args.source
target_dir=args.target

test_path_validity(source_dir)
test_if_path_has_file(source_dir,"README.md")
test_path_validity(target_dir)

readme_loc=file_append_to_path(source_dir,"README.md")

text=get_text_of_file(readme_loc)

print(text)

print("PARSED: ",)
new_readme_text=run_latexifyer(text)
save_text_to_file(file_append_to_path(target_dir,"README.md"),new_readme_text)