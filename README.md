# FastQC Report Generator
FastQC Report Generator is a lightweight command-line tool for creating report files and visualisations from [FastQC](https://github.com/s-andrews/FastQC) text files.

## System Requirements
- Python 3.4+ is required to run FastQC Report Generator.
- FastQC Report Generator requires the following scientific libraries (which can be installed using pip or conda): 
  - Matplotlib
  - Seaborn
  - NumPy
  - Pandas
  - SciPy

## Installation
FastQC Report Generator does not require an installation procedure, simply open the terminal in Linux / MacOS or the Command Prompt in Windows, navigate to the fastqc_report directory and run fastqc_report.py (see below) using Python from the command-line.

## Usage
To generate reports for specific FastQC modules (e.g., <i>Per base sequence quality</i> (module 2) and <i>K-mer Content</i> (module 12) parsed from an input file (<i>fastqc.txt</i>) in output directory (<i>outdir</i>), type the following in the command-line:

```
python fastqc_report.py fastqc.txt outdir m2 m12 m1
```

To generate reports and graphs for <b>all</b> modules, type:

```
python fastqc_report.py fastqc.txt outdir m1 -all
```

Alternatively, all reports can be generated in the Python console by typing:

```
runfile("fastqc_report.py", args="fastqc.txt outdir m1 -all")
```

For additional help, add the ```–h``` or ```--help``` flag:

```
python fastqc_report.py -h  
```
