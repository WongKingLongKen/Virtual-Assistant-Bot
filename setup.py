import nltk
import ssl
import os

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Create data directory if it doesn't exist
nltk_data_dir = os.path.expanduser('~/nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    print("Successfully downloaded NLTK data")
except Exception as e:
    print(f"Error downloading NLTK data: {str(e)}")