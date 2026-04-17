# OSRS Price Data Pipeline

An automated end-to-end data pipeline that ingests real-time Old School RuneScape GE data, stores it in a PostgreSQL database, and transforms it into a Star Schema using **dbt**.

## Architecture/Services
*   Written in Python 3.12
*   Docker: Dockerfile & Docker Compose were utilized to manage services
*   Apache Airflow: Orchestrator to schedule the task every 5 minutes
*   PostgreSQL: Database
*   dbt: Utilized for transforming data



## How it works
1. Extracts data from https://prices.runescape.wiki/osrs/, making an API request for all transaction data within the past 5 minutes
2. Loads the raw data into PostgreSQL
3. dbt transforms the data into a Fact-Dimension Format:
   
       Fact Table: GE Transactions, all transactional data such as sales volume, high and low price, margins, tax, and alch profitability
   
       Dimension Tables:
   
           Item Metadata - Contains the item name, examine text, and the icon
   
           Price Metadata - Contains the High Alch value, Low Alch value, and the Base value
   
           Trade Metadata - Contains the membership status, 6 hour trade limit
4. Airflow orchestrates this every 5 minutes, with dbt only adding new rows to the Fact table, and updating the Metadata Dimensional Tables with only updated data

## ERD of the Database
<img width="2550" height="1478" alt="Blank diagram(2)" src="https://github.com/user-attachments/assets/b7ce0a9d-6aa9-4496-9c30-dcacf52ade00" />


## Significant Transformations
For the Fact Table, some of the significant transformations made were:
1. Transaction ID - A composite key composed of the item's id alongside the timestamp to create a unique identifier for each row
2. GE Tax - Calculates the tax on an item (2% or 5 million)
3. Net GE Margin - Accounting for tax and the item high/low margin, shows the profit margin for each item if you were to flip/resell
4. Alch Profit - Finds the latest low price of the item and nature runes, and shows how much you would profit/lose from High Alching the item
