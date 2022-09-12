"""This module contains functionality for generating reports and visualising
Per tile sequence quality data from FastQC files.
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis.qc_module import Module


class PerTileSeqQlty(Module):
    """Class for per tile sequence quality QC module."""

    def __init__(self, infile, outdir):
        """Constructor for Per tile sequence quality objects.

        Objects from this class inherit fastqc input file and output directory
        names from QCModule superclass, using QCModule constructor.

        :param infile: input FastQC file
        :type infile: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(infile, outdir)
        self.name = 'Per tile sequence quality'

    def prep_data(self):
        """Process data into appropriate types and create dataframe.

        :return: df: pandas dataframe containing data for plotting
        :rtype: pandas.DataFrame
        :raises: ValueError: module data not in FastQC format
        """
        try:
            lines, columns = self.clean_lines()
            # cast data in each line to appropriate type
            data = ((int(line[0]), int(line[1]), float(line[2])) for line in lines[2:])
        except ValueError:
            print('Module data is not in FastQC format.')
            sys.exit(1)
        else:
            # exclude module header and column lines
            df = pd.DataFrame(data, columns=columns)
            # create pivot table
            df = df.pivot('Tile', 'Base', 'Mean')
            df = df.sort_values(by='Tile', ascending=False)
            return df

    def create_graph(self):
        """Plot graph for Per tile sequence quality and save as PNG file.

        :return: None
        :rtype: None
        """
        df = self.prep_data()
        # set up figure
        fig, ax = plt.subplots(figsize=(12, 6))
        # generate custom diverging palette
        sns.heatmap(df, cmap='RdBu', cbar=False)
        plt.title('Quality per tile', fontsize=10)
        ax.set_xlabel('Position in read (bp)', fontsize=8)
        ax.set_ylabel('Tile', fontsize=8)
        plt.xticks(np.arange(df.columns.size), df.columns, rotation=0,
                   fontsize=6, ha='left')
        ax.set_yticklabels(df.index[::4], fontsize=6)
        ax.yaxis.set_ticks_position('none')
        ax.xaxis.set_ticks_position('none')

        # save figure as png
        path = os.path.join(self.dir_name, 'graph.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Graph file generated for {self.name}.')

    def module_output(self):
        """Generate output for Per tile sequence quality analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        self.create_graph()
        print('Completed.\n' + '-' * 80)
