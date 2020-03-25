import argparse

import logging
from pathlib import Path

from latex_to_png import *
from file_handling import *

import os


import sys

def on_error(msg):
	logging.error(msg)
	sys.exit(-1)

	
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
					output+="{}".format(ltx.get_latex_image_path())
				buffer=""
				
				return idle_state
			elif len(buffer)>0:
				
				on_error("Line {}: Expected a single termination '$' of inline equation:{}".format(output.count("\n"),buffer))
		else:
			buffer+=token
		return inline_equation_state
		
		
	def header_injection_state(token,peek):

		nonlocal buffer, output
		logging.debug("INEJCT '{}' '{}'".format(token,peek))
		if token=="$":
			if peek=="@":
				ltx.set_header_injection(buffer)
				buffer=""
				return sleep_one
			elif len(buffer)>0:
				on_error("Line {}: Expected a single termination '$@' of header injection: {}".format(output.count("\n"),buffer))
		elif token=="@" and len(buffer)==0:
			pass
		else:
			buffer+=token
		return header_injection_state
		
	def full_equation_state(token,peek):
		nonlocal buffer, output
		logging.debug("FULL '{}' '{}'".format(token,peek))
		if token=="$":
			if peek=="$":
				if generate_output:
					ltx.consume_latex(buffer)
					output+="{}".format(ltx.get_latex_image_path())
				buffer=""
				return sleep_one
			elif len(buffer)>0:
				on_error("Line {}: Expected a single termination '$$' of equation: {}".format(output.count("\n"),buffer))
		else:
			buffer+=token
		return full_equation_state
		
	def escape_state(token,peek):
		nonlocal buffer, output
		logging.debug("ESCAPE '{}' '{}'".format(token,peek))
		buffer+=token
		if token!="$":
			return idle_state
		return escape_state
	
	def idle_state(token,peek):
		nonlocal buffer, output
		logging.debug("IDLE '{}' '{}'".format(token,peek))
		if token=="$":
			if peek=="$":
				logging.debug("TRIGEER FULL")
				output+=buffer
				buffer=""
				return full_equation_state
			if peek=="@":
				logging.debug("TRIGEER INEJCTION")
				output+=buffer
				buffer=""
				return header_injection_state		
			else:
				logging.debug("TRIGEER INLINE")
				output+=buffer
				buffer=""
				return inline_equation_state
		if token=="\\":
			if peek=="$":
				output+=buffer
				buffer=""
				return escape_state
			else:
				buffer+=token
		else:
			buffer+=token
		return idle_state
	
	
	def sleep_one(token,peek):
		if token not in ["$","@"]:
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


parser = argparse.ArgumentParser(description='Add latex to README files.')

#parser.add_argument('source',  type=str, 
 #                   help='location of source file')

#parser.add_argument('target',  type=str, 
 #                   help='location of target file')

parser.add_argument('-p',dest="build_std_show",action='store_true', 
                    help='display latex compiler process output')

parser.add_argument('-v', '--verbose', action='count', default=0,help='verbose mode -v or -vv')
parser.add_argument('-c',dest="clean",action='store_false', 
                    help='do not clean output folder')

parser.add_argument('-D', dest="resolution", default=120,help='dvipng output resolution argument (-D)')
parser.add_argument('-n',dest="nonce",action='store_false', 
                    help='Disable random nonce in image names (nonce prevents caching)')

parser.add_argument('-s', dest="source_readme", default="README.md",help='name of source README.md relative to doc folder (Default: README.md)')
parser.add_argument('-l', dest="doc_folder", default="doc",help='target doc folder, (default ./doc) (relative)')
parser.add_argument('-o', dest="new_readme", default="README.md",help='New readme file with image tags, i.e. the public one (default README.md)')


"""
Formating guide: https://docs.python.org/3/library/logging.html#logging.Formatter


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

FORMAT = '%(filename)s:%(lineno)d [%(levelname)s] %(message)s'
if verbosity==0:
	FORMAT = '[%(levelname)s] %(message)s'
	logging.basicConfig(level=logging.WARNING,format=FORMAT)
elif verbosity==1:
	logging.basicConfig(level=logging.INFO,format=FORMAT)
elif verbosity==2:
	logging.basicConfig(level=logging.DEBUG,format=FORMAT)



"""
Program structure
The files will locate themselfs and exectue the code relative to the /mdtex location where they are stored.

Note:In docker the entrypoint is the mounted (I.e, the one containing the doc folder) 
folder which the user just ran the docker run command in (Using the readme-tex-docker script).

The Makefile in /mdtex/Makefile runs localy in the mdtex folder and uses the /mdtex/build folder.



"""



rel_target_dir=args.doc_folder
target_dir=os.getcwd()+"/"+rel_target_dir
taget_readme=args.source_readme
new_readme_file=args.new_readme




if not path_exists(target_dir):
	logging.error("Could not find the folder{}, please create it and add the file {} to it! This file will be parsed and the latex images will be added to the folder".format(target_dir,taget_readme))
	sys.exit(-1)
if not path_has_file(target_dir,taget_readme):
	logging.error("Could not find the file {} in the folder {}, please add it, this file will be parsed".format(target_dir,taget_readme))
	sys.exit(-1)




logging.info("doc folder "+target_dir)
logging.info("Resolution {}, nonce {}".format(args.resolution,args.nonce))


test_path_validity(target_dir)

#eadme_loc=file_append_to_path(source_dir,)




text=get_text_of_file(target_dir+"/"+taget_readme)

ltx=LatexPngGenerator(args.build_std_show,target_dir,rel_target_dir,
					resolution=args.resolution,generate_nonce=args.nonce)

if args.clean:
	ltx.clean_output_folder()


run_latexifyer(ltx,text,generate_output=False)
new_readme_text=run_latexifyer(ltx,text)

save_text_to_file(new_readme_file,new_readme_text)


#OK




