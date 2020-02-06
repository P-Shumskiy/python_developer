import io
import subprocess
import pandas as pd
import numpy as np
import tempfile


class PipelineError(Exception):
    pass


# 1) collect coverage statistics by bedtools genomecov -ibam sorted_bashirli.bam -bg > coverage_tab
# ADD TO PYTHON SUBPROCESS TODO

# 2) Plot raw coverage by pandas and seaborn TODO
# 3) Filter low coverage regions TODO
# 4) Plot new graphs TODO
# 5) How to obtain names of genes???? TODO
# 6) How to get regions from bed files with primers to count statistics only for these regions  TODO


# def take_genes_from_bed(name_of_bed: str):
#     names = ['chr', 'start', 'stop', 'gene', 'to_drop', 'strand']
#     df = pd.read_csv(name_of_bed, sep="\t",
#                      header=None,
#                      names=names,
#                      skiprows=1)
#
#     df = df.drop('to_drop', axis=1)
#     return np.unique(df.gene.values)
#
#
#
# df = pd.read_csv("coverage_tab", sep="\t", names=['sequence', 'start', 'stop', 'coverage'])

target_regions_ = "DHS-003Z.primers-150bp.bed"
patient_ = "sorted_bashirli.bam"
save_name = patient_.split(".bam")[0]


def depth_calculation_in_target_regions(target_regions: str = target_regions_,
                                        patient: str = patient_) -> pd.DataFrame:
    command = f"samtools bedcov {target_regions} {patient}".strip().split(' ')
    temp_file = tempfile.NamedTemporaryFile()

    samtools_bedcov = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

    with open(temp_file.name, 'w')as temp:
        temp.write(samtools_bedcov.stdout)

    if not samtools_bedcov.stderr:
        names = ["chr", "start", "end", "gene", "to_drop", "strand", "depth"]
        df = pd.read_csv(temp_file, sep="\t", names=names).drop("to_drop", axis=1)

        return df

    raise PipelineError(f"an error occurred during the\n >>>> {' '.join(command)} <<<<\nERROR from {samtools_bedcov.stderr}")


def depth_calculation_for_genes(df):
    dct = {"gene": [],
           "mean_cov_depth_X": []}

    for gene in np.unique(df.gene.values):
        dct["gene"].append(gene)
        dct["mean_cov_depth_X"].append(df[df.gene == gene].depth.sum() /
                                       (df[df.gene == gene].end - df[df.gene == gene].start).sum())

    result = pd.DataFrame(dct)

    result = result.sort_values('mean_cov_depth_X', ascending=False) \
        .reset_index() \
        .drop('index', axis=1)

    result["mean_cov_depth_X"] = result["mean_cov_depth_X"].apply(round)

    return result


if __name__ == '__main__':
    df = depth_calculation_in_target_regions()
    df = depth_calculation_for_genes(df=df)
    df.to_excel(f"./gene_coverage/{save_name}.xlsx", sheet_name=f"{save_name}", index=False)
    print(df.head())
