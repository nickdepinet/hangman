import sys
import time

from hangman import Hangman

class AI():
    
    words = {}
    freq = []
    possible = []
    eng = None

    def __init__(self, dictionary, man):
        self.eng = man
        #Build the word dictionary
        with open(dictionary) as f:
            for line in f:
                w = line.strip().lower()
                if len(w) == len(self.eng.current):
                    self.possible.append(w)
        self.possible = list(set(self.possible))
                #uncomment to allow multiple word guesses
                #if len(w) in self.words:
                #    self.words[len(w)].append(w)
                #else:
                #    self.words[len(w)] = [w]
        #self.possible = list(set(self.words[len(self.eng.current)]))

    def trim_possible(self):
        cur = ''.join(self.eng.current)
        print "Pre Trim Length: " + str(len(self.possible))
        for p in self.possible[:]:
            for f in self.eng.failed:
                if f in p:
                    self.possible.remove(p)
            for x in range(len(cur)):
                if not cur[x] == '_':
                    if not p[x] == cur[x]:
                        #print "p: " + p
                        #print p[x] + " not equal " + cur[x] + " at " + str(x)
                        self.possible.remove(p)
                        break
        print "Post Trim Length: " + str(len(self.possible))
        if len(self.possible)<20:
            print "Post Trim: "
            print self.possible

    def move(self):
        freq_dict = {}
        if len(self.possible) == 1:
            self.eng.guess(self.possible.pop())
        else:
            for p in self.possible:
                # Find the number of words a letter is in
                # More useful than total appearances
                for c in set(p):
                    if c in freq_dict:
                        freq_dict[c] += 1
                    else:
                        freq_dict[c] = 1
            self.freq = [x for x in sorted(freq_dict, key=freq_dict.get)]
            next_ltr = self.freq.pop()
            while next_ltr in self.eng.failed or next_ltr in self.eng.current:
                next_ltr = self.freq.pop()
            self.eng.guess(next_ltr)
        if not self.eng.won():
            self.trim_possible()
        
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
    if not len(sys.argv) == 3:
        print "Usage: python ai.py word_file goal_word"
        sys.exit(1)
    
    man = Hangman(sys.argv[2].strip().lower())
    bot = AI(sys.argv[1], man)

    bot.play()


