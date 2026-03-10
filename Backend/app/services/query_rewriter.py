from typing import List, Dict

def rewrite_query_with_history(query: str, chat_history: List[Dict[str, str]]) -> str:
    """
    Rewrite follow-up questions into standalone queries using chat history.
    
    Examples:
    - "what about economy?" -> "what are the baggage rules for economy class?"
    - "that for Air India?" -> "what are the baggage rules for Air India?"
    """
    if not chat_history:
        return query
    
    # Check if query is a follow-up (short, uses pronouns, lacks context)
    query_lower = query.lower().strip()
    
    follow_up_indicators = [
        'what about', 'how about', 'and for', 'that for', 'what for',
        'in that case', 'for that', 'about that', 'and that'
    ]
    
    is_follow_up = (
        len(query.split()) < 6 or
        any(indicator in query_lower for indicator in follow_up_indicators) or
        query_lower.startswith(('and ', 'but ', 'also ', 'what ', 'how '))
    )
    
    if not is_follow_up:
        return query
    
    # Build context from last 2 exchanges
    context_parts = []
    for msg in chat_history[-2:]:
        if msg.get('query'):
            context_parts.append(f"Previous question: {msg['query']}")
    
    if not context_parts:
        return query
    
    # Simple rewriting: combine context with current query
    context_str = " ".join(context_parts)
    
    # Extract key terms from context
    context_lower = context_str.lower()
    
    # If query mentions class/category, add context topic
    if any(word in query_lower for word in ['economy', 'business', 'first', 'premium']):
        if 'baggage' in context_lower or 'luggage' in context_lower:
            return f"baggage rules for {query}"
        elif 'flight' in context_lower:
            return f"flight information for {query}"
    
    # If query is very short, prepend last topic
    if len(query.split()) <= 3:
        # Extract main topic from last query
        last_query = chat_history[-1].get('query', '').lower()
        if 'baggage' in last_query:
            return f"baggage {query}"
        elif 'flight' in last_query:
            return f"flight {query}"
        elif 'refund' in last_query:
            return f"refund {query}"
    
    return query


def filter_relevant_chunks(chunks: List[Dict], query: str) -> List[Dict]:
    """
    Filter chunks to keep only those relevant to the query topic.
    """
    if not chunks:
        return []
    
    query_lower = query.lower()
    
    # Define topic keywords
    baggage_keywords = ['baggage', 'luggage', 'bag', 'carry-on', 'checked', 'cabin', 'weight', 'allowance']
    flight_keywords = ['flight', 'delay', 'schedule', 'departure', 'arrival', 'boarding']
    refund_keywords = ['refund', 'cancellation', 'ticket', 'booking', 'payment']
    travel_keywords = ['travel', 'destination', 'tour', 'visit', 'trip', 'hotel']
    
    # Determine query topic
    query_topics = []
    if any(kw in query_lower for kw in baggage_keywords):
        query_topics.append('baggage')
    if any(kw in query_lower for kw in flight_keywords):
        query_topics.append('flight')
    if any(kw in query_lower for kw in refund_keywords):
        query_topics.append('refund')
    if any(kw in query_lower for kw in travel_keywords):
        query_topics.append('travel')
    
    if not query_topics:
        return chunks  # Can't determine topic, return all
    
    # Filter chunks by topic relevance
    filtered = []
    for chunk in chunks:
        content_lower = chunk.get('content', '').lower()
        source_lower = chunk.get('metadata', {}).get('source', '').lower()
        
        # Check if chunk matches any query topic
        is_relevant = False
        
        if 'baggage' in query_topics:
            if any(kw in content_lower or kw in source_lower for kw in baggage_keywords):
                is_relevant = True
        
        if 'flight' in query_topics:
            if any(kw in content_lower or kw in source_lower for kw in flight_keywords):
                is_relevant = True
        
        if 'refund' in query_topics:
            if any(kw in content_lower or kw in source_lower for kw in refund_keywords):
                is_relevant = True
        
        if 'travel' in query_topics:
            if any(kw in content_lower or kw in source_lower for kw in travel_keywords):
                is_relevant = True
        
        if is_relevant:
            filtered.append(chunk)
    
    # If filtering removed everything, return top 2 original chunks
    if not filtered and chunks:
        return chunks[:2]
    
    return filtered
