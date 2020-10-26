import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
class Main:
    def __init__(self):
        train = pd.read_csv('corona_fake.csv')
        train = train.fillna(' ')
        train['total'] = train['title'] + ' ' + train['text']
        train = train[['total', 'label']]
        stop_words = stopwords.words('english')
        lemmatizer = WordNetLemmatizer()
        for index, row in train.iterrows():
            filter_sentence = ''
            sentence = row['total']

            sentence = re.sub(r'[^\w\s]', '', sentence)

            words = nltk.word_tokenize(sentence)

            words = [w for w in words if not w in stop_words]

            for words in words:
                filter_sentence = filter_sentence  + ' ' +str(lemmatizer.lemmatize(words)).lower()
            train.loc[index, 'total'] = filter_sentence

        train = train[['total', 'label']]
        X_train = train['total']
        Y_train = train['label']
        count_vectorizer = CountVectorizer()
        count_vectorizer.fit_transform(X_train)
        freq_term_matrix = count_vectorizer.transform(X_train)
        tfidf = TfidfTransformer(norm = "l2")
        tfidf.fit(freq_term_matrix)
        tf_idf_matrix = tfidf.fit_transform(freq_term_matrix)
        X_train, X_test, y_train, y_test = train_test_split(tf_idf_matrix,Y_train, random_state=0)
        Lr = LogisticRegression(C=10.0,random_state=0)
        Lr.fit(X_train, y_train)

        print("Accuracy : " + str(round(Lr.score(X_test,y_test),3)*100) + "%")
if __name__ == '__main__':
    Main()

