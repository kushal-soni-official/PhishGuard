import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Assuming nltk data is downloaded
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except LookupError:
    print("Downloading required NLTK corpora...")
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

def preprocess_text(text: str) -> str:
    """
    Cleans, tokenizes, removes stopwords and lemmatizes the text.
    """
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers and extra whitespace
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize and lemmatize
    tokens = text.split()
    if lemmatizer:
        cleaned_tokens = [
            lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in stop_words and len(token) > 2
        ]
        return " ".join(cleaned_tokens)
    else:
        return " ".join([t for t in tokens if t not in stop_words])

def get_tfidf_features(corpus: list[str], max_features: int = 1000):
    """
    Trains a TF-IDF vectorizer on the corpus (used during training).
    Returns the vectorizer and the transformed matrix.
    """
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(corpus)
    return vectorizer, X
