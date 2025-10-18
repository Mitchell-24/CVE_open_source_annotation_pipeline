# CVE Open Source Annotation

This is a data pipeline to annotate the entire dataset of CVEs between 1999 and 2023 with an open-source label. The pipeline relies on two LLMs from Mistral AI to infer the name of the software from the CVE description and to label each software name as open-source, closed-source, or unknown. These labels are extremely useful for security researchers investigating differences in vulnerabilities between closed- and open-source software. 

## Requirements

- Python 3.10+

- requests==2.32.5

- mistralai==1.9.11