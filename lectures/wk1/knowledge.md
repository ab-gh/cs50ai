# week 1: knowledge

**Knowledge-based agents**: agents that reason by operating on internal representations of knowledge.

How do we enable computers to understand logical reason?

**Sentence**: an assertion about the world in a knowledge represantation language.

## propositional logic

Sentences respresented by symbols

`P`: Harry visited Hagrid today

**Logical Connectives**

- `¬` (`!`): Not
- `^`: And
- `v`: Or
- `->`: Implication
- `<->`: Biconditional
- `|=`: Entailment

### not (`!`)

| `P` | `!P` |
| :---: |:---:|
| false | true |
| true | false |

### and (`^`)

| `P` | `Q` | `P^Q` |
| :---: |:---:|:---:|
| false | false | false |
| false | true | false |
| true | false | false |
| true | true | true |

### or (`v`)

| `P` | `Q` | `PvQ` |
| :---: |:---:|:---:|
| false | false | false |
| false | true | true |
| true | false | true |
| true | true | true |

### implies (`->`)
- Implication is only false if the premise is true but the conclusion is false

| `P` | `Q` | `P->Q` |
| :---: |:---:|:---:|
| false | false | true |
| false | true | true |
| true | false | false |
| true | true | true |

### biconditional (`<->`)
- If And Only If (Iff)
- This is an `XAND`

| `P` | `Q` | `P<->Q` |
| :---: |:---:|:---:|
| false | false | true |
| false | true | false |
| true | false | false |
| true | true | true |

### model

**Model**: Assignment of a truth value to every propositional symbol (a possible world)

- `P`: it is raining
- `Q`: it is tuesday
- {`P`=True, `Q`=False}
- Therefore it is raining but it is not Tuesday

**Knowledge Base**: A set of sentences known by the KBA

### entails (`|=`)
- `a|=b`
- In every model in which `a` is true, `b` is also true

## inference

The process of deriving new sentences from old ones

- `P`: It is a Tuesday.
- `Q`: It is raining.
- `R`: Harry will go for a run.

**KB**: 
1. `(P^!Q)->R`
2. `P` (P is true)
3. `!Q` (Q is false)

**Inference**: `KB|=R` (KB entails that R is true)

## model checking

To determine if `KB|=a`
- Enumerate all possible models
- If in every model where KB is true, `a` is true, then `KB|=a`

|P|Q|R|KB|
| :---: | :---: | :---: | :---: |
|false|false|false|false|
|false|false|true|false|
|false|true|false|false|
|false|true|true|false|
|true|false|false|false|
|true|false|true|true|
|true|true|false|false|
|true|true|true|false|

## knowledge engineering

The process of figuring out how to represent propositions and logic in AI.

### a game of clue

- One of the people is the murderer: `(mustard v plum v scarlet)`
- One of the rooms is the crime scene: `(ballroom v kitchen v library)`
- One of the tools was the weapon: `(knife v revolver v wrench)`

Now someone sees their own cards:

- `!mustard`
- `!kitchen`
- `!revolver`

Someone might guess a trio, and might be wrong, but only in this combination:

- `!scarlet v !library v !wrench`

You might see another card:

- `!plum`

Therefore you know that `scarlet` must be true.

- `!ballroom`

Now we know that `scarlet ^ library ^ knife`

## inference rules

Can we make Model Checking quicker, and not have to enumerate every single option in the space?

### modus ponens

Premise:
- If it is raining, Harry is inside.
- It is raining.

Inference:
- Harry is inside.

**Modus Ponens**: If `a->b` and `a`, then we can infer `b`

### and elimination

If `a ^ b`, then we can infer `a`

### double negation elimination

If `!(!a)`, then we can infer `a`

### implication elimination

If `a->b`, then we can infer `!a v b`

### biconditional elimination

If `a<->b`, then we can infer `(a->b) ^ (b->a)`

### de morgan's law

If `!(a ^ b)`, then we can infer `!a v !b`

If `!(a v b)`, then we can infer `!a ^ !b`

### distributive property

If `(a ^ (b v c))`, then we can infer `(a ^ b) v (a ^ c)`

If `(a v (b ^ c)`, then we can infer `(a v b) ^ (a v c)`

## resolution

**Unit resolution**: If `P v Q` and `!P`, then `Q`
- This relies on complementary literals, two of the same atomic propositions where one is negated

**Generalised**: If `P v Q` and `!P v R`, then `Q v R`

**Disjunction**: Connections of ors

**Conjunction**: Connections of ands

**Conjunctive normal form**: A logical sentence that is a conjunction of disjunctive clauses
- Eg: `(A v B v C) ^ (A v !E) ^ (F v G)`

### example

- KB: `(A v B) ^ (!B v C) ^ (!C)`
- Query: `A`
- Assumption in CNF: `(A v B) ^ (!B v C) ^ (!C) ^ (!A)`
