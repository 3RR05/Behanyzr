import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class Driftvisualizer:
    """Creating visualizations for drift analysis report"""
    
    def __init__(self):
        self.colors = {
            'positive': '#52d053',
            'negative': '#765898',
            'neutral': "#676767",
            'primary': '#3498db'
        }
    
    def to_base64(self, fig):
        # Converting matplotlib figure to base64 string for embedding in HTML
        
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        buf.close()
        plt.close(fig)
        return f"data:image/png;base64,{img_str}"
    
    def plt_senti_timeline(self, drf_df, title="Sentiment Over Time"):
        # Line plot which shows the drfit evolution
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Converting time_window to string for plotting
        
        x = range(len(drf_df))
        labels = [str(tw) for tw in drf_df['time_window']]
        
        # Plotting average sentiment
        
        ax.plot(x, drf_df['avg_sentiment'], 
                marker='o', linewidth=2, markersize=8,
                color=self.colors['primary'], label='Average Sentiment')
        
        # Addding confidence band (std deviation)
        
        ax.fill_between(
            x,
            drf_df['avg_sentiment'] - drf_df['sentiment_std'],
            drf_df['avg_sentiment'] + drf_df['sentiment_std'],
            alpha=0.2, color=self.colors['primary'], label='±1 Std Dev'
        )
        
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.set_xlabel('Time Window', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sentiment Score', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x[::max(1, len(x)//10)]) 
        ax.set_xticklabels(labels[::max(1, len(x)//10)], rotation=45, ha='right')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.to_base64(fig)
    
    def plt_senti_dist(self, df, title="Sentiment Distribution"):
        # Histogram for sentiment scores
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df['sentiment_score'], bins=30, 
                color=self.colors['primary'], alpha=0.7, edgecolor='black')
        mean_sent = df['sentiment_score'].mean()
        ax.axvline(mean_sent, color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {mean_sent:.3f}')
        ax.set_xlabel('Sentiment Score', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return self.to_base64(fig)
    
    def plt_aty_timeline(self, aty_df, title="Activity Over Time"):
        # Dual-axis plot: post count and unique authors
        
        fig, ax1 = plt.subplots(figsize=(14, 6))
        
        x = range(len(aty_df))
        labels = [str(tw) for tw in aty_df['time_window']]
        
        color1 = self.colors['primary']
        ax1.set_xlabel('Time Window', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Post Count', color=color1, fontsize=12, fontweight='bold')
        ax1.bar(x, aty_df['post_count'], alpha=0.6, color=color1, label='Posts')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.set_xticks(x[::max(1, len(x)//10)])
        ax1.set_xticklabels(labels[::max(1, len(x)//10)], rotation=45, ha='right')
        
        ax2 = ax1.twinx()
        clr = self.colors['positive']
        ax2.set_ylabel('Unique Authors', color=clr, fontsize=12, fontweight='bold')
        ax2.plot(x, aty_df['unique_authors'], 
                 marker='o', linewidth=2, markersize=6, color=clr, label='Authors')
        ax2.tick_params(axis='y', labelcolor=clr)
        
        ax1.set_title(title, fontsize=14, fontweight='bold', pad=20)
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        return self.to_base64(fig)
    
    def plt_wrd_cloud_comp(self, vocab_evolution, time_windows=None):
        # Comparing top words across time windows
        exp = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'me', 'him', 'us', 'them',
        'who', 'what', 'which', 'whose', 'whom', 'myself', 'yourself', 'himself',
        'herself', 'itself', 'ourselves', 'themselves', 'each', 'every', 'all',
        'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'not', 'only',
        'same', 'so', 'than', 'too', 'very', 'just', 'any', 'either', 'neither',
        'about', 'above', 'after', 'against', 'along', 'among', 'around', 'before',
        'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'during',
        'except', 'if', 'into', 'near', 'off', 'out', 'outside', 'over', 'past',
        'since', 'through', 'throughout', 'till', 'under', 'until', 'up', 'upon',
        'while', 'within', 'without', 'although', 'because', 'unless', 'whether',
        'though', 'when', 'where', 'how', 'why', 'then', 'however', 'also',
        'get', 'got', 'getting', 'go', 'going', 'went', 'gone', 'make', 'made',
        'making', 'know', 'knew', 'knowing', 'think', 'thought', 'thinking',
        'take', 'took', 'taken', 'come', 'came', 'coming', 'see', 'saw', 'seen',
        'use', 'used', 'using', 'want', 'wanted', 'say', 'said', 'saying',
        'look', 'looked', 'looking', 'give', 'gave', 'given', 'keep', 'kept',
        'let', 'put', 'seem', 'seemed', 'tell', 'told', 'try', 'tried', 'ask',
        'need', 'feel', 'felt', 'become', 'became', 'leave', 'left', 'mean',
        'like', 'just', 'really', 'actually', 'basically', 'literally', 'pretty',
        'even', 'still', 'already', 'always', 'never', 'ever', 'yet', 'often',
        'much', 'many', 'lot', 'lots', 'things', 'thing', 'people', 'person',
        'way', 'time', 'times', 'year', 'years', 'day', 'days', 'something',
        'anything', 'everything', 'nothing', 'someone', 'anyone', 'everyone',
        'first', 'new', 'good', 'well', 'back', 'right', 'old',
        'one', 'two', 'three', 'four', 'five', 'six', 'seven',
        'eight', 'nine', 'ten', 'also', 'etc', 'ie', 'eg', 'vs', 'per', 're'
        }
        
        windows = sorted(vocab_evolution.keys())
        
        if time_windows is None:
            selected = [windows[0], windows[-1]]
        else:
            selected = time_windows
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        for idx, window in enumerate(selected):
            ax = axes[idx]
            
            fil= [(w, c) for w, c in vocab_evolution[window]['top_words'] if w.lower() not in exp ]
            if not fil:
                ax.text(0.5, 0.5, 'No meaningful words\nfound after filtering', 
                        ha='center', va='center', transform=ax.transAxes, 
                        fontsize=12, color='gray', style='italic')
                ax.set_title(f'Top Words: {window}', fontsize=12, fontweight='bold')
                ax.axis('off')
                continue
            
            words, counts = zip(*fil[:15])
            
            # Horizontal bar chart
            
            y_pos = np.arange(len(words))
            ax.barh(y_pos, counts, color=self.colors['primary'], alpha=0.7)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(words)
            ax.invert_yaxis()
            ax.set_xlabel('Frequency', fontsize=11, fontweight='bold')
            ax.set_title(f'Top Words: {window}', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        return self.to_base64(fig)
         
    def plt_cumul_drift(self, drift_df, title="Cumulative Sentiment Drift"):
        # Show cumulative sentiment change

        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = range(len(drift_df))
        labels = [str(tw) for tw in drift_df['time_window']]
        cumulative = drift_df['cumulative_change'].fillna(0)
        
        colors = [self.colors['positive'] if val >= 0 else self.colors['negative'] 
                  for val in cumulative]
        
        ax.fill_between(x, 0, cumulative, alpha=0.3, color=self.colors['primary'])
        ax.plot(x, cumulative, linewidth=2.5, color=self.colors['primary'])
        ax.bar(x, cumulative, color=colors, alpha=0.4, width=0.8)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        ax.set_xlabel('Time Window', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cumulative Change', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x[::max(1, len(x)//10)])
        ax.set_xticklabels(labels[::max(1, len(x)//10)], rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.to_base64(fig)
    
    def create_dashboard(self, df, drift_report):
        # Generating all visualization as dictionary
        
        charts = {}
        
        sentiment_drift_df = pd.DataFrame(drift_report['sentiment_drift'])
        activity_drift_df = pd.DataFrame(drift_report['activity_drift'])
        
        try:
            charts['sentiment_timeline'] = self.plt_senti_timeline(sentiment_drift_df)
        except Exception as e:
            print(f"The Sentiment timeline had some problems to clean up: {e}")
        
        try:
            charts['sentiment_distribution'] = self.plt_senti_dist(df)
        except Exception as e:
            print(f"Zeroed while creating the Sentiment distribution: {e}")
        
        try:
            charts['activity_timeline'] = self.plt_aty_timeline(activity_drift_df)
        except Exception as e:
            print(f"Got something to chew while creating Activity timeline: {e}")
        
        try:
            charts['word_comparison'] = self.plt_wrd_cloud_comp(
                drift_report['vocabulary_evolution']
            )
        except Exception as e:
            print(f"Something wrong while creating Word comparison: {e}")
        
        try:
            charts['cumulative_drift'] = self.plt_cumul_drift(sentiment_drift_df)
        except Exception as e:
            print(f"Gated out while creating Cumulative drift: {e}")
        
        return charts