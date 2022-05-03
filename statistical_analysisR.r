#Generate 130 random ratings per raters randomly distributed across subjects
manual_original <- matrix(, nrow = 580, ncol = 12)
manual_defaced <- matrix(, nrow = 580, ncol = 12)
for (i in 1:12) {
    ind <- sample(1:580, 130, replace = F)
    manual_original[ind, i] <- sample(1:4, 130, replace = T)
    manual_defaced[ind, i] <- sample(1:4, 130, replace = T)
}

#Run Continuation ratio mixed effects regression

set.seed(1234)
n <- 580 # number of subjects
K <- 12 # number of measurements per subject
t_max <- 2 # maximum follow-up time

# we construct a data frame with the design: 
# everyone has a baseline measurement, and then measurements at random follow-up times
DF <- data.frame(sub = rep(seq_len(n), each = K),
                 rater = c(replicate(n, c(0, sort(runif(K - 1, 0, t_max))))),
                 defaced = rep(gl(2, n/2, labels = c("original", "defaced")), each = K))

# design matrices for the fixed and random effects
# we exclude the intercept from the design matrix of the fixed effects because in the
# CR model we have K intercepts (the alpha_k coefficients in the formulation above)
X <- model.matrix(~ defaced * rater, data = DF)[, -1]
Z <- model.matrix(~ rater, data = DF)

thrs <- c(-1.5, 0, 0.9) # thresholds for the different ordinal categories
betas <- c(-0.25, 0.24, -0.05) # fixed effects coefficients
D11 <- 0.48 # variance of random intercepts
D22 <- 0.1 # variance of random slopes

# we simulate random effects
b <- cbind(rnorm(n, sd = sqrt(D11)), rnorm(n, sd = sqrt(D22)))
# linear predictor
eta_y <- drop(X %*% betas + rowSums(Z * b[DF$id, , drop = FALSE]))
# linear predictor for each category under forward CR formulation
# for the backward formulation, check the note below
eta_y <- outer(eta_y, thrs, "+")
# marginal probabilities per category
mprobs <- cr_marg_probs(eta_y)
# we simulate ordinal longitudinal data
DF$y <- unname(apply(mprobs, 1, sample, x = ncol(mprobs), size = 1, replace = TRUE))
DF$y <- factor(DF$y, levels = 1:4, labels = c("excluded", "poor", "good", "excellent"))

cr_vals <- cr_setup(DF$y)
cr_data <- DF[cr_vals$subs, ]
cr_data$y_new <- cr_vals$y
cr_data$cohort <- cr_vals$cohort
