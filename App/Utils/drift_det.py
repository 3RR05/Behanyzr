import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter

class Driftanalyzer:
    # Detect changes in the patterns over time
    
    def cal_sentiment_drift(self, df, time_column= 'time_window', sentiment_column= 'sentiment_score'):
        # Group data by time window
        
        drf_df= df.groupby(time_column).agg({
            sentiment_column : ['mean', 'std', 'count'], 'id' : 'count'
        }).reset_index()
        
        # Flattening column names
        
        drf_df.columns= ['time_window', 'avg_sentiment', 'sentiment_std', 'sentiment_count', 'total_texts']
        
        # Calculate changes from previous data
        
        drf_df['sentiment_change']= drf_df['avg_sentiment'].diff()
        
        # Calculate cumulative changes
        
        drf_df['cumulative_change']= drf_df['sentiment_change'].cumsum()
        
        return drf_df
    
    def dct_sig_shifts(self, drf_df, threshold= 0.2):
        
        shifts = []
        
        for i, r in drf_df.iterrows():
            if pd.notna(r['sentiment_change']) and abs(r['sentiment_change']) > threshold:
                shifts.append({
                    'time_window' : str(r['time_window']),
                    'change' : round(r['sentiment_change'],3),
                    'new_sentiment' : round(r['avg_sentiment'],3),
                    'direction' : 'Positive' if r['sentiment_change'] > 0 else 'Negative',
                    'magnitude' : 'Large' if abs(r['sentiment_change']) > 0.3 else 'Moderate'
                })
                
        return shifts
    
    def cal_voc_drift(self, df, time_column='time_window', text_column= 'clean_text', top_n= 20):
        # Checking vocabulary changes over time
        
        voc_evol= {}
        
        for win, grp in df.groupby(time_column):
            all_txt= ''.join(grp[text_column])
            
            wrds= all_txt.split()
            wrd_count= Counter(wrds)
            
            top_w= wrd_count.most_common(top_n)
            
            voc_evol[str(win)]= {
                'top_words' : top_w,
                'unique_words' : len(wrd_count),
                'total_words' : len(wrds)
            }
        
        return voc_evol
    
    def cal_aty_drift(self, df, time_column='time_window'):
        # Checking the posting activity over time
        
        aty = df.groupby(time_column).agg({
            'id': 'count',
            'author': 'nunique',
            'word_count': 'mean'
        }).reset_index()
        
        aty.columns = ['time_window', 'post_count', 'unique_authors', 'avg_length']
        
        # Calculate changes
        
        aty['post_count_change']= aty['post_count'].pct_change() * 100
        aty['author_change']= aty['unique_authors'].pct_change() * 100
        
        return aty
    
    def dct_topic_shifts(self, voc_evol):
        # Checking for dominant topics
        
        shifts = []
        windows = sorted(voc_evol.keys())
        
        for i in range(1, len(windows)):
            prev_window = windows[i-1]
            curr_window = windows[i]
            
            prev_words = set([w for w, c in voc_evol[prev_window]['top_words'][:10]])
            curr_words = set([w for w, c in voc_evol[curr_window]['top_words'][:10]])
            
            # Calculate overlap
            
            overlap = len(prev_words & curr_words) / 10.0
            
            if overlap < 0.5:
                shifts.append({
                    'from_window': prev_window,
                    'to_window': curr_window,
                    'overlap': round(overlap, 2),
                    'new_topics': list(curr_words - prev_words)[:5]
                })
        
        return shifts
    
    def gen_drift_rpt(self, df, time_window='D'):
        """ Generate drift analysis report """
        
        # Calculate all drift metrics
        
        sentiment_drift = self.cal_sentiment_drift(df, 'time_window')
        vocab_drift = self.cal_voc_drift(df, 'time_window')
        activity_drift = self.cal_aty_drift(df, 'time_window')
        
        # Detect significant changes
        
        sentiment_shifts = self.dct_sig_shifts(sentiment_drift)
        topic_shifts = self.dct_topic_shifts(vocab_drift)
        
        return {
            'sentiment_drift': sentiment_drift.to_dict('records'),
            'vocabulary_evolution': vocab_drift,
            'activity_drift': activity_drift.to_dict('records'),
            'significant_shifts': sentiment_shifts,
            'topic_shifts': topic_shifts,
            'summary': {
                'total_windows': len(sentiment_drift),
                'significant_sentiment_shifts': len(sentiment_shifts),
                'topic_shifts': len(topic_shifts),
                'overall_sentiment_trend': 'positive' if sentiment_drift['cumulative_change'].iloc[-1] > 0 else 'negative'
            }
        } 