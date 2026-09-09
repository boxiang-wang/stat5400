# Section 2.3 -- the plotnine example. plotnine is not installed in the browser session.
# plotnine is the Python port of ggplot2; install it with:  pip install plotnine
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_smooth

statedf = pd.read_csv("notes/section2/data/state.csv")

p = ggplot(statedf, aes("Area", "Population")) + geom_point()
print(p + geom_smooth(method="lowess", se=False))
