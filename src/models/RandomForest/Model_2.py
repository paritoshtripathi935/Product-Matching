import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
import string


# Define the function for preprocessing text data
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = ''.join(word for word in text if not word.isdigit())
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize text
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Rejoin tokens into a string
    text = ' '.join(tokens)
    return text

class Model_1:
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.model_path = "rf_model.pkl"
    
    def loadData(self):
        # Load the data into a pandas DataFrame
        data = pd.read_csv(self.data_path)
        # Preprocess the text data
        data['name'] = data['name'].apply(preprocess_text)
        data['description'] = data['description'].apply(preprocess_text)
        # Drop rows with missing values
        data.dropna(inplace=True)
        # Convert the category labels to numerical values
        categories = data['category'].unique()
        cat_dict = {}
        for i, cat in enumerate(categories):
            cat_dict[cat] = i
        data['category'] = data['category'].map(cat_dict)
        # Split the data into training and testing sets
        self.train_data = data.sample(frac=0.8, random_state=1)
        self.test_data = data.drop(self.train_data.index)
    
    def trainModel(self):
        # Define the vectorizer
        vectorizer = TfidfVectorizer()
        # Fit the vectorizer to the training data
        X_train = vectorizer.fit_transform(self.train_data['name'] + ' ' + self.train_data['description'])
        y_train = self.train_data['category']
        # Train the random forest classifier
        self.rf_model = RandomForestClassifier(n_estimators=100)
        self.rf_model.fit(X_train, y_train)
    
    def testModel(self):
        # Transform the test data using the fitted vectorizer
        vectorizer = TfidfVectorizer()

        X_test = vectorizer.transform(self.test_data['name'] + ' ' + self.test_data['description'])
        y_test = self.test_data['category']
        # Make predictions on the test data
        y_pred = self.rf_model.predict(X_test)
        # Print the classification report
        print(classification_report(y_test, y_pred))
    
    def saveModel(self):
        # Save the trained model to disk
        import pickle
        with open(self.model_path, 'wb') as file:
            pickle.dump(self.rf_model, file)
    
    def loadModel(self):
        # Load the trained model from disk
        import pickle
        with open(self.model_path, 'rb') as file:
            self.rf_model = pickle.load(file)
        # Load the test data from disk
    
    def predict(self, name, description):
        vectorizer = TfidfVectorizer()

        # Load the test data from disk
        test_data = pd.read_csv('data/test_data.csv')
        # Preprocess the text data
        test_data['name'] = test_data['name'].apply(preprocess_text)
        test_data['description'] = test_data['description'].apply(preprocess_text)
        # Transform the test data using the fitted vectorizer
        X_test = vectorizer.transform(test_data['name'] + ' ' + test_data['description'])
        # Make predictions on the test data
        y_pred = self.rf_model.predict(X_test)
        # Print the classification report
        print(classification_report(test_data['category'], y_pred))

if __name__ == "__main__":
    model = Model_1("data/train_data.csv")
    model.loadData()
    model.trainModel()
    model.testModel()
    model.saveModel()
    model.predict("test", "test")
