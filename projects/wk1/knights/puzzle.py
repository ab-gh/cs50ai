from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
AStatement0 = And(AKnight, AKnave)
knowledge0 = And(
    # Context
    Not(Biconditional(AKnight, AKnave)), # A is a knight or a knave but not both
    # Statements
    Or(
        Biconditional(AKnight, AStatement0), # If A is a knight their statement is the truth
        Biconditional(AKnave, Not(AStatement0)) # If A is a knave their statement is false
    ) 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
AStatement1 = And(AKnave, BKnave)
BStatement1 = ()
knowledge1 = And(
    # Context
    Not(Biconditional(AKnight, AKnave)),
    Not(Biconditional(BKnight, BKnave)),
    # Statements
    Or(
        Biconditional(AKnight, AStatement1),
        Biconditional(AKnave, Not(AStatement1))
    )
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
AStatement2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BStatement2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # Context
    Not(Biconditional(AKnight, AKnave)),
    Not(Biconditional(BKnight, BKnave)),
    # Statements
    Or(
        Biconditional(AKnight, AStatement2),
        Biconditional(AKnave, Not(AStatement2))
    ),
    Or(
        Biconditional(BKnight, BStatement2),
        Biconditional(BKnave, Not(BStatement2))
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
AStatement3 = Or(AKnight, AKnave)
BStatement3 = And(
    Or(
        Biconditional(AKnave, Not(AKnave)), # If A is a Knave, their claimed statement would be false
        Biconditional(AKnight, AKnave) # If A is a Knight, their claimed statement would be true
    ),
    CKnave)
CStatement3 = AKnight
knowledge3 = And(
    # Context
    Not(Biconditional(AKnight, AKnave)),
    Not(Biconditional(BKnight, BKnave)),
    Not(Biconditional(CKnight, CKnave)),
    # Statements
    Or(
        Biconditional(AKnight, AStatement3),
        Biconditional(AKnave, Not(AStatement3))
    ),
    Or(
        Biconditional(BKnight, BStatement3),
        Biconditional(BKnave, Not(BStatement3))
    ),
    Or(
        Biconditional(CKnight, CStatement3),
        Biconditional(CKnave, Not(CStatement3))
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
