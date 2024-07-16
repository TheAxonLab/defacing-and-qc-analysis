simulate_data <- function(n_rated, n_sub, n_rater, perc_biased, ratings_range=1:4, bias = 1){
    #' Simulate human ratings of image quality. The ratings are randomly sampled from ratings_range 
    #' and randomly distributed across subjects. To introduce a bias in the ratings of defaced images, 
    #' we add the bias to a predefined precentage of the ratings on original images. The percentage of scan 
    #' affected varies between raters. By assigning a different number to n_sub and n_rated, we can simulate
    #' missing data.
    #'
    #' Parameters
    #' ----------
    #' n_rated = nbr of subjects rated per rater
    #' n_sub = nbr of subjects in the dataset
    #' n_rater = nbr of raters
    #' perc_biased = vector (1 x n_rater) establishing the percentage of scans biased per rater
    #' ratings_range = sequence defining the possible values of the manual ratings
    #' bias = the number that is added to original ratings 
    #' labels = vector of string corresponding to ratings' labels
    #'
    #' Returns 
    #' -------
    #' df : dataframe containing the manual ratings
    
    #Set random seed
    set.seed(1234)

    manual_original <- matrix(, nrow = n_sub, ncol = n_rater)
    manual_defaced <- matrix(, nrow = n_sub, ncol = n_rater)

    for (i in 1:n_rater) {
        #Each rater rates subjects picked at random
        ind_sub <- sample(1:n_sub, n_rated, replace = F)
        #random original ratings sampled from ratings_range
        ratings <- sample(ratings_range, n_rated, replace = T)
        manual_original[ind_sub, i] <- ratings

        #To simulate a positive bias towards defaced data, we improve the ratings of a 
        #predefined percentage of the original scans
        ind_rat <- sample(1:n_rated, round(n_rated*perc_biased[i]/100), replace = F)
        ratings_biased <- ratings
        ratings_biased[ind_rat] <- ratings_biased[ind_rat] + bias
        #The scale stops at 4 so clip higher values to 4 
        ratings_biased[ratings_biased > max(ratings_range)] <- max(ratings_range)

        #Set the biased ratings as the ratings on the defaced condition
        manual_defaced[ind_sub, i] <- ratings_biased
    }

    manual_original_vec <- c(manual_original)
    manual_defaced_vec <- c(manual_defaced)

    defaced <- rep(c(0, 1), times = n_rater*n_sub)
    sub <- rep(rep(1:n_sub, each=2), times = n_rater)
    rater <- rep(1:n_rater, each=n_sub*2)

    #Convert to dataframe to use in regression
    df <- data.frame(subject = sub)
    df$defaced <- factor(defaced, levels = 0:1, labels = c("original", "defaced"))
    df$rater_id <- factor(rater, levels = 1:n_rater, labels = sprintf("rater%02d", 1:n_rater))
    df$rating <- factor(c(rbind(manual_original_vec, manual_defaced_vec)), levels = ratings_range)

    return(df)
}

simulate_normal_data <- function(n_rated, n_sub, n_rater, perc_biased, mean=20, sd=10, bias = 10){
    #' Simulate human ratings of image quality. The ratings are randomly sampled from a normal distribution 
    #' and randomly distributed across subjects. To introduce a bias in the ratings of defaced images, 
    #' we add the bias to a predefined precentage of the ratings on original images. The percentage of scan 
    #' affected varies between raters. By assigning a different number to n_sub and n_rated, we can simulate
    #' missing data.
    #'
    #' Parameters
    #' ----------
    #' n_rated = nbr of subjects rated per rater
    #' n_sub = nbr of subjects in the dataset
    #' n_rater = nbr of raters
    #' perc_biased = vector (1 x n_rater) establishing the percentage of scans biased per rater
    #' file = filename to save dataset
    #' mean = mean of the normal ratings distribution
    #' sd = standard deviation of the normal ratings distribution
    #' bias = the number that is added to original ratings 
    #' labels = vector of string corresponding to ratings' labels
    #'
    #' Returns 
    #' -------
    #' df : dataframe containing the manual ratings
    
    #Set random seed
    set.seed(1234)

    #Generate normal ratings
    normal_ratings <- rnorm(n_rated*n_rater, mean=mean, sd=sd)

    #Add noise by truncation
    noisy_ratings <- trunc(normal_ratings)

    manual_original <- matrix(, nrow = n_sub, ncol = n_rater)
    manual_defaced <- matrix(, nrow = n_sub, ncol = n_rater)

    for (i in 1:n_rater) {
        #Each rater rates subjects picked at random
        ind_sub <- sample(1:n_sub, n_rated, replace = F)
        ratings_r <- noisy_ratings[seq((i-1)*n_rated+1,i*n_rated)]
        manual_original[ind_sub, i] <- ratings_r

        #To simulate a positive bias towards defaced data, we improve the ratings of a 
        #predefined percentage of the original scans
        ind_rat <- sample(1:n_rated, round(n_rated*perc_biased[i]/100), replace = F)
        ratings_biased <- ratings_r
        ratings_biased[ind_rat] <- ratings_biased[ind_rat] + bias
        #Clip values that are higher than the max of the original ratings
        ratings_biased[ratings_biased > max(ratings_r)] <- max(ratings_r)

        #Set the biased ratings as the ratings on the defaced condition
        manual_defaced[ind_sub, i] <- ratings_biased
    }

    manual_original_vec <- c(manual_original)
    manual_defaced_vec <- c(manual_defaced)

    defaced <- rep(c(0, 1), times = n_rater*n_sub)
    sub <- rep(rep(1:n_sub, each=2), times = n_rater)
    rater <- rep(1:n_rater, each=n_sub*2)

    #Convert to dataframe to use in regression
    df <- data.frame(subject = sub)
    df$defaced <- factor(defaced, levels = 0:1, labels = c("original", "defaced"))
    df$rater_id <- factor(rater, levels = 1:n_rater, labels = sprintf("rater%02d", 1:n_rater))
    df$rating <- c(rbind(manual_original_vec, manual_defaced_vec))

    return(df)
}

# Simulate normally distributed data with a bias
n_sub <- 185 #nbr of subjects available in the dataset
n_rated <- 185
n_rater <- 4 #nbr of raters
mean <- 20
sd <- 10
#Define for each rater the percentage of biased ratings
perc_biased <- c(20, 40, 50, 60)
bias <- 10

df <- simulate_normal_data(n_rated, n_sub, n_rater, perc_biased, mean=mean, sd=sd, bias=bias)
df$rating <- as.numeric(df$rating)

#Write dataframe to file
saveRDS(df, file = "simulated_normal_ratings.rds")

# Simulate normally distributed data without a bias
#Define for each rater the percentage of biased ratings
perc_biased <- c(10,10,10,10)
bias <- 1

df <- simulate_normal_data(n_rated, n_sub, n_rater, perc_biased, mean=mean, sd=sd, bias=bias)
df$rating <- as.numeric(df$rating)

#Write dataframe to file
saveRDS(df, file = "simulated_normal_nobias_ratings.rds")
