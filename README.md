# _Chart Me_ Charting that keeps you in the EDA flow

---

Chart Me is a high level charting library designed to expedite the Exploratory Data Analyis Process. There's a few automated eda tools like [sweet viz](https://pypi.org/project/sweetviz/) that give a great initial set of visualizations. [lux](https://github.com/lux-org/lux) is a great tool to leverage - which gives a feel of AI assistance - but not always on the mark. The other alternative is hand-writing Altair code, which takes me out of the EDA flow looking up syntax or building functions..._Chart Me_ serves to keep you in the data analytics flow of discovery by keeping visualization commands to **one function** to remember.
[![v0.1.3](https://img.shields.io/pypi/v/chart_me.svg)](https://pypi.org/project/chart_me/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Interrogate](https://raw.githubusercontent.com/lgarzia/chart_me/master/interrogate_badge.svg)](https://interrogate.readthedocs.io/)

## Chart Me Documentation

See [Read the Docs](https://chart-me.readthedocs.io/en/latest/index.html) for more details

## **Usage Warnings**

_Consider this is beta/proof-of-concept mode at this time. Limited to bivariate charts and doesn't support geographical data and lightly tested_

## Installation

```bash
$ pip install chart_me
```

## Simple Usage

`chart_me` used to quickly generate visualizations during eda process

```python
import chart_me as ce
ce.chart_me(df, 'col_1', 'col_2') #<-- reads as c-e-chart_me

```

![example](https://github.com/lgarzia/chart_me/blob/master/docs/source/_static/Example_Screenshot.png?raw=true)
