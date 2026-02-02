# GED - Gene Edit Distance

GED designed to assess the difficulty of tranforming a query DNA sequence to a target DNA sequence.

## Use Cases

Given a suspicious DNA sequences and a database of toxins, the GED algorithm detects toxin-related fragments, estimates a toxicity score, and reports toxin-like sequences that can be assembled.  
Optionally, GED can reorder and reorient detected fragments based on their locations in the target sequence, enabling analysis of obfuscated inputs where fragment order or orientation is altered.


## Blast definitions
As part of our algorithm we use the [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) framework.
**Hit** represents a sequence in a database that contains at least one segment similar to the query sequence.
The matching segments within the query and target sequences, exhibiting a high degree of similarity, are called **HSP**. Each HSP is assigned a score, reflecting the degree of similarity between the respective sequences.
Since our BLAST database consists toxin-related sequences, any hit may indicate the presence of potentially malicious elements within the query. The HSPs, in this context, represent fragments of the potential toxin that are aligned with the query sequence.


### Usage and Configurations
Blast requires [install BLAST](https://www.ncbi.nlm.nih.gov/books/NBK569861/) and dataset.
Several parameters and paths must be properly configured. These are our core configurations and the only way to change them will be in the [config.ini](code/ged_flow/config.ini) "gene-edit-distance/config.ini" file.

```python
[blast_paths]
blastn_path = ./blast/bin/blastn
blastx_path = ./blast/bin/blastx

[blast_parameters]
db = "/data/blastDB/Uniprot_ToxinVenom_DNA"
evalue = 0.01
```

Beside these configs there are several parameters you needed to define in your run of the algorithm.
These can be defined as default parameters in the config.ini file, but also you will be asked to configure as part of
the flow so make sure you know what they mean, if now you may always press skip and got to the default parameters:

## Configuration File

The file [config.ini](code/ged_flow/config.ini) contains all the configurable parameters for GED, devided into sections:

### blast_paths:

- ```blastn_path:``` Path to the installation of blastn.
- ```blastx_path:``` Path to the installation of blastx.

### blast_params:

- ```db:``` Name of db.
- ```evalue:``` E-value for blast.

### running_parameters:

- ```maximum_active_cut_points:``` Number of concatenation HSPs.

### calculation_weights:

- ```rm:``` Reward matching character.
- ```pmm``` Penalties for every mismatching character.
- ```pgo``` Penalties for gap openings.
- ```pgx``` Penalties for gap extensions.
- ```grp``` Gap removal probability.
- ```prm:``` Gap removal penalty that substitutes some gap opening and extension penalties in the target sequence.

### ged_results:
- ```ged_toxin_threshold``` GED score threshold for assigning the toxin flag.

## Dataset Information

GED is designed to analyze DNA sequences in FASTA format. The dataset should meet the following requirements:

### Database Requirements

GED utilizes a database of toxin sequences. We
use [Uniprot Toxin Venom DNA dataset](https://www.uniprot.org/help/Toxins) but it possible to use other datasets
like [NCBI BLAST databases](https://www.ncbi.nlm.nih.gov/books/NBK569850/). Ensure the database contains relevant toxin
data in a compatible format for the BLAST framework.

## Gene Editing Tools

In order to detect obfuscated toxins, GED looks for parts of the query that can be assembled together to new sequences.
It then checks if these new sequences are similar to known toxins.  
It does so using different modules that detect either cut points on the query sequence, or exons.

### Hypothetical Cut Point

This simple module is not biologically correct and is used to test the flow of our algorithm.  
It uses the data we get from the BLAST run on the query sequence, and returns the start and end of
the [HSPs](https://www.ncbi.nlm.nih.gov/books/NBK62051/) found as possible cutpoints.

In future work, there will be support for restriction enzymes, introns, and CRISPR.

# Running Example

## Input Arguments
The GED pipeline is executed from the command line and accepts the following arguments:
### Positional Arguments
* **`order_address` (FASTA file)**
The input files must be in standard FASTA format, containing nucleotide sequences.
Example to valid input is the file: [dataset_gapfuscation.fasta](/data/dataset_gapfuscation.fasta) that contains 44 sequences derived from 10 toxins.
The dataset includes 10 sequences obfuscated by introns and others modified by various restriction enzymes, providing a
robust testbed to evaluate the GED algorithm.
* **`result_path`**
Path to the location where the results will be saved.
### Optional Arguments
* **`--reorder`**
  Enable HSP-based reordering of sequences.
  When this flag is set, `--batch-size` **must** also be provided.

* **`--batch-size`**
  Batch size used during HSP-based reordering.
  This argument is **required** when `--reorder` is enabled and must be a positive integer.

## Example Usage

```bash
# Run GED on gapfuscation dataset
python /code/ged_flow/Main.py /data/dataset_gapfuscation.fasta /results/dataset_gapfuscation_results.csv

# Run GED on swapfuscation dataset
python /code/ged_flow/Main.py /data/dataset_swapfuscation.fasta /results/dataset_swapfuscation_results.csv --reorder --batch-size=1

# Run GED on recomfuscation dataset
python /code/ged_flow/Main.py /data/dataset_recomfuscation.fasta /results/dataset_recomfuscation_results.csv --reorder --batch-size=2
```

# Expected Output

For FASTA file, a corresponding CSV file (path: /results/dataset_results.csv), containing:

* Sequence Query: the query input.
* Sequence Description: description from the FASTA header. The decription in the provided dataset file include information about the obfuscated toxin and the obfuscation method.
* Sequence with gaps between HSPs: the query with gaps between the HSPs (the malicious parts of code). Base on this gaped sequence GED calculate score.
* Ged Score: score for the most toxic-like assembled sequence. A higher score indicates a more suspicious (i.e., potentially toxic) sequence.
* Toxin flag: Binary indicator of toxicity.  
  A value of 1 indicates the sequence is flagged as toxin (GED score above the threshold); 0 indicates benign.
* Time Running: Seconds runtime for processing that sequence.

# Defending Synthetic DNA Orders Against Splitting-Based Obfuscation
GED is first introduced in the article "Defending Synthetic DNA Orders Against Splitting-Based Obfuscation". The algorithm is explained in detail in Section 4.4, with Figure 3.d illustrating the GED workflow.
The process begins with [Collect HSPs per Hit](code/ged_flow/hit_collector/HitCollector.py), followed by [Generating Subsets Based on HSPs](code/ged_flow/SubsetGenerator.py). It then proceeds through the [cut point detection and merge](code/ged_flow/cutpoints_detection/HypotheticalCutPointsDetector.py) step, and finally selects the alignment with the best score.

As described in the article, GED uses two types of scoring penalties:
* [Gap removal penalty](code/ged_flow/score_calculator/ScoreByGapPenalty.py)
* [Adjusted alignment score](code/ged_flow/score_calculator/ScoreByAdjustedAlignment.py)