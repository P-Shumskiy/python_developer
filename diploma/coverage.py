import subprocess
import pandas as pd
import numpy as np


# 1) collect coverage statistics by  bedtools genomecov -ibam sorted_bashirli.bam -bg > coverage_tab
# ADD TO PYTHON SUBPROCESS TODO

# 2) Plot raw coverage by pandas and seaborn TODO
# 3) Filter low coverage regions TODO
# 4) Plot new graphs TODO
# 5) How to obtain names of genes???? TODO
# 6) How to get regions from bed files with primers to count statistics only for these regions  TODO


def take_genes_from_bed(name_of_bed: str):
    names = ['chr', 'start', 'stop', 'gene', 'to_drop', 'strand']
    df = pd.read_csv(name_of_bed, sep="\t",
                     header=None,
                     names=names,
                     skiprows=1)

    df = df.drop('to_drop', axis=1)
    return np.unique(df.gene.values)



df = pd.read_csv("coverage_tab", sep="\t", names=['sequence', 'start', 'stop', 'coverage'])
