import typing

from mousetools.entities.base import EntityBase
from mousetools.ids import DestinationIds, FacilityServiceEntityTypes


class Destination(EntityBase):
    """Class for Destination Entities."""

    def __init__(self, entity_id: typing.Union[str, DestinationIds]):
        if isinstance(entity_id, DestinationIds):
            entity_id = entity_id.value
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.DESTINATIONS,
        )
