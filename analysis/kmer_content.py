import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class KmerContent(Module):
    """Class containing methods for Kmer-content module analysis.

    KmerContent is a subclass of Module class from QCModule and inherits clean_line
    """

    def __init__(self, fastqc, outdir):
        """Constructor for KmerContent object

        :param fastqc: FastQC input file
        :type fastqc: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(fastqc, outdir)
        self.name = 'Kmer Content'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df: pandas dataframe containing data for plotting.
        :rtype: pandas.DataFrame
        :raises: ValueError: module data not in FastQC format.
        """
        try:
            lines, columns = self.clean_lines()
            data = [(line[0], int(line[1]), float(line[2]), float(line[3]),
                     int(line[4])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Max Obs/Exp Position']
            # sort by count descending order and subset top 6 most freq sequences
            df = df.sort_values(by='Count', ascending=False)[:6]
            df = df.sort_index()
            return df

    def create_graph(self):
        """Plot graph for K-mer content and save as PNG file.

        :return: None
        :rtype: None
        """
        df = self.prep_data()
        # plot data
        sns.set_style()
        fig, ax = plt.subplots(1, 1)
        # if each kmer is found only at a single position
        # i.e. 1 entry per sequence plot as a bar plot, otherwise
        # plot a line plot
        if df['Sequence'].unique().size == df['Sequence'].size:
            sns.barplot(x=df['Max Obs/Exp Position'], y=df['Obs/Exp Max'],
                        hue=df['Sequence'])
        else:
            sns.lineplot(x=df['Max Obs/Exp Position'], y=df['Obs/Exp Max'],
                         hue=df['Sequence'])
        ax.set_title('Relative enrichment over read length')
        ax.legend(loc='best', facecolor='white')
        plt.yticks(np.arange(0, 101, 10))
        ax.set_xlabel('Position in read (bp)')
        ax.set_ylabel('')

        # Show the spine of the axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # hide top axis
        ax.spines['top'].set_visible(False)
        # save figure
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for K-mer content analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
