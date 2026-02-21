import requests
from bs4 import BeautifulSoup
from datetime import datetime
from App import db
from App.Model import Datasource, Textdata

class Redditscraper:
    
    """ This will scrape the deets without API, Also aggreeing with robot.txt. It will only scrape posts under restriction"""
    
    def __init__(self, subreddit, max_posts= 50):
        self.subreddit= subreddit
        self.max_posts= max_posts
        self.base_url= f'https://old.reddit.com/r/{subreddit}'
        self.headers= {'User-agent' : 'Chromium(Educational Research Bot)'}
        
    def scrape_posts(self):
        # Scrape Posts From Subreddits
        
        posts= []
        
        try:
            # Requests Subreddit Pages
            res= requests.get(
                self.base_url, 
                headers= self.headers, 
                timeout= 10
                )
            
            # Check 'Res' Status
            res.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(res.text, 'lxml')
            
            # Extract Posts
            post_elements = soup.find_all('div', class_= 'thing', limit= self.max_posts )
            
            for post in post_elements:
                try:
                    # Extract Titles
                    title_elements= post.find('a', class_='title')
                    if not title_elements:
                        continue
                    
                    title = title_elements.get_text(strip= True)
                    
                    # Extract Timestamps
                    time_elements= post.find('time')
                    timestamp= None
                    if time_elements and time_elements.get('datetime'):
                        timestamp= datetime.fromisoformat(time_elements['datetime'].replace('Z',' +00:00'))
                        
                    
                    # Extract Author Names
                    author_elements= post.find('a', class_='author')
                    author= author_elements.get_text(strip= True) if author_elements else 'Unknown'
                    
                    # Add On the 'Posts' List
                    posts.append({
                        'Title': title, 
                        'Author': author, 
                        'Timestamp': timestamp or datetime.utcnow()
                        })
                
                except Exception as e:
                    print(f"Something Wrong while Parsing The Post: {e}") 
                    continue
                
            print(f"Successfully Scraped {len(posts)} from r/{self.subreddit}") 
            return posts
        
        except requests.exceptions.RequestException as e:
            print(f"Something Wrong While Requesting: {e}")
            return []
    
    def save_db(self, posts):
        # Saving The Scraped Posts to Database
        
        # Get Or Create The Datasource
        source= Datasource.query.filter_by(
            name= f"Reddit - r/{self.subreddit}",
            source_type= "Reddit"
        ).first()
        
        if not source:
            source= Datasource(
                name= f"Reddit - r/-{self.subreddit}",
                source_type= "Reddit",
                url= self.base_url
            )
            
            db.session.add(source)
            db.session.commit()
            
        # Update Last Scraped Time
        source.last_scraped= datetime.utcnow()
        
        # Save Posts
        saved_count= 0
        for post_data in posts:
            text_entry= Textdata(
                source_id= source.id,
                text= post_data['Title'],
                author= post_data['Author'],
                og_timestamp= post_data['Timestamp']
            )
            db.session.add(text_entry)
            saved_count+= 1
        
        db.session.commit()
        print(f"Total Posts Saved To The Database : {saved_count}")
        
        return saved_count