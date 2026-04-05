import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from backend.models.feature_extractor import extract_features
from backend.utils.nlp_processor import get_tfidf_features

DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset', 'phishing_data.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')

def train():
    print("Loading dataset...")
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        print("Please run the download_data.py script first.")
        return
        
    df = pd.read_csv(DATASET_PATH)
    
    # Expected columns: raw_email, label (1 = phishing, 0 = safe)
    if 'raw_email' not in df.columns or 'label' not in df.columns:
        print("Dataset must contain 'raw_email' and 'label' columns.")
        return
        
    print(f"Dataset loaded. Total samples: {len(df)}")
    
    # 1. Extract raw features for each email
    print("Extracting features from emails... (This may take a while)")
    extracted_features = []
    for idx, row in df.iterrows():
        feat = extract_features(row['raw_email'])
        feat['label'] = row['label']
        extracted_features.append(feat)
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1} / {len(df)} emails")
            
    feat_df = pd.DataFrame(extracted_features)
    
    # 2. Process Text with TF-IDF
    print("Training TF-IDF vectorizer...")
    corpus = feat_df['clean_text'].tolist()
    vectorizer, text_features = get_tfidf_features(corpus, max_features=1000)
    
    # 3. Combine numeric features with text features
    numeric_cols = [
        'num_urls', 'num_suspicious_urls', 'num_ip_urls', 'num_shortened_urls',
        'auth_missing', 'auth_score', 'num_attachments', 'num_suspicious_attachments'
    ]
    numeric_features = feat_df[numeric_cols].values
    
    X = np.hstack((numeric_features, text_features.toarray()))
    y = feat_df['label'].values
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Random Forest
    print("Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=1)
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    
    # 6. Save Models
    os.makedirs(MODEL_DIR, exist_ok=True)
    rf_path = os.path.join(MODEL_DIR, 'rf_model.pkl')
    tfidf_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    
    joblib.dump(clf, rf_path)
    joblib.dump(vectorizer, tfidf_path)
    
    print(f"Model saved to {rf_path}")
    print(f"Vectorizer saved to {tfidf_path}")

if __name__ == "__main__":
    train()
