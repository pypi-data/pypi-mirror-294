from bs4 import BeautifulSoup
from uk_bin_collection.uk_bin_collection.common import *
from uk_bin_collection.uk_bin_collection.get_bin_data import AbstractGetBinDataClass


# import the wonderful Beautiful Soup and the URL grabber
class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def parse_data(self, page: str, **kwargs) -> dict:
        # Make a BS4 object
        soup = BeautifulSoup(page.text, features="html.parser")
        soup.prettify()

        # Extract data
        bin_data = {"bins": []}

        # Find the table containing the bin collection data
        table = soup.find("table", {"class": "eb-EVDNdR1G-tableContent"})

        if table:
            rows = table.find_all("tr", class_="eb-EVDNdR1G-tableRow")

            for row in rows:
                columns = row.find_all("td")
                if len(columns) >= 4:
                    collection_type = columns[1].get_text(strip=True)
                    collection_date = columns[3].get_text(strip=True)

                    # Validate collection_date format
                    if re.match(r"\d{2}/\d{2}/\d{4}", collection_date):
                        bin_entry = {
                            "type": collection_type,
                            "collectionDate": collection_date,
                        }
                        bin_data["bins"].append(bin_entry)

        return bin_data
