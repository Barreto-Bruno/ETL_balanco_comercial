# Script Internacional Trade - Case

This code downloads data from a government site, collects variables from an Excel file, consolidates the data, and exports it to a CSV file.

## Prerequisites

- Python 3.8
- Libraries: pandas, matplotlib, datetime, backoff, requests, bs4, and logging

## Installation

1. Make sure you have Python 3.8 installed correctly on your system.
2. Install the required libraries by running the following command in the terminal:

   ```shell
   pip install pandas matplotlib datetime backoff requests bs4 logging

# Functions
## conecction(url)
Establishes a connection to a specified URL and retrieves the data.

 - Parameters:
   - url (str): The URL to establish a connection with.
 - Returns:
   - requests.Response: The response object containing the data retrieved from the URL.

## collect_variables(file)
Collects variables from an Excel file and returns them along with other data.

- Parameters:
  - file (str): The path to the Excel file to collect variables from.
- Returns:
  - Tuple[pandas.DataFrame, int, list, list, list or str]: A tuple containing the DataFrame with the variables, lists for co_country, co_trans, co_ncm, and state.

## link_download
Retrieves and processes download links from a specific URL.

- Returns:
  - Tuple[str, int]: A tuple containing the selected download link as a string and the current year as an integer.

## consolidates_data
Consolidates data from a CSV file (inside link provide by link_download) based on specified filters.

- Parameters:
  - link_base (str): The link to the CSV file to be downloaded and processed.
  - co_country (int, optional): The country code for filtering the data. Defaults to 275.
  - co_trans (int, optional): The transportation code for filtering the data. Defaults to 1.
  - co_ncm (int, optional): The product code for filtering the data. Defaults to 33030010.
  - state (str, optional): The state abbreviation for filtering the data. Defaults to 'SP'.
- Returns:
  - pd.DataFrame: The filtered and consolidated DataFrame containing columns: 'CO_ANO', 'CO_MES', 'CO_NCM', 'CO_UNID','CO_PAIS', 'SG_UF_NCM', 'CO_VIA', 'CO_URF', 'CUSTO_TOTAL', 'PRECO_POR_KG', sorted by 'CO_MES'.

License
This code is licensed under the MIT License. See the LICENSE file for details.