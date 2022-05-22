# Welcome to _Chart Me_ Library - Package ReadMe

This package is inspired by desire to speed up my EDA process in Python.
The big idea is creating a Tableau like experience within Python Jupyter Notebook.
For instance - in Tableau - I can add two pills and chart is auto-generated.

## Installation

```bash
$ pip install chart_me
```

## Usage

`chart_me` used to quickly generate visualizations during eda process

```python
import chart_me as ce
ce.chart_me(df, 'col_1', 'col_2') #<-- reads as c-e-chart_me

```

## Motivation

Results is a series of chart with sensible defaults based on datatypes

The closest library I found is [LUX](https://github.com/lux-org/lux) which is a great library. I find it's default a bit
unhelpful for the most parts; it has a feature of specifying column of interest.

I wanted a solution that's a little more intuitive and keeps me in the flow of eda.

I'm also a **huge** fan of [SWEET VIZ](https://pypi.org/project/sweetviz/). As I start my
eda process with a sweet viz kickout; From here, my intent is to leverage _Chart Me_ and lux to quickly work through the eda process.

**Altair:** Altair is an absolutely brilliant data visualization package. I'm a big fan of the javascript based libraries. The ultimate motivation for chart_me is to
speed up the altair scripting. Writing altair scripts everytime I want a visual is painful. I didn't want to create a module of one off visualizations - like; give me a pareto chart. Chart Me should provide my usual libraries.
