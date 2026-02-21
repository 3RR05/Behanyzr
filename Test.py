from App import create_app, db
from App.Utils.scraper import Redditscraper

def test_scraper():
    # Testing The Functionality
    app= create_app()
    
    with app.app_context():
        # Creating Database Tables
        db.create_all()
        
        subreddit = str(input("Enter The Subreddit Page : "))
        # Initialize The Scraper
        scraper= Redditscraper(subreddit, max_posts=15)
        
        # Scrape Posts
        posts= scraper.scrape_posts()
        
        print(f"\n Total Scraped Posts : {len(posts)}")
        if posts:
            print("\n Sample Posts :")
            for i, p in enumerate(posts[:3]):
                print(f"\n {i}. {p['Title'][:100]}...\n Author : {p['Author']} \n Time : {p['Timestamp']}")
            
        # Save Into Database
        if posts:
            saved= scraper.save_db(posts)
            print(f"\n Saved {saved} Posts To Database")
                        
if __name__ == '__main__':
    test_scraper()