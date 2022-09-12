"""This module contains functionality for generating reports and visualising
Sequence Length Distribution data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class SeqLengthDistribution(Module):
    """Class for Sequence Length Distribution QC module."""
    def __init__(self, infile, outdir):
        super().__init__(infile, outdir)
        self.name = 'Sequence Length Distribution'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df:
        :rtype: pandas.DataFrame
        :raises: ValueError: module data not in FastQC format
        """
        try:
            lines, columns = self.clean_lines()
            data = [(line[0], float(line[1])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Length']
            return df

    def create_graph(self):
        """Plot graph for Sequence Length Distribution and save as PNG file.

        :return: None
        :rtype: None
        """
        df = self.prep_data()
        # plot graph
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(1, 1)
        # if number of lengths is 1 or less plot a bar plot
        if df.index.size <= 1:
            sns.barplot(x=df.index, y=df['Count'])
        sns.lineplot(x=df['Length'], y=df['Count'], color='red')
        ax.set_title('Distribution of sequence lengths over all sequences')
        ax.set_xlabel('Sequence Length (bp)')
        # turn off scientific notation on y axis
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        # show spines of axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # hide top axis
        ax.spines['top'].set_visible(False)
        # save fig
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Sequence length distribution analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
