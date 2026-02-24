import re
import pandas as pds
from datetime import datetime as dt

class Preprocess:
    """ Cleaning text data to prepare for analysis """
    
    def __init__(self):
         self.sp_wrds = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
         
    # Cleaning Texts
    
    def clean_txt(self, txt):
        if not txt or not isinstance(txt, str):
            return "Praise The Fool"
        
        txt= txt.lower()
        txt= re.sub(r'http\S+|www\S+', '', txt)
        txt= re.sub(r'\S+@\S+', '', txt)
        txt= re.sub(r'[^a-z0-9\s.,\'!?]', '', txt)
        txt= re.sub(r'\s+', ' ', txt).strip()
        
        return txt
    
    def rm_sp_wrds(self, txt):
        wrds= txt.split()
        fil_wrds= [w for w in wrds if w not in self.sp_wrds]
        return ' '.join(fil_wrds)
    
    # Extracting texts
    
    def ext_wrds(self, wrds, min_len= 3):
        wrds= self.clean_txt(wrds)
        wrds= wrds.split()
        
        wrds= [w for w in wrds if len(w) >= min_len]
        
        return wrds
    
    # Creating DataFrame
    
    def crte_dataframe(self, txt_list):
        rec= []
        
        for t in txt_list:
            rec.append({  
                'id': t.id,
                'text': t.text,
                'clean_text': self.clean_txt(t.text),
                'author': t.author,
                'timestamp': t.og_timestamp or t.collected_at,
                'word_count': len(t.text.split()),
                'source_id': t.source_id
                })
            
        df= pds.DataFrame(rec)
        df['timestamp']= pds.to_datetime(df['timestamp'])
        df= df.sort_values('timestamp').reset_index(drop= True)
        
        return df
    
    # Including Time Window column to Group
    
    def crte_time_wdw(self, df, win= 'D'):
        df= df.copy()
        df['time_window']= df['timestamp'].dt.to_period(win)
        
        return df