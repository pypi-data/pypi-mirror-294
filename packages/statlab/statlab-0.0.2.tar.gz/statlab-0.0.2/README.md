
# statlab
[![PyPi version](https://badgen.net/pypi/v/statlab)](https://pypi.org/project/statlab)


statlab is a new Python package offering a variety of statistical and machine learning tools.

This package is being developed by Noam Rotenberg and Zan Chaudhry.


# Products

## "ord" ordinal classification tools
Submodule contains:
+ TreeOrdinalClassifier
+ SubtractionOrdinalClassifier
+ Functions to calculate classification metrics on ordinal data

Submodule developed by: Noam Rotenberg, Andreia Faria, Brian Caffo

Examples coming soon!


# Usage

Install: ``!pip install statlab``

Import a single module: ``import statlab.ord`` - imports only ord

Import all modules: ``from statlab.all import *`` - can access any function without prefixes, e.g., ``TreeOrdinalClassifier(base_clf)``

Specific example:
```
!pip install statlab
import statlab.ord
base_clf = # some sklearn-style classifier
clf = statlab.ord.TreeOrdinalClassifier(base_clf)
```

# Future work:

+ Dataset mislabeling detection and classification
+ Naive Bayes classifier using nonparametric statistics
+ Automated nonlinear feature tuning
