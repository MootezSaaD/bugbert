## CSCI 6409 Group 5 Project: Improving Duplicate Bug Report Detection using Large Language Modelling

### Dataset Construction
To construct the dataset for this project, we utilized the dataset provided in the MSR'22 paper titled "An alternative issue tracking dataset of public Jira repositories." The dataset can be accessed [here](https://zenodo.org/record/7182101).

We employed their data extraction script to convert the dataset into two CSV files. The first CSV contains information about bug reports, including fields such as Issue ID, Type, Status, Priority, Description, and Title. The second CSV contains information about link types and the connections between the issues.

Afterwards, we removed irrelevant fields from both CSV files. Finally, we created two JSONL files that include information about the bug reports: ID, Title, Description, and the IDs of duplicate bug reports.

You can find the CSV and JSONL files created during the dataset construction process [here](https://zenodo.org/record/8124992).