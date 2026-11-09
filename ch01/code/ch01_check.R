# Chapter 1 independent cross-check in base R (no packages needed).
# Reads the data written by ch01_replicate.py and writes ../output/results_R.csv
# Run:  Rscript ch01_check.R   (from the code folder)
skew <- function(a) { d <- a - mean(a); mean(d^3) / mean(d^2)^1.5 }
data <- "../data/"; out <- "../output/"
perf <- read.csv(paste0(data, "performance.csv"))
scc  <- read.csv(paste0(data, "scc.csv"))$scc_thousand_per_ml
x <- scc
r <- list()
r$milk_mean <- mean(perf$milk_305d_kg)
r$milk_sd   <- sd(perf$milk_305d_kg)
hm <- tapply(perf$milk_305d_kg, perf$herd, mean)
r$herd_A_mean <- hm[["A"]]; r$herd_B_mean <- hm[["B"]]; r$herd_C_mean <- hm[["C"]]
r$herd_season_cells <- nrow(unique(perf[, c("herd", "season")]))
r$herd_year_cells <- nrow(unique(perf[, c("herd", "year")]))
r$herd_year_season_cells <- nrow(unique(perf[, c("herd", "year", "season")]))
for (nm in c("original", "sqrt", "ln")) {
  a <- switch(nm, original = x, sqrt = sqrt(x), ln = log(x))
  r[[paste0("scc_", nm, "_mean")]] <- mean(a)
  r[[paste0("scc_", nm, "_median")]] <- median(a)
  r[[paste0("scc_", nm, "_sd")]] <- sd(a)
  r[[paste0("scc_", nm, "_skew")]] <- skew(a)
}
r$z_820_original <- (820 - mean(x)) / sd(x)
r$z_380_original <- (380 - mean(x)) / sd(x)
r$z_820_ln <- (log(820) - mean(log(x))) / sd(log(x))
r$z_380_ln <- (log(380) - mean(log(x))) / sd(log(x))
r$geometric_mean <- exp(mean(log(x)))
r$prob1_arith <- mean(c(50, 100, 200)); r$prob1_geo <- exp(mean(log(c(50, 100, 200))))
r$prob2_diff <- (asin(sqrt(0.64)) - asin(sqrt(0.36))) * 180 / pi
write.csv(data.frame(name = names(r), value = unlist(r)), paste0(out, "results_R.csv"), row.names = FALSE)
cat("R cross-check written\n")

# Added checks: spreadsheet-style skewness and Worked Example 1.1
adj <- function(a) { n <- length(a); skew(a) * sqrt(n * (n - 1)) / (n - 2) }
r2 <- list(scc_original_skew_spreadsheet = adj(x), scc_ln_skew_spreadsheet = adj(log(x)),
           we1_mean = mean(c(40, 80, 160, 320)), we1_sd = sd(c(40, 80, 160, 320)),
           we1_ln_mean = mean(log(c(40, 80, 160, 320))), we1_ln_sd = sd(log(c(40, 80, 160, 320))),
           we1_geo = exp(mean(log(c(40, 80, 160, 320)))))
write.table(data.frame(name = names(r2), value = unlist(r2)), paste0(out, "results_R.csv"),
            sep = ",", row.names = FALSE, col.names = FALSE, append = TRUE, quote = TRUE)
