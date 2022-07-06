simulate_data <- function(n_rated, n_sub, n_rater, perc_biased, file="", ratings_range=1:4, bias = 1, 
    labels = c("excluded", "poor", "good", "excellent")){
    #' Simulate human ratings of image quality. The ratings are randomly sampled from ratings_range 
    #' and randomly distributed across subjects. To introduce a bias in the ratings of defaced images, 
    #' we add the bias to a predefined precentage of the ratings on original images. The percentage of scan 
    #' affected varies between raters.
    #'
    #' Parameters
    #' ----------
    #' n_rated = nbr of subjects rated per rater
    #' n_sub = nbr of subjects in the dataset
    #' n_rater = nbr of raters
    #' perc_biased = vector (1 x n_rater) establishing the percentage of scans biased per rater
    #' file = filename to save dataset
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
        #random original ratings sampled from {1,2,3,4}
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
    df <- data.frame(sub = sub)
    df$defaced <- factor(defaced, levels = 0:1, labels = c("original", "defaced"))
    df$rater <- factor(rater, levels = 1:n_rater, labels = sprintf("rater%02d", 1:n_rater))
    df$ratings <- factor(c(rbind(manual_original_vec, manual_defaced_vec)), levels = ratings_range, labels = labels)

    #Write dataframe to file
    if (file != ""){
        saveRDS(df,file=file)
    }

    return(df)
}
