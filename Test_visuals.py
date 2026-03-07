import os
from App import create_app, db
from App.Model import Textdata
from App.Utils.prep import Preprocess
from App.Utils.sentiment import Sentimentanalyzer
from App.Utils.drift_det import Driftanalyzer
from App.Utils.visual import Driftvisualizer

def test_visualizations():
    app = create_app()
    
    with app.app_context():
        # Getting data
        
        texts = Textdata.query.all()
        
        if not texts:
            print("Data must be empty as your bank account, load some data using the Scraper..")
            return
        
        print("Generating Visualizations...\n")
        prep= Preprocess()
        sentinyzr= Sentimentanalyzer()
        drift= Driftanalyzer()
        visual= Driftvisualizer()
        
        df = prep.crte_dataframe(texts)
        df = sentinyzr.analyze_df(df)
        df = prep.crte_time_wdw(df, win='D')
        
        drift_report = drift.gen_drift_rpt(df)
        
        # Generate charts
        
        charts = visual.create_dashboard(df, drift_report)
        
        print(f"Generated {len(charts)} charts:")
        for name in charts.keys():
            print(f"  ✓ {name}")
        
        html = f"""
        <html>
        <head><title>Test Visualization</title></head>
        <body>
            <h1>Sentiment Timeline</h1>
            <img src="{charts['sentiment_timeline']}" width="100%">
            <img src="{charts['sentiment_distribution']}" width="100%">
            <img src="{charts['activity_timeline']}" width="100%">
            <img src="{charts['word_comparison']}" width="100%">
            <img src="{charts['cumulative_drift']}" width="100%">
        </body>
        </html>
        """
        
        with open('Test_chart.html', 'w') as f:
            f.write(html)
        
        print("\n✓ Saved Test_chart.html ~")
        
        # Saving the Dataframe as excel to checks the data
        b_dir= os.path.dirname(os.path.abspath(__file__))
        o_dir= os.path.join(b_dir,'Test_data')
        os.makedirs(o_dir, exist_ok= True)
        
        name= os.path.join(o_dir, 'Data_Output.xlsx')
        t, b= os.path.splitext(name)
        c= 1
        while os.path.exists(name):
            name= f"{t}_{c}{b}"
            c+= 1
            
        df.to_excel(name, index= False)
        print(f">.< Excel Sheet saved at {name} >.<")

if __name__ == '__main__':
    test_visualizations()
