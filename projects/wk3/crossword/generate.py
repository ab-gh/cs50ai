import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }


    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters


    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()


    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)


    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop over each variable (space for word) in the crossword
        # Use copy to prevent domains from being modified while looping
        for var in self.domains.copy():
            # Get all unary constraints for this variable
            for value in self.domains[var].copy():
                # Check if the value is consistent with all unary constraints
                if len(value) != var.length:
                    # If not, remove the value from the domain
                    self.domains[var].remove(value)
        # No return value is necessary
            

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # return set a default return value of False
        ret_val = False
        # define a tuple of the two variables without their domains
        var_tup = (x, y)
        # define lists of the variable's domains
        x_values = self.domains[x].copy()
        y_values = self.domains[y].copy()
        # if the two variables exist in overlaps
        if var_tup in self.crossword.overlaps:
            # if that overlap is not None
            if self.crossword.overlaps.get(var_tup) is not None:
                # assign the overlap
                overlap = self.crossword.overlaps[var_tup]
                # generate the list of letters that x has to match with
                y_matches = [val[overlap[1]] for val in y_values]
                # for each of x's domain values
                for value in x_values:
                    # if that value cannot match with y's domain values
                    if value[overlap[0]] not in y_matches:
                        # remove that value from the domain
                        self.domains[x].remove(value)
                        # set a flag for return value
                        ret_val = True
                # return True if any changes were made
        return ret_val
            
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = [arc for arc in self.crossword.overlaps if arc is not None]
        while len(arcs) != 0:
            (x, y) = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                # if the domain of x is not empty, enqueue neighbors
                for neighbor in self.crossword.neighbors(x):
                    if neighbor is not None and not neighbor == y:
                        arcs.append((neighbor, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # for each variable in the crossword
        for variable in self.crossword.variables:
            # if the variable is not assigned a value
            if variable not in assignment:
                # the crossword is not complete
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # for each of the current assignments
        for word in assignment:
            # if the word does not fit in the gaps
            if len(assignment[word]) != word.length:
                # reject attempt
                return False
            # if the word is already in the assignment
            if list(assignment.values()).count(assignment[word]) > 1:
                # reject attempt
                return False
            # for each of the overlaps
            for overlap in self.crossword.overlaps:
                # if the overlap isn't empty and is an overlap for the word
                # overlaps are a superset: if the overlap of (x, y) is in the set, so is (y, x), so we can just go by the first overlap element
                if self.crossword.overlaps[overlap] is not None and overlap[0] == word:
                    # try to access the word assignment for the other overlap target
                    try:
                        test_word = assignment[overlap[1]]
                    # if it does not exist in the assignment
                    except KeyError:
                        # continue to the next overlap
                        continue
                    # if the other overlap target has been assigned
                    else:
                        # extract the letter we want to match for the overlap
                        test_letter = test_word[self.crossword.overlaps[overlap][1]]
                        # if the letters do not match
                        if assignment[word][self.crossword.overlaps[overlap][0]] != test_letter:
                            # reject attempt
                            return False
        return True           
            

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # retrieve the domain for the variable
        domain = self.domains[var]
        # initialise a dictionary for sorting the values in the variable's domain
        sorting_dict = {}   
        # for each of the values in the variable's domain   
        for value in domain:
            # set the constraint counter to zero
            sorting_dict[value] = 0
            # for each of the neighbors of the variable
            for neighbor in self.crossword.neighbors(var):
                # retrieve the overlap indexes
                overlap = self.crossword.overlaps[(neighbor, var)]
                # for each of the overlap's possible values (the overlap's domain)
                for test in self.domains[neighbor]:
                    # if the overlap letter is not the same
                    if test[overlap[0]] != value[overlap[1]]:
                        # this value constrains the neighbor's domain
                        sorting_dict[value] += 1
        # sort the dictionary by the value of the sorting key
        sorted_vars = sorted(domain, key=lambda x: sorting_dict[x])
        return sorted_vars


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # sort crossword variables that are not in assignment by the length of their domain lists
        available = sorted([x for x in self.crossword.variables if x not in assignment], key=lambda x: len(self.domains[x]))
        # sort the list of available variables that have the same size domain as the shortest by the number of neighbors they have
        available = sorted([x for x in available if len(self.domains[x]) == len(self.domains[available[0]])], key=lambda x: len(self.crossword.neighbors(x)))
        # return the last element of the array
        return available.pop()

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if the assignment is complete
        if self.assignment_complete(assignment):
            # return the assignment, crossword is complete
            return assignment
        # pick a variable to try to assign
        var = self.select_unassigned_variable(assignment)
        # for each value in the variable's domain
        for value in self.order_domain_values(var, assignment):
            # attempt to assign this value and fit it into the crossword
            # make a copy of the current assignments
            trial = assignment.copy()
            # add the trial value to the test assignment
            trial[var] = value
            # if the test assignment is consistent
            if self.consistent(trial):
                # add the trial assignment to the current list of assignments
                assignment[var] = value
                # take the next backtrack step with this new assign,ent
                result = self.backtrack(assignment)
                # if the backtrack is a success
                if result is not None:
                    # we have a match
                    return result
                # a backtrack further down failed, so remove the trial assignment
                assignment.pop(var)
        # no assignment was possible, return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
