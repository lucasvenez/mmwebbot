[![DOI](https://zenodo.org/badge/155539529.svg)](https://zenodo.org/badge/latestdoi/155539529)

# MMWebBot: a crawler for the MMRF CoMMpass Study Dataset

It aims at collecting data from the research.themmrf.org repository automatically.

## Execution Instructions

To run this application you need a valid login and password for the research.themmrf.org repository. You should ask a valid login at https://themmrf.org/rg-signup/. With a valid login you should create two local files: `.username` and `.password` in the application root folder.

With these files you just need to run:

```python
python mmwebbot.py
```

All output data will be placed at `data` folder. The final data will contains a folder with direct correspondence to the repository menu.
