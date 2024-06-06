library(markovchain)

lambda <- 20 / 60 / 60 # seconds.
miu <- 1 / 12 / 60  # seconds.
iterations <- 60 * 60 * 1000  # seconds.


states <- c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

transition_matrix <- matrix(0, nrow = length(states), ncol = length(states))

rate_one_arrival <- lambda * exp(-lambda)
rate_one_departure <- miu * exp(-miu)

transition_matrix[1, 2] <- rate_one_arrival
transition_matrix[1, 1] <- 1 - transition_matrix[1, 2]

transition_matrix[11, 10] <- rate_one_departure
transition_matrix[11, 11] <- 1 - transition_matrix[11, 10]

for (i in 2:length(states) - 1) {
    for (j in 1:length(states)) {
        if (j == i + 1) {
            transition_matrix[i, j] <- rate_one_arrival
        } else if (j == i - 1) {
            transition_matrix[i, j] <- rate_one_departure
        } else {
            transition_matrix[i, j] <- 0
        }
    }
}

for (i in 2:length(states) - 1) {
    transition_matrix[i, i] <- 1 - sum(transition_matrix[i, ])
}

mc <- new("markovchain", states = states, transitionMatrix = transition_matrix, name = "Car Washer", byrow = TRUE)

results <- c()
for (j in 1:200) {
    lose_client <- 0
    set.seed(24124*j + 2343234)
    simulation <- rmarkovchain(iterations, mc, t0 = "0")
    for (i in 1:length(simulation))
    {
        if (simulation[i] == "10") {
            prob <- runif(1, 0, 1)
            if (prob <= rate_one_arrival) {
                lose_client <- lose_client + 1
            }
        }
    }
    results <- c(results, lose_client)
    print(mean(results))
}

# Assume that 'data' is your data
data <- results # replace with your data

# Calculate the mean and standard deviation
mean_data <- mean(data)
sd_data <- sd(data)


# Create the histogram
plot <- hist(data, main = "Histogram with Mean and SD", xlab = "Data", border = "black", col = "lightblue", xlim = range(c(data, mean_data - sd_data, mean_data + sd_data)))

# Add the mean
abline(v = mean_data, col = "red", lwd = 2)
text(
    x = mean_data, 
    y = par("usr")[4], 
    labels = paste("Mean =", round(mean_data, 2)), 
    pos = 2, col = "red"
)

# Add the standard deviation
abline(v = mean_data - sd_data, col = "blue", lwd = 2, lty = 2)
abline(v = mean_data + sd_data, col = "blue", lwd = 2, lty = 2)
