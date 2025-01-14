import typing

from BaseClasses import Tutorial, Item, ItemClassification, Region, Entrance
from .Locations import location_table, Sims4Location
from .Items import item_table, skills_table, Sims4Item, junk_table, filler_set
from .Options import sims4_options
from .Regions import sims4_career_paths, sims4_aspiration_milestones, sims4_skill_dependencies, \
    sims4_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld


class Sims4APWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up The Sims 4 for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["mrsummer360"]
    )]


class Sims4World(World):
    """
    The Sims 4 is the fourth installment in The Sims franchise. Like the previous games in the series,
    The Sims 4 focuses on creating and controlling a neighborhood of virtual people, called "Sims".
    """

    def create_item(self, name: str) -> Item:
        item_id: int = self.item_name_to_id[name]

        return Sims4Item(name,
                         item_table[item_id]["classification"],
                         item_id, player=self.player)

    def create_event(self, event: str):
        return Sims4Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        pool = []

        count_to_fill = len(location_table)

        for item in item_table.values():
            for i in range(item["count"]):
                sims4_item = self.create_item(item["name"])
                pool.append(sims4_item)

        count_to_fill = count_to_fill - len(pool)

        for item_name in self.multiworld.random.choices(sorted(filler_set), k=count_to_fill):
            item = self.create_item(item_name)
            item.classification = item.classification
            pool.append(item)

        self.multiworld.itempool += pool

    def create_region(self, name: str, locations=None, exits=None):
        ret = Region(name, self.player, self.multiworld)
        if locations:
            for location in locations:
                loc_id = self.location_name_to_id.get(location, None)
                location = Sims4Location(self.player, location, loc_id, ret)
                ret.locations.append(location)
        if exits:
            for region_exit in exits:
                ret.exits.append(Entrance(self.player, region_exit, ret))
        return ret

    def create_regions(self):
        menu = self.create_region("Menu", locations=None, exits=None)
        for location in self.location_name_to_id:
            menu.locations.append(Sims4Location(self.player, location, self.location_name_to_id.get(location), menu))

        self.multiworld.regions.append(menu)

    game: str = "The Sims 4"
    topology_present = False
    web = Sims4APWeb()

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}

    data_version = 0
    base_id = 0x73340001
    required_client_version = (0, 4, 0)

    area_connections: typing.Dict[int, int]

    option_definitions = sims4_options

    set_rules = set_rules
