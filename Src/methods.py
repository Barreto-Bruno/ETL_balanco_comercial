""" Support Functions. """
import datetime
from typing import Tuple, Union
import requests
import backoff
from bs4 import BeautifulSoup as bs
import ssl
import pandas as pd
import logging

ssl._create_default_https_context = ssl._create_unverified_context
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="Src/log.txt", level=logging.INFO, format="%(asctime)s %(message)s"
)


@backoff.on_exception(
    backoff.expo,
    (ConnectionError, ConnectionAbortedError, ConnectionRefusedError),
    max_tries=10
)
def connection(url) -> requests.Response:
    """
    Establishes a connection to a specified URL and retrieves the data.

    Args:
        url (str): The URL to establish a connection with.

    Returns:
        requests.Response: The response object containing the data retrieved from the URL.

    """
    logger.info(f"Coletando os dados do site")
    return requests.get(url)


def collect_variables(file: str) -> Tuple[pd.DataFrame, int, list, list, Union[list, str]]:
    """
    Collects variables from an Excel file and returns them along with other data.

    Args:
        file (str): The path to the Excel file to collect variables from.

    Returns:
        Tuple[pandas.DataFrame, int, list, list, list or str]: A tuple containing the DataFrame with the variables,
        lists for co_country, co_trans, co_ncm, and state.

    """
    variables = pd.read_excel(file)
    try:
        co_country = int(variables['CO_PAIS'].iloc[0])
        co_country = list(variables['CO_PAIS'])
        co_trans = list(variables['CO_VIA'])
        co_ncm = list(variables['CO_NCM'])
        state = list(variables['ESTADO'])
    except Exception as e:
        logger.info(f"Não foi encontrado dado na planilha Config.xlsx")
        co_country = 0
        co_trans = 0
        co_ncm = 0
        state = ""
    else:
        logger.info(f"Dados coletados na planilha Config.xlsx")
    return variables, co_country, co_trans, co_ncm, state


def link_download() -> Union[Tuple[str, int], requests.HTTPError]:
    """
    Retrieves and processes download links from a specific URL.

    Returns:
        Tuple[str, int]: A tuple containing the selected download link as a string and the current year as an integer.

    Raises:
        requests.HTTPError: If an error occurs while establishing a connection or retrieving the links.

    """
    try:
        url = "https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/estatisticas/base-de-dados-bruta"
        today = datetime.date.today()
        if today.month != 1:
            year = today.year
        else:
            year = today.year - 1
        ret = connection(url)
        ret.raise_for_status()
        soup = bs(ret.text)
        sheets = soup.find_all('a', {'class': 'external-link'})
    except Exception as e:
        logger.info(f"Link com erro")
        raise
    links = []
    for href in sheets:
        links.append({href.get("href")})
    logger.info(f"links coletados")
    links2 = []
    for link in links:
        link2 = str(link)
        link3 = link2[2:-2]
        links2.append(link3)
    logger.info(f"links tratados")
    links_ncm = list(filter(lambda k: 'ncm' in k, links2))
    links_imp = list(filter(lambda k: 'IMP' in k, links_ncm))
    links_year = list(filter(lambda k: str(year) in k, links_imp))
    logger.info(f"links filtrados para NCM, importação e ano {str(year)}")
    link_final = links_year[0]
    logger.info(f"links selecionado foi: {link_final}")
    return link_final, year


def consolidates_data(link_base, co_country=275, co_trans=1, co_ncm=33030010, state='SP') -> pd.DataFrame:
    """
      Consolidates data from a CSV file based on specified filters.

      Args:
          link_base (str): The link to the CSV file to be downloaded and processed.
          co_country (int, optional): The country code for filtering the data. Defaults to 275.
          co_trans (int, optional): The transportation code for filtering the data. Defaults to 1.
          co_ncm (int, optional): The product code for filtering the data. Defaults to 33030010.
          state (str, optional): The state abbreviation for filtering the data. Defaults to 'SP'.

      Returns:
          pd.DataFrame: The filtered and consolidated DataFrame containing columns: 'CO_ANO', 'CO_MES', 'CO_NCM', 'CO_UNID',
          'CO_PAIS', 'SG_UF_NCM', 'CO_VIA', 'CO_URF', 'CUSTO_TOTAL', 'PRECO_POR_KG', sorted by 'CO_MES'.

      """
    df = pd.read_csv(link_base, delimiter=";")
    logger.info("Arquivo CSV baixado com sucesso!")
    df_filter = df.query(
        f"CO_PAIS == {str(co_country)} & CO_VIA == {str(co_trans)} & CO_NCM == {str(co_ncm)} & SG_UF_NCM == '{state}'")

    logger.info(
        f"Base filtrada com o Código do País {str(co_country)}, Código de transporte {str(co_trans)}, Código do produto {str(co_ncm)} e Estado de {state}"
    )
    df_filter['CUSTO_TOTAL'] = (
            df_filter['VL_FOB'] + df_filter['VL_FRETE'] + df_filter['VL_SEGURO']
    )
    df_filter['PRECO_POR_KG'] = round(
        (df_filter['VL_FOB'] + df_filter['VL_FRETE'] + df_filter['VL_SEGURO'])
        / df_filter['KG_LIQUIDO']
        ,2
    )
    logger.info("Cálculo de Preço por KG realizado")
    return df_filter[
        [
            'CO_ANO',
            'CO_MES',
            'CO_NCM',
            'CO_UNID',
            'CO_PAIS',
            'SG_UF_NCM',
            'CO_VIA',
            'CO_URF',
            'CUSTO_TOTAL',
            'PRECO_POR_KG']
    ].sort_values(by="CO_MES")
