import csv
import itertools
import sys
import copy

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    ## trait_probability: phenotype scenario probability
    ## gene_number_probability: genotype scenario probability
    # generate set for zero genes
    zero_genes = people.keys() - (one_gene | two_genes)
    # initialise probability at 1
    total_probability = 1
    # compute total probability of given scenario
    for person in people:
        # retrieve person's phenotype probability (list comp)
        trait_probability = PROBS['trait'][2 if person in two_genes else 1 if person in one_gene else 0][person in have_trait]
        # check if person has parents in set
        if people[person]["mother"] == None or people[person]["father"] == None:
            # If there are no parents, assume and retrieve unconditional genotype
            gene_number_probability = PROBS["gene"][2 if person in two_genes else 1 if person in one_gene else 0]
        else:
            # retrieve parents
            mother = people[person]["mother"]
            father = people[person]["father"]
            # initialise parent's probabilities at 1
            ## these are later combined for the genotype probability given the persons's genotype in this scenario
            ## 0: (1-mother) + (1-father)
            ## 1: (1-mother)(father) + (1-father)(mother)
            ## 2: mother + father
            ## mutation is ignored for single-gene carriers as the mutation effects cancel out in all cases
            parent_probability = dict()
            for parent in [mother, father]:
                parent_probability[parent] = 1
            # find how many genes person has
            if person in zero_genes:
                # If genotype scenario is zero genes, use multiplicative probabiltiy of *not* carrying the gene
                for parent in [mother, father]:
                    if parent in zero_genes:
                        # Child only inherits bad gene if mutation occours
                        parent_probability[parent] *= PROBS['mutation']
                    elif parent in one_gene:
                        # Child inherits 'half' a bad gene
                        parent_probability[parent] *= 0.5
                    elif parent in two_genes:
                        # Child inherits bad gene unless mutation occours
                        parent_probability[parent] *= (1 - PROBS['mutation'])
                # Calculate inheritance probability for zero genes
                gene_number_probability = (1-parent_probability[mother]) * (1-parent_probability[father])
            elif person in one_gene:
                # If genotype scenario is one gene, use additive probability of the two multiplicative probabilities...
                # when one parent passes on the gene and the other parent does *not* pass on the gene
                for parent in [mother, father]:
                    # retrieve other parent
                    _tmp_other_parent = [p for p in [mother, father] if p != parent][0]
                    if parent in zero_genes:
                        # Child only inherits bad gene if mutation occours
                        parent_probability[parent] *= PROBS['mutation']
                        # Child effectively inherits good gene from other parent
                        parent_probability[_tmp_other_parent] *= (1 - PROBS['mutation'])
                    elif parent in one_gene:
                        # Child inherits 'half' a bad gene from BOTH parents
                        parent_probability[parent] *= 0.5
                        parent_probability[_tmp_other_parent] *= 0.5
                    elif parent in two_genes:
                        # Child inherits bad gene unless mutation occours
                        parent_probability[parent] *= (1 - PROBS['mutation'])
                        # Child effectively inherits good gene from other parent
                        parent_probability[_tmp_other_parent] *= PROBS['mutation']
                # Calculate inheritance probability for one gene
                gene_number_probability = parent_probability[mother] + parent_probability[father]
            elif person in two_genes:
                # If genotype scenario is two genes, use multiplicative probabiltiy of carrying both genes
                for parent in [mother, father]:
                    if parent in zero_genes:
                        # Child only inherits bad gene if mutation occours
                        parent_probability[parent] *= PROBS['mutation']
                    elif parent in one_gene:
                        # Child inherits 'half' a gene
                        parent_probability[parent] *= 0.5
                    elif parent in two_genes:
                        # Child inherits bad gene unless mutation occours
                        parent_probability[parent] *= (1 - PROBS['mutation'])
                # Calculate inheritance probability for two genes
                gene_number_probability = parent_probability[mother] * parent_probability[father]
        # Calculate person's genotype probability AND phenotype probability
        person_probability = gene_number_probability * trait_probability
        # ... previous probabilities AND this probability
        total_probability *= person_probability
    # return total
    return total_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # assign gene number for person
        if person in one_gene:
            gene_count = 1
        elif person in two_genes:
            gene_count = 2
        else:
            gene_count = 0
        # assign trait for person
        if person in have_trait:
            trait_presence = True
        else:
            trait_presence = False
        # update probabilities
        probabilities[person]['gene'][gene_count] += p
        probabilities[person]['trait'][trait_presence] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Calculate gene and trait probability totals
        gene_total = sum(probabilities[person]['gene'].values())
        trait_total = sum(probabilities[person]['trait'].values())
        # Divide each value in trait and gene by their totals to normalise (multiply by reciprocal)
        for i in probabilities[person]['gene']:
            probabilities[person]['gene'][i] /= gene_total
        for j in probabilities[person]['trait']:
            probabilities[person]['trait'][j] /= trait_total


if __name__ == "__main__":
    main()
