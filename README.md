# PITCH Program

This is a tool which allows us to take PITCH data and displays a table of the top 10 symbols by executed volume

Written using Python, it attempts to achieve this criteria whilst also providing a platform to improve on with future upgrades

## Assumptions

The following assumptions were made in the creation of the tool:
- The "S" Character at the start of each line is not relevant and may be removed
- Volume is calculated using Order Executed and Trade Messages
- Trade Break and Long Messages are ignored
- Cancelled orders do not count towards total volume
- Executed orders will modify an existing add order, replacing the quantity with a new quantity

## Setup and Installation

Python 3.10 was used in development, whilst the tool will work on earlier versions it is highly recommended that Python version 3.10 is used

Use the package manager pip to install the following:

```bash
pip install pydantic
```






