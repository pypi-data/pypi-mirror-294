import logging

import httpx

from mousetools.auth import auth_obj
from mousetools.exceptions import EntityIDNotFoundError
from mousetools.urls import (
    WDPRAPPS_FACILITY_SERVICE_BASE_URL,
    WDPRO_FACILITY_SERVICE_BASE_URL,
)

logger = logging.getLogger(__name__)


class DisneyAPIMixin:
    def get_disney_data(self, url: str):
        """
        Sends a request to the Disney API at the given url and returns the data.

        Args:
            url (str): API url to request data from.

        Returns:
            (dict): The disney data.

        Raises:
            (EntityIDNotFoundError): If the entity is not found.
            (httpx.HTTPError): All other errors during http request.
        """
        logger.info("Sending request to %s", url)
        response = httpx.get(url, headers=auth_obj.get_headers())
        logger.debug("Response status: %s", response.status_code)

        try:
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError:
            logger.warning("Request failed. Retrying with updated url...")
            if WDPRO_FACILITY_SERVICE_BASE_URL in url:
                url = url.replace(
                    WDPRO_FACILITY_SERVICE_BASE_URL, WDPRAPPS_FACILITY_SERVICE_BASE_URL
                )
            else:
                url = url.replace(
                    WDPRAPPS_FACILITY_SERVICE_BASE_URL, WDPRO_FACILITY_SERVICE_BASE_URL
                )
            logger.debug("Sending new request to %s", url)
            response = httpx.get(url, headers=auth_obj.get_headers())
            logger.debug("Response status: %s", response.status_code)
            if response.status_code == httpx._status_codes.codes.NOT_FOUND:
                raise EntityIDNotFoundError
            response.raise_for_status()
            data = response.json()

        return data
