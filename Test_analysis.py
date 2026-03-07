from App import create_app, db
from App.Model import Textdata
from App.Utils.prep import Preprocess
from App.Utils.sentiment import Sentimentanalyzer
from App.Utils.drift_det import Driftanalyzer
import pandas as pd

def test_analysis():
    
    app= create_app()
    
    with app.app_context():
        # Fetching data from database
        
        txt= Textdata.query.all()
        
        if not txt:
            print("Some flies are flying inside the database, Fend them off and run scraper to collect data")
            return 
        
        print(f"Analyzing {len(txt)} texts...Hold On!")
        
        prep= Preprocess()
        senti= Sentimentanalyzer()
        drift= Driftanalyzer()
        
        df= prep.crte_dataframe(txt)
        print(f"Dataframe Created: {df.shape}")
        
        df= senti.analyze_df(df)
        print(f"\nSentiment Distribution: ")
        print(df['sentiment_label'].value_counts())
        
        df= prep.crte_time_wdw(df, win= 'D')
        
        report= drift.gen_drift_rpt(df)
        
        print(f"\n ~~~~~ Drift Analysis Report ~~~~~")
        print(f"Time windows analyzed: {report['summary']['total_windows']}")
        print(f"Significant sentiment shifts: {report['summary']['significant_sentiment_shifts']}")
        print(f"Topic shifts detected: {report['summary']['topic_shifts']}")
        print(f"Overall trend: {report['summary']['overall_sentiment_trend']}")
        
        if report['significant_shifts']:
            print(f"\n ~~~~~ Significant Shifts ~~~~~")
            for s in report['significant_shifts']:
                print(f"{s['time_window']} : {s['direction']} shift of {s['change']}")
        
if __name__== '__main__':
    test_analysis()
