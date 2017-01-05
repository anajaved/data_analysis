setwd('~/Desktop')
children <- read.csv('children.csv', header = T, row.names = 1, check.names = F)
neonatal<- read.csv('neonatal.csv', header = T, row.names = 1, check.names = F)

summary(children)
qplot(x=children$`2008`, data=children, xlab = "Number of Deaths",
      ylab="Number of Countries" ,color=I('dark blue'), geom='freqpoly', 
      main="All Causes of Death in Children 1-59 months (per 1,000) in 2008") + 
  scale_x_continuous(breaks = seq(0,200,25))


qplot(x=neonatal$`2008`, data=neonatal, color=I('green'), 
      xlab = "Number of Deaths", ylab="Number of Countries", geom='freqpoly', 
      main="All Causes of Death in Newborns (per 1,000) in 2008") + 
  scale_x_continuous(breaks = seq(0,70,10))

