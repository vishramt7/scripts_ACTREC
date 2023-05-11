
library(maftools)

maf_files = list.files(path = "/home/vishram/vcf_to_maf", pattern = "*.filt.maf", full.names = TRUE)
mymaf = maftools::merge_mafs(mafs = maf_files, verbose = TRUE)
maftools::write.mafSummary(maf = mymaf, basename = "merged_maf")
