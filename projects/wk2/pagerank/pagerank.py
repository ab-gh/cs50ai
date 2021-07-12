import os
import random
import re
import sys
from decimal import Decimal
from fractions import Fraction
from numbers import Rational
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
       print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
       print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    # Random choice from all pages in corpus at 0.15 split between all pages
    for choice in corpus:
        model[choice] = (1-damping_factor) / len(corpus)
    # Random choice from all links in page at 0.85 split between all links
    for choice in corpus[page]:
        if len(corpus[page]) > 0:
            model[choice] += damping_factor / len(corpus[page])
        else:
            model[choice] += damping_factor / len(corpus)
    return model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise distribution
    sample = dict()
    # Fill distribution with zeroes
    for page in corpus:
        sample[page] = 0
    # Choose a starting page at true random
    page = random.choice(list(corpus.keys()))
    # Iterate n deep
    for i in range(1, n+1):
        # Record that we have visited this page
        sample[page] += 1
        # Collect transition model probabilities
        distribution = transition_model(corpus, page, damping_factor)
        # Choose a new page according to transition model
        page = random.choices(list(distribution.keys()), weights=list(distribution.values()), k=1)[0]
    # Normalise sample
    sample = {page: value / n for page, value in sample.items()}
    return sample

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise distribution
    iterative_distribution = {page: 1/len(corpus) for page in corpus}
    # Initialise distribution change
    deltas = {page: 1 for page in corpus}
    # Set threshold level for accuracy of convergence
    threshold = 0.0005
    # Iterate until convergence threshold met for all values
    while max(deltas.values()) > threshold:
        # Calculate new distribution
        # Copy old distribution for calculating deltas
        old_iterative_distribution = copy.deepcopy(iterative_distribution)
        # For each page in corpus
        for page in iterative_distribution:
            # Initialise summation term temp var
            summation_term = 0
            # For test pages that could link to this page
            for link in corpus:
                # If test page does link to this page
                if page in corpus[link]:
                    # Add probability of the link divided by the number of links
                    summation_term += iterative_distribution[link] / len(corpus[link])
                # If test page links nowhere
                if len(corpus[link]) == 0:
                    # Page has one link to every page in the corpus
                    summation_term += iterative_distribution[link] / len(corpus)
            # Calculate probability P(p): (1-d)/N + d*sum_{over i}(P(i)/N(i))
            new_probability = ((1-damping_factor) / len(corpus)) + (summation_term * damping_factor)
            # Update probability
            iterative_distribution[page] = new_probability
        # Calculate delta(P(p)) for convergence threshold check
        deltas = {page: abs(iterative_distribution[page] - old_iterative_distribution[page]) for page in deltas}
    return iterative_distribution



if __name__ == "__main__":
    main()
