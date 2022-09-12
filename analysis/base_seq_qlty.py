"""This module contains functionality for generating reports and visualising
Per tile sequence quality data from FastQC files.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.qc_module import Module


class PerBaseSeqQlty(Module):
    """Class for storing and analysing Per base sequence quality FastQC module
    data.
    """

    def __init__(self, fastqc, outdir):
        """Constructor for Per base sequence quality object

        :param fastqc: input FastQC file
        :type fastqc: str
        :param outdir: output directory for module reports and graphs
        :type outdir: str
        """
        super().__init__(fastqc, outdir)
        self.name = 'Per base sequence quality'

    def get_encoding(self):
        """Extract encoding information from FastQC file.

        :return: encoding: type of quality score encoding
        :rtype: str
        """
        encoding = ''
        fr = open(self.infile, 'r')
        for line in fr.readlines():
            if line.startswith('Encoding'):
                encoding = line.strip('\n').split('\t')[1]
                break
        return encoding

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df - DataFrame containing data for module
        :rtype: pandas.DataFrame
        :raises: ValueError: if data not in FastQC format
        """
        try:
            lines, columns = self.clean_lines()
            # cast data in each line to appropriate types
            data = (
                (int(line[0]), float(line[1]), float(line[2]), float(line[3]),
                 float(line[4]), float(line[5]), float(line[6]))
                for line in lines[2:])
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            # exclude module header and column lines
            df = pd.DataFrame(data, columns=columns)
            df.index = df['Base']
            return df

    def create_graph(self):
        """Plot graph for Per base sequence quality and save as PNG file.

        :return: None
        :rtype: None
        """
        # get dataframe from process data function
        df = self.prep_data()
        # Plot boxplots
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(12, 6))

        # extract boxplot stats from dataframe to be used for plotting
        bxpstats = [
            {"label": i, "med": df.loc[i, 'Median'],
             "q1": df.loc[i, 'Lower Quartile'],
             "q3": df.loc[i, 'Upper Quartile'],
             "whislo": df.loc[i, '10th Percentile'],
             "whishi": df.loc[i, '90th Percentile']} for i in df.Base]
        # create horizontal spans on figure to categorise score quality
        ax.axhspan(28, df['90th Percentile'].max() + 2, color='green',
                   alpha=0.3)
        ax.axhspan(20, 28, color='yellow', alpha=0.2)
        ax.axhspan(0, 20, color='red', alpha=0.2)

        # style boxplot properties
        boxprops = dict(facecolor='yellow')
        medianprops = dict(linestyle='-', linewidth=1.0, color='red')
        ax.bxp(bxpstats, boxprops=boxprops, medianprops=medianprops,
               showbox=True, showfliers=False, patch_artist=True)
        ax.plot(df['Mean'], linewidth=1.0, color='blue', zorder=5)

        # set plot title and axes labels
        ax.set_title(
            f'Quality scores across all bases ({self.get_encoding()} encoding)')
        ax.set_xlabel('Position in read (bp)')
        ax.set_ylabel('Quality score (Phred)')
        plt.xticks(fontsize=7)
        plt.yticks(np.arange(0, df['90th Percentile'].max() + 2, 2), fontsize=7)
        plt.ylim(0, df['90th Percentile'].max() + 1)
        # show spines of axes
        for s in ['left', 'bottom']:
            ax.spines[s].set_linewidth(1)
            ax.spines[s].set_color('black')

        # Don't show top axis to prevent overlap
        ax.spines['top'].set_visible(False)
        # save figure
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Per base sequence quality analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
