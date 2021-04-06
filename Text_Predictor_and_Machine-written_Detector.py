from utilities import *

def parse_story(file_name):
    '''
    This function returns ordered list of words with bad removed from the text in the file given by file_name
    str -> list
    Ex.
    >>f = 'test_text_parsing.txt'
    >>print(parse_story(f))
    output: ['the', 'code', 'should', 'handle', 'correctly', 'the', 'following', ':', 'white', 'space', '.', 'sequences', 'of', 'punctuation', 'marks', '?', '!', '!', 'periods', 'with', 'or', 'without', 'spaces', ':', 'a', '.', '.', 'a', '.', 'a', "don't", 'worry', 'about', 'numbers', 'like', '1', '.', '5', 'remove', 'capitalization']
    '''

    with open(file_name) as fil:
        p = [line.strip('\n') for line in fil]

    BAD_CHARS = ['"', "(", ")", "{", "}", "[", "]", "_"]
    VALID_PUNCTUATION = ['?', '.', '!', ',', ':', ';']

    result = []
    for i in p:
        if i != '':
            result.append(i.lower())

    st = ' '.join(result)

    for i in VALID_PUNCTUATION:
        st = st.replace(i, ' ' + i + ' ')

    for i in BAD_CHARS:
        st = st.replace(i, ' ')

    st = st.split()

    return st


# f = 'test_text_parsing.txt'
# print(parse_story(f))



def get_prob_from_count(counts):
    '''
    This function returns a list of probabilities derived from counts
    list -> list
    Ex.
    >>get_prob_from_count([10, 20, 40, 30])
    output: [0.1, 0.2, 0.4, 0.3]
    '''
    probabilities = [0 for i in range(len(counts))]
    for i in range(len(counts)):
        probabilities[i] = counts[i] / sum(counts)
    return probabilities

# print(get_prob_from_count([10, 20, 40, 30]))



def build_ngram_counts(words, n):
    '''
    This function takes in the parsed story list and returns a dictionary of N-grams and counts the words that follow the N gram
    key of dict is the tuple containing the n-gram, value is a list containing two lists: first is words, second is correspondng counts
    (list, int) -> dict
    Ex.
    >>words = ['the', 'child', 'will', 'go', 'out', 'to', 'play']
    >>print(build_ngram_counts(words, 2))
    output: {('the', 'child'): [['will'], [1]], ('child', 'will'): [['go'], [1]], ('will', 'go'): [['out'], [1]], ('go', 'out'): [['to'], [1]], ('out', 'to'): [['play'], [1]]}
    '''
    d1 = dict()
    for i in range(n, len(words)):
        key = tuple(words[i - n:i])
        if key not in d1:
            d1[key] = [[words[i]], [1]]
        else:
            if words[i] not in d1[key][0]:
                d1[key][0].append(words[i])
                d1[key][1].append(1)
            else:
                d1[key][1][d1[key][0].index(words[i])] = d1[key][1][d1[key][0].index(words[i])] + 1
    return d1

# words = ['the', 'child', 'will', 'go', 'out', 'to', 'play']
# print(build_ngram_counts(words, 2))
# words1 = ['the', 'child', 'will', 'go', 'out', 'to', 'play', ',', 'and', 'the', 'child', 'can', 'not', 'be', 'sad', 'anymore', '.']
# words2 = ['hi', 'hi', 'hi', 'hi', 'hi']
# words3 = ['hello','there','is','there','is','hello','is','hello']
# print(build_ngram_counts(words1, 2))
# print(build_ngram_counts(words2, 2))
# print(build_ngram_counts(words3, 2))
# print(build_ngram_counts(words3, 1))


def prune_ngram_counts(counts, prune_len):
    '''
    This function prunes the words that occurs less frequently in an n-gram dictionary
    (dict, int) --> dict
    Ex.
    >>ngram_counts = {('i', 'love'): [['js', 'py3', 'c', 'no'], [20, 2, 3, 5]],
      ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [5, 7, 5, 5]],
      ('toronto', 'is'): [['six', 'drake', 'dope', 'hi', 'T', 'full'], [2, 3, 10, 5, 4, 4]]}
    >>print(prune_ngram_counts(ngram_counts, 3))
    output: {('i', 'love'): [['js', 'no', 'c'], [20, 5, 3]], ('u', 'r'): [['nice', 'cool', 'lit'], [7, 5, 5]], ('toronto', 'is'): [['dope', 'hi', 'T', 'full'], [10, 5, 4, 4]]}
    '''
    for i in counts.keys():
        if len(counts[i][1]) <= prune_len:
            continue
        else:
            a = sorted(counts[i][1])
            b = a[prune_len:].count(a[prune_len - 1])
            c = b + prune_len
            p = sorted(list(zip(counts[i][0], counts[i][1])), key=lambda x: x[1], reverse=True)
            l = []
            for j in zip(*p):
                l.append(list(j))
            counts[i] = [l[0][:c], l[1][:c]]
    return counts


