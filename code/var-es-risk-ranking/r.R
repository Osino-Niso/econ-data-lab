# The same analytic model as python.py (returns in percent).
expected_return <- 2
sd_target <- 10

distributions <- function() {
  p <- 0.04; q <- 0.08; r <- 0.88; middle_c <- -5
  f <- function(bad_c) {
    good_c <- -(p * bad_c + q * middle_c) / r
    p*bad_c^2 + q*middle_c^2 + r*good_c^2 - sd_target^2
  }
  bad_c <- uniroot(f, c(-100, -10), tol=1e-12)$root
  good_c <- -(p * bad_c + q * middle_c) / r
  list(
    A=list(ret=c(-8,12), prob=c(0.50,0.50)),
    B=list(ret=c(bad_c,middle_c,good_c)+expected_return,prob=c(p,q,r))
  )
}

metrics <- function(ret, prob, alpha=0.95) {
  stopifnot(all(prob>=0), abs(sum(prob)-1)<1e-10, alpha>0, alpha<1)
  mu <- sum(ret*prob)
  sd <- sqrt(sum(prob*(ret-mu)^2))
  loss <- -ret
  asc <- order(loss)
  VaR <- loss[asc][which(cumsum(prob[asc])>=alpha-1e-12)[1]]
  rest <- 1-alpha
  weighted <- 0
  for (i in order(loss,decreasing=TRUE)) {
    used <- min(prob[i], rest)
    weighted <- weighted + used*loss[i]
    rest <- rest-used
    if (rest<1e-12) break
  }
  c(mean=mu,sd=sd,VaR95=VaR,ES95=weighted/(1-alpha))
}

x <- lapply(distributions(), function(d) metrics(d$ret,d$prob))
print(x)
stopifnot(all(abs(x$A-c(2,10,8,8))<1e-8))
stopifnot(all(abs(x$B-c(2,10,3,37.34538341093389))<1e-8))
stopifnot(x$A[['VaR95']]>x$B[['VaR95']])
stopifnot(x$A[['ES95']]<x$B[['ES95']])
cat('All checks passed.\n')
