# amr_pipeline

## 1. We start with raw fastq files (pair end)
- From sequencing center
- We need to do quality check. Criteria are length (if less than 75bp), remove bases of low quality, remove adapters. These can result in wrong interpretation downstream
- Remove reads that map to the human genome
- Output: quality controlled fastq

## 2. Run Metaphlan2 to get relative abundance of taxonomy
- Input: quality controlled fastq
- Estimating taxonomy abundance from metagenomes.
- Cheng has a script to parse the Metaplhan outputs into different level and 'OTU' table
- Output: 'OTU' table

## 3. Antibiotic resistance inference
- Input: quality controlled fastq + reference database in fasta file (from SARG); metadata is a text file (ask Anni)
- ShortBRED quantifies antibiotic resistance gene abundance based on hits to unique marker sequences
- Metadata connects variants to genes to antibiotic class
- Output here is a ShortBRED quantification file that gives you normalized abundance (reads per kilobase million) --> can be converted into a table


