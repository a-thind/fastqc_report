"""FastQC Report Generator main script

Command-line script which uses various FastQC module classes to parse, analyse
and visualise various QC module data in FastQC input files.

:exception: FileNotFoundError: Input file does not exist in
:exception: ValueError: Input file does not have FastQC format.

.. py:functions: create_argparse: create ArgumentParser object.
.. py:function: process_args: parse command-line arguments.
.. py:function: main: entry point to program.

"""
import argparse
import sys


from analysis import basic_stats as m1
from analysis import base_seq_qlty as m2
from analysis import tile_seq_qlty as m3
from analysis import seq_qlty_scores as m4
from analysis import base_seq_content as m5
from analysis import seq_gc_content as m6
from analysis import base_n_content as m7
from analysis import seq_len_distribution as m8
from analysis import seq_duplication_levels as m9
from analysis import overrepresented_seqs as m10
from analysis import adapter_content as m11
from analysis import kmer_content as m12


def create_argparser():
    """
    .. py:function:: create_argparser()

    Creates parser for parsing command-line input for the program.

    :return: parser: ArgumentParser Object required for command-line parsing
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description='''FastQC Report Generator and
        QC module visualiser.''')
    # Add flags
    parser.add_argument('file', metavar='fastqc_file', type=str,
                        help='FastQC file for parsing')
    parser.add_argument('outdir', metavar='outdir', help='Output directory')
    parser.add_argument('m1', metavar='stats',
                        help='Basic statistics from FastQC')
    parser.add_argument('-m2', '--per_base_seq_qlty', action='store_true',
                        help='Per base sequence quality')
    parser.add_argument('-m3', '--per_tile_seq_qlty', action='store_true',
                        help='Per tile sequence quality')
    parser.add_argument('-m4', '--per_seq_qlty_scores', action='store_true',
                        help='Per sequence quality scores')
    parser.add_argument('-m5', '--per_base_seq_content', action='store_true',
                        help='Per base sequence content')
    parser.add_argument('-m6', '--per_sequence_gc_content', action='store_true',
                        help='Per sequence GC content')
    parser.add_argument('-m7', '--per_base_n_content', action='store_true',
                        help='Per base N content')
    parser.add_argument('-m8', '--seq_len_dist', action='store_true',
                        help='Sequence Length Distribution')
    parser.add_argument('-m9', '--seq_dup_levels', action='store_true',
                        help='Sequence Duplication Levels')
    parser.add_argument('-m10', '--overrep_seq', action='store_true',
                        help='Overrepresented sequences')
    parser.add_argument('-m11', '--adapter_content', action='store_true',
                        help='Adapter Content')
    parser.add_argument('-m12', '--kmer_content', action='store_true',
                        help='K-mer Content')
    parser.add_argument('-all', '--all_modules', action='store_true',
                        help='All QC analysis')
    return parser


def process_args(args):
    """
    .. py:function:: process_args(args)

    Parses command line arguments and triggers appropriate FastQC modular
    analysis.
    
    :param args: command-line arguments
    :type args: Namespace obj
    :return: None
    :rtype: None
    """
    # dict mapping optional module names with corresponding cml args and classes
    module_options = dict(
        per_base_seq_qlty=[args.per_base_seq_qlty, m2.PerBaseSeqQlty],
        per_tile_seq_qlty=[args.per_tile_seq_qlty, m3.PerTileSeqQlty],
        per_seq_qlty_scores=[args.per_seq_qlty_scores, m4.PerSeqQltyScores],
        per_base_seq_content=[args.per_base_seq_content, m5.PerBaseSeqContent],
        per_sequence_gc_content=[args.per_sequence_gc_content,
                                 m6.PerSeqGCContent],
        per_base_n_content=[args.per_base_n_content, m7.PerBaseNContent],
        seq_len_dist=[args.seq_len_dist, m8.SeqLengthDistribution],
        seq_dup_levels=[args.seq_dup_levels, m9.SeqDuplicationLevels],
        overrep_seq=[args.overrep_seq, m10.OverrepresentedSeqs],
        adapter_content=[args.adapter_content, m11.AdapterContent],
        kmer_content=[args.kmer_content, m12.KmerContent]
    )

    if args.file:
        if args.outdir:
            try:
                # generate basic stats using input file
                stats = m1.BasicStatistics(args.file, args.outdir)
                stats.module_output()
            except FileNotFoundError:
                # If input file is not found notify user and exit program
                print('Input file not found.')
                sys.exit(1)
            else:
                # Loop through module arg names and call appropriate classes
                if args.all_modules:
                    print('Generating reports and graphs for all remaining analysis...')
                    for name in module_options:
                        # If user provides 'all' arg then instantiate all module
                        # classes
                        module = module_options[name][1](args.file, args.outdir)
                        module.module_output()
                        # notify user all reports have been created
                        if name == "kmer_content":
                            print("All module reports have been created.")
                            sys.exit(0)

                else:
                    for name in module_options:
                        if module_options[name][0]:
                            # else if independent module args are provided then
                            # instantiate the respective module class
                            module = module_options[name][1](args.file, args.outdir)
                            module.module_output()


def main():
    """The entry point for the program."""
    parser = create_argparser()
    # parse command-line input
    args = parser.parse_args()
    process_args(args)


if __name__ == '__main__':
    main()