def probify_ngram_counts(counts):
    '''
    This function inputs a n-gram dictionary, converts it to probabilites
    (dict) --> dict
    Ex.
    >>counts = {('i', 'love'): [['js', 'py3', 'c'], [20, 20, 10]],
    ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]],
    ('toronto', 'is'): [['six', 'drake'], [2, 3]]}
    >>print(probify_ngram_counts(counts))
    output: {('i', 'love'): [['js', 'py3', 'c'], [0.4, 0.4, 0.2]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [0.32, 0.28, 0.2, 0.2]], ('toronto', 'is'): [['six', 'drake'], [0.4, 0.6]]}
    '''
    d = {}
    for i, j in counts.items():
        l = [j[0], get_prob_from_count(j[1])]
        d.update({i: l})
    return d

'''
counts = {('i', 'love'): [['js', 'py3', 'c'], [20, 20, 10]],
('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]],
('toronto', 'is'): [['six', 'drake'], [2, 3]]}
print(probify_ngram_counts(counts))
'''



def build_ngram_model(words, n):
    '''
    This function creates and returns dict that keeps 15 most likely words that follow a N-gram, with corresponding next words in descending order of probability
    (list, int) --> dict
    Ex.
    >>words = ['the', 'child', 'will', 'the', 'child', 'can', 'the', 'child', 'can', 'the', 'child', 'may', 'go', 'home', '.']
    >>print(build_ngram_model(words, 3))
    output: {('the', 'child', 'will'): [['the'], [1.0]], ('child', 'will', 'the'): [['child'], [1.0]], ('will', 'the', 'child'): [['can'], [1.0]], ('the', 'child', 'can'): [['the'], [1.0]], ('child', 'can', 'the'): [['child'], [1.0]], ('can', 'the', 'child'): [['can', 'may'], [0.5, 0.5]], ('the', 'child', 'may'): [['go'], [1.0]], ('child', 'may', 'go'): [['home'], [1.0]], ('may', 'go', 'home'): [['.'], [1.0]]}
    '''
    a = build_ngram_counts(words, n)
    b = prune_ngram_counts(a, 15)
    c = probify_ngram_counts(b)
    return c


# words = ['the', 'child', 'will', 'the', 'child', 'can', 'the', 'child', 'can', 'the', 'child', 'may', 'go', 'home', '.']
# print(build_ngram_model(words, 3))


def gen_bot_list(ngram_model, seed, num_tokens = 0):
    '''
    This function returns a randomly generated list of tokens starting with 'seed', selecting following word using gen_next_token
    list ends when list contains num_tokens tokens
    gen_next_token is violated
    (dict, tuple, int) -> list
    Ex.
    >>ngram_model = {('the', 'child'): [['will', 'can','may'], [0.5, 0.25, 0.25]],
    ('child', 'will'): [['the'], [1.0]],
    ('will', 'the'): [['child'], [1.0]],
    ('child', 'can'): [['the'], [1.0]],
    ('can', 'the'): [['child'], [1.0]],
    ('child', 'may'): [['go'], [1.0]],
    ('may', 'go'): [['home'], [1.0]],
    ('go', 'home'): [['.'], [1.0]]}
    >>random.seed(10)
    >>print(gen_bot_list(ngram_model, ('hello', 'world'))) # []
    >>print(gen_bot_list(ngram_model, ('hello', 'world'), 5)) # ['hello', 'world']
    >>print(gen_bot_list(ngram_model, ('the', 'child'), 5)) # ['the', 'child', 'will', 'the', 'child']
    >>print(gen_bot_list(ngram_model, ('child', 'will'), 10))
    output: []
            ['hello', 'world']
            ['the', 'child', 'can', 'the', 'child']
            ['child', 'will', 'the', 'child', 'may', 'go', 'home', '.']
    '''
    a = list(seed)

    if len(seed) >= num_tokens:
        return a[: num_tokens]
    if seed not in ngram_model:
        return a

    while True:
        if len(a) >= num_tokens or seed not in ngram_model or ngram_model[seed][0] == []:
            return a
        else:
            ha = gen_next_token(seed, ngram_model)
            a.append(ha)
            seedl = list(seed)
            l1 = seedl[1:]
            l1.append(ha)
            seed = tuple(l1)


