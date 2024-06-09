data <- read.csv("./lost_average.csv", row.names = 1)
par(mfrow = c(3, 1))
hist(data[, 1], main = "60*60*10 iterations", xlab = "Lost Clients", ylab = "")
hist(data[, 2], main = "60*60*100 iterations", xlab = "Lost Clients", ylab = "")
hist(data[, 3], main = "60*60*1000 iterations", xlab = "Lost Clients", ylab = "")


par(mfrow = c(1, 1))
library(ggplot2)
library(dplyr)

# Define the functions
fun.1 <- function(x) { (1-x)*x**10 / (1-x**11) }
fun.2 <- function(x) { (1-x)*x**20 / (1-x**21) }
fun.3 <- function(x) { (1-x)*x**5 / (1-x**6) }

# Prepare the data frame with x-values
xs <- c(1, 2, 4, 8, 16)
df <- data.frame(x = xs)

# Plot the functions
ggplot(df, aes(x)) +
  theme_classic() +
  theme(
    legend.position = c(.95,.95),
    legend.justification = c("right", "top"),
    legend.box.just = "right",
    legend.margin = margin(6, 6, 6, 6)
  )+
  geom_function(fun = fun.1, colour = "red", size = 1) + 
  geom_function(fun = fun.2, colour = "blue", size = 1) +
  geom_function(fun = fun.3, colour = "yellow", size = 1) +
  scale_x_continuous( limits = range(xs)) +
  scale_y_continuous()