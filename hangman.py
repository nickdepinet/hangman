# Hangman Game Plus AI
# Nick Depinet

import sys

class Hangman():

    goal = ""
    current = []
    failed = []

    def __init__(self, goal):
        self.goal = goal
        for x in range(len(goal)):
            self.current.append("_")

    def won(self):
        return self.isGoal(''.join(self.current))

    def lost(self):
        return len(self.failed) >= 7

    def isGoal(self, string):
        return self.goal == string

    def guess(self, letter):
        if len(letter) > 1:
            if self.isGoal(letter):
                self.current = letter.split('')
                return True
            self.failed.append(letter)
            return False
        pos = self.find(letter)
        if len(pos) > 0:
            for x in pos:
                self.current[x] = letter
            return True
        self.failed.append(letter)
        return False
    
    def find(self, letter):
        return [idx for idx, l in enumerate(self.goal) if l == letter]

    def __str__(self):
        lf = len(self.failed)
        head = " O " if lf>0 else "   "
        arms = "/  " if lf==2 else "/| " if lf==3 else "/|\\" if lf>3 else "   "
        abd = " | " if lf>4 else "   "
        legs = "/  " if lf==6 else "/ \\" if lf>6 else "   "
        cur = ''.join(self.current)
        done = ''.join(self.failed)
        out = "".join([
                "\nWelcome to hangman!\n\n"
                "  ____\n",
                "  |  |\n",
                " " + head + " |\n",
                " " + arms + " |\n",
                " " + abd + " | \n",
                " " + legs + " |\n",
                "     |\n",
                " ____|____\n\n",
                "Current State: " + cur + "\n",
                "Failed Guesses: " + done + "\n\n"])
        return out

    def play(self):
        in_play = True
        while in_play:
            print self

            gs = raw_input("Make a Guess! (One letter or the whole thing): ")
            print gs
            print "Good Guess!\n" if self.guess(gs) else "Oh No! Try Another Letter!\n"
            in_play = not self.won() and not self.lost()
        print self
        print "Congratulations! You Won!\n" if self.won() else "Sorry, you lost :(\n"


if __name__ == "__main__":
    
    man = Hangman("test")
    man.play()
        
