import csv
import sys
import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def force(string):
    """
    a function that determines if a given string can be represented as an int,
    float, shorthand '%b' month string, TRUE/FALSE, or visitor type
    and convert it to the corresponding type.
    
    for month strings, it will return the zero-indexed month number
    for TRUE/FALSE, it will return 1/0
    for visitor type, it will return 1 if returning, 0 if not returning
    """
    # if the string is only alpha (A-Z, a-z) or underscore
    if string.isalpha() or "_" in string:
        try:
            # try convert to a datetime object with '%b', and calculate the month number zero-indexed
            if len(string) == 3:
                a = datetime.datetime.strptime(string, "%b").month-1
            else:
                a = datetime.datetime.strptime(string, '%B').month-1
        except ValueError:
            # if it fails, attempt either TRUE/FALSE conversion
            if string in ["TRUE", "FALSE"]:
                a = 1 if string == "TRUE" else 0
            # or returning/not returning conversion
            if string in ["Returning_Visitor", "New_Visitor", "Other"]:
                a = 1 if string == "Returning_Visitor" else 0
    # if the string is numbers (or ".")
    else:
        try:
            # attempt to convert to int
            a = int(string)
        # if float
        except ValueError:
            # convert to float
            a = float(string)
    return a



def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # initialise the lists
    evidence = list()
    labels = list()
    # open CSV file
    with open(filename, "r") as f:
        # read CSV file
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        # for each row in the CSV file
        for row in reader:
            # append up to the penultimate element of the row
            evidence.append([force(x) for x in row[:len(row)-1]])
            # append the last element of the row
            labels.append(1 if row[-1] == 'TRUE' else 0)
    # return as tuple
    return (evidence, labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # initialise model
    model = KNeighborsClassifier(n_neighbors=1)
    # fit model
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # initialise the variables
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    # compare the labels and predictions with zip
    for compare in zip(labels, predictions):
        if compare[0] == 1 and compare[1] == 1:
            true_positives += 1
        if compare[0] == 0 and compare[1] == 0:
            true_negatives += 1
        if compare[0] == 0 and compare[1] == 1:
            false_positives += 1
        if compare[0] == 1 and compare[1] == 0:
            false_negatives += 1
    # calculate the sensitivity and specificity
    sensitivity = true_positives / (true_positives + false_negatives)
    specificity = true_negatives / (true_negatives + false_positives)
    # return as tuple
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
