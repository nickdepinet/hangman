import sys
import time
import operator

from hangman import Hangman

class AI():
    
    words = {}
    freq = []
    wpossible = set()
    possible = set()
    eng = None

    def __init__(self, dictionary, man, wcount):
        self.eng = man
        curlen = len(self.eng.current)
        #Build the word dictionary
        with open(dictionary) as f:
            for line in f:
                w = line.strip().lower()
                if len(w) == curlen:
                    self.possible.add(w)
        with open(wcount) as c:
            for line in c:
                w = line.strip().split()
                if len(w[0]) == curlen:
                    w[0] = w[0].lower()
                    w[1] = int(w[1])
                    self.wpossible.add(tuple(w))

    def trim_possible_s(self,guess):
        cur = [i for i,x in enumerate(self.eng.current) if x == guess]
        print "Pre Trim Length: " + str(len(self.possible))
        for p in list(self.possible):
            for x in cur:
                if not p[x] == guess:
                    self.possible.remove(p)
                    break
        for w in list(self.wpossible):
            for x in cur:
                if not w[0][x] == guess:
                    self.wpossible.remove(w)
                    break
        print "Post Trim Length: " + str(len(self.possible))
        if len(self.possible)<20:
            print "Post Trim: "
            print self.possible
            if len(self.wpossible)<20:
                print self.wpossible

    def trim_possible_f(self,guess):
        cur = ''.join(self.eng.current)
        print "Pre Trim Length: " + str(len(self.possible))
        tmp = filter(lambda x: guess not in set(x), self.possible)
        self.possible = tmp
        tmp = filter(lambda x: guess not in set(x[0]), self.wpossible)
        self.wpossible = tmp
        print "Post Trim Length: " + str(len(self.possible))
        if len(self.possible)<20:
            print "Post Trim: "
            print self.possible
            if len(self.wpossible) < 20:
                print self.wpossible

    def word_freq(self,cur_ltr):
        wfreq = sorted(self.wpossible, key=operator.itemgetter(1))
        if len(wfreq) == 0:
            return cur_ltr
        word = wfreq.pop()[0]
        print "Word: " + ''.join(word)
        word = set(word)
        next_ltr = word.pop()
        while next_ltr in self.eng.failed or next_ltr in self.eng.current:
            if len(word) == 0:
                word = set(wfreq.pop()[0])
            next_ltr = word.pop()
        return next_ltr

    def move(self):
        freq_dict = {}
        if len(self.possible) == 1:
            self.eng.guess(self.possible.pop())
        else:
            for p in self.possible:
                # Find the number of words a letter is in
                # More useful than total appearances
                # Only in big words
                if len(self.eng.current) > 5:
                    ltrs = set(p)
                else:
                    ltrs = p
                for c in ltrs:
                    if c in freq_dict:
                        freq_dict[c] += 1
                    else:
                        freq_dict[c] = 1
                for f in set(self.eng.failed):
                    if f in freq_dict: del freq_dict[f]
                for c in set(self.eng.current):
                    if c in freq_dict: del freq_dict[c]
            
            #self.freq = [x for x in sorted(freq_dict, key=freq_dict.get)]
            self.freq = sorted(freq_dict.items(), key=operator.itemgetter(1))
            print "Letter Freq: "
            print self.freq
            next_ltr = self.freq[-1][0]
            if len(self.freq) > 1:
                if len(set(x[1] for x in self.freq)) <= 1:
                    next_ltr = self.word_freq(next_ltr)
            print "Guessing: " + next_ltr
            res = self.eng.guess(next_ltr)
        if not self.eng.won():
            if res:
                self.trim_possible_s(next_ltr)
            else:
                self.trim_possible_f(next_ltr)
        
    def play(self):
        in_play = True
        turns = 0
        while in_play:
            print self.eng
            turns += 1
            self.move()
            in_play = not self.eng.won() and not self.eng.lost()
            #time.sleep(0.5)
        print self.eng
        print "The computer won in " + str(turns) + " turns.\n" if self.eng.won() else "That word was too hard, the ai lost.\n"

if __name__ == "__main__":
    import cProfile
    if not len(sys.argv) == 4:
        print "Usage: python ai.py word_file word_count_file goal_word"
        sys.exit(1)
    
    man = Hangman(sys.argv[3].strip().lower())
    bot = AI(sys.argv[1], man, sys.argv[2])

    #bot.play()

    cProfile.run('bot.play()', sort='cumulative')

