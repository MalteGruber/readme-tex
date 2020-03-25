import os
from subprocess import call
from file_handling import *
import glob

import logging

class LatexPngGenerator:
    def __init__(self,show_build_output,
                 abs_target_dir,rel_target_dir,
                 resolution,generate_nonce):
        self.img_cnt=0
        self.resolution=resolution
        self.github_img_tax=""
        self.show_build_output=show_build_output
        self.abs_taget_dir=abs_target_dir
        self.rel_target_dir=rel_target_dir
        self.generate_nonce=generate_nonce
        self.header_injection=""
    def _get_github_img_tag(self,path,desc):
        return "![{}]({})".format(desc,path)
    
    
    def set_header_injection(self,header_injection):
      self.header_injection=header_injection
      
    def clean_output_folder(self):

        files = glob.glob(self.abs_taget_dir+"/teximg/tex_img_*")        
        for file in files:
            try:
                os.remove(file)
            except:
                print("Error while deleting file : ", file)
                
          
    def consume_latex(self,tex):
        self._consume_latex(tex)
        
    def consume_latex_inline(self,tex):
        self._consume_latex(tex,inline=True)
        
    def _consume_latex(self,tex,inline=False):
        
        logging.debug("Generating image for "+tex.strip())
        logging.debug("Image count is "+str(self.img_cnt))
        
        #Insert forula into the template file and save it
        template=get_text_of_file(get_mdtex_folder()+"/template.tex")
        
        dollar="$$"
        if inline:
            dollar="$"   
        template=template.replace("HEADER_INJECTION_HERE",self.header_injection)
        template=template.replace("FORMULA_PLACED_HERE",dollar+tex+dollar);
        
        save_text_to_file(get_mdtex_folder()+"/formula.tex",template)
        
        
        N=5
        nonce=""
        if self.generate_nonce:
            import random
            import string
            nonce=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
            nonce="_"+nonce
        
        relative_name="teximg/tex_img_"+str(self.img_cnt)+nonce+".png"
        
        outname=file_append_to_path(self.abs_taget_dir,relative_name)

        self.img_cnt+=1
        
        logging.debug("make with output to "+outname)
        
        void = open('/dev/null', 'w')
        
        cmd=["make","-C",get_mdtex_folder(),"all","OUTNAME="+outname,"RESOLUTION="+str(int(self.resolution)),"DOC_FOLDER="+self.abs_taget_dir]
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

        self.github_img_tax=self._get_github_img_tag(self.rel_target_dir+"/"+relative_name,tex.replace("\n",""))

    def get_latex_image_path(self):
        return self.github_img_tax
