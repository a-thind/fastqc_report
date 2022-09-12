"""This module contains functionality for generating reports and visualising
Per sequence GC content data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class PerSeqGCContent(Module):
    """Class for Per sequence GC content QC module."""

    def __init__(self, fastqc, outdir):
        super().__init__(fastqc, outdir)
        self.name = 'Per sequence GC content'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df: pandas dataframe containing data for plotting
        :rtype: pandas.DataFrame
        :raises: ValueError: module data not in FastQC format
        """
        try:
            lines, columns = self.clean_lines()
            data = [(float(line[0]), float(line[1])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['GC Content']
        return df

    def create_graph(self):
        """Plot graph for Per Sequence GC content and save as PNG file.

        :return: None
        :rtype: None
        """
        from scipy.stats import norm
        df = self.prep_data()

        # Fit Gaussian distribution and plot
        # get mean and sd for counts
        x = df['GC Content']
        freq = df['Count']
        mean = (freq * x).sum() / freq.sum()
        dev = freq * (x - mean) ** 2
        sd = np.sqrt(dev.sum() / (freq.sum() - 1))

        # Generate normal distribution with computed mean and sd
        fit = norm.pdf(x, mean, sd)

        # Plot the data
        sns.set_style('darkgrid')
        # Plot the measured data
        fig, ax = plt.subplots(1, 1)
        sns.lineplot(x=x, y=freq, color='red', label='GC count per read')
        # Plot modelled normal distribution for GC content
        sns.lineplot(x=x, y=fit / fit.sum() * freq.sum(), color='blue',
                     label='Theoretical distribution')
        # Set legend
        ax.legend(loc='best', facecolor='white')
        # configure axes
        # turn off scientific notation on y-axis
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        ax.set_title('GC distribution over all sequences')
        plt.xlim(x.min(), x.max())
        ax.set_ylim(0)
        ax.set_xticks(np.arange(0, 101, 5))
        ax.set_xlabel('Mean GC content (%)')
        ax.set_ylabel('Count')
        # Show the spine of the axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # remove top axis from display
        ax.spines['top'].set_visible(False)
        # Save figure
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}')

    def module_output(self):
        """Generate output for Per sequence GC content analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
