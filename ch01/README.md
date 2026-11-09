# Chapter 1: Nature and Structure of Animal Breeding Data

| File | What it is |
|---|---|
| `data/pedigree.csv` | Constructed pedigree of 7 cows (Table 1.2) |
| `data/performance.csv` | Constructed performance file, 10 records (Table 1.4) |
| `data/scc.csv` | 24 constructed somatic cell counts (thousand cells per mL) |
| `data/herd_size.csv` | Herds and cows by herd size, from Table 1 of Al Kalaldeh et al. (2021), CC BY 4.0 |
| `code/ch01_replicate.py` | Python script: regenerates every number in sections 1.5 and 1.8 and the practical; 31 hand-versus-library checks |
| `code/ch01_check.R` | Independent check in base R (no packages) |
| `output/` | Saved results and the verification records |

Run `python ch01_replicate.py` in `code`, then `Rscript ch01_check.R`. The expected values are printed in the chapter's Computer exercise (section 1.9). Spreadsheet note: the spreadsheet SKEW function is sample-adjusted (3.82 and 1.97 for these data) and differs from the plain skewness (3.58 and 1.84) used in the chapter.
