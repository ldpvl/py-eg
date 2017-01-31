# eg from python cookbook - keeping the last N items
from collections import deque

def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        print("Before appending:", previous_lines)
        previous_lines.append(line)
        print("After appending:", previous_lines)
    print("EXIT SEARCH")

if __name__ == '__main__':
    with open('resources/collections-deque.txt', mode='r') as file:
        for line, previous_lines in search(file, 'KEYWORD', 5):
            for plines in previous_lines:
                print(plines, end='')
            print(line, end='')
            print('-' * 20)
