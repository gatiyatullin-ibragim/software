def can_book(start, end, now, blocked, existing):
    if not (0 <= start < end <= 1440):
        return False
    if start <= now:
        return False
        
    if end - start > 120:
        return False
        
    if blocked:
        return False
        
    for b_start, b_end in existing:
        if max(start, b_start) < min(end, b_end):
            return False
            
    return True