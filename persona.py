#!/usr/bin/env python3
"""
Persona Module - Mbap style enforcement
Ensures responses follow Mbap's speaking style
"""


def apply_mbap_style(text):
    """
    Apply Mbap persona style to response
    
    Rules:
    - Remove "saya", "aku", "gue"
    - No questions at the end
    - Direct, firm tone
    - No extra emojis
    
    Args:
        text: Raw response text
        
    Returns:
        Styled response
    """
    if not text:
        return "Mbap belum menelusuri lebih lanjut..."
    
    # Words to remove
    forbidden = ['saya', 'aku', 'gue', ' Saya', ' Aku', ' Gue']
    
    for word in forbidden:
        text = text.replace(word, '')
    
    # Remove questions at end
    text = text.strip()
    if text.endswith('?'):
        text = text[:-1].strip()
    
    # Remove question marks in last sentence
    sentences = text.split('.')
    if sentences:
        last = sentences[-1].strip()
        if '?' in last:
            last = last.replace('?', '').strip()
            sentences[-1] = last
            text = '.'.join(sentences)
    
    # Limit length
    max_length = 500
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text.strip()


def is_valid_mbap(text):
    """
    Check if text follows Mbap style
    
    Returns:
        True if valid, False otherwise
    """
    if not text:
        return False
    
    # Check forbidden words
    forbidden = ['saya', 'aku', 'gue']
    for word in forbidden:
        if word in text.lower():
            return False
    
    return True


if __name__ == "__main__":
    # Test
    test_texts = [
        "Saya觉得 itu benar.",
        "Aku akan menjawab.",
        "Mbap belum menelusuri lebih lanjut...",
        "Pertanyaan yang bagus! Ada yang ingin ditanyakan?"
    ]
    
    for t in test_texts:
        print(f"Input: {t}")
        print(f"Output: {apply_mbap_style(t)}")
        print()