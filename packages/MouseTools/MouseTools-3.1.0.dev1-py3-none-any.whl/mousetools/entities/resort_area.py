from mousetools.entities.base import EntityBase
from mousetools.ids import FacilityServiceEntityTypes


class ResortArea(EntityBase):
    """Class for Resort Area Entities."""

    def __init__(self, entity_id: str):
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.RESORT_AREAS,
        )
