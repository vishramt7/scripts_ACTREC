library(pROC)

data3 <- read.table("C:/Users/Hematopath/Documents/Vishram/IDH2_VAF_cases_vs_controls_cleaned_inv.txt", header = FALSE)
rocobj3 <- roc(data3[,2], data3[,1], print.auc=TRUE)
#print (data3[,2])
sensitivity3 <- coords(rocobj3, x = "all", ret=c("sensitivity"))
specificity3 <- coords(rocobj3, x = "all", ret=c("specificity"))
median_sens_OB <- (median(sensitivity3$sensitivity))
median_spec_OB <- (median(specificity3$specificity))

jpeg("C:/Users/Hematopath/Documents/Vishram/IDH2_VAF_cases_vs_controls_cleaned_inv.jpg",units="in", width=4, height=4, res=600)
plot(rocobj3, print.auc=TRUE,print.auc.x = 0.5,print.auc.y = 0.3, col="blue")
legend("bottomright", legend=c("IDH2_VAF"), col=c("blue"),lty=1:1,cex=1.0)
dev.off()
print(median_sens_OB)
print(median_spec_OB)