from app.db import documents_col

def est_jaccard(submission_id1, submission_id2):
    """Estimate Jaccard similarity from two MinHash signatures"""
    
    doc1 = documents_col.find_one({"submission_id": submission_id1})
    doc2 = documents_col.find_one({"submission_id": submission_id2})
    
    if doc1 is None or doc2 is None:
        raise ValueError("One or both submission IDs not found in database.")
    
    sig1 = doc1.get("minhash_signature")
    sig2 = doc2.get("minhash_signature")
    
    if sig1 is None or sig2 is None:
        raise ValueError("MinHash signature missing for one or both submissions.")
    
    matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
    return matches / len(sig1)
