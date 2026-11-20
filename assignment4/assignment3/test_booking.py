from booking import can_book

def test_all_cases():
    now = 540
    existing = [(600, 660)]

    # Touching: 660-720 -> Available
    assert can_book(660, 720, now, False, existing) == True
    
    # Overlap: 630-690 -> Unavailable
    assert can_book(630, 690, now, False, existing) == False
    
    # Blocked: 660-720, blocked=True -> Unavailable
    assert can_book(660, 720, now, True, existing) == False
    
    # Exactly 120 min: 720-840 -> Available
    assert can_book(720, 840, now, False, existing) == True
    
    # 121 min: 720-841 -> Unavailable
    assert can_book(720, 841, now, False, existing) == False
    
    # Starts now: 540-570 -> Unavailable
    assert can_book(540, 570, now, False, existing) == False

    print("All tests passed successfully!")

if __name__ == "__main__":
    test_all_cases()