# LLHTranslate
A script to add multilingual support for LLHelper.

# Usage

## 1. Parse
python3 parse.py path/to/file

This generates a dictionary file to translate.

## 2. Translate
Currently the dictionary file is stored in a format such that each key is followed by its translation, separated by a line break (\\n).

Translate the file by filling up the dictionary file.

## 2.5 Sanity Check
python3 parse.py --parse path/to/file

This checks whether there is any missed key.

## 3. Generate
python3 gen.py path/to/file [--newpath path]

This generates the translated file.
