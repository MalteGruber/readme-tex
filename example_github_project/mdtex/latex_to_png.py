import os
from subprocess import call
from file_handling import *

import logging

class LatexPngGenerator:
    def __init__(self,show_build_output,target_dir):
        self.img_cnt=0
        self.github_img_tax=""
        self.show_build_output=show_build_output
        self.target_dir=target_dir
    def _get_github_img_tag(self,path,desc):
        return "![{}]({})".format(desc,path)
    
    
    
    
    def consume_latex(self,tex):
        self._consume_latex(tex)
        
    def consume_latex_inline(self,tex):
        self._consume_latex(tex,"template_inline.tex")
    def _consume_latex(self,tex,template_file="template.tex"):
        
        logging.debug("Generating image for "+tex.strip())
        logging.debug("Image count is "+str(self.img_cnt))
        
        #Insert forula into the template file and save it
        template=get_text_of_file(get_mdtex_folder()+"/"+template_file)        
        template=template.replace("FORMULA_PLACED_HERE",tex);
        
        save_text_to_file(get_mdtex_folder()+"/formula.tex",template)
        
        relative_name="teximg/tex_img_"+str(self.img_cnt)+".png"
        outname=file_append_to_path(self.target_dir,relative_name)
        self.img_cnt+=1
        
        logging.debug("make with output to "+outname)
                        
        void = open('/dev/null', 'w')
        
        cmd=["make","-C",get_mdtex_folder(),"all","OUTNAME="+outname]
        if self.show_build_output:
            print("Calling",cmd)
            void=None
        else: 
            logging.debug("Latex build process not printed")
            
            
        ret=call(cmd,stdout=void,stderr=void)
        logging.debug("Process returned {}".format(ret))
        if ret!=0:
            logging.error("Could not compile the formula `{}`".format(tex.strip()))
        
        
        if void!=None:
            
            void.close()
        
        self.github_img_tax=self._get_github_img_tag(relative_name,tex.replace("\n",""))

    def get_latex_image_path(self):
        return self.github_img_tax
