import argparse
import re
import subprocess
import pandas as pd
import numpy as np
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime
import sys


class PipelineError(Exception):
    pass


def time_check(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print(f"finished in {(end_time - start_time).seconds} seconds")

    return wrapper


def breadth_calculation_in_target_regions(target_regions: str, sample: str) -> pd.DataFrame:
    command = f"bedtools coverage -a {target_regions} -b {sample}".strip().split(' ')
    temp_file = tempfile.NamedTemporaryFile()

    bedtools_coverage = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

    with open(temp_file.name, 'w')as temp:
        temp.write(bedtools_coverage.stdout)

    if not bedtools_coverage.stderr or re.findall(r"WARNING", bedtools_coverage.stderr):
        names = ["chr", "start", "end", "gene", "to_drop", "strand", "n_reads",
                 "n_bases_covered", "length_of_gene_fragment", "percent covered (%)"]
        df = pd.read_csv(temp_file, sep="\t", names=names).drop("to_drop", axis=1)

        return df

    raise PipelineError(
        f"an error occurred during the\n >>>> {' '.join(command)} <<<<\nERROR from {bedtools_coverage.stderr}"
    )


def depth_calculation_in_target_regions(target_regions: str, sample: str) -> pd.DataFrame:
    command = f"samtools bedcov {target_regions} {sample}".strip().split(' ')
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
             "percent covered (%)": []}

    for gene in df.gene.unique():
        percent = df[df.gene == gene]["percent covered (%)"].mean()
        cover["gene"].append(gene)
        cover["percent covered (%)"].append(round(percent * 100, 2))

    df = pd.DataFrame(cover).sort_values(by="gene", ascending=False) \
        .reset_index() \
        .drop("index", axis=1)

    return df


def depth_calculation_for_genes(df):
    dct = {"gene": [],
           "mean coverage depth (X)": []}

    for gene in np.unique(df.gene.values):
        dct["gene"].append(gene)
        dct["mean coverage depth (X)"].append(df[df.gene == gene].depth.sum() /
                                              (df[df.gene == gene].end - df[df.gene == gene].start).sum())

    result = pd.DataFrame(dct)

    result = result.sort_values(by="gene", ascending=False) \
        .reset_index() \
        .drop('index', axis=1)

    result["mean coverage depth (X)"] = result["mean coverage depth (X)"].apply(round)

    return result


def analysis(sample, target):
    save_name = sample.split("/")[-1].rstrip(".bam")

    depth = depth_calculation_in_target_regions(sample=sample, target_regions=target)
    depth = depth_calculation_for_genes(df=depth)

    breadth = breadth_calculation_in_target_regions(sample=sample, target_regions=target)
    breadth = breadth_calculation_for_genes(df=breadth)

    result = pd.concat([depth, breadth["percent covered (%)"]], axis=1) \
        .sort_values("percent covered (%)", ascending=False).reset_index(drop=True)

    result.to_excel(f"./gene_coverage/depth.{save_name}.xlsx", sheet_name=f"{save_name}", index=False)
    print(f"analysis of {sample} DONE\n"
          f"analysis results saved in {os.getcwd()}/gene_coverage/{save_name}.xlsx")

    graph(result, save_name)


def graph(df, save_name):
    def quality_setter(depth):
        if depth < 101:
            return "< 100"
        elif 100 < depth < 500:
            return "100-500"
        elif 501 < depth < 1000:
            return "500-1000"
        elif depth > 1001:
            return "> 1000"

    df["quality"] = df["mean coverage depth (X)"].apply(quality_setter)

    colors = ["forest green", "green", "amber", "red"]
    palette = sns.palplot(sns.xkcd_palette(colors))

    x = df.gene
    y = df["percent covered (%)"]

    figsize = (15, 6) if len(df) <= 51 else (30, 6)
    plt.figure(figsize=figsize)

    fig = sns.barplot(x=x, y=y, hue=df["quality"],
                      orient='v', palette=palette, hue_order=["> 1000", "500-1000", "100-500", "< 100"], dodge=False);
    plt.legend(title="Depth X", loc="upper right", bbox_to_anchor=(0.5, 0.5, 0.5, 0.5))
    loc, labels = plt.xticks()
    fig.set_xticklabels(labels, rotation=60);

    full_name = f"{os.path.abspath('./figs/')}/{save_name}.svg"
    plt.savefig(full_name, format="svg")
    print(f"graph saved in {full_name}/{save_name}.svg\n")


@time_check
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", help="Name of mapped sample file <BAM>", type=str)
    parser.add_argument("--target", help="Name of target regions file <BED>", type=str)
    parser.add_argument("--all", help="specify DIRECTORY and TARGET_NAME", metavar="directory primers",
                        nargs='*')
    args = parser.parse_args()

    if args.all:
        directory, target = args.all[0], args.all[1]
        print(f"MODE: all samples in directory\n"
              f"DIRECTORY: {os.getcwd()}/{directory}\n"
              f"TARGET REGIONS: {os.getcwd()}/{target}\n")

        for sample in os.listdir(f"{os.getcwd()}/{directory}"):
            sample = os.path.abspath(f"{directory}/{sample}")
            if not sample.endswith("bam"):
                continue

            analysis(sample=sample, target=target)
        return

    elif args.sample and args.target:
        print(f"MODE: one sample\n"
              f"SAMPLE: {args.sample}\n"
              f"TARGET: {args.target}\n")
    else:
        print(f"NO SPECIFIED INPUT SAMPLE OR TARGET, use -help")
        sys.exit()

    analysis(sample=args.sample, target=args.target)


if __name__ == '__main__':
    main()
