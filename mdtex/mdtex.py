import argparse

import logging
from pathlib import Path
import os
from subprocess import call
from latex_to_png import *
from file_handling import *


class LatexPngGenerator:
	def __init__(self,show_build_output=False):
		self.img_cnt=0
		self.github_img_tax=""
		self.show_build_output=show_build_output
		
	def _get_github_img_tag(self,path,desc):
		return "![{}]({})".format(desc,path)

	def consume_latex(self,tex):
		logging.debug("Generating image for "+tex.strip())
		logging.debug("Image count is "+str(self.img_cnt))
		
		#Insert forula into the template file and save it
		template=get_text_of_file(get_mdtex_folder()+"/template.tex")
		template=template.replace("FORMULA_PLACED_HERE",tex);
		#save_text_to_file(get_mdtex_folder()+"/formula.tex",template)
		
		relative_name="teximg/tex_img_"+str(self.img_cnt)+".png"
		outname=file_append_to_path(target_dir,relative_name)
		self.img_cnt+=1
		
		logging.debug("make with output to "+outname)
		
		
		
		void = open('/dev/null', 'w')
		if self.show_build_output:
			void=None
		else: 
			logging.debug("Latex build process not printed")
		ret=call(["make","-C",get_mdtex_folder(),"all","OUTNAME="+outname],stdout=void,stderr=void)
		logging.debug(ret)
		
		if void!=None:
			
			void.close()
		
		self.github_img_tax=self._get_github_img_tag(relative_name,tex.replace("\n",""))

	def get_latex_image_path(self):
		return self.github_img_tax

def run_latexifyer(ltx,text):
	text=text.split("$$")
	ret=""
	for i in range(len(text)):
		if(i%2==0 ):
			ret+=text[i]
		else:
			ltx.consume_latex(text[i])
			ret+=ltx.get_latex_image_path()
	return ret
	
def get_abs_path_from_relative(rel):
	return str(Path(rel).resolve())

"""

"""
parser = argparse.ArgumentParser(description='Add latex to README files.')
parser.add_argument('source',  type=str, 
                    help='location of source file')
parser.add_argument('target',  type=str, 
                    help='location of target file')
parser.add_argument('--p',dest="build_std_show",action='store_true', 
                    help='location of target file')


"""
Formating guide: https://docs.python.org/3/library/logging.html#logging.Formatter
"""
FORMAT = '%(filename)s:%(lineno)d [%(levelname)s]\t%(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
logging.debug("Testing")

args = parser.parse_args()

source_dir=get_abs_path_from_relative(args.source)
target_dir=get_abs_path_from_relative(args.target)


logging.info("Reading from "+source_dir)
logging.info("Writing to "+target_dir)


test_path_validity(source_dir)
test_if_path_has_file(source_dir,"README.md")
test_path_validity(target_dir)

readme_loc=file_append_to_path(source_dir,"README.md")

text=get_text_of_file(readme_loc)

ltx=LatexPngGenerator(args.build_std_show)

new_readme_text=run_latexifyer(ltx,text)
save_text_to_file(file_append_to_path(target_dir,"README.md"),new_readme_text)






