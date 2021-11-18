import re
from nltk.corpus import wordnet

class RepeatReplacer(object):
    def __init__(self):
        self.regex = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        if wordnet.synsets(word):
            return word
        loop_res = self.regex.sub(self.repl, word)
        if(word == loop_res):
            if wordnet.synsets(loop_res):
                return ori_word
            else:
                return loop_res
        else:
            return self.replace(loop_res)
        
    def check_replace(self, word):
        word_change = replacer.replace(word)
        if wordnet.synsets(word_change):
            return word_change
        else:
            return word
           