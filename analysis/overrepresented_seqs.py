"""This module contains functionality for generating reports from
 Overrepresented sequence data from FastQC files.
"""
from analysis.qc_module import Module


class OverrepresentedSeqs(Module):
    """Class for analysing Overrepresented Sequences module data from FastQC"""

    def __init__(self, fastqc, outdir):
        """Constructor for overrepresented sequence objects

        :keyword: name: module name set to "Overrepresented sequences"
        :param fastqc:
        :type fastqc:
        :param outdir:
        :type outdir:
        """
        super().__init__(fastqc, outdir)
        self.name = 'Overrepresented sequences'

    def module_output(self):
        """Generate output for Overrepresented sequences analysis.

        :return: None
        :rtype: None
        """
        super().module_output()
        self.make_dir()
        self.create_report()
        self.create_filter_text()
        print('Completed.\n' + '-' * 80)
