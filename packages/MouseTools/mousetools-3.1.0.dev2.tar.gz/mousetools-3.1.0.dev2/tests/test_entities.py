from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest

from mousetools.entities.attraction import Attraction
from mousetools.entities.character import Character
from mousetools.entities.destination import Destination
from mousetools.entities.dining_event import DiningEvent
from mousetools.entities.dinner_show import DinnerShow
from mousetools.entities.entertainment import Entertainment
from mousetools.entities.entertainment_venue import EntertainmentVenue
from mousetools.entities.event import Event
from mousetools.entities.guest_services import GuestServices
from mousetools.entities.land import Land
from mousetools.entities.menu import Menus
from mousetools.entities.merchandise_facility import MerchandiseFacility
from mousetools.entities.park import ThemePark, WaterPark
from mousetools.entities.point_of_interest import PointOfInterest
from mousetools.entities.resort import Resort
from mousetools.entities.resort_area import ResortArea
from mousetools.entities.restaurant import Restaurant
from mousetools.ids import (
    DestinationIds,
    DisneylandResortParkIds,
    FacilityServiceEntityTypes,
    WaltDisneyWorldParkIds,
)

DESTINATION_PARAMS = [
    pytest.param(Destination(DestinationIds.WALT_DISNEY_WORLD), id="Destination"),
    pytest.param(Destination(DestinationIds.DISNEYLAND_RESORT), id="Destination"),
]
ATTRACTION_PARAMS = [pytest.param(Attraction("80010110"), id="Attraction")]
CHARACTER_PARAMS = [pytest.param(Character("18188665"), id="Character")]
DINING_EVENT_PARAMS = [pytest.param(DiningEvent("140873"), id="DiningEvent")]
DINNER_SHOW_PARAMS = [pytest.param(DinnerShow("80010856"), id="DinnerShow")]
ENTERTAINMENT_PARAMS = [pytest.param(Entertainment("19322758"), id="Entertainment")]
ENTERTAINMENT_VENUE_PARAMS = [
    pytest.param(EntertainmentVenue("80008259"), id="EntertainmentVenue")
]
EVENT_PARAMS = [pytest.param(Event("19615365"), id="Event")]
GUEST_SERVICES_PARAMS = [pytest.param(GuestServices("18373473"), id="GuestServices")]
LAND_PARAMS = [pytest.param(Land("80007936"), id="Land")]
MERCHANDISE_FACILITY_PARAMS = [
    pytest.param(MerchandiseFacility("90002944"), id="MerchandiseFacility")
]
THEME_PARK_PARAMS = [
    pytest.param(ThemePark(WaltDisneyWorldParkIds.MAGIC_KINGDOM), id="ThemePark"),
    pytest.param(ThemePark(DisneylandResortParkIds.DISNEYLAND), id="ThemePark"),
]
WATER_PARK_PARAMS = [
    pytest.param(WaterPark(WaltDisneyWorldParkIds.TYPHOON_LAGOON), id="WaterPark")
]
POINT_OF_INTEREST_PARAMS = [
    pytest.param(PointOfInterest("19615278"), id="PointOfInterest")
]
RESORT_PARAMS = [pytest.param(Resort("80010390"), id="Resort")]
RESORT_AREA_PARAMS = [pytest.param(ResortArea("80069772"), id="ResortArea")]
RESTAURANT_PARAMS = [pytest.param(Restaurant("19233597"), id="Restaurant")]
MENU_PARAMS = [pytest.param(Menus("19256571"), id="Menus")]

TEST_ALL_ENTITIES = pytest.mark.parametrize(
    "entity_obj",
    DESTINATION_PARAMS
    + ATTRACTION_PARAMS
    + CHARACTER_PARAMS
    + DINING_EVENT_PARAMS
    + DINNER_SHOW_PARAMS
    + ENTERTAINMENT_PARAMS
    + ENTERTAINMENT_VENUE_PARAMS
    + EVENT_PARAMS
    + GUEST_SERVICES_PARAMS
    + LAND_PARAMS
    + MERCHANDISE_FACILITY_PARAMS
    + THEME_PARK_PARAMS
    + WATER_PARK_PARAMS
    + POINT_OF_INTEREST_PARAMS
    + RESORT_PARAMS
    + RESORT_AREA_PARAMS
    + RESTAURANT_PARAMS
    + MENU_PARAMS,
)


@TEST_ALL_ENTITIES
def test_repr(entity_obj):
    assert entity_obj.__class__.__name__ in repr(entity_obj)


@TEST_ALL_ENTITIES
def test_id(entity_obj):
    assert isinstance(entity_obj.entity_id, str)


@TEST_ALL_ENTITIES
def test_name(entity_obj):
    assert isinstance(entity_obj.name, str)


@TEST_ALL_ENTITIES
def test_type(entity_obj):
    assert isinstance(entity_obj.entity_type, str)


@TEST_ALL_ENTITIES
def test_sub_type(entity_obj):
    assert isinstance(entity_obj.sub_type, str) or entity_obj.sub_type is None


@TEST_ALL_ENTITIES
def test_url_friendly_id(entity_obj):
    assert (
        isinstance(entity_obj.url_friendly_id, str)
        or entity_obj.url_friendly_id is None
    )


@TEST_ALL_ENTITIES
def test_coordinates(entity_obj):
    assert isinstance(entity_obj.coordinates, dict) or entity_obj.coordinates is None


@TEST_ALL_ENTITIES
def test_ancestor_destination_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_destination_id, str)
        or entity_obj.ancestor_destination_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_theme_park_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_theme_park_id, str)
        or entity_obj.ancestor_theme_park_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_water_park_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_water_park_id, str)
        or entity_obj.ancestor_water_park_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_resort_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_resort_id, str)
        or entity_obj.ancestor_resort_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_land_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_land_id, str)
        or entity_obj.ancestor_land_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_resort_area_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_resort_area_id, str)
        or entity_obj.ancestor_resort_area_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_entertainment_venue_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_entertainment_venue_id, str)
        or entity_obj.ancestor_entertainment_venue_id is None
    )


@TEST_ALL_ENTITIES
def test_ancestor_restaurant_id(entity_obj):
    assert (
        isinstance(entity_obj.ancestor_restaurant_id, str)
        or entity_obj.ancestor_restaurant_id is None
    )


@TEST_ALL_ENTITIES
def test_time_zone(entity_obj):
    assert isinstance(entity_obj.time_zone, ZoneInfo)


# TODO check for other types with duration
@pytest.mark.parametrize("entity_obj", ENTERTAINMENT_PARAMS)
def test_duration(entity_obj):
    assert isinstance(entity_obj.duration, time) or entity_obj.duration is None


@TEST_ALL_ENTITIES
def test_status(entity_obj):
    status = entity_obj.get_status()
    assert isinstance(status, str) or status is None


@TEST_ALL_ENTITIES
def test_wait_time(entity_obj):
    wait_time = entity_obj.get_wait_time()
    assert isinstance(wait_time, int) or wait_time is None


@TEST_ALL_ENTITIES
def test_last_updated(entity_obj):
    last_updated = entity_obj.get_last_updated()
    assert isinstance(last_updated, datetime) or last_updated is None


@TEST_ALL_ENTITIES
def test_today_operating_hours(entity_obj):
    hours = entity_obj.get_today_operating_hours()
    assert isinstance(hours, dict) or hours is None


@TEST_ALL_ENTITIES
def test_today_showtimes(entity_obj):
    showtimes = entity_obj.get_today_showtimes()
    assert isinstance(showtimes, list) or showtimes is None


@pytest.mark.parametrize("entity_obj", DESTINATION_PARAMS)
def test_children_entity_ids(entity_obj):
    assert isinstance(entity_obj.get_children_entity_ids("entertainments"), list)

    assert isinstance(entity_obj.get_children_entity_ids("resorts"), list)

    assert isinstance(entity_obj.get_children_entity_ids("shops"), list)

    assert isinstance(
        entity_obj.get_children_entity_ids(FacilityServiceEntityTypes.LANDS), list
    )
