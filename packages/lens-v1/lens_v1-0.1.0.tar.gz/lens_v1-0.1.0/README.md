# Learning Entities from Narratives of Skin Cancer (LENS)
<img src="lens_logo_v1.png" alt="LENS Logo" width="800" height="270"/>  

**Learning Entities from Narratives of Skin Cancer (LENS)** is a Python library designed for Named Entity Recognition (NER) specifically tailored to narratives related to skin cancer. LENS is designed to recognize and categorize important entities within skin cancer narratives. It is equipped with 24 distinct tags (see file `annotation_guidelines.pdf`), which allow for the extraction of key information from unstructured text. This information can be linked to biomedical ontologies such as **[SNOMED-CT](https://colab.research.google.com/github/CogStack/MedCATtutorials/blob/main/notebooks/specialised/Preprocessing_SNOMED_CT.ipynb#scrollTo=o-TxIJ4N9T4Q)** and **[MedCAT](https://github.com/CogStack/MedCAT?tab=readme-ov-file)**, facilitating structured data analysis in clinical and research settings.


## Objective

The primary objective of LENS is to process input text—such as online narratives from platforms like Reddit—and return the corresponding **LENS tags**. These tags allow for the categorization of various entities mentioned in the text, facilitating further analysis and integration with biomedical ontologies.

## Installation

To install the latest version of LENS, please run the following command:

```bash
pip install lens-ner==0.1.0
```

## Usage Example

Below is an example of how to use LENS to extract entities from a skin cancer narrative:

```python
from lens_ner.model import Lens

lens = Lens()
text = "I was diagnosed with melanoma last year. I'm currently undergoing immunotherapy and sometimes feel nauseous."
entities = lens.get_entities(text)
print(entities)
```

## Functionalities

LENS provides a range of functionalities to meet diverse user needs:

1. **Extract all LENS entities:** Identify and extract all recognized entities from a given text.
```python
entities = lens.get_entities(text)
print(entities)
```

2. **Display all entities:** Output the extracted entities with their corresponding tags.
```python
lens.display_entities(text)
```

3. **Extract entities for a specific label:** Extract entities corresponding to a specific tag, such as `INV` (Investigation).
```python
entities = lens.get_entities(text, tag_list=['INV'])
print(entities)
```

4. **Extract entities for a subset of labels:** Focus on a subset of tags, for example, `TRT` and `SYM`.
```python
entities = lens.get_entities(text, tag_list=['TRT', 'INV'])
print(entities)
```

5. **Display entities for a subset of labels:** Output entities for specific tags, such as `TRT`, `SYM`, and `INV`.
```python
lens.display_entities(text, tag_list=['TRT', 'SYM','INV'])
```

6. **Extract all MedCAT Mappings:** Link recognized entities to MedCAT biomedical concepts.
```python
lens.display_entities(text)
```

7. **Extract all SNOMED-CT Mappings:** Link recognized entities to SNOMED-CT concepts.
```python
lens2medcat = lens.lens2medcat(text)
print(lens2medcat)
```

8. **Save the annotations in JSON format:** Save the extracted entities and mappings in a structured JSON file for further analysis.
```python
lens2snomedct = lens.lens2snomedct(text)
print(lens2snomedct)
```

## Tutorial

A comprehensive tutorial on how to use LENS, including advanced features, is available [here](link-to-tutorial).

## License

Unknown

This README file provides a formal and detailed overview of the LENS system, including installation instructions, usage examples, and available functionalities. It is designed to be informative and accessible to users who wish to integrate LENS into their projects.
