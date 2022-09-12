"""This module contains functionality for generating reports and visualising
Adapter content data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class AdapterContent(Module):
    """Class for analysis of Adapter Content module data from FastQC."""

    def __init__(self, fastqc, outdir):
        """
        Constructor for Adaptor Content objects

        :param fastqc: input fastqc file
        :type fastqc: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(fastqc, outdir)
        self.name = 'Adapter Content'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df: pandas dataframe containing data for plotting
        :rtype: pandas.DataFrame
        :raises::ValueError: module data not in FastQC format
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
            df.index = df['Position']
        return df

    def create_graph(self):
        """Plot graph for Adapter content and save as PNG file.

        :return: None
        :rtype: None
        """
        df = self.prep_data()
        # plot graph
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=df['Position'],
                     y=df['Illumina Universal Adapter'].cumsum(),
                     label='Illumina Universal Adapter', color='red')

        sns.lineplot(x=df['Position'],
                     y=df['Illumina Small RNA Adapter'].cumsum(),
                     label='Illumina Small RNA Adapter', color='blue')
        sns.lineplot(x=df['Position'],
                     y=df['Nextera Transposase Sequence'].cumsum(),
                     label='Nextera Transposase Sequence', color='black')
        sns.lineplot(x=df['Position'], y=df['SOLID Small RNA Adapter'].cumsum(),
                     label='SOLID Small RNA Adapter', color='pink')

        ax.legend(loc='best', facecolor='white')
        ax.set_xlabel('Position in read (bp)')
        ax.set_ylabel('Cumulative proportion of library (%)')
        ax.set_title('% Adapter')
        plt.yticks(np.arange(0, 101, 10))
        ax.axes.set_xlim(0)
        # format tick lables on x axis so first 9 base are shown
        # then intervals of 2
        tick_labels = np.concatenate([np.arange(1, 10),
                                      df['Position'][10::2].values])
        plt.xticks(tick_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        # Show the spine of the axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')
        # remove top axis
        ax.spines['top'].set_visible(False)
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Adapter content analysis.

        :return: None
        :rtype:
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
