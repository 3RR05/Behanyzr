import requests
import time
from datetime import datetime
from App import db
from App.Model import Datasource, Textdata


class Redditscraper:
    # Scrape posts and comments from Reddit
    
    def __init__(self, subreddit, max_posts=15):
        self.subreddit = subreddit
        self.max_posts = max_posts
        self.base_url = f"https://www.reddit.com/r/{subreddit}"
        self.headers = {'User-Agent': 'Behanyzr (Educational Project)'}

    def get_json(self, url):
        # Fetching JSON data from Reddit
        
        try:
            res = requests.get(url, headers=self.headers, timeout=60)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f"Can't fetch a fly in {url}: {e}")
            return None

    def scrape_post_comments(self, post_id, post_title, author, timestamp):
        # Fetching comments from the posts
        
        results = []
        url = f"https://www.reddit.com/r/{self.subreddit}/comments/{post_id}.json"
        
        data = self.get_json(url)
        if not data or len(data) < 2:
            results.append({
                'text': post_title,
                'author': author,
                'timestamp': timestamp,
                'content_type': 'post_title'
            })
            return results

        try:
            post_data = data[0]['data']['children'][0]['data']
            selftext = post_data.get('selftext', '').strip()

            if selftext and selftext not in ('[deleted]', '[removed]') and len(selftext) > 5:
                results.append({
                    'text': selftext,
                    'author': author,
                    'timestamp': timestamp,
                    'content_type': 'post_body'
                })
                
            else:
                results.append({
                    'text': post_title,
                    'author': author,
                    'timestamp': timestamp,
                    'content_type': 'post_title'
                })
            # Fetching Comments
            
            comments = data[1]['data']['children']

            for c in comments[:20]:
                try:
                    if c.get('kind') != 't1':
                        continue

                    comment_data = c['data']
                    comment_text = comment_data.get('body', '').strip()

                    if not comment_text:
                        continue
                    if comment_text in ('[deleted]', '[removed]'):
                        continue
                    if len(comment_text) < 5:
                        continue

                    comment_author = comment_data.get('author', 'Unknown')

                    # Converting Unix timestamp to datetime
                    
                    comment_created = comment_data.get('created_utc')
                    if comment_created:
                        comment_time = datetime.utcfromtimestamp(comment_created)
                    else:
                        comment_time = timestamp

                    results.append({
                        'text': comment_text,
                        'author': comment_author,
                        'timestamp': comment_time,
                        'content_type': 'comment'
                    })

                except Exception as e:
                    print(f"Something gone wrong, Skipping comments: {e}")
                    continue

        except (KeyError, IndexError) as e:
            print(f"Got some fishbone while parsing the posts data: {e}")
            results.append({
                'text': post_title,
                'author': author,
                'timestamp': timestamp,
                'content_type': 'post_title'
            })

        return results

    def scrape_posts(self):
        # Fetching posts, comments and its underlying tags via Reddit's JSON
        
        print(f"\nScraping from r/{self.subreddit} (up to {self.max_posts} posts)... >_<")
        all_items = []

        listing_url = f"{self.base_url}.json?limit={self.max_posts}"
        data = self.get_json(listing_url)

        if not data:
            print("You might flagged Dude!..")
            return []

        posts = data['data']['children']
        print(f"{len(posts)} posts Extracted.")

        for i, post in enumerate(posts, 1):
            try:
                post_data = post['data']

                title = post_data.get('title', '')
                post_id = post_data.get('id', '')
                author = post_data.get('author', 'Unknown')
                
                created_utc = post_data.get('created_utc')
                timestamp = datetime.utcfromtimestamp(created_utc) if created_utc else datetime.utcnow()

                print(f"~~ [{i}/{len(posts)}] {title[:60]}...")

                # Fetching post body and comments
                
                items = self.scrape_post_comments(post_id, title, author, timestamp)
                all_items.extend(items)

                print(f"~~~~ Got {len(items)} text items\n")
                time.sleep(1.5)

            except Exception as e:
                print(f"Something gone wrong in this post-{i}: {e}")
                continue

        print(f"\nTotal contents collected: {len(all_items)}")
        print(f"Post Bodies/Titles : {sum(1 for x in all_items if x['content_type'] in ('post_body', 'post_title'))}")
        print(f"Comments           : {sum(1 for x in all_items if x['content_type'] == 'comment')}")
        return all_items

    def save_db(self, items):
        # Saving it to database

        source = Datasource.query.filter_by(
            name=f"Reddit - r/{self.subreddit}",
            source_type="reddit"
        ).first()

        if not source:
            source = Datasource(
                name=f"Reddit - r/{self.subreddit}",
                source_type="reddit",
                url=self.base_url
            )
            db.session.add(source)
            db.session.commit()

        source.last_scraped = datetime.utcnow()

        saved_count = 0
        for item in items:
            entry = Textdata(
                source_id=source.id,
                text=item['text'],
                author=item['author'],
                og_timestamp=item['timestamp']
            )
            db.session.add(entry)
            saved_count += 1

        db.session.commit()
        print(f"loaded {saved_count} contents to database, Gig finisehd.")
        return saved_count