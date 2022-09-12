"""This module contains functionality for generating reports and visualising
Per base sequence content data from FastQC files."""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class PerBaseSeqContent(Module):
    """Class for Per base sequence content QC module."""
    def __init__(self, fastqc, outdir):
        """Constructor for PerBaseSeqContent objects

        :param fastqc: input FastQC file
        :type fastqc: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(fastqc, outdir)
        self.name = 'Per base sequence content'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df: pandas dataframe containing data for plotting
        :rtype: pandas.DataFrame
        :raises: ValueError: module data not in FastQC format
        """
        try:
            lines, columns = self.clean_lines()
            data = [(int(line[0]), float(line[1]), float(line[2]), float(line[3]),
                     float(line[4])) for line in lines[2:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Base']
            return df

    def create_graph(self):
        """Plot graph for Per base sequence content and save as PNG file.

        :return: None
        :rtype: None
        """
        df = self.prep_data()
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=df['Base'], y=df['G'], color='red', label='% G')
        sns.lineplot(x=df['Base'], y=df['A'], color='blue', label='% A')
        sns.lineplot(x=df['Base'], y=df['T'], color='green', label='% T')
        sns.lineplot(x=df['Base'], y=df['C'], color='black', label='% C')

        # configure legend
        ax.legend(loc='upper right', facecolor='white', frameon=True)
        # configure axes
        ax.set_title('Sequence content across all bases')
        ax.set_xlabel('Position in read (bp)')
        ax.set_ylabel('Proportion (%)')
        ax.set_xticks(df.index[::2])
        ax.axes.set_xlim(0)
        ax.set_yticks(np.arange(0, 101, 10))

        # configure spines of axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        ax.spines['top'].set_visible(False)

        # Save plot
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Per base sequence content analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
