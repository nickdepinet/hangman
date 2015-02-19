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
                if len(w) in self.words:
                    self.words[len(w)].append(w)
                else:
                    self.words[len(w)] = [w]
        self.possible = self.words[len(self.eng.current)]

    def trim_possible(self):
        for p in self.possible:
            for x in range(len(self.eng.current)):
                if not p[x] == self.eng.current[x] and not self.eng.current[x] == '_':
                    self.possible.remove(p)
                    break
        print "Possible:\n"
        print self.possible
        print "\n" 

    def move(self):
        freq_dict = {}
        for p in self.possible:
            for c in p:
                if c in freq_dict:
                    freq_dict[c] += 1
                else:
                    freq_dict[c] = 1
        self.freq = [x for x in sorted(freq_dict, key=freq_dict.get)]
        next_ltr = self.freq.pop()
        while next_ltr in self.eng.failed or next_ltr in self.eng.current:
            next_ltr = self.freq.pop()
        self.eng.guess(next_ltr)
        self.trim_possible()
        
    def play(self):
        in_play = True
        turns = 0
        while in_play:
            turns += 1
            self.move()
            in_play = not self.eng.won() and not self.eng.lost()
            print self.eng
            time.sleep(0.5)
        print self.eng
        print "The computer won in " + turns + " turns.\n" if self.eng.won() else "That word was too hard, the ai lost.\n"

if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print "Usage: python ai.py word_file goal_word"
        sys.exit(1)
    
    man = Hangman(sys.argv[2].strip().lower())
    bot = AI(sys.argv[1], man)

    bot.play()


