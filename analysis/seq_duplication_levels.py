"""This module contains functionality for generating reports and visualising
Sequence Duplication Levels data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class SeqDuplicationLevels(Module):
    """Class for Sequence Duplication Levels QC module."""
    def __init__(self, infile, outdir):
        """Contructor method for Sequence Duplication Levels objects.

        :param infile: input FastQC file
        :type infile: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(infile, outdir)
        self.name = 'Sequence Duplication Levels'

    def clean_lines(self):
        """Clean lines for Sequence duplication levels module.

        :return: lines, columns, total_perc
        :rtype: tuple(list, list, list)
        """
        lines = [line.strip('\n').split('\t') for line in self.lines]
        total_perc = [elem.strip('#') if elem.startswith('#') else float(elem)
                      for elem in lines[1]]
        columns = [elem.strip('#') if elem.startswith('#') else elem for elem in
                   lines[2]]
        return lines, columns, total_perc

    def prep_data(self):
        """Process data into appropriate types and create dataframe and
        total percentages list

        :returns: df, total_perc: dataframe and total percentages for plotting
        :rtype: tuple(pandas.DataFrame, list)
        """
        try:
            lines, columns, total_perc = self.clean_lines()
            data = [(line[0], float(line[1]), float(line[2])) for line in lines[3:]]
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            df = pd.DataFrame(data=data, columns=columns)
            df.index = df['Duplication Level']
            return df, total_perc

    def create_graph(self):
        """Plot graph for Sequence duplication and save as PNG file.

        :return:
        :rtype:
        """
        df, total_perc = self.prep_data()

        # plot figure
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.lineplot(x=df['Duplication Level'],
                     y=df['Percentage of deduplicated'],
                     color='red', label='% Deduplicated sequences')
        sns.lineplot(x=df['Duplication Level'], y=df['Percentage of total'],
                     color='blue', label='% Total sequences')
        ax.set_title(
            f'Percent of seqs remaining if deduplicated {total_perc[1]:.2f}%',
            fontsize=12)
        ax.set_xlabel('Sequence Duplication Level', fontsize=10)
        ax.set_ylabel('Total Library (%)')
        plt.xticks(fontsize=8)
        plt.yticks(np.arange(0, 101, 10), fontsize=8)
        ax.legend(loc='best', facecolor='white')
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
        print(f'Graph file generated for {self.name}')

    def module_output(self):
        """Generate output for Sequence Duplication Levels analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
