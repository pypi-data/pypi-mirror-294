"""A group of items that belong to a CursesMenu."""

from __future__ import annotations

from collections.abc import Iterable, MutableSequence
from typing import TYPE_CHECKING, Any, cast, overload

if TYPE_CHECKING:
    from collections.abc import Iterator

    from cursesmenu.curses_menu import CursesMenu
    from cursesmenu.items.menu_item import MenuItem
else:
    CursesMenu = Any
    MenuItem = Any


class ItemGroup(MutableSequence[MenuItem]):
    """
    A group of items that belong to a CursesMenu.

    Holds the items and ensures that the menu updates when a new one is added.
    Implements MutableSequence, so should act like a list.
    """

    def __init__(
        self,
        menu: CursesMenu,
        items: Iterable[MenuItem] | None = None,
    ) -> None:
        """Initialize the group."""
        if items is None:
            items = []
        self.items: list[MenuItem] = list(items)
        self.menu = menu

        for item in items:
            item.menu = self.menu

    def insert(self, index: int, value: MenuItem) -> None:
        """Insert an item."""
        value.menu = self.menu
        self.items.insert(index, value)
        self.menu.adjust_screen_size()

    @overload
    def __getitem__(self, i: int) -> MenuItem: ...

    @overload
    def __getitem__(self, i: slice) -> ItemGroup: ...

    def __getitem__(self, i: int | slice) -> MenuItem | ItemGroup:
        if isinstance(i, slice):
            return ItemGroup(self.menu, self.items[i])
        else:
            return self.items[i]

    @overload
    def __setitem__(self, i: int, item: MenuItem) -> None: ...

    @overload
    def __setitem__(self, i: slice, item: Iterable[MenuItem]) -> None: ...

    def __setitem__(
        self,
        i: int | slice,
        item: MenuItem | Iterable[MenuItem],
    ) -> None:
        """Set an item."""
        from cursesmenu.items.menu_item import MenuItem

        if isinstance(i, int):
            item = cast(MenuItem, item)
            item.menu = self.menu
            self.items[i] = item
        else:
            item = cast(Iterable[MenuItem], item)
            for it in item:
                it.menu = self.menu
            self.items[i] = item

        self.menu.adjust_screen_size()

    @overload
    def __delitem__(self, i: int) -> None: ...

    @overload
    def __delitem__(self, i: slice) -> None: ...

    def __delitem__(self, i: int | slice) -> None:
        """Delete an item."""
        del self.items[i]
        self.menu.adjust_screen_size()

    def __iter__(self) -> Iterator[MenuItem]:
        """Get an iterator for the group."""
        return iter(self.items)

    def __len__(self) -> int:
        """Get the number of items in the group."""
        return len(self.items)

    def __add__(self, other: ItemGroup) -> ItemGroup:
        """
        Add two groups together.

        The resulting group will have the menu of the first group.
        """
        return ItemGroup(self.menu, self.items + other.items)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemGroup):
            return NotImplemented
        if self.menu != other.menu:
            return False
        if len(self) != len(other):
            return False
        return all(item1 == item2 for item1, item2 in zip(self, other))
