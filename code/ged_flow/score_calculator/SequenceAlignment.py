def sequence_alignment(sequence1, sequence2):
    match = 0
    mismatch = 0
    gaps_opened = 0
    gaps_extended = 0
    is_last_char_gap = False

    for i in range(min(len(sequence1), len(sequence2))):
        if sequence1[i] == sequence2[i]:
            match += 1
            is_last_char_gap = False
        elif sequence1[i] == '-' or sequence2[i] == '-':
            if not is_last_char_gap:
                gaps_opened += 1
                is_last_char_gap = True
            else:
                gaps_extended += 1
        else:
            mismatch += 1
            is_last_char_gap = False

    return match, mismatch, gaps_opened, gaps_extended
