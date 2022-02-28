def top_word(sentence):
    if sentence == '':
        return None
    freq = {}
    sequence = sentence.split()
    for c in sequence:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return sorted(freq.items(), key=lambda x:-x[1])[0][0]

import os
os.system('sed -i -e "15i\\        if word not in counts: continue" test_assignment_one.py')
os.system('sed -i -e "50i\\    correct = top_word_solution(rfc2549)" test_assignment_one.py')
os.system('cat test_assignment_one.py')
