"""
Scraper for New York Court of Appeals
CourtID: ny
Court Short Name: NY
History:
 2014-07-04: Created by Andrei Chelaru, reviewed by mlr.
 2015-10-23: Parts rewritten by mlr.
 2016-05-04: Updated by arderyp to handle typos in docket string format
"""

import os
import re
from datetime import date

from juriscraper.AbstractSite import logger
from juriscraper.lib.html_utils import get_html5_parsed_text
from juriscraper.lib.string_utils import convert_date_string
from juriscraper.OpinionSite import OpinionSite


def set_api_token_header(scraper_site: OpinionSite) -> None:
    """
    Puts the NY_API_TOKEN in the X-Api-Token header
    Creates the Site.headers attribute, copying the
    scraper_site.request[headers]

    :param scraper_site: a Site Object
    :returns: None
    """
    if scraper_site.test_mode_enabled():
        return

    api_token = os.environ.get("NY_API_TOKEN")
    if not api_token:
        logger.warning(
            "NY_API_TOKEN environment variable is not set. "
            "It is required for scraping New York Courts"
        )
        return

    scraper_site.request["headers"]["X-APIKEY"] = api_token
    scraper_site.needs_special_headers = True


class Site(OpinionSite):
    DOWNLOAD_URL_SUB_PATH = "td[2]//@href[not(contains(., 'DecisionList'))]"
    FOUR_CELLS_SUB_PATH = "//*[count(td)=3"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        # https://www.nycourts.gov/ctapps/Decisions/2015/Dec15/December15.html
        self.url = "http://www.nycourts.gov/ctapps/Decisions/{year}/{mon}{yr}/{month}{yr}.html".format(
            year=today.year,
            yr=today.strftime("%y"),
            mon=today.strftime("%b"),
            month=today.strftime("%B"),
        )
        self.court_id = self.__module__
        set_api_token_header(self)

    def _make_html_tree(self, text):
        return get_html5_parsed_text(text)

    def _get_case_names(self):
        path = f"{self.FOUR_CELLS_SUB_PATH} and {self.DOWNLOAD_URL_SUB_PATH}]"
        case_names = []
        for element in self.html.xpath(path):
            case_name_parts = []
            for t in element.xpath("./td[3]/p/font/text()"):
                if t.strip():
                    case_name_parts.append(t)
            if not case_name_parts:
                # No hits for first XPath, try another that sometimes works.
                for t in element.xpath("./td[3]//text()"):
                    if t.strip():
                        case_name_parts.append(t)
            if case_name_parts:
                case_names.append(", ".join(case_name_parts))
        return case_names

    def _get_download_urls(self):
        return self.html.xpath(
            f"{self.FOUR_CELLS_SUB_PATH}]/{self.DOWNLOAD_URL_SUB_PATH}"
        )

    def _get_case_dates(self):
        case_dates = []
        case_date = False
        # Process rows. If it's a date row,
        # save the date, continue, then add
        # date for each opinion row below it
        for row in self.html.xpath("//tr[not(.//table)]"):
            date_from_row = self.get_date_from_text(row.text_content())
            if date_from_row:
                case_date = date_from_row
                continue
            elif self._row_contains_opinion(row) and case_date:
                case_dates.append(case_date)
        return case_dates

    def _get_precedential_statuses(self):
        return ["Published"] * len(self.case_names)

    def _get_docket_numbers(self):
        docket_numbers = []
        for cell in self.html.xpath(f"{self.FOUR_CELLS_SUB_PATH}]/td[1]"):
            text = cell.text_content()
            date_from_text = self.get_date_from_text(text)
            if not date_from_text:
                if re.search(r"N(o|O|0)\.?,?", text):
                    docket = self._sanitize_docket_string(text)
                    docket_numbers.append(docket)
        return docket_numbers

    def _sanitize_docket_string(self, raw_docket_string):
        """Handle typos and non-standard docket number strings

        Dockets on this page should be in format of "No. #",
        but sometimes they forget the period, or use a comma
        instead.  We want to trip all variations of that out
        and replace slash delimiters with coma delimiters.
        """
        for abbreviation in ["No.", "No ", "No, ", "NO. "]:
            raw_docket_string = raw_docket_string.replace(abbreviation, "")
        return ", ".join(raw_docket_string.split(" / "))

    def _row_contains_opinion(self, row):
        p1 = "./td[3]"
        p2 = f"./{self.DOWNLOAD_URL_SUB_PATH}"
        return row.xpath(p1) and row.xpath(p2)

    def get_date_from_text(self, text):
        try:
            return convert_date_string(text)
        except ValueError:
            return False
