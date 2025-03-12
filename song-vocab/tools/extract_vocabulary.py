import re
from typing import List

def extract_vocabulary(text: str) -> List[str]:
    """Extract unique words from text."""
    # Clean the text and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove duplicates and sort
    unique_words = sorted(set(words))
    return unique_words