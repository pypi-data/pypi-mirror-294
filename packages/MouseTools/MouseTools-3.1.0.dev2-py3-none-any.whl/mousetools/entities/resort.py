from mousetools.entities.base import EntityBase
from mousetools.ids import FacilityServiceEntityTypes


class Resort(EntityBase):
    """Class for Resort Entities."""

    def __init__(self, entity_id: str):
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.RESORTS,
        )
