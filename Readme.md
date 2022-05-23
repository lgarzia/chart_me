# _Chart Me_ - Charting the keeps you in the EDA flow

---

Chart Me is a high level charting library designed to expedite the Exploratory Data Analyis Process. There's a few automated eda tools like [sweet viz](https://pypi.org/project/sweetviz/) that give a great initial set of visualizations. [lux](https://github.com/lux-org/lux) is a great tool to leverage, which I recommend as an AI assistance type feel. What I wanted was a fast charting tool when I was digging in a bit. Leveraging Tableau is great - excepts it's a walled garden software. The other alternative is hand-writing Altair code, which takes me out of the flow from Data Mining to Software development...Chart Me serves to keep you in the data analytics flow of discovery in Python environment.

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
