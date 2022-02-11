Its Image Captioning Customized Version of PARLAY.
Here are the following setps to follow.

**Create and activate Virtual envirnment.**

    1) virtualenv -p python3 env 
    2) source env/bin/activate
    
**Install official git repo as a utility.**
 
    1) pip install parlai
    2) python projects/personality_captions/interactive.py -mf models:personality_captions/transresnet/model

**Copy Data Folder.**
1) Copy data folder from env env/lib/python3.6/site-packages/data into Current Working Directory.

**Run Python File.**
    
    1)python main.py
