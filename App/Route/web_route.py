from flask import render_template, request, flash, redirect, url_for
from App.Route import m_bp
from App import db
from App.Model import Datasource, Textdata
from App.Utils.scraper import Redditscraper
from App.Utils.scraper_news import Newsscraper
from App.Utils.prep import Preprocess
from App.Utils.sentiment import Sentimentanalyzer
from App.Utils.drift_det import Driftanalyzer
from App.Utils.visual import Driftvisualizer


@m_bp.route('/')
def index():
    # Homepage
    
    total_sources= Datasource.query.count()
    total_texts= Textdata.query.count()
    recent_sources= Datasource.query.order_by(Datasource.last_scraped.desc()).limit(5).all()
    
    return render_template('B_index.html', 
                         total_sources=total_sources,
                         total_texts=total_texts,
                         recent_sources=recent_sources,
                         max=max)

@m_bp.route('/collect', methods=['GET', 'POST'])
def collect_data():
    # Data Collection Page
    
    if request.method == 'POST':
        source_type = request.form.get('source_type')
        
        if source_type == 'reddit':
            subreddit = request.form.get('subreddit', 'python')
            max_posts = int(request.form.get('max_posts', 50))
            
            try:
                scraper = Redditscraper(subreddit, max_posts)
                posts = scraper.scrape_posts()
                
                if posts:
                    saved = scraper.save_db(posts)
                    flash(f'Collected {saved} posts from r/{subreddit}', 'Success')
                else:
                    flash('Not even a fly collected, perhaps the subreddit might not exist', 'Warning')
                    
            except Exception as e:
                flash(f'Something gone wrong while collecting data : {str(e)}', 'Danger')
        
        elif source_type == 'news':
            query = request.form.get('query', 'technology')
            max_articles = int(request.form.get('max_articles', 50))
            
            try:
                scraper = Newsscraper(query=query, max_articles=max_articles)
                articles = scraper.scrape_arts()
                
                if articles:
                    saved = scraper.save_db(articles)
                    flash(f'Collected {saved} articles about "{query}"', 'Success')
                else:
                    flash('No articles found.', 'Warning')
                    
            except Exception as e:
                flash(f'Something wrong while collecting data : {str(e)}', 'Danger')
        
        return redirect(url_for('main.collect_data'))
    
    sources = Datasource.query.all()
    return render_template('B_collect.html', sources=sources)

@m_bp.route('/analyze/<int:source_id>')
def analyze_source(source_id):
    # Analyze specific data source using source_id
    
    source = Datasource.query.get_or_404(source_id)
    texts = Textdata.query.filter_by(source_id=source_id).all()
    
    if not texts:
        flash('No data to analyze for this one.', 'Warning')
        return redirect(url_for('main.index'))
    
    # Process data
    
    preprocessor = Preprocess()
    sentiment_analyzer = Sentimentanalyzer()
    drift_detector = Driftanalyzer()
    visualizer = Driftvisualizer()
    
    # Create analysis pipeline
    
    df = preprocessor.crte_dataframe(texts)
    df = sentiment_analyzer.analyze_df(df)
    df = preprocessor.crte_time_wdw(df, window='D')
    
    # Generate drift report
    
    drift_report = drift_detector.gen_drift_rpt(df)
    
    # Create visualizations
    
    charts = visualizer.create_dashboard(df, drift_report)
    
    return render_template('B_analysis.html',
                         source=source,
                         report=drift_report,
                         charts=charts,
                         total_texts=len(texts))

@m_bp.route('/sources')
def list_sources():
    # Listing all data
    
    sources = Datasource.query.order_by(Datasource.created_at.desc()).all()
    
    # Adding text count for each source
    
    source_data = []
    for source in sources:
        text_count = Textdata.query.filter_by(source_id=source.id).count()
        source_data.append({
            'source': source,
            'text_count': text_count
        })
    
    return render_template('B_sources.html', source_data=source_data)

@m_bp.route('/about')
def about():
    # About page
    
    return render_template('B_about.html')