library(markovchain)

lambda <- 20 / 60 / 60 # seconds.
miu <- 1 / 12 / 60  # seconds.
iterations <- 60 * 60 * 1000  # seconds.

queue_capacity <- 10

states <- seq(0, queue_capacity, 1)

transition_matrix <- matrix(0, nrow = length(states), ncol = length(states))

rate_one_arrival <- lambda
rate_one_departure <- miu 

transition_matrix[1, 2] <- rate_one_arrival
transition_matrix[1, 1] <- 1 - transition_matrix[1, 2]

transition_matrix[queue_capacity+1, queue_capacity] <- rate_one_departure
transition_matrix[queue_capacity+1, queue_capacity+1] <- 1 - transition_matrix[queue_capacity+1, queue_capacity]

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


generate_results <- function(iteration)
{
  results <- c()
  for (j in 1:200) {
    lose_client <- 0
    set.seed(24124*j + 2343234)
    simulation <- rmarkovchain(iteration, mc, t0 = "0")
    for (i in 1:length(simulation))
    {
      if (simulation[i] == queue_capacity) {
        prob <- runif(1, 0, 1)
        if (prob <= rate_one_arrival) {
          lose_client <- lose_client + 1
        }
      }
    }
    results <- c(results, lose_client)
  }
  return(results)
}

vector_list <- lapply(iterations_range, generate_results)
df <- as.data.frame(vector_list)
colnames(df) <- c(iterations_range)
write.csv(df, "./lost_average.csv")