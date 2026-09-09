# STAT 5400 - Section 2.3 - Vibe task
# Open this file in a Codespace (Copilot on) and let the completion help you.
#
# TASK: this R line gives the mean population of each region:
#
#     tapply(statedf[, "Population"], statedf[, "reg"], mean)
#
# Ask a model for the pandas version, put it below, and run it.
#
# Verify: your table must match these numbers, in this order.
#
#     Northeast        5495.1111
#     South            4208.1250
#     North Central    4803.0000
#     West             2915.3077
#
# The order is the point. R prints the regions in factor level order.
# pandas sorts alphabetically unless the column is a Categorical with
# the levels given in the right order.
import pandas as pd

statedf = pd.read_csv("notes/section2/data/state.csv")

# your translation here
