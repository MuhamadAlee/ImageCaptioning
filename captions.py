from http.server import BaseHTTPRequestHandler, HTTPServer
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.core.image_featurizers import ImageLoader
from typing import Dict, Any
import glob
import pandas as pd
import json
import cgi
import PIL.Image as Image
from base64 import b64decode
import io
import os
import random
import nltk


class Caption():
    
    SHARED: Dict[str, Any]={}
    IMAGE_LOADER=None 
    def __init__(self):
         
         self.SHARED: Dict[str, Any] = {}
         self.IMAGE_LOADER = None
         self.setup_interactive()




    def setup_interactive(self):
        """
        Set up the interactive script.
        """
        parser = setup_args()
        opt = parser.parse_args()
        print(opt)
        if not opt.get('model_file'):
            raise RuntimeError('Please specify a model file')
        if opt.get('fixed_cands_path') is None:
            opt['fixed_cands_path'] = os.path.join(
                '/'.join(opt.get('model_file').split('/')[:-1]), 'candidates.txt'
            )
        opt['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'
        opt['image_mode'] = 'resnet152'
        
        
        self.SHARED['opt'] = opt
        self.SHARED['image_loader'] = ImageLoader(opt)

        # Create model and assign it to the specified task
        self.SHARED['agent'] = create_agent(opt, requireModelExists=True)
        self.SHARED['world'] = create_task(opt, self.SHARED['agent'])




   
    def Generator(self,encoded, personality):
        """
        Generate a model response.

        :param data:
            data to send to model

        :return:
            model act dictionary
        """
        reply = {}
       
        # reply['text'] = data['personality'][0].decode()
        n = random.randint(0,1)
        reply['text']=personality
        
        
        # img_data = str(data['image'][0])
        # _, encoded = img_data.split(',', 1)
        image = Image.open(encoded).convert('RGB')
        reply['image'] = self.SHARED['image_loader'].extract(image)
        self.SHARED['agent'].observe(reply)
        model_res = self.SHARED['agent'].act()
        caption=model_res["text"]
        # cap=self.preprocess(caption)
        # print("Caption==>",caption)
        # image.save(caption+".png")
        # image.save(cap+".png")
        return caption

    def preprocess(self,txt):
        pronouns=["you","he","him","she","her","it","they","them","your","man","woman","men","women","girl","boy","girls","boys","this","that","lady","ladies","what","wife"]
        txt = txt.lower()
        tokens = nltk.word_tokenize(txt)
        rem=[]
        for tk in tokens:
            if(tk in pronouns):
               rem.append(tk)
            if (tk=="beautiful"):
               tk.replace("beautiful","beauty")

        for tk in rem:
            tokens.remove(tk)
        
        txt=""    
        for tk in tokens:
            txt+=tk+" "
        return txt 
        

def process_images():
    for i in range(1,4):
        a=Caption()
        lst_caption=[]
        lst_images=[]
        personalities = [ "Attractive",  "Enthusiastic",  "Happy", "Romantic", "Sentimental","Charming","Profound","Sophisticated","Fun-loving","Exciting","Adventurous"]
        for img in glob.glob(str(i)+"/*.png"):
            for personality in personalities:
                lst_caption.append(a.Generator(img,personality))
                lst_images.append(img)

        df = pd.DataFrame(list(zip(lst_images, lst_caption)), columns = ['images', 'captions'])
        df.to_csv(str(i)+".csv")

process_images()