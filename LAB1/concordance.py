"""
SYSC 2100 Winter 2023
Lab 1, Part 3, Exercise 4, Extra-Practice Exercise 5
"""

__author__ = 'Rama Alkhouli'

import string

# For information about the string module, type help(string) at the shell
# prompt, or browse "The Python Standard Library", Section "Built-in Types",
# Subsection "Text Sequence Type - str" in the documentation
# (available @ python.org).


def build_concordance(filename: str) -> dict[str, list[int]]:
    """Return a concordance of words in the text file
    with the specified filename.

    The concordance is stored in a dictionary. The keys are the words in the
    text file. The value associated with each key is a list containing the line
    numbers of all the lines in the file in which the word occurs.)

    >>> concordance = build_concordance('sons_of_martha.txt')
    """
    infile = open(filename, "r")
    line_no = 0
    hist = {}

    for line in infile:
        word_list = line.split()
        line_no +=1
        print (line_no)

        for word in word_list:
            word = word.strip(string.punctuation).lower()

            if word != '':
                if word not in hist.keys():
                    count = []
                else:
                    count = hist [word]

            if line_no not in count:
                count.append(line_no)
                hist[word] = count

    print(hist)



# Extra-Practice: Exercise 5 Solution


if __name__ == '__main__':
    # Write your solution to Extra-practice Exercise 5 here
    filename = "two_cities.txt"
    build_concordance(filename)
    build_concordance("sons_of_martha.txt")