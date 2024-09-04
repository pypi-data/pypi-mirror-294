import logging
import typing
from datetime import datetime, time
from zoneinfo import ZoneInfo

from mousetools.exceptions import AncestorDestinationMissingError
from mousetools.ids import DestinationIds, FacilityServiceEntityTypes
from mousetools.mixins.disney import DisneyAPIMixin
from mousetools.mixins.themeparksapi import ThemeParkAPIMixin
from mousetools.urls import WDPRO_FACILITY_SERVICE_BASE_URL

logger = logging.getLogger(__name__)


class EntityBase(DisneyAPIMixin, ThemeParkAPIMixin):
    def __init__(
        self,
        entity_id: str,
        facility_service_entity_type: typing.Union[str, FacilityServiceEntityTypes],
    ):
        self.entity_id: str = entity_id
        self.disney_data: typing.Optional[dict] = None

        if isinstance(facility_service_entity_type, FacilityServiceEntityTypes):
            facility_service_entity_type = facility_service_entity_type.value
        self._facility_service_url = f"{WDPRO_FACILITY_SERVICE_BASE_URL}/{facility_service_entity_type}/{self.entity_id}"

    @property
    def name(self) -> typing.Optional[str]:
        """
        The name of the entity.

        Returns:
            (typing.Optional[str]): The name of the entity, or None if it was not found.
        """

        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["name"]
        except KeyError:
            logger.debug("No name found for %s", self.entity_id)
            return None

    @property
    def entity_type(self) -> typing.Optional[str]:
        """
        The type of entity this is.

        Returns:
            (typing.Optional[str]): The type of entity this is, or None if it was not found.
        """

        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["type"]
        except KeyError:
            logger.debug("No entity type found for %s", self.entity_id)
            return None

    @property
    def sub_type(self) -> typing.Optional[str]:
        """
        The sub type of entity.

        Returns:
            (typing.Optional[str]): The sub type of entity, or None if it was not found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["subType"]
        except KeyError:
            logger.debug("No sub type found for %s", self.entity_id)
            return None

    @property
    def url_friendly_id(self) -> typing.Optional[str]:
        """
        The url friendly id of the entity.

        Returns:
            (typing.Optional[str]): The url friendly id of the entity, or None if not found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            _id = self.disney_data["urlFriendlyId"]
            return _id
        except KeyError:
            logger.debug("No url friendly id found for %s", self.entity_id)
            return None

    @property
    def coordinates(self) -> typing.Optional[dict[str, float]]:
        """
        The coordinates of this entity

        Returns:
            (typing.Optional[dict[str, float]]): A dict with "lat" and "lng" keys containing the coordinates of this entity as floats, or None if no coordinates are found
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return {
                "lat": float(
                    self.disney_data["coordinates"]["Guest Entrance"]["gps"][
                        "latitude"
                    ]
                ),
                "lng": float(
                    self.disney_data["coordinates"]["Guest Entrance"]["gps"][
                        "longitude"
                    ]
                ),
            }
        except KeyError as e:
            print(e)
            logger.debug("No coordinates found for %s", self.entity_id)
            return None

    @property
    def ancestor_destination_id(self) -> typing.Optional[str]:  # type: ignore
        """
        The id of the ancestor destination of this entity.

        Returns:
            (typing.Optional[str]): The id of the ancestor destination of this entity, or None if it was not found.
        """
        # TODO check other ancestors to guess dest if not found
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorDestination"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            try:
                return (
                    self.disney_data["ancestorDestination"]["id"]
                    .split("?")[0]
                    .split("/")[-1]
                )
            except KeyError:
                logger.debug("No ancestor destination id found for %s", self.entity_id)
                return None

    @property
    def ancestor_theme_park_id(self):
        """
        The id of the theme park of this entity.

        Returns:
            (typing.Optional[str]): Theme park id, or None if no such id is found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorThemePark"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No ancestor theme park id found for %s", self.entity_id)
            return None

    @property
    def ancestor_water_park_id(self) -> typing.Optional[str]:
        """
        The if of the water park of this entity.

        Returns:
            (typing.Optional[str]): Water park id, or None if no such id is found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorWaterPark"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No ancestor water park id found for %s", self.entity_id)
            return None

    @property
    def ancestor_resort_id(self) -> typing.Optional[str]:
        """
        The id of the resort of the entity.

        Returns:
            (typing.Optional[str): Resort id, or None if no such id is found.
        """

        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorResort"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No ancestor resort ids found for %s", self.entity_id)
            return None

    @property
    def ancestor_land_id(self) -> typing.Optional[str]:
        """
        The if of the land of this entity.

        Returns:
            (typing.Optional[str]): Land id, or None if no such id is found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorLand"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No ancestor land id found for %s", self.entity_id)
            return None

    @property
    def ancestor_resort_area_id(self) -> typing.Optional[str]:
        """
        The id of the resort area of this entity.

        Returns:
            (typing.Optional[str]): Resort area id, or None if no such id is found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorResortArea"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No ancestor resort area ids found for %s", self.entity_id)
            return None

    @property
    def ancestor_entertainment_venue_id(self) -> typing.Optional[str]:
        """
        The id of entertainment venues of this entity.

        Returns:
            (typing.Optional[str]): Entertainment venue id, or None if no such id is found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorEntertainmentVenue"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug(
                "No ancestor entertainment venue ids found for %s", self.entity_id
            )
            return None

    @property
    def ancestor_restaurant_id(self) -> typing.Optional[str]:
        """
        The id of the restaurant of this entity.

        Returns:
            (typing.Optional[str]): Restaurant id, or None if no such id is found.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return (
                self.disney_data["links"]["ancestorRestaurant"]["href"]
                .split("?")[0]
                .split("/")[-1]
            )
        except KeyError:
            logger.debug("No ancestor restaurant ids found for %s", self.entity_id)
            return None

    @property
    def time_zone(self) -> ZoneInfo:
        """
        The time zone of the entity.

        Returns:
            (ZoneInfo): The time zone of the entity.
        """

        if self.ancestor_destination_id is None:
            return ZoneInfo("UTC")
        if self.ancestor_destination_id in DestinationIds.WALT_DISNEY_WORLD.value:
            return ZoneInfo("America/New_York")
        elif self.ancestor_destination_id in DestinationIds.DISNEYLAND_RESORT.value:
            return ZoneInfo("America/Los_Angeles")

        return ZoneInfo("UTC")

    @property
    def related_location_ids(self) -> typing.List[str]:
        """
        The ids of the related locations of this entity.

        Returns:
            (typing.List[str]): The ids of the related locations of this entity.
        """
        # https://api.wdprapps.disney.com/facility-service/entertainments/19322758
        raise NotImplementedError

    @property
    def duration(self) -> typing.Optional[time]:
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return time.fromisoformat(
                ":".join(self.disney_data["duration"].split(":")[:3])
            )
        except KeyError:
            logger.debug("No duration found for %s", self.entity_id)
            return None

    def get_status(self) -> typing.Optional[str]:
        """
        The current status of the entity.

        Returns:
            (typing.Optional[str]): The current status of the entity, or None if no such data exists.
        """
        try:
            live_data = self.get_entity_live_tp()
        except AncestorDestinationMissingError:
            return None

        try:
            return live_data["liveData"][0]["status"]
        except (KeyError, IndexError):
            logger.debug("No status found for %s", self.entity_id)
            return None

    def get_wait_time(self) -> typing.Optional[int]:
        """
        The current wait time for the entity.

        Returns:
            (typing.Optional[int]): The current wait time for the entity, or None if no such data exists.
        """
        try:
            live_data = self.get_entity_live_tp()
        except AncestorDestinationMissingError:
            return None

        try:
            return live_data["liveData"][0]["queue"]["STANDBY"]["waitTime"]
        except (KeyError, IndexError):
            logger.debug("No wait time found for %s", self.entity_id)
            return None

    def get_last_updated(self) -> typing.Optional[datetime]:
        """
        The last time the entity's data was updated on ThemePark.wiki.

        Returns:
            (typing.Optional[datetime]): The last time the entity's data was updated, or None if no such data exists.
        """
        try:
            live_data = self.get_entity_live_tp()
        except AncestorDestinationMissingError:
            return None

        try:
            return datetime.strptime(
                live_data["liveData"][0]["lastUpdated"],
                "%Y-%m-%dT%H:%M:%SZ",
            ).replace(tzinfo=ZoneInfo("UTC"))
        except (KeyError, IndexError):
            logger.debug("No last updated found for %s", self.entity_id)
            return None

    def get_today_operating_hours(
        self,
    ) -> typing.Optional[dict[str, dict[str, datetime]]]:
        """
        The operating hours for today for the entity.

        Returns:
            (typing.Optional[dict[str, dict[str, datetime]]]): A dictionary of the operating hours for today, or None if no such data exists.
        """

        try:
            live_data = self.get_entity_live_tp()
        except AncestorDestinationMissingError:
            return None

        temp = {}

        try:
            for i in live_data["liveData"][0]["operatingHours"]:
                temp[i["type"]] = {
                    "start_time": datetime.strptime(
                        i["startTime"],
                        "%Y-%m-%dT%H:%M:%S%z",
                    ).replace(tzinfo=self.time_zone),
                    "end_time": datetime.strptime(
                        i["endTime"],
                        "%Y-%m-%dT%H:%M:%S%z",
                    ).replace(tzinfo=self.time_zone),
                }
        except (KeyError, IndexError):
            logger.debug("No operating hours found for %s", self.entity_id)
            return None

        return temp

    def get_today_showtimes(self) -> typing.Optional[list[datetime]]:
        """
        The showtimes for today for the entity.

        Returns:
            (typing.Optional[list[datetime]]): A list of the showtimes for today, or None if no such data exists.
        """
        try:
            live_data = self.get_entity_live_tp()
        except AncestorDestinationMissingError:
            return None

        temp = []

        try:
            for i in live_data["liveData"][0]["showtimes"]:
                temp.append(
                    datetime.strptime(i["startTime"], "%Y-%m-%dT%H:%M:%S%z").replace(
                        tzinfo=self.time_zone,
                    ),
                )
        except (KeyError, IndexError):
            logger.debug("No showtimes found for %s", self.entity_id)
            return None

        return temp

    def get_children_entity_ids(
        self, entity_type: typing.Union[str, FacilityServiceEntityTypes]
    ) -> list[str]:
        """
        Get the children entity IDs for the given entity type.

        Args:
            entity_type (typing.Union[str, FacilityServiceEntityTypes]): The type of entity to get children for.

        Returns:
            (list[str]): A list of the children entity IDs, or an empty list if no such data exists
        """
        if isinstance(entity_type, FacilityServiceEntityTypes):
            entity_type = entity_type.value

        children_url = f"{self._facility_service_url}/{entity_type}"
        data = self.get_disney_data(children_url)
        if data:
            return [
                i["links"]["self"]["href"].split("?")[0].split("/")[-1]
                for i in data["entries"]
            ]

        return []

    def __str__(self) -> str:
        return f"{self.entity_type}: {self.name} ({self.entity_id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(entity_id='{self.entity_id}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, EntityBase):
            return self.entity_id == other.entity_id
        return False