def gen_bot_text(token_list, bad_author):
    '''
    If bad_author is True, this function returns the string containing all tokens in token_list, separated by a space;
    otherwise, returns the string following grammar rules
    (list, boolean) -> str
    Ex.
    >>token_list = ['this', 'is', 'a', 'string', 'of', 'i', '.', 'which', 'needs', 'to', 'be', 'created', '.']
    >>print(gen_bot_text(token_list, False))
    output:This is a string of I. Which needs to be created.
    '''

    if bad_author:
        return ' '.join(token_list)
    else:
        new_token_list = []
        if token_list[0] in VALID_PUNCTUATION:
            new_token_list.append(token_list[0])
        else:
            new_token_list.append(token_list[0].capitalize())

        for m in range(1, len(token_list)):
            word = token_list[m]
            previous_word = token_list[m - 1]

            if word in VALID_PUNCTUATION:
                new_token_list.append(word)

            elif previous_word in END_OF_SENTENCE_PUNCTUATION or word.capitalize() in ALWAYS_CAPITALIZE:
                new_token_list.append(' ' + word.capitalize())

            else:
                new_token_list.append(' ' + word)

        return ''.join(new_token_list)

# token_list = ['this', 'is', 'a', 'string', 'of', 'i', '.', 'which', 'needs', 'to', 'be', 'created', '.']
# print(gen_bot_text(token_list, False))




def write_story(file_name, text, title, student_name, author, year):
    '''
    writes the text to file
    file_name: name of the output file
    text: string of the input text
    title: string of the title of text
    student_name: my name
    author: author of the original text
    year: year published
    (str, str, str, str, str, int) -> file (.txt)
    Ex.
    text = ' '.join(parse_story('308.txt'))
    write_story('test_write_story_student.txt', text, 'Three Men in a Boat', 'Jerome K. Jerome', 'Jerome K. Jerome', 1889)
    token_list = parse_story('308.txt')
    text = gen_bot_text(token_list, False)
    write_story('test_gen_bot_text_student.txt', text, 'Three Men in a Boat', 'Jerome K. Jerome', 'Jerome K. Jerome', 1889)
    '''
    file1 = open(file_name, 'w+')
    for i in range(10):
        file1.write('\n')

    a = title + ': ' + str(year) + ', ' + 'UNLEASHED'
    file1.write(a)
    file1.write('\n')

    b = student_name + ', inspired by ' + author
    file1.write(b)
    file1.write('\n')

    c = 'Copyright year published ' + '(' + str(year) + '), publisher: EngSci press'
    file1.write(c)
    file1.write('\n')

    for i in range(17):
        file1.write('\n')
    file1.write('CHAPTER 1\n\n')

    text1 = text.split()
    content = []
    character = 0
    line = []
    pl = 2
    pagenumber = 1
    chapternumber = 2

    for i in range(len(text1)):
        word = text1[i]
        character += len(word) + 1
        if character - 1 > 90:
            content.append(' '.join(line) + '\n')
            character = len(word) + 1
            line = []
            pl = pl + 1

            if pl == 28:
                pl = 0
                content.append('\n' + str(pagenumber) + '\n')
                pagenumber = pagenumber + 1

                if pagenumber != 1 and pagenumber % 12 == 1:
                    content.append('CHAPTER ' + str(chapternumber) + '\n\n')
                    chapternumber = chapternumber + 1
                    pl = pl + 2

        line.append(word)

    content.append(' '.join(line) + '\n')
    character = 0
    line = []
    pl = pl + 1

    content.extend(['\n' for i in range(29 - pl)])
    content.append(str(pagenumber).rstrip())

    file1.writelines(content)

    file1.close()



# practice on open, write and read files

# Write
'''
f = open("own practice.txt", "w")
f.write("ppprogramingggggggggggggg")
f.close()
# for 'write', file.close() should be at the end.
'''
'''
# with open("own practice.txt", 'w') as fw:
with open("own practice.txt", "w") as fw:
    fw.write("anything you want")
'''


# Read
'''
f = open('own practice.txt', 'r')
abigstring = f.read()
f.close()

print(abigstring)
print(type(abigstring))
print(abigstring.startswith("You are the best. You will get 100!"))
print(abigstring.startswith("You are the best.\nYou will get 100!"))
'''


fr = open('own practice.txt', 'r')
oneline = fr.readline
"""
for i in fr:
    print(i)
"""
"""
for oneline in fr:
    print(oneline)
print(oneline.startswith("You are the best.\nYou will get 100!"))
"""

