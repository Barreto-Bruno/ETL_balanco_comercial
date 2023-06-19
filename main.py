import ssl
import logging
from Src.methods import (
    link_download,
    collect_variables,
    consolidates_data
)

ssl._create_default_https_context = ssl._create_unverified_context
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="Src/log.txt", level=logging.INFO, format="%(asctime)s %(message)s"
)

if __name__ == "__main__":
    variables, co_country, co_trans, co_ncm, state = collect_variables("Src/Config.xlsx")
    link_csv, year = link_download()
    if isinstance(co_country, list):
        for country, trans, ncm, state in zip(co_country, co_trans, co_ncm, state):
            df_final = consolidates_data(
                link_csv, co_country=country, co_trans=trans, co_ncm=ncm, state=state
            )
            df_final.to_csv(
                f"report_{str(year)}_{str(country)}_{str(trans)}_{str(ncm)}_{state}.csv",
                index=False
            )
    else:
        df_final = consolidates_data(
            link_csv,
            co_country=co_country,
            co_trans=co_trans,
            co_ncm=co_ncm,
            state=state
        )
        df_final.to_csv(f"report_{str(year)}_275_1_33030010_SP.csv", index=False)
    logger.info("Planilha exportada e processo concluído!")
