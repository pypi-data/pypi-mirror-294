import typing

from mousetools.entities.base import EntityBase
from mousetools.ids import FacilityServiceEntityTypes


class MenuItem:
    def __init__(self, raw_item_data: dict):
        self._raw_item_data = raw_item_data

    def __repr__(self) -> str:
        return f"MenuItem(entity_id={self.entity_id}, name={self.name})"

    @property
    def entity_id(self) -> typing.Optional[str]:
        """
        The entity id of the menu item.

        Returns:
            (typing.Optional[str]): The entity id of the menu item.
        """
        try:
            return self._raw_item_data["id"]
        except KeyError:
            return None

    @property
    def name(self) -> typing.Optional[str]:
        """
        The name of the menu item.

        Returns:
            (typing.Optional[str]): The name of the menu item.
        """
        try:
            return self._raw_item_data["name"]
        except KeyError:
            return None

    @property
    def type_name(self) -> typing.Optional[str]:
        """
        The type of the menu item.

        Returns:
            (typing.Optional[str]): The type of the menu item.
        """
        try:
            return self._raw_item_data["type"]
        except KeyError:
            return None

    @property
    def price(self) -> typing.Optional[dict]:
        """
        The price of the menu item.

        Examples:
            {'price_qualifier': 'Per Serving', 'price_without_tax': 6.29}

        Returns:
            (typing.Optional[dict]): The price of the menu item.
        """
        try:
            for i in self._raw_item_data["prices"]:
                if i["type"] == "Retail":
                    return {
                        "price_without_tax": float(
                            i["priceSpecifications"][0]["priceWithoutTax"]
                        ),
                        "price_qualifier": i["priceSpecifications"][0][
                            "priceQualifier"
                        ],
                    }
        except KeyError:
            return None

        return None


class Menu:
    def __init__(self, raw_menu_data: dict):
        self._raw_menu_data = raw_menu_data

    def __repr__(self) -> str:
        return f"Menu(entity_id={self.entity_id}, name={self.name})"

    @property
    def entity_id(self) -> typing.Optional[str]:
        """
        The entity id of the menu.

        Returns:
            (typing.Optional[str]): The entity id of the menu.
        """
        try:
            return self._raw_menu_data["id"]
        except KeyError:
            return None

    @property
    def name(self) -> typing.Optional[str]:
        """
        The name of the menu.

        Returns:
            (typing.Optional[str]): The name of the menu.
        """
        try:
            return self._raw_menu_data["name"]
        except KeyError:
            return None

    @property
    def type_name(self) -> typing.Optional[str]:
        """
        The type of the menu.

        Returns:
            (typing.Optional[str]): The type of the menu.
        """
        try:
            return self._raw_menu_data["type"]
        except KeyError:
            return None

    @property
    def menu_items(self) -> list[MenuItem]:
        """
        The menu items of the menu.

        Returns:
            (list[MenuItem]): The menu items of the menu.
        """
        try:
            return [MenuItem(i) for i in self._raw_menu_data["menuItems"]]
        except KeyError:
            return []


class Menus(EntityBase):
    """Class for Menu Entities."""

    def __init__(self, entity_id: str):
        super().__init__(
            entity_id=entity_id,
            facility_service_entity_type=FacilityServiceEntityTypes.MENU_ITEMS,
        )

    @property
    def price_range(self) -> typing.Optional[str]:
        """
        The price range of the menu.

        Examples:
            "$ ($14.99 and under per adult)"

        Returns:
            (typing.Optional[str]): Price range of menu desribed in $.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["priceRange"]
        except KeyError:
            return None

    @property
    def service_style(self) -> typing.Optional[str]:
        """
        The service style of the menu.

        Returns:
            (typing.Optional[str]): The service style of the menu.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["serviceStyle"]
        except KeyError:
            return None

    @property
    def meal_period_type(self) -> typing.Optional[str]:
        """
        The meal period type of the menu.

        Returns:
            (typing.Optional[str]): The meal period type of the menu.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["mealPeriodType"]
        except KeyError:
            return None

    @property
    def primary_cuisine_type(self) -> typing.Optional[str]:
        """
        The primary cuisine type of the menu.

        Returns:
            (typing.Optional[str]): The primary cuisine type of the menu.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return self.disney_data["primaryCuisineType"]
        except KeyError:
            return None

    @property
    def menus(self) -> list[Menu]:
        """
        Returns a list of all the menus associated with this entity.

        Returns:
            (list[Menu]): List of Menu objects that are associated with this entity.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._facility_service_url)
        try:
            return [Menu(i) for i in self.disney_data["menus"]]
        except KeyError:
            return []
