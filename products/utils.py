from rapidfuzz import process, fuzz
from .models import Product

def get_search_vocabulary():
    # Build a vocabulary from categories and common tags/words
    vocab = set()
    for p in Product.objects.all():
        if p.category:
            vocab.add(p.category.lower())
        if p.tags and isinstance(p.tags, list):
            for tag in p.tags:
                vocab.add(tag.lower())
        elif p.tags and isinstance(p.tags, str):
            for tag in p.tags.split(','):
                vocab.add(tag.strip().lower())
        
        # Add some name words
        if p.product_name:
            for word in p.product_name.lower().split():
                if len(word) > 3:
                    vocab.add(word)
    return list(vocab)

def correct_typo(query):
    vocab = get_search_vocabulary()
    if not vocab:
        return query
    
    # Use extractOne to find the best match
    match = process.extractOne(query.lower(), vocab, scorer=fuzz.WRatio)
    if match:
        best_match, score, _ = match
        # If score is sufficiently high (e.g., > 80), treat it as a typo correction
        if score > 80:
            return best_match
    return query
