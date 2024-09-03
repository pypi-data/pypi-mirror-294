import typing

from mousetools.entities.base import EntityBase
from mousetools.ids import (
    DisneylandResortParkIds,
    FacilityServiceEntityTypes,
    WaltDisneyWorldParkIds,
)


class ThemePark(EntityBase):
    """Class for Theme Park Entities."""

    def __init__(
        self,
        entity_id: typing.Union[str, WaltDisneyWorldParkIds, DisneylandResortParkIds],
    ):
        if isinstance(entity_id, WaltDisneyWorldParkIds) or isinstance(
            entity_id, DisneylandResortParkIds
        ):
            entity_id = entity_id.value
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.THEME_PARKS,
        )


class WaterPark(EntityBase):
    """Class for Water Park Entities."""

    def __init__(
        self,
        entity_id: typing.Union[str, WaltDisneyWorldParkIds, DisneylandResortParkIds],
    ):
        if isinstance(entity_id, WaltDisneyWorldParkIds) or isinstance(
            entity_id, DisneylandResortParkIds
        ):
            entity_id = entity_id.value
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.WATER_PARKS,
        )
