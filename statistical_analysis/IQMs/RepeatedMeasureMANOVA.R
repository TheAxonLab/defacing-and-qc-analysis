iqms <- matrix(rnorm(1160*61),nrow=1160)
df <- as.data.frame(iqms)

df$subject <- seq(1,580)
df$defaced <- factor(c(rep(0,times=580),rep(1,times=580)), levels = 0:1, labels = c("original", "defaced"))

library(MANOVA.RM)
#Construct formula
dep_var <- ''
iqms_keys <- colnames(iqms_df)
#Remove non-iqms column names
iqms_keys <- iqms_keys[-c(1,length(iqms_keys))]
for (key in iqms_keys){
    dep_var <- paste(dep_var, sprintf('%s +',key))
}
dep_var = substring(dep_var,1, nchar(dep_var)-2)

(fmla <- as.formula(paste(paste(iqms_keys, collapse= "+"), " ~ defaced")))

fit <- multRM(fmla, data = iqms_df, subject = subject, within = defaced)
summary(fit)