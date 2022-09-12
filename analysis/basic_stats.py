"""This module contains functionality for displaying data from Basic Statistics
from a FastQC file."""

from analysis.qc_module import Module


class BasicStatistics(Module):
    """Class for Basic Statistics QC module."""

    def __init__(self, infile, outdir):
        """Constructor for Basic Statistics objects

        :param infile: input FastQC file
        :type infile: str
        :param outdir: output directory
        :type outdir: str
        """
        super().__init__(infile, outdir)
        self.name = 'Basic Statistics'

    def display_stats(self):
        """Displays data from Basic Statistics QC module on command line.

        :return: None
        :rtype: None
        """
        stats = ''.join(self.lines)
        print(stats)

    # override abstract module method
    def module_output(self):
        """Generate output for Basic Statistics FastQC module.

        Tha abstract method is extended to display basic statistics on the
        command-line.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.display_stats()
        print('Completed.\n' + '-' * 80)
