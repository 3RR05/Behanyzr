from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sen

class Sentimentanalyzer:
    # Using Vader for intensifiers
    
    def __init__(self):
        self.analyzer = sen()
        
    def ext_sentiment_words(self, text):
        # Return Positive and Negative words
        
        positive_words = []
        negative_words = []

        if not text or not isinstance(text, str):
            return positive_words, negative_words

        for word in text.split():
            # Cleaning words
            
            clean_word = word.strip('.,!?;:"\'-').lower()
            if not clean_word:
                continue

            score = self.analyzer.polarity_scores(clean_word)['compound']

            if score >= 0.05:
                positive_words.append(clean_word)
            elif score <= -0.05:
                negative_words.append(clean_word)

        return positive_words, negative_words

    def analyze_sentiment(self, text):
        # Analyzing Sentiments
        
        if not text or not isinstance(text, str):
            return {
                'score': 0.0,
                'label': 'The words are robbed',
                'positive_words': [],
                'negative_words': []
            }
        
        scores = self.analyzer.polarity_scores(text)

        # Compound scores overall into clip between (-1 to 1)
        
        compound = scores['compound']

        if compound >= 0.05:
            label = 'Positive'
        elif compound <= -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'

        positive_words, negative_words= self.ext_sentiment_words(text)

        return {
            'score': round(compound, 2),
            'label': label,
            'positive_words': positive_words,
            'negative_words': negative_words
        }

    def analyze_df(self, df, text_column= 'text'):
        # Adding the data into a Dataframe and injects data into it
        
        df = df.copy()

        sentiments = df[text_column].apply(self.analyze_sentiment)

        df['sentiment_score'] = sentiments.apply(lambda x: x['score'])
        df['sentiment_label'] = sentiments.apply(lambda x: x['label'])
        df['positive_word_count'] = sentiments.apply(lambda x: len(x['positive_words']))
        df['negative_word_count'] = sentiments.apply(lambda x: len(x['negative_words']))

        return df