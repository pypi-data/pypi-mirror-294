import logging
from enum import Enum

logger = logging.getLogger(__name__)


class DestinationIds(str, Enum):
    WALT_DISNEY_WORLD: str = "80007798;entityType=destination"
    """The destination id for Walt Disney World."""
    DISNEYLAND_RESORT: str = "80008297;entityType=destination"
    """The destination id for Disneyland Resort."""


class WaltDisneyWorldParkIds(str, Enum):
    MAGIC_KINGDOM: str = "80007944;entityType=theme-park"
    """The Park id for Magic Kingdom."""
    EPCOT: str = "80007838;entityType=theme-park"
    """The Park id for Epcot."""
    HOLLYWOOD_STUDIOS: str = "80007998;entityType=theme-park"
    """The Park id for Hollywood Studios."""
    ANIMAL_KINGDOM: str = "80007823;entityType=theme-park"
    """The Park id for Animal Kingdom."""
    TYPHOON_LAGOON: str = "80007981;entityType=water-park"
    """The Park id for Typhoon Lagoon."""
    BLIZZARD_BEACH: str = "80007834;entityType=water-park"
    """The Park id for Blizzard Beach."""


class DisneylandResortParkIds(str, Enum):
    DISNEYLAND: str = "330339;entityType=theme-park"
    """The Park id for Disneyland."""
    CALIFORNIA_ADVENTURE: str = "336894;entityType=theme-park"
    """The Park id for California Adventure."""


class ThemeParkAPIIds(str, Enum):
    WALT_DISNEY_WORLD: str = "e957da41-3552-4cf6-b636-5babc5cbc4e5"
    """The ThemeParks.Wiki id for Walt Disney World."""
    MAGIC_KINGDOM: str = "75ea578a-adc8-4116-a54d-dccb60765ef9"
    """The ThemeParks.Wiki id for Magic Kingdom."""
    EPCOT: str = "47f90d2c-e191-4239-a466-5892ef59a88b"
    """The ThemeParks.Wiki id for Epcot."""
    HOLLYWOOD_STUDIOS: str = "288747d1-8b4f-4a64-867e-ea7c9b27bad8"
    """The ThemeParks.Wiki id for Hollywood Studios."""
    ANIMAL_KINGDOM: str = "1c84a229-8862-4648-9c71-378ddd2c7693"
    """The ThemeParks.Wiki id for Animal Kingdom."""
    TYPHOON_LAGOON: str = "b070cbc5-feaa-4b87-a8c1-f94cca037a18"
    """The ThemeParks.Wiki id for Typhoon Lagoon."""
    BLIZZARD_BEACH: str = "ead53ea5-22e5-4095-9a83-8c29300d7c63"
    """The ThemeParks.Wiki id for Blizzard Beach."""

    DISNEYLAND_RESORT: str = "bfc89fd6-314d-44b4-b89e-df1a89cf991e"
    """The ThemeParks.Wiki id for Disneyland Resort."""
    DISNEYLAND: str = "7340550b-c14d-4def-80bb-acdb51d49a6"
    """The ThemeParks.Wiki id for Disneyland."""
    CALIFORNIA_ADVENTURE: str = "832fcd51-ea19-4e77-85c7-75d5843b127c"
    """The ThemeParks.Wiki id for California Adventure."""


class FacilityServiceEntityTypes(str, Enum):
    DESTINATIONS: str = "destinations"
    """Facility service url path for destinations."""
    THEME_PARKS: str = "theme-parks"
    """Facility service url path for theme parks."""
    WATER_PARKS: str = "water-parks"
    """Facility service url path for water parks."""
    CHARACTERS: str = "characters"
    """Facility service url path for characters."""
    DINING_EVENTS: str = "dining-events"
    """Facility service url path for dining events."""
    DINNER_SHOWS: str = "dinner-shows"
    """Facility service url path for dinner shows."""
    RESTAURANTS: str = "restaurants"
    """Facility service url path for restaurants."""
    ENTERTAINMENTS: str = "entertainments"
    """Facility service url path for entertainments."""
    ENTERTAINMENT_VENUES: str = "entertainment-venues"
    """Facility service url path for entertainment venues."""
    EVENTS: str = "events"
    """Facility service url path for events."""
    GUEST_SERVICES: str = "guest-services"
    """Facility service url path for guest services."""
    RESORTS: str = "resorts"
    """Facility service url path for resorts."""
    RESORT_AREAS: str = "resort-areas"
    """Facility service url path for resort areas."""
    ATTRACTIONS: str = "attractions"
    """Facility service url path for attractions."""
    POINTS_OF_INTEREST: str = "points-of-interest"
    """Facility service url path for points of interest."""
    LANDS: str = "lands"
    """Facility service url path for lands."""
    MERCHANDISE_FACILITIES: str = "shops"
    """Facility service url path for merchandise facilities."""
    MENU_ITEMS: str = "menu-items"
    """Facility service url path for menu items."""
