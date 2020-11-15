# CustomAssembly
This program is a Python script used to reorganize and filter contigs in a [Flye](https://github.com/fenderglass/Flye) DNA assembly.

# Overview
This tool is designed to take in a FASTA file containing a [Flye](https://github.com/fenderglass/Flye) assembly as input, 
and use a configuration file to process and filter the contigs into three output files; 
a main output file, a second output file containing specified microbial contigs, 
and a third output file containing specified DNA contigs to be removed from the assembly.

# Usage

### Input and ouput FASTA file formats
For the FASTA input of CustomAssembly, the sequence names must be in the format of 
"contig_{sequence name}" or "scaffold_{sequence name}" in order to properly be processed.
As well, the FASTA outputs of CustomAssembly will output the sequences name as "contig_{sequence name}".

### Running the program
Usage of `CustomAssembly` is as follows:

	python CustomAssembly.py [-h] -i <input> -o <output> -c <config> -m <microbial> -d <deleted>
		
		<input>
			input file in FASTA format (with sequence naming format of "contig_<sequence name>") 
			containing sequences that will be processed
		<output>
			output file in FASTA format containing processed sequences,
			excluding sequences that were specified to be filtered out
		<config>
			input file in .config configuration file format (specified below)
		<microbial>
			output file in FASTA format containing microbial sequences 
			that were specified to be filtered out
		<deleted>
			output file in FASTA format containing other (non-microbial) sequences
			that were specified to be filtered out
	options:
		-h, --help
			prints out the above usage statement

While you do not have to specify microbial or other sequences to be removed, you must still provide file paths
to all possible output files (include the -m and -d arguments) for CustomAssembly to run properly.

### Configuration file format
The configuration file should be formatted as a .config file that specifies five possible operations 
that can be done on the assembly, each on a new line, and which sequences should be included in the operation.

The operations are as follows:

	d: delete - all specified contigs are removed from the main output file and outputted to the <deleted> file.
	    format: d:<contig name>,<contig name>,...
    i: invert - all specified contigs get inverted (sequence gets reversed and inverted by base pair)
        format: i:<contig name>,<contig name>,...
    c: combine - all specified contigs get combined into one large sequence with name <new_contig_name> in the given order, adding * to end of <contig name> indicates to invert that specific contig
        format: c:<new_contig_name>:<contig name>,<contig name>*,...
    m: microbial - all specified contigs are removed from the main output file outputted to the <microbial> file.
        format: m:<contig name>,<contig name>,...

An example configuartion file would be:
	
	d:1,5,8,15
	i:4,6
	c:combined:3,10*,18*,22
	m:19,20

The configuration file does not need to include specifications for all operations, and you can have multiple lines
for the same operations (for example, you can have multiple combined sequences, can specify sequences to be deleted over multiple lines).

# Disclaimer
This tool was primarily used as an internal tool to process D. Melanogaster Flye assemblies with sizes 
in the hundreds of megabases, and thus has only been tested with FASTA inputs with size 130-150MB. 
Feel free to modify and/or build upon this code to fit your specific usage and needs.

# License
This porgram is licensed under the Apache License Version 2.0. A copy of the Apache 2.0 license can be found [here](https://github.com/AvivBenchorin/CustomAssembly/blob/main/LICENSE).
