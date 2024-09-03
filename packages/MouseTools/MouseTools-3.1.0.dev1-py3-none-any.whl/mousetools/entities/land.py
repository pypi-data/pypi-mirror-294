from mousetools.entities.base import EntityBase
from mousetools.ids import FacilityServiceEntityTypes


class Land(EntityBase):
    """Class for Land Entities."""

    def __init__(self, entity_id: str):
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.LANDS,
        )
