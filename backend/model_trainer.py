import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Provide a very small, toy dataset just to make the prototype work out-of-the-box.
# In a real-world scenario, you would load thousands of records from a CSV/DB here.
DUMMY_DATA = [
    # REAL NEWS (Label 1)
    ("The stock market experienced a significant drop today due to rising inflation concerns.", 1),
    ("NASA successfully launched its new rover to Mars this morning.", 1),
    ("The local government announced a new initiative to plant a million trees by 2030.", 1),
    ("Scientists have discovered a new species of deep-sea jellyfish in the Pacific Ocean.", 1),
    ("A major tech company released its quarterly earnings report, showing a 15% increase in revenue.", 1),
    ("The President signed a new healthcare bill into law after months of debate.", 1),
    
    # FAKE NEWS (Label 0)
    ("Aliens have officially landed in New York City and are demanding to speak to the UN.", 0),
    ("Drinking hot water with lemon will instantly cure all known diseases, secret doctors reveal.", 0),
    ("The earth is actually flat and scientists have been hiding the edge from us for centuries.", 0),
    ("If you share this post with 10 people, you will magically receive $10,000 in your bank account tomorrow.", 0),
    ("Celebrity spotted eating rocks for breakfast, claims it's the ultimate secret to eternal youth.", 0),
    ("Breaking: The moon is made entirely of cheese, new leaked footage from space proves.", 0),
]

def train_and_save_model():
    print("Preparing dummy dataset...")
    texts = [item[0] for item in DUMMY_DATA]
    labels = [item[1] for item in DUMMY_DATA]

    print("Training TF-IDF Logistic Regression model...")
    # Create a pipeline that vectorizes the text and then trains a classifier
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
        ('classifier', LogisticRegression())
    ])

    # Train the model
    pipeline.fit(texts, labels)

    # Ensure the models directory exists (we'll just save it in the backend folder for simplicity)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "fake_news_model.pkl")

    print(f"Saving model to {model_path}...")
    joblib.dump(pipeline, model_path)
    print("Training complete! Model is ready for inference.")

if __name__ == "__main__":
    train_and_save_model()
