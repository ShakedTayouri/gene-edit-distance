 # GED - Gene Edit Distance

GED designed to assess the difficulty of assembling a toxin from a DNA sequence.

1. [Use cases](#use-cases)
2. [Usage and configurations](#-usage-and-configurations)
    1. [Configuration file](#configuration-file)
3. [Dataset information](#dataset_information)
   1. [Input Format](#input_format)
   2. [Database Requirements](database_equirements)
4. [Gene editing tools](#gene-editing-tools)
    1. [Hypothetical](#Hypothetical)


 ## Use Cases
For a given suspicious DNA sequence and a database of toxins, our algorithm will return score of toxicity and  sequences similar to toxins from the DB that can be assembled.

 ## Usage and Configurations
As part of our algorithm we use the [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) framework.
After installing BLAST, several parameters and paths must be properly configured.
These are our core configurations and the only way to change them will be in the [config.ini](config.ini) file.

```python
[blast_paths]
blastn_path = /ncbi-blast-2.11.0+/bin/blastn
blastx_path = /ncbi-blast-2.11.0+/bin/blastx

[blast_parameters]
db = "Uniprot_ToxinVenom_DNA"
evalue = 0.01
```

Beside these configs there are several parameters you needed to define in your run of the algorithm.
These can be defined as default parameters in the config.ini file, but also you will be asked to configure as part of the flow so make sure you know what they mean, if now you may always press skip and got to the default parameters:


 ## Configuration File
The file [config.ini](config.ini) contains all the configurable parameters for GED, devided into sections:


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

 ### calculation_weights:
 - ```io_paths``` Fasta input path.
 - ```result``` Blast path file for the temp results.  
 
## Dataset Information
GED is designed to analyze DNA sequences in FASTA format. The dataset should meet the following requirements:
### Input Format
The input files must be in standard FASTA format, containing nucleotide sequences.
Example to valid input is the file: ```dataset.fasta``` that contains 54 sequences derived from 10 toxins. The dataset includes 10 sequences obfuscated by introns and others modified by various restriction enzymes, providing a robust testbed to evaluate the GED algorithm.
### Database Requirements
GED utilizes a database of toxin sequences (e.g., Uniprot_ToxinVenom_DNA). Ensure the database contains relevant toxin data in a compatible format for the BLAST framework.

## Gene Editing Tools
In order to detect obfuscated toxins, GED looks for parts of the query that can be assembled together to new sequences. It then checks if these new sequences are similar to known toxins.  
It does so using different modules that detect either cut points on the query sequence, or exons.

### Hypothetical
This simple module is not biologically correct and is used to test the flow of our algorithm.  
It uses the data we get from the BLAST run on the query sequence, and returns the start and end of the [HSPs](https://www.ncbi.nlm.nih.gov/books/NBK62051/) found as possible cutpoints.

In future work, there will be support for restriction enzymes, introns, and CRISPR.