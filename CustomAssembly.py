import sys, getopt

usage_prompt = """
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
"""
def invert(sequence):

        inverted_sequence = ''
        for char in sequence:
                if char == 'A':
                        inverted_sequence += 'T'
                elif char == 'C':
                        inverted_sequence += 'G'
                elif char == 'G':
                        inverted_sequence += 'C'
                elif char == 'T':
                        inverted_sequence += 'A'
        return inverted_sequence[::-1]


def process_assembly(infilepath, outfilepath, configfilepath, microbialfilepath, deletedfilepath):

        configfile = open(configfilepath, 'r')
        contig_directory = {}
        delete_list = []
        invert_list = []
        microbial_list = []

        deleting = False
        inverting = False
        combining = (False, '', '')
        separating_microbes = False
        
	for line in configfile:
                inputs = line.split(':', 1)
                operation = inputs[0]
                if operation == 'd':
                        for contig in inputs[1].rstrip().split(','):
                                delete_list.append(contig)
                elif operation == 'i':
                        for contig in inputs[1].rstrip().split(','):
                                invert_list.append(contig)
                elif operation == 'c':
                        combineinputs = inputs[1].rstrip().split(':', 1)
                        contig_name = combineinputs[0]
                        contig_directory[contig_name] = []
                        for contig in combineinputs[1].rstrip().split(','):
                                to_invert = False
                                if '*' in contig:
                                	contig = contig[:-1]
                                	to_invert = True
                                contig_directory[contig_name].append([[contig, to_invert], ''])
                elif operation == 'm':
                        for contig in inputs[1].rstrip().split(','):
                                microbial_list.append(contig)
        configfile.close()
        
	infile = open(infilepath, 'r')
        outfile = open(outfilepath, 'w')
        microbialfile = open(microbialfilepath, 'w')
	deletedfile = open(deletedfilepath, 'w')
        
	for line in infile:
                if '>' in line:
                        if len([contig for contig in delete_list if 'contig_' + contig + '_' in line or 'scaffold_' + contig + '_' in line]) > 0:
                                deleting = True
                                inverting = False
                                combining = (False, '', '')
                                separating_microbes = False
				deletedfile.write(line)
                        elif len([contig for contig in invert_list if 'contig_' + contig + '_' in line or 'scaffold_' + contig + '_' in line]) > 0:
                                deleting = False
                                inverting = True
                                combining = (False, '', '')
                                separating_microbes = False

                        elif len([contig for contig in microbial_list if 'contig_' + contig + '_' in line or 'scaffold_' + contig + '_' in line]) > 0:
                                deleting = False
                                inverting = False
                                combining = (False, '', '')
                                separating_microbes = True
                                microbialfile.write(line)

                        else:
                                combining = (False, '', '')
                                for combined_contig, contigs_list in contig_directory.items():
                                	contig_holder = [contig_list[0][0] for contig_list in contigs_list if 'contig_' + contig_list[0][0] + '_' in line or 'scaffold_' + contig_list[0][0] + '_' in line]
                                	if(len(contig_holder) > 0):
                                        	deleting = False
                                        	inverting = False
                                        	combining = (True, combined_contig, contig_holder[0])
                                       		separating_microbes = False
                                        	break
                                if combining[0] == True:
                                	continue

                                deleting = False
                                inverting = False
                                separating_microbes = False
                                outfile.write(line)
                
                elif deleting:
                        deletedfile.write(line)
                elif inverting:
                        outfile.write(invert(line))
                elif separating_microbes:
                        microbialfile.write(line)
                elif(combining[0]):
                        for contig_list in contig_directory[combining[1]]:
                                contig = contig_list[0]
                                if(contig[0] == combining[2]):
                                        contig_list[1] = line.rstrip()
                                        break
                else:
                        outfile.write(line)

        for combined_contig, contigs_list in contig_directory.items():
                outfile.write('>contig_' + combined_contig + '\n')
                for contig_list in contigs_list:
                        contig = contig_list[0]
                        sequence = contig_list[1]
                        if(contig[1]):
                                sequence = invert(sequence)
                        outfile.write(sequence + "N" * 100)
                outfile.write('\n')

        infile.close()
        outfile.close()
        microbialfile.close()

def main():
        infile = ''
        outfile = ''
        configfile = ''
        microbialfile = ''
	deletedfile = ''
        try:
                opts, args = getopt.getopt(sys.argv[1:], "hi:o:c:m:d:", ["help"])
        except getopt.GetoptError as err:
                print(usage_prompt)
                print(str(err))
        	return
	for opt, arg in opts:
                if opt in ('-h', '--help'):
                        print(usage_prompt)
                	return
		elif opt == '-i':
                        infile = arg
                elif opt == '-o':
                        outfile = arg
                elif opt == '-c':
                        configfile = arg
                elif opt == '-m':
                        microbialfile = arg
		elif opt == '-d':
			deletedfile = arg
		else:
			print(usage_prompt)
			return
        process_assembly(infile,outfile,configfile,microbialfile,deletedfile)



if __name__ == "__main__":
        main()


        

