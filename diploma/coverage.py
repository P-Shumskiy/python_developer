import argparse
import subprocess
import pandas as pd
import numpy as np
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime


class PipelineError(Exception):
    pass


parser = argparse.ArgumentParser()
parser.add_argument("--sample", help="Name of mapped sample file <BAM>", type=str)
parser.add_argument("--capture", help="Name of target regions file <BED>", type=str)
args = parser.parse_args()

if args.sample:
    print(f"SAMPLE: {args.sample}")
else:
    print(f"NO SPECIFIED INPUT SAMPLE, USING DEFAULT")
if args.capture:
    print(f"CAPTURE: {args.capture}")
else:
    print(f"NO SPECIFIED INPUT CAPTURE, USING DEFAULT")

target_regions_ = args.capture or "DHS-003Z.primers-150bp.bed"
sample = args.sample or "sorted_bashirli.bam"
save_name = sample.split(".bam")[0]


def time_check(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print(f"finished in {(end_time - start_time).seconds} seconds")

    return wrapper


def breadth_calculation_in_target_regions(target_regions: str = target_regions_,
                                          patient: str = sample) -> pd.DataFrame:  # TODO need to be refactored as
    command = f"samtools coverage -a {patient} -b {target_regions}".strip().split(' ')
    temp_file = tempfile.NamedTemporaryFile()

    samtools_coverage = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

    with open(temp_file.name, 'w')as temp:
        temp.write(samtools_coverage.stdout)

    if not samtools_coverage.stderr:
        names = ["chr", "start", "end", "gene", "to_drop", "starnd", "n_reads",
                 "n_bases_covered", "length_of_gene_fragment", "percent_covered"]
        df = pd.read_csv(temp_file, sep="\t", names=names).drop("to_drop", axis=1)

        return df

    raise PipelineError


def depth_calculation_in_target_regions(target_regions: str = target_regions_,
                                        patient: str = sample) -> pd.DataFrame:
    command = f"samtools bedcov {target_regions} {patient}".strip().split(' ')
    temp_file = tempfile.NamedTemporaryFile()

    samtools_bedcov = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

    with open(temp_file.name, 'w')as temp:
        temp.write(samtools_bedcov.stdout)

    if not samtools_bedcov.stderr:
        names = ["chr", "start", "end", "gene", "to_drop", "strand", "depth"]
        df = pd.read_csv(temp_file, sep="\t", names=names).drop("to_drop", axis=1)

        return df

    raise PipelineError(
        f"an error occurred during the\n >>>> {' '.join(command)} <<<<\nERROR from {samtools_bedcov.stderr}")


def breadth_calculation_for_genes(df):
    cover = {"gene": [],
             "percent_covered": []}

    for gene in df.gene.unique():
        percent = df[df.gene == gene].percent_covered.mean()
        cover["gene"].append(gene)
        cover["percent_covered"].append(round(percent * 100, 2))

    df = pd.DataFrame(cover).sort_values(by="percent_covered", ascending=False) \
        .reset_index() \
        .drop("index", axis=1)

    return df


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


@time_check
def main():
    depth = depth_calculation_in_target_regions()
    depth = depth_calculation_for_genes(df=depth)

    breadth = breadth_calculation_in_target_regions()
    breadth = breadth_calculation_for_genes(df=breadth)

    # result = depth.join(on=depth, how=inner)

    depth.to_excel(f"./gene_coverage/depth.{save_name}.xlsx", sheet_name=f"{save_name}", index=False)
    print(f"saved to {os.getcwd()}/gene_coverage/{save_name}.xlsx")
    breadth.to_excel(f"./gene_coverage/breadth.{save_name}.xlsx", sheet_name=f"{save_name}", index=False)
    print(f"saved to {os.getcwd()}/gene_coverage/{save_name}.xlsx")

    barplot_for_genes = sns.barplot(depth.gene, depth.mean_cov_depth_X)  # TODO pretty barplot
    fig = barplot_for_genes.get_figure()
    fig.savefig(f"figures/{save_name}.png")
    print(f"saved to {os.getcwd()}/figures/{save_name}.png")


if __name__ == '__main__':
    main()
