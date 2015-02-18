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

    def guess(self, letter):
        pos = self.find(letter)
        if len(pos) > 0:
            for x in pos:
                current[x] = letter
            return True
        failed.append(letter)
        return False
    
    def find(self, letter):
        return [idx for idx, l in enumerate(goal) if l == letter]

    def __str__(self):
        lf = len(self.failed)
        head = " O " if lf>0 else "   "
        arms = "/  " if lf==2 else "/| " if lf==3 else "/|\\" if lf>3 else "   "
        abd = " | " if lf>4 else "   "
        legs = "/  " if lf>5 else "/ \\" if lf>6 else "   "
        cur = ''.join(self.current)
        done = ''.join(self.failed)
        out = "".join([
                "Welcome to hangman!\n\n"
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


if __name__ == "__main__":
    
    man = Hangman("test")
    
    print man
        
