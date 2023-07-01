library(maftools)

laml.maf <- "mergedAnnov_maftools.maf.gz"
laml = read.maf(maf = laml.maf)

write.mafSummary(maf = laml, basename = 'laml')

jpeg("/home/vishram/vcf_to_maf/oncoplot.jpg",units="in", width=10, height=6, res=600)
oncoplot(maf = laml)
dev.off ()
