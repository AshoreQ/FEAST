# iSideWith Example

Training Classifiers
--------------------

```
./populate_objectsdb.sh
python determine_unique_features.py objectsdb.sqlite3 Trump TrumpClassifier.json
python determine_unique_features.py objectsdb.sqlite3 Clinton ClintonClassifier.json
```

Evaluating Classifiers
----------------------

```
python determine_classifier_accuracy.py
```

