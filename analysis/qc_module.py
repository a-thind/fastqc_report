"""This module provides generic I/O functionality for all FastQC module
subclasses in the analysis package."""
import os
import sys
from abc import ABC, abstractmethod


class Module(ABC):
    """Abstract class for a FastQC analysis module providing basic parsing and
    file I/O functionality for all FastQC modular analyses.
    """

    def __init__(self, infile, outdir):
        """Constructor for generic Module object.

        :param infile: input FastQC file
        :type infile: str
        :param outdir: output directory for generated reports and graphs
        :type outdir: str
        """
        self.lines = []
        self.name = ''
        self.dir_name = ''  # basic stats doesn't have this
        self.infile = infile
        self.outdir = outdir

    def parse_text(self):
        """General parser for parsing FastQC Modules from input FastQC file.

        :return: None
        :rtype: None
        :raises: ValueError: if the QC module is missing from input file.
        """
        with open(self.infile, 'r') as f:
            for line in f:
                if line.startswith(f'>>{self.name}'):
                    self.lines.append(line)
                    for modline in f:
                        if not modline.startswith('>>END'):
                            self.lines.append(modline)
                        else:
                            break
        # check the module is in the file
        try:
            # if module is absent from file the lines attribute will be empty
            if not len(self.lines):
                raise ValueError
        except ValueError:
            print(f'Module "{self.name}" missing from input file.')
            sys.exit(1)

    def make_dir(self):
        """Create directory for the QC module in output directory.

        :return: None
        :rtype: None
        """
        # remove whitespace from module dir name
        dir_name = self.name.replace(' ', '_')
        # append module dir name to outdir
        self.dir_name = os.path.join(self.outdir, dir_name)
        # check whether module directory exists
        if not os.path.exists(self.dir_name):
            # if it doesn't exist create new directory
            os.makedirs(self.dir_name)
        # if the module directory exists then exit the function ask user if
        # they want to continue
        else:
            while True:
                # warn user of potential file overwriting
                answer = input(
                    f'WARNING: {self.name} module directory exists in output '
                    f'directory, any report files in the directory will be '
                    f'overwritten. Proceed (Y/N)? ')
                if answer.lower() == 'y':
                    break
                elif answer.lower() == 'n':
                    sys.exit()

    def create_report(self):
        """Generate report text file containing parsed lines for the QC module
        from input FastQC file.

        :return: None
        :rtype: None
        """
        path = os.path.join(self.dir_name, 'QC_report.txt')
        with open(path, 'w') as f:
            lines = ''.join(self.lines)
            f.write(lines)
            print(f'Report text file generated for {self.name}.')

    def create_filter_text(self):
        """Create filter text file from parsed QC module.

        Filter information (pass/warn/fail) is parsed from the QC module and
        written to a text file.

        :return: None
        :rtype: None
        """
        path = os.path.join(self.dir_name, 'filter.txt')
        # split the header line for module and extract the filter info
        # (second element)
        filter_info = self.lines[0].split('\t')[1]
        with open(path, 'w') as f:
            f.write(filter_info)
            print(f'Filter text file generated for {self.name}.')

    def clean_lines(self):
        """Clean, strip and split parsed lines for given QC module.

        :return: lines, columns
        :rtype: tuple(list, list)
        """
        # strip newline char and split using tab
        lines = [line.strip('\n').split('\t') for line in self.lines]
        # strip '#' from start of columns row
        columns = [colname.strip('#') if colname.startswith('#') else colname
                   for colname in lines[1]]
        return lines, columns

    @abstractmethod
    def module_output(self):
        """Generate all output for a QC module.

        Depending on module output may include: report text file, filter text
        file, graph png file or screen display of module data.

        :return: None
        :rtype: None
        """
        self.parse_text()
        print(f'Generating output for {self.name}...')
