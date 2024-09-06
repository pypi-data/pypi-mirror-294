# DarijaDistance Library

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

DarijaDistance is a specialized Python library crafted to handle the unique linguistic nuances of Moroccan Darija. It offers powerful tools for word comparison, distance measurement, translation lookup, and more; making it a valuable tool for natural language processing (NLP) tasks involving Darija.

## Features

- **Word Distance Calculation**: Calculate the distance between two words based on various factors, including letter differences, vowel swaps, and more.
- **Closest Word Finder**: Identify the closest words to a given word using positional encoding and other techniques.
- **Translation Lookup**: Retrieve potential translations for Darija words, including confidence scores.
- **Customizable**: Includes various methods to handle different types of word comparisons, including specific cases like vowel swaps and character replacements.

## Installation

You can install DarijaDistance via pip:

```bash
pip install DarijaDistance
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/aissam-out/DarijaDistance.git
cd DarijaDistance
pip install .
```

## Usage

Here are some basic usage examples to get you started:

### Calculating Word Distance

```python
from DarijaDistance.word_distance import WordDistance

wd = WordDistance()

vowel_dist = wd.distance_between("kelb", "kalb")
consonant_dist = wd.distance_between("kelb", "kedb")
print(f"Vowel: {vowel_dist} - Consonant: {consonant_dist}")
# Vowel: 2.2 - Consonant: 4

repeated_letter = wd.distance_between("abc", "abbc")
different_letter = wd.distance_between("abc", "abdc")
print(f"Repeated: {repeated_letter} - Different: {different_letter}")
# Repeated: 2 - Different: 3

dist_1 = wd.distance_between("9alam", "qalam")
dist_2 = wd.distance_between("9alam", "3alam")
print(f"Distance A: {dist_1} - Distance B: {dist_2}")
# Distance A: 2.2 - Distance B: 4

distance = wd.distance_between("so9", "sou9")
print(f"Distance: {distance}")
# Distance: 0
```

Traditional distance measures like Levenshtein focus on the number of insertions, deletions, and substitutions required to transform one word into another. While useful, these methods treat all characters equally, ignoring the phonetic and linguistic nuances present in languages like Darija.

### Finding Closest Words

```python
closest_words, min_distance = wd.get_closests("kulb")
print(f"Closest words to 'kulb': {closest_words} - min distance = {min_distance}")
# output: ['klb', 'kelb', 'kalb'] - 2.1
```

The WordDistance library encodes each character on a conceptual 3-dimensional plane, assigning numeric values to vowels, consonants and digits based on their relative importance and proximity within the Darija language. Summing these values creates a "sum image" for each word, simplifying comparisons and boosting performance. While this sum abstracts away some details, like the exact order of letters, it effectively reduces search complexity. Therefore, the integration of this 3-dimensional representation with summation produces a robust and efficient distance metric, positioning WordDistance as a superior tool for accurately assessing word similarities while ensuring optimal computational efficiency.

### Looking Up Translations

```python
translation = wd.lookup_translation_word("klb")
print(f"Potential translations for 'klb': {translation}")
```

For tasks such as finding the closest words and looking up translations, the WordDistance library relies on the Darija Open Dataset [(DODa)](https://github.com/darija-open-dataset/dataset), which was used to create the embedded pickle files that power these features. Specifically, the `hash_table_word.pickle` and `hash_table_sum.pickle` files. This structure enables efficient word lookup and comparison within the Darija language. However, for functions like `distance_between()` and other tools that do not require an underlying dataset, the library remains dataset agnostic and can operate with any words, regardless of their language or context.

## Checking for names

```python
wd.check_name("aissam")
# output: (True, {'potential translations': ['Aissam'], 'confidence': '100%'})
wd.check_name("tomobil")
# output: (False, {})
```

DarijaDistance library also includes a check_name method, designed to verify whether a given word is recognized as a name within the system. This function quickly scans the list of known names and returns a boolean indicating whether the word is a match. If a match is found, the function also provides potential translations along with a confidence score, ensuring that you can identify and work with names accurately in your applications.

## Managing Names and Translations with DarijaDataManager

The DarijaDataManager class provides easy-to-use methods for adding names and translations to your local datasets, ensuring your data is always up-to-date.

### Adding Names
You can add a new name to the list using the add_name method. If the name already exists, it won't be added again.

```python
from DarijaDistance.preprocess import DarijaDataManager

data_manager = DarijaDataManager()

data_manager.add_name("aissam")
```

### Adding Translations
Similarly, you can add new word translations using the add_translations method. The method ensures that only unique translations are added.

```python
from DarijaDistance.preprocess import DarijaDataManager

data_manager = DarijaDataManager()

translations = [("la", "no"), ("klb", "dog")]
data_manager.add_translations(translations)
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or find a bug, please open an issue or submit a pull request to the Github repo.

## Running Tests

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/aissam-out/DarijaDistance/blob/main/License) file for more details.

## Contact

If you have any questions or feedback, you can find me on LinkedIn: [Aissam Outchakoucht](https://www.linkedin.com/in/aissam-outchakoucht/) or on X: [@aissam_out](https://x.com/aissam_out).
