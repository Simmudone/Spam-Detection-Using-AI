#app/data_cleaner.py
import pandas as pd
import re
import string
import nltk
#from sklearn.preprocessing import LabelEncoder

# Download stopwords (only first time)
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load the dataset
df = pd.read_csv('data/dataset.csv')
df = df.drop_duplicates()

# Rename columns if needed
df.columns = ['label', 'text']

# Check for missing values
print("\nMissing values:\n", df.isnull().sum())

# Encode labels: 'spam' → 1, 'ham' → 0
'''le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])'''
df['label'] = df['label'].map({'ham': 'not_spam', 'spam': 'spam'})

# Clean text function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # remove URLs
    text = re.sub(r'\S+@\S+', '', text)                # remove emails
    text = re.sub(r'<.*?>+', '', text)                 # remove HTML tags
    text = re.sub(r'\[.*?\]', '', text)                # remove [stuff]
    text = re.sub(r'[^\w\s]', '', text)                # remove punctuation
    text = re.sub(r'\n', ' ', text)                    # remove newlines
    text = re.sub(r'\w*\d\w*', '', text)               # remove words with numbers
    text = re.sub(r'(.)\1{2,}', r'\1', text)           # reduce repeated characters
    text = text.encode('ascii', 'ignore').decode()     # remove emojis / non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()           # remove extra spaces

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text


# Apply cleaning
df['clean_text'] = df['text'].astype(str).apply(clean_text)

# Show sample
print("\nCleaned sample:")
print(df[['label', 'clean_text']].head())

# Save to new CSV
df.to_csv('data/cleaned_dataset.csv', index=False)
print("\nSaved cleaned data to 'cleaned_dataset.csv'")