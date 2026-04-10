#!/usr/bin/env python3
"""
RAG Engine - Simple keyword-based search
Lightweight - no heavy ML dependencies
"""
import json
import re
from pathlib import Path

# Knowledge base path
KB_PATH = Path(__file__).parent / "kb.json"


def load_kb():
    """Load knowledge base from JSON file"""
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_kb(query, top_k=3):
    """
    Search knowledge base using keyword matching
    
    Args:
        query: User question
        top_k: Number of results to return
        
    Returns:
        List of relevant text chunks
    """
    # Load KB
    kb = load_kb()
    
    # Extract keywords from query
    query_words = set(re.findall(r'\w+', query.lower()))
    
    # Score each chunk
    results = []
    for chunk in kb:
        text = chunk.get('text', '')
        text_lower = text.lower()
        chunk_words = set(re.findall(r'\w+', text_lower))
        
        # Calculate overlap score
        overlap = query_words & chunk_words
        score = len(overlap)
        
        # Bonus for exact phrase match
        if query.lower() in text_lower:
            score += 10
        
        if score > 0:
            results.append((score, text))
    
    # Sort by score and return top_k
    results.sort(key=lambda x: x[0], reverse=True)
    
    return [r[1] for r in results[:top_k] if r[0] > 0]


def get_context(query, max_length=500):
    """
    Get context for a query
    
    Args:
        query: User question
        max_length: Max length of combined context
        
    Returns:
        Combined context string
    """
    results = search_kb(query, top_k=3)
    
    if not results:
        return ""
    
    # Combine results up to max_length
    context = ""
    for result in results:
        if len(context) + len(result) > max_length:
            break
        context += result + "\n\n"
    
    return context.strip()


if __name__ == "__main__":
    # Test
    test_q = "keraton Boko"
    results = search_kb(test_q)
    print(f"Query: {test_q}")
    print(f"Results: {len(results)}")
    if results:
        print(f"First result: {results[0][:100]}...")