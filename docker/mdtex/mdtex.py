import argparse

import logging
from pathlib import Path

from latex_to_png import *
from file_handling import *


import sys
def on_error(msg):
	print("ERROR:",msg)
	sys.exit(-1)
	
def run_latexifyerOLD(ltx,text):
	
	
	
	text=text.split("$$")
	ret=""
	
	
	for i in range(len(text)):
	
		if(i%2==0 ):
			ret+=text[i]
		else:
			ltx.consume_latex(text[i])
			ret+=ltx.get_latex_image_path()
			
	return ret





	
def run_latexifyer(ltx,text,generate_output=True):
	
	output=""
	buffer=""

	def inline_equation_state(token,peek):
		nonlocal buffer, output
		logging.debug("INLINE '{}' '{}'".format(token,peek))
		if token=="$":
			if peek!="$":
				
				if generate_output:
					ltx.consume_latex_inline(buffer)
					output+="<{}>".format(ltx.get_latex_image_path())
				buffer=""
				
				return idle_state
			elif len(buffer)>0:
				
				on_error("Line {}: Expected a single termination '$' of inline equation:{}".format(output.count("\n"),buffer))
		else:
			buffer+=token
		return inline_equation_state
		

	def full_equation_state(token,peek):
		nonlocal buffer, output
		logging.debug("FULL '{}' '{}'".format(token,peek))
		if token=="$":
			if peek=="$":
				if generate_output:
					ltx.consume_latex(buffer)
					output+="<{}>".format(ltx.get_latex_image_path())
				buffer=""
				return sleep_one
			elif len(buffer)>0:
				on_error("Line {}: Expected a single termination '$$' of equation: {}".format(output.count("\n"),buffer))
		else:
			buffer+=token
		return full_equation_state
		
	
	def idle_state(token,peek):
		nonlocal buffer, output
		logging.debug("IDLE '{}' '{}'".format(token,peek))
		if token=="$":
			if peek=="$":
				logging.debug("TRIGEER FULL")
				output+=buffer
				buffer=""
				return full_equation_state
			else:
				logging.debug("TRIGEER INLINE")
				output+=buffer
				buffer=""
				return inline_equation_state
		else:
			buffer+=token
		return idle_state
	
	
	def sleep_one(token,peek):
		if token!="$":
			print("ERROR!!!")
		return idle_state
		
	state=idle_state
	
	text+=" "# Last peek is this space.
	for i in range(len(text)-1):
		token=text[i]
		peek=text[i+1]
		state=state(token,peek)
	output+=buffer
		
	
	
	
	return output
	
def get_abs_path_from_relative(rel):
	return str(Path(rel).resolve())

"""

"""
parser = argparse.ArgumentParser(description='Add latex to README files.')


parser.add_argument('source',  type=str, 
                    help='location of source file')

parser.add_argument('target',  type=str, 
                    help='location of target file')

parser.add_argument('-p',dest="build_std_show",action='store_true', 
                    help='display latex compiler process output')
parser.add_argument('-v', '--verbose', action='count', default=0,help='verbose mode -v or -vv')




"""
Formating guide: https://docs.python.org/3/library/logging.html#logging.Formatter



Level

Numeric value
CRITICAL	50
ERROR	40
WARNING	30
INFO	20
DEBUG	10
NOTSET	0
"""


#FORMAT = '%(filename)s:%(lineno)d [%(levelname)s]\t%(message)s'


args = parser.parse_args()

"""
none:0
-v:1 Info
-vv:2 
"""

verbosity=args.verbose


FORMAT = '%(filename)s:%(lineno)d [%(levelname)s]\t%(message)s'
if verbosity==0:
	FORMAT = '%(message)s'
	logging.basicConfig(level=logging.WARNING,format=FORMAT)
elif verbosity==1:
	logging.basicConfig(level=logging.INFO,format=FORMAT)
elif verbosity==2:
	logging.basicConfig(level=logging.DEBUG,format=FORMAT)
	


source_dir=get_abs_path_from_relative(args.source)
target_dir=get_abs_path_from_relative(args.target)


logging.info("Reading from "+source_dir)
logging.info("Writing to "+target_dir)

test_path_validity(source_dir)
test_if_path_has_file(source_dir,"README.md")
test_path_validity(target_dir)

readme_loc=file_append_to_path(source_dir,"README.md")

text=get_text_of_file(readme_loc)

ltx=LatexPngGenerator(args.build_std_show,target_dir)
run_latexifyer(ltx,text,generate_output=False)
new_readme_text=run_latexifyer(ltx,text)

save_text_to_file(file_append_to_path(target_dir,"README.md"),new_readme_text)


#OK




