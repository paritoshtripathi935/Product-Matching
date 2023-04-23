import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer
import joblib

import re
import string

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(' +', ' ', text)
    text = text.strip()
    
    return text

class Model:
    def __init__(self):
        self.amazonDb = 'data/Amazon/amazon.db'
        self.flipkartDb = 'data/Flipkart/flipkart.db'
        self.modelStorage = 'data/models/RandomForest/savedModels'
        pass

    def loadDataAmz(self):
        # create a connection to the SQLite database
        conn = sqlite3.connect(self.amazonDb)

        # read data from a table into a Pandas DataFrame
        df = pd.read_sql('SELECT * FROM products', conn)

        # close the database connection
        conn.close()

        # print the number of prroducts in the DataFrame
        #print('Number of products: ', len(df))

        return df

    def loadDataFlip(self):
        # create a connection to the SQLite database
        conn = sqlite3.connect(self.flipkartDb)

        # read data from a table into a Pandas DataFrame
        df = pd.read_sql('SELECT * FROM products', conn)

        # close the database connection
        conn.close()

        # print the number of prroducts in the DataFrame
        #print('Number of products: ', len(df))

        return df
    
    def processData(self, df):
        
        df['price'] = df['price'].str.replace(',', '')

        # Replace "None" values in the "price" column with NaN
        df["price"].replace("None", float("nan"), inplace=True)

        # Convert the "price" column to float
        df["price"] = df["price"].astype(float)

        # Drop rows with missing values
        df.dropna(inplace=True)

        # Convert price column to float
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Convert categorical variables to numerical values
        df['category'] = df['category'].astype('category').cat.codes

        # Reset the index
        df.reset_index(drop=True, inplace=True)

        print(f"Processing Data: Done")


        # Process the description column
        vectorizer = CountVectorizer(stop_words='english', max_features=500)
        desc_matrix = vectorizer.fit_transform(df['description'])
        desc_df = pd.DataFrame(desc_matrix.toarray(), columns=vectorizer.get_feature_names_out())
        name_matrix = vectorizer.fit_transform(df['name'])
        name_df = pd.DataFrame(name_matrix.toarray(), columns=vectorizer.get_feature_names_out())
        
        df = pd.concat([df, name_df], axis=1)
        df = pd.concat([df, desc_df], axis=1)

        # Split the data into training and testing sets
        X = df.drop(['id', 'sku', 'image_path', 'timestamp', 'URL', 'name', 'description'], axis=1)
        y = df['category']

        return X, y

    def trainModel(self, X, y):
        # Process the description column
        print(f"Model 1: Random Forest Classifier Training")
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a random forest model
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)

        # Evaluate the model
        y_pred = rf.predict(X_test)
        #print(classification_report(y_test, y_pred))


        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        

        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")

        return rf
    
    def main(self):
        # Load the data
        df_amz = self.loadDataAmz()
        df_fk = self.loadDataFlip()

        # combine both dataframes
        df = pd.concat([df_amz, df_fk])

        # Process the data
        X, y = self.processData(df)

        # Train the model
        model = self.trainModel(X, y)
        joblib.dump(model, f"{self.modelStorage}/randomForest_1.pkl")

if __name__ == '__main__':
    model = Model()
    model.main()