"""This module contains functionality for generating reports and visualising
Per base N content data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class PerBaseNContent(Module):
    """Class for Per base N content QC module."""
    def __init__(self, fastqc, outdir):
        """Constructor for Per base N content objects

        :param fastqc: input fastqc
        :type fastqc: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(fastqc, outdir)
        self.name = 'Per base N content'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df: pandas dataframe containing data for plotting
        :rtype: pandas.DataFrame
        :raises: ValueError: module data not in FastQC format
        """
        try:
            lines, columns = self.clean_lines()
            data = [(int(line[0]), float(line[1])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Base']
            return df

    def create_graph(self):
        """Plot graph for base N content and save as PNG file.

        :return: None
        :rtype: None
        """
        df = self.prep_data()
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.lineplot(x=df['Base'], y=df['N-Count'] * 100, label='%N',
                     color='red')
        ax.legend(facecolor='white')
        ax.set_title('N content across all bases')
        plt.xlim(df.index.min(), df.index.max())
        plt.xticks(df.index[::2])
        plt.yticks(np.arange(0, 101, 10))
        plt.ylim(0, 100)
        ax.set_xlabel('Position in read (bp)')
        ax.set_ylabel('Percentage of base calls (%)')
        # Show the spine of the axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # remove top axis
        ax.spines['top'].set_visible(False)
        # save figure
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Per base N content analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
