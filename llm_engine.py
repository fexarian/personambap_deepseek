#!/usr/bin/env python3
"""
LLM Engine - OpenRouter integration for Mbap Bot
Uses urllib (no additional dependencies)
"""
import os
import json
import urllib.request
import urllib.parse
import re
from pathlib import Path

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Knowledge base path
KB_PATH = Path(__file__).parent / "dicky_knowledge.json"

# Persona system prompt
SYSTEM_PROMPT = """Anda adalah Mbap (Kang Dicky Zainal Arifin).
Jawab dengan gaya Mbap - langsung, tanpa \"saya/aku/gue\".
Tidak boleh ada pertanyaan di akhir jawaban.
Gunakan hanya informasi dari knowledge base."""


def load_knowledge():
    """Load knowledge base"""
    try:
        with open(KB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def search_knowledge(query, knowledge_base, top_k=3):
    """Search knowledge base using simple keyword matching"""
    query_words = set(re.findall(r'\w+', query.lower()))
    results = []
    
    for chunk in knowledge_base:
        text_lower = chunk.get('text', '').lower()
        chunk_words = set(re.findall(r'\w+', text_lower))
        overlap = query_words & chunk_words
        score = len(overlap)
        
        if query.lower() in text_lower:
            score += 10
        
        if score > 0:
            results.append((score, chunk))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:top_k] if r[0] > 0]


def call_llm(query, model="nvidia/nemotron-3-super-120b-a12b:free"):
    """Call LLM with knowledge context"""
    if not OPENROUTER_API_KEY:
        return "OPENROUTER_API_KEY tidak diset"
    
    # Load knowledge
    kb = load_knowledge()
    
    # Search relevant chunks
    chunks = search_knowledge(query, kb)
    
    if not chunks:
        return "Mbap belum menelusuri lebih lanjut..."
    
    # Format context
    context = "\n".join([c.get('text', '')[:300] for c in chunks])
    
    # Build messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nPertanyaan: {query}\n\nJawab:"}
    ]
    
    # Prepare request
    data = json.dumps({
        "model": model,
        "messages": messages
    }).encode('utf-8')
    
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mbapbot.local"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content']
            else:
                return "Error: " + str(result.get('error', 'Unknown'))
    
    except Exception as e:
        return f"Error: {str(e)}"


def answer_question(query):
    """Answer question using LLM"""
    return call_llm(query)


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "keraton Boko di mana?"
    answer = answer_question(query)
    print(f"Q: {query}")
    print(f"A: {answer}")