import logging
import re
from typing import Tuple

logger = logging.getLogger(__name__)

# Common words by language (English focus, extensible)
COMMON_WORDS_EN = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "be", "been", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "can", "in",
    "on", "at", "to", "for", "of", "with", "by", "from", "about",
    "as", "into", "through", "during", "before", "after", "above",
    "below", "up", "down", "out", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "same",
    "so", "than", "too", "very", "just", "that", "this", "these",
    "those", "i", "you", "he", "she", "it", "we", "they", "what",
    "which", "who", "whom", "if", "if", "because", "while", "your",
    "his", "her", "its", "our", "their", "my", "me", "him", "us"
}

COMMON_WORDS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o",
    "pero", "es", "son", "fue", "fueron", "ser", "ha", "han", "hacer",
    "hace", "en", "de", "del", "al", "a", "para", "por", "con", "sin",
    "sobre", "entre", "antes", "despues", "durante", "desde", "hasta", "que",
    "como", "cuando", "donde", "porque", "si", "no", "mas", "menos", "muy",
    "ya", "tambien", "solo", "este", "esta", "estos", "estas", "ese", "esa",
    "esos", "esas", "aqui", "alli", "yo", "tu", "usted", "el", "ella", "nosotros",
    "ustedes", "ellos", "ellas", "mi", "mis", "tu", "tus", "su", "sus", "nuestro",
    "nuestra", "sus", "se", "me", "te", "le", "les", "lo", "la", "uno", "cada"
}


def get_common_words_for_lang(lang: str) -> set:
    normalized = (lang or "en").strip().lower()
    # Accept values like "es", "en", or "es,en"
    if "," in normalized:
        parts = [p.strip() for p in normalized.split(",") if p.strip()]
    else:
        parts = [normalized]

    common_words = set()
    for item in parts:
        if item.startswith("es"):
            common_words.update(COMMON_WORDS_ES)
        if item.startswith("en"):
            common_words.update(COMMON_WORDS_EN)

    if not common_words:
        common_words = COMMON_WORDS_EN

    return common_words

def validate_extracted_text(
    text: str,
    min_chars: int = 50,
    min_valid_words: int = 5,
    min_word_ratio: float = 0.3,
    lang: str = "en",
) -> Tuple[bool, float, str]:
    """
    Validate if extracted text is real (not garbage/noise).
    
    Returns:
        Tuple[is_valid, confidence, reason]
    
    Heuristics:
    - Minimum character count
    - Minimum valid words (common English words)
    - Word ratio: valid_words / total_words
    """
    text_clean = text.strip()
    
    if not text_clean:
        return False, 0.0, "Empty text"
    
    if len(text_clean) < min_chars:
        return False, float(len(text_clean)) / min_chars, f"Too few chars ({len(text_clean)} < {min_chars})"
    
    # Extract words including Spanish accented characters.
    words = re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', text_clean.lower())
    
    if not words:
        return False, 0.0, "No valid words found"
    
    # Count common words according to configured language(s).
    common_words = get_common_words_for_lang(lang)
    valid_words = sum(1 for word in words if word in common_words)
    word_ratio = valid_words / len(words) if words else 0.0
    
    if valid_words < min_valid_words:
        return False, word_ratio, f"Too few common words ({valid_words} < {min_valid_words})"
    
    if word_ratio < min_word_ratio:
        return False, word_ratio, f"Low word ratio ({word_ratio:.2%} < {min_word_ratio:.2%})"
    
    reason = f"Valid: {len(text_clean)} chars, {valid_words}/{len(words)} words ({word_ratio:.2%})"
    return True, word_ratio, reason


def is_pdf_likely_scanned(
    extracted_text: str,
    pages_count: int = 1,
    threshold: float = 0.05
) -> Tuple[bool, float]:
    """
    Detect if PDF is likely scanned (no embedded text).
    
    Returns:
        Tuple[is_scanned, confidence]
    
    Logic:
    - If extracted text is very poor relative to page count, likely scanned.
    - e.g., 1-2 pages with < 50 chars each = probably scanned
    """
    if not extracted_text.strip():
        return True, 1.0
    
    avg_chars_per_page = len(extracted_text.strip()) / max(pages_count, 1)
    
    # Scanned PDFs often have minimal/no text
    if avg_chars_per_page < 30:
        confidence = min(1.0, 1.0 - (avg_chars_per_page / 30))
        return True, confidence
    
    return False, 0.0
