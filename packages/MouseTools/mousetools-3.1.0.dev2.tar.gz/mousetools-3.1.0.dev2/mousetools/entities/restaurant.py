import logging
import typing

from mousetools.entities.base import EntityBase
from mousetools.ids import FacilityServiceEntityTypes

logger = logging.getLogger(__name__)


class Restaurant(EntityBase):
    """Class for Restaurant Entities."""

    def __init__(self, entity_id: str):
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.RESTAURANTS,
        )

    @property
    def service_styles(self) -> typing.Optional[list[str]]:
        """
        The service styles offered by the restaurant.

        Returns:
            (typing.Optional[list[str]]): The service styles offered by the restaurant.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["serviceStyles"]
        except KeyError:
            logger.debug("No service styles found for %s", self.entity_id)
            return None

    @property
    def menu_id(self) -> typing.Optional[str]:
        """
        The menu id associated with the restaurant.

        Returns:
            (typing.Optional[str]): The menu id associated with the restaurant.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["menuItems"][0]["links"]["self"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No menu id found for %s", self.entity_id)
            return None
