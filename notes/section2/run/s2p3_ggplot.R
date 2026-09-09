# Section 2.3 -- the ggplot2 example. ggplot2 is not installed in the browser session.
library(ggplot2)

data(state)
statedf <- data.frame(abb=state.abb,
  div=state.division,
  reg=state.region,
  state.x77[ , c("Population", "Area")])

p <- ggplot(statedf, aes(Area, Population)) +
  geom_point()
p + geom_smooth(method="loess", se=FALSE)
