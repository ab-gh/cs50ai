import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells is equal to the number of counts
        if len(self.cells) == self.count:
            # Return a copy of the cells
            # While deepcopy's arent strictly needed, let's play it safe
            return copy.deepcopy(set(self.cells))
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the cells are equal to zero
        if self.count == 0:
            # Return a copy of the cells
            return copy.deepcopy(set(self.cells))
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # Remove the mine from the sentence
            self.cells.remove(cell)
            # Remove the mine from the count
            self.count -= 1
            # Return True to flag the removal
            return True
        else:
            return False

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # Remove the safe from the sentence
            self.cells.remove(cell)
            # Return True to flag the removal
            return True
        else:
            return False


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        flags = 0
        # Add the mine to the internal list
        self.mines.add(cell)
        for sentence in self.knowledge:
            # Remove the mine from each sentence
            flag = sentence.mark_mine(cell)
            # Count up how many times the mine was removed from a sentence
            if flag: flags += 1
        return flags

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        flags = 0
        self.safes.add(cell)
        for sentence in self.knowledge:
            flag = sentence.mark_safe(cell)
            # Count up how many times the safe was removed from a sentence
            if flag: flags += 1
        return flags

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Add this cell as safe
        self.mark_safe(cell)
        # Add this move as made
        self.moves_made.add(cell)
        # Get surrounding cells
        surrounding = set()
        # For each cell in the range n-1 to n+1 in the x and y coordinates
        for c in itertools.product(*(range(n-1, n+2) for n in cell)):
            # If this cell isnt the cell itsself, and it is between the grid borders
            if c != cell and 0 <= c[0] < self.height and 0 <= c[1] < self.width:
                # Add it to the surrounding cells
                surrounding.add(c)
        # Remove the safe cells and moves made from surrounding cells
        surrounding -= self.safes | self.moves_made
        # Add a new knowledge sentence
        self.knowledge.append(Sentence(surrounding, count))
        # Get new safes and mines
        self.update()
        # Make new inferences
        inferences = self.infer()
        # While there are inferences we can make
        while inferences:
            for sentence in inferences:
                # Add the inferences to the knoledge
                self.knowledge.append(sentence)
            # Get the new safes and mines
            self.update()
            # Make new inferences
            inferences = self.infer()

    def update(self):
        # Start with one repeat of updating
        repeats = 1
        while repeats != 0:
            # No new repeats by default
            repeats = 0
            # Track empty sentences
            to_remove = []
            # For each sentence
            for sentence in self.knowledge:
                # Clean up empty sets
                if len(sentence.cells) == 0:
                    to_remove.append(sentence)
                # Add the sentences known safes to the internal list
                for safe in sentence.known_safes():
                    # Flag another repeat if any sentences were updated
                    repeats += self.mark_safe(safe)
                for mine in sentence.known_mines():
                    # Flag another repeat if any sentences were updated
                    repeats += self.mark_mine(mine)
            # Clean out the empty sets
            self.knowledge = [s for s in self.knowledge if s not in to_remove]
            
    def infer(self):
        inferences = []
        to_remove = []
        # Iterate over every sentence
        for s1 in self.knowledge:
            if len(s1.cells) == 0:
                # Clean up empty sets
                to_remove.append(s1)
                continue
            # Iterate over every sentence again
            for s2 in self.knowledge:
                if len(s2.cells) == 0:
                    # Clean up empty sets
                    to_remove.append(s2)
                    continue
                # If the two sentences aren't the same
                if s1 != s2:
                    # And if s2 is a subset of s1
                    if s2.cells.issubset(s1.cells):
                        # An inference can be made
                        new_sentence = Sentence(s1.cells.difference(s2.cells), s1.count-s2.count)
                        # If this inference isn't already known
                        if new_sentence not in self.knowledge:
                            # Add the new sentence inferred
                            inferences.append(new_sentence)
        # Clean out the empty sets
        self.knowledge = [s for s in self.knowledge if s not in to_remove]
        return inferences

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Find a safe move
        for move in self.safes:
            # If the move hasn't already been made and isnt a mine
            if move not in self.moves_made and move not in self.mines:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Start in the top left
        for x in range(0, self.width):
            for y in range(0, self.height):
                # If the random move hasn't been made and isn't a mine
                if (x, y) not in self.moves_made and (x, y) not in self.mines:
                    return (x, y)
        return None
