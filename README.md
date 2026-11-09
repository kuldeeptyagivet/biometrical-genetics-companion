# Biometrical Genetics: companion code and data

Code, constructed data sets and saved results for the chapters of the book *Biometrical Genetics* (Animal Genetics and Breeding, M.V.Sc. and Ph.D. syllabus: Biometrical Genetics I and II). Each chapter has a folder `chNN` with `data`, `code` and `output`. The chapter's Computer exercise says which script to run and which values to expect.

## How to use it (no Git needed)
1. Click the green **Code** button and choose **Download ZIP**, then unzip it.
2. Install Python 3 and run `pip install -r requirements.txt`. R (optional) is needed only for the independent check scripts.
3. Open a terminal in the chapter's `code` folder, for example `ch01/code`, and run `python ch01_replicate.py`. For the R check run `Rscript ch01_check.R`.
4. Compare your output with the files in the chapter's `output` folder and with the values printed in the chapter.

## Contents
| Folder | Chapter | Status |
|---|---|---|
| `ch01` | Nature and Structure of Animal Breeding Data | available |

## How the results are checked
Each number is computed by hand-written formulas and by a standard library, and the script stops if they disagree. An independent R script repeats the calculations and its results are compared with the Python results (`output/verification_python.txt`, `output/verification_R.txt`).

## Data
All data sets are constructed for teaching, except where a README states a published source. No real herd or owner information is included.

## Licences
Code: MIT (`LICENSE`). Data and saved outputs: Creative Commons Attribution 4.0 (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). The numbers in `ch01/data/herd_size.csv` are taken from Table 1 of Al Kalaldeh et al. (2021), Genetics Selection Evolution 53:73, https://doi.org/10.1186/s12711-021-00667-6, published under CC BY 4.0.

## Citing
Archived on Zenodo. The DOI of the first release (v0.1.0, Chapter 1) is https://doi.org/10.5281/zenodo.24080314. The DOI that always resolves to the latest version is https://doi.org/10.5281/zenodo.24080313.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24080313.svg)](https://doi.org/10.5281/zenodo.24080313)
