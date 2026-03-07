from flask import jsonify, request
from App.Route import a_bp
from App import db
from App.Model import Datasource, Textdata
from App.Utils.prep import Preprocess
from App.Utils.sentiment import Sentimentanalyzer
from App.Utils.drift_det import Driftanalyzer
from datetime import datetime, timedelta

@a_bp.route('/sources', methods=['GET'])
def get_sources():
    # List all data sources
    
    sources = Datasource.query.all()
    
    return jsonify({
        'success': True,
        'count': len(sources),
        'sources': [{
            'id': s.id,
            'name': s.name,
            'type': s.source_type,
            'url': s.url,
            'created_at': s.created_at.isoformat() if s.created_at else None,
            'last_scraped': s.last_scraped.isoformat() if s.last_scraped else None,
            'text_count': Textdata.query.filter_by(source_id=s.id).count()
        } for s in sources]
    })

@a_bp.route('/sources/<int:source_id>', methods=['GET'])
def get_source(source_id):
    # Return data from specific source_id
    
    source = Datasource.query.get_or_404(source_id)
    
    return jsonify({
        'success': True,
        'source': {
            'id': source.id,
            'name': source.name,
            'type': source.source_type,
            'url': source.url,
            'created_at': source.created_at.isoformat() if source.created_at else None,
            'last_scraped': source.last_scraped.isoformat() if source.last_scraped else None,
            'text_count': Textdata.query.filter_by(source_id=source.id).count()
        }
    })

@a_bp.route('/analyze', methods=['POST'])
def analyze_data():
    # Analyze data
    
    data = request.get_json()
    
    if not data or 'source_id' not in data:
        return jsonify({
            'success': False,
            'error': 'Need source_id!'
        }), 400
    
    source_id = data['source_id']
    time_window = data.get('time_window', 'D')
    
    # Validate time window
    
    if time_window not in ['H', 'D', 'W', 'M']:
        return jsonify({
            'success': False,
            'error': 'time_window must be H, D, W, or M'
        }), 400
    
    texts = Textdata.query.filter_by(source_id=source_id).all()
    
    if not texts:
        return jsonify({
            'success': False,
            'error': 'No data found for this source'
        }), 404
    
    preprocessor = Preprocess()
    sentiment_analyzer = Sentimentanalyzer()
    drift_detector = Driftanalyzer()
    
    df = preprocessor.crte_dataframe(texts)
    df = sentiment_analyzer.analyze_df(df)
    df = preprocessor.crte_time_wdw(df, window= time_window)
    
    report = drift_detector.gen_drift_rpt(df)
    
    return jsonify({
        'success': True,
        'analysis': report
    })

@a_bp.route('/sentiment/timeline', methods=['GET'])
def sentiment_timeline():
    # Return Sentiment overtime
    
    source_id = request.args.get('source_id', type=int)
    days = request.args.get('days', default=7, type=int)
    
    if not source_id:
        return jsonify({
            'success': False,
            'error': 'Need source_id!'
        }), 400
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    texts = Textdata.query.filter(
        Textdata.source_id == source_id,
        Textdata.collected_at >= cutoff_date
    ).all()
    
    if not texts:
        return jsonify({
            'success': False,
            'error': 'No recent data found'
        }), 404
    
    # Quick sentiment analysis
    
    preprocessor = Preprocess()
    sentiment_analyzer = Sentimentanalyzer()
    
    df = preprocessor.crte_dataframe(texts)
    df = sentiment_analyzer.analyze_df(df)
    df = preprocessor.crte_time_wdw(df, window= 'D')
    
    # Aggregate the data by day
    
    daily_sentiment = df.groupby('time_window')['sentiment_score'].mean()
    
    return jsonify({
        'success': True,
        'timeline': [{
            'date': str(date),
            'sentiment': float(score)
        } for date, score in daily_sentiment.items()]
    })

@a_bp.route('/stats', methods=['GET'])
def get_stats():
    # Return overall statistics
    
    total_sources = Datasource.query.count()
    total_texts = Textdata.query.count()
    
    # Recent activity (last 24 hours)
    
    yesterday = datetime.utcnow() - timedelta(hours=24)
    recent_texts = Textdata.query.filter(
        Textdata.collected_at >= yesterday
    ).count()
    
    # Average sentiment (last 100 texts)
    
    recent = Textdata.query.order_by(
        Textdata.collected_at.desc()
    ).limit(100).all()
    
    if recent:
        preprocessor = Preprocess()
        sentiment_analyzer = Sentimentanalyzer()
        df = preprocessor.crte_dataframe(recent)
        df = sentiment_analyzer.analyze_df(df)
        avg_sentiment = df['sentiment_score'].mean()
    else:
        avg_sentiment = 0.0
    
    return jsonify({
        'success': True,
        'stats': {
            'total_sources': total_sources,
            'total_texts': total_texts,
            'texts_24h': recent_texts,
            'avg_sentiment_recent': round(float(avg_sentiment), 3)
        }
    })
# Error handling

@a_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@a_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500