import requests
from datetime import datetime as dt
from App import db
from App.Model import Datasource, Textdata

class Newsscraper:
    """ Scrape News articles using API """
    
    def __init__(self, api_key= None, query= "economy", mx_art= 50):
        self.api_key= api_key
        self.query= query
        self.mx_art= mx_art
        self.base_url= "https://newsapi.org/v2/everything"
        
    def scrape_arts(self):
        # Scrape articles from NewsAPI
        
        prm= {
            'q' : self.query,
            'pagesize' : min(self.mx_art, 100),
            'sortby' : 'publishedAt',
            'language' : 'en',
            'apikey' : self.api_key
        }
        
        arts= []
        
        try:
            
            res= requests.get(self.base_url, params=prm, timeout= 10)
            res.raise_for_status()
            
            deets= res.json()
            for ar in deets.get('article', []):
            # Combining title and description
            
                txt= ar.get('title','')
                des= ar.get('description')
            
                if des:
                    txt += "--" + des
            
                if txt:
                    arts.append({
                        'text' : txt,
                        'author' : ar.get('author') or 'Stand User Could be Anyone',
                        'timestamp' : dt.fromisoformat(ar['publishedAt'].replace('Z', ' +00:00'))
                        if ar.get('publishedAt') else dt.utcnow()
                    })

            print(f"Gathered {len(arts)} Articles from {self.base_url}")
            return arts
            
        except requests.exceptions.RequestException as e:
            print(f"Got some fishbone while fetching: {e}")
            return []
        except Exception as e:
            print(f"Got something thrown out while processing the Articles: {e}")
            return []
        
    def save_db(self, arts):
        # Saving the Articles into Database
        
        source= Datasource.query.filter_by(
            name= f"NewsAPI - {self.query}",
            source_type= "News"
        ).first()
        
        if not source:
            source= Datasource(
                name= f"NewsAPI - {self.query}",
                source_type= "News",
                url= self.base_url
            )
            
            db.session.add(source)
            db.session.commit()
        
        source.last_scraped= dt.utcnow()
        
        sv_count= 0
        
        for ar in arts:
            text_entry= Textdata(
                source_id= source.id,
                text= ar['text'],
                author= ar['author'],
                og_timestamp= ar['timestamp']
            )
            
            db.session.add(text_entry)
            saved_count+= 1
        
        db.session.commit()
        
        print(f"Saved {saved_count} Articles to Database")
        
        return saved_count