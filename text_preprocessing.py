import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Define stop words to remove
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text) 
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove special characters, and punctuation
    text = re.sub(r'[^A-Za-z0-9%\s\.\$€£]', '', text) 
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_text(text):
    # Tokenize the cleaned text
    return word_tokenize(text,language='english', preserve_line=True)

def remove_stop_words(tokens):
    # Remove stop words from the tokenized text
    return [word for word in tokens if word.lower() not in stop_words]

def preprocess_text(text):
    # Combine all steps into a preprocessing pipeline
    cleaned_text = clean_text(text)
    tokens = tokenize_text(cleaned_text)
    filtered_tokens = remove_stop_words(tokens)
    return filtered_tokens


