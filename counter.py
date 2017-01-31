# eg from python cookbook - 1.12. Determining the Most Frequently Occurring Items in a Sequence
from collections import Counter

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]

word_counts = Counter(words)

print(word_counts)
print('Top 3 common words:', word_counts.most_common(3))
print("Number of 'eyes':", word_counts['eyes'])

print("Increasing number of counts of the words 'eyes' and 'the' ", end='')
word_counts['eyes'] += 1
word_counts['the'] += 2
print(word_counts.most_common(3))

print("Increasing number of counts of the words 'eyes' and 'the' using update method ", end='')
word_counts.update(['eyes', 'eyes', 'the'])
print(word_counts.most_common(3))

other_word_counts = Counter()
other_word_counts['eyes'] = 5
other_word_counts['the'] = 3

print(word_counts)
print(other_word_counts)
print('Subtracting two counters', word_counts - other_word_counts)
print('Adding two counters', word_counts + other_word_counts)
