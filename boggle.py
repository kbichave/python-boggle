from random import choice
from string import ascii_uppercase
import logging
import time
import argparse




class FindWordsInGrid:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.paths = []
        
    def get_grid(self):
        """Return a dictionary of grid positions to random letters"""
        return {(x, y): choice(ascii_uppercase) for x in range(self.X) for y in range(self.Y)}


    def get_neighbours(self):
        """Return a dictionary with all the neighbours surrounding a particular position"""
        self.neighbours = {}

        for position in self.grid:
            x, y = position
            positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                        (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
            self.neighbours[position] = [p for p in positions if 0 <= p[0] < self.X and 0 <= p[1] < self.Y]
        return self.neighbours


    def path_to_word(self, path):
        """Convert a list of grid positions to a word"""
        return ''.join([self.grid[p] for p in path])


    def search(self, path):
        """Recursively search the self.grid for words"""
        word = self.path_to_word(path)
        logging.debug('%s: %s' % (path, word))
        if word not in self.stems:
            return
        if word in self.dictionary:
            self.paths.append(path)
        for next_pos in self.neighbours[path[-1]]:
            if next_pos not in path:
                self.search(path + [next_pos])
            else:
                logging.debug('skipping %s because in path' % self.grid[next_pos])

    def get_dictionary(self):
        """Return a list of uppercase english words, including word stems"""
        self.stems, self.dictionary = set(), set()
        with open('words.txt') as f:
            for word in f:
                word = word.strip().upper()
                self.dictionary.add(word)

                for i in range(len(word)):
                    self.stems.add(word[:i + 1])

        return self.dictionary, self.stems

    def get_words(self):
        """Search each self.grid position and return all the words found"""
        for position in self.grid:
            logging.info('searching %s' % str(position))
            self.search([position])
        return [self.path_to_word(p) for p in self.paths]


    def print_grid(self):
        """Print the self.grid as a readable string"""
        s = ''
        for y in range(self.Y):
            for x in range(self.X):
                s += self.grid[x, y] + ' '
            s += '\n'
        print (s)
    
    def print_words(self):
        """ Creates a grid, gets neighbours, prints the grid and display list of words"""
        self.grid = self.get_grid()
        self.neighbours = self.get_neighbours()
        self.dictionary, self.stems = self.get_dictionary()
        self.print_grid()
        words = list(dict.fromkeys(self.get_words()))
        print (words)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=4, \
        help="Width of the grid. That is number of letters in row of the grid")
    parser.add_argument("--height", type=int, default=4, \
            help="Height of the grid. That is number of letters in column of the grid")   
    parser.add_argument('--info', action="store_true", default=False, help='Enable logging info messages. Default False')
    parser.add_argument('--debug', action="store_true", default=False, help='Enable logging debug messages. Default False') 
    args = parser.parse_args()

    if args.info:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    findwords = FindWordsInGrid(args.width, args.height)
    findwords.print_words()
