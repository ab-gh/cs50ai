zero_gene=set()
one_gene=set()
two_genes=set()
mother = 1
father = 1
PROBS = dict()
prob = 1

if mother in zero_gene and father in zero_gene:
    prob *= PROBS["mutation"] * (1 - PROBS["mutation"]) + (1 - PROBS["mutation"]) * PROBS["mutation"]
if mother in zero_gene and father in one_gene:
    prob *= PROBS["mutation"] * 0.5 + (1 - PROBS["mutation"]) * 0.5
if mother in zero_gene and father in two_genes:
    prob *= PROBS["mutation"] * PROBS["mutation"] + (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])

if mother in one_gene and father in zero_gene:
    prob *= 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]
if mother in one_gene and father in one_gene:
    prob *= 0.5 * 0.5 + 0.5 * 0.5
if mother in one_gene and father in two_genes:
    prob *= 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])

if mother in two_genes and father in zero_gene:
    prob *= (1 - PROBS["mutation"]) * (1 - PROBS["mutation"]) + PROBS["mutation"] * PROBS["mutation"]
if mother in two_genes and father in one_gene:
    prob *= (1 - PROBS["mutation"]) * 0.5 + PROBS["mutation"] * 0.5
if mother in two_genes and father in two_genes:
    prob *= (1 - PROBS["mutation"]) * PROBS["mutation"] + PROBS["mutation"] * (1 - PROBS["mutation"])