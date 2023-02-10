from BaseClasses import Item, ItemClassification

class XenobladeXItem(Item):
    game: str = "XenobladeX"

# Specifies the items you can receive
# The first layer is for the object group
# The second one is for the items itself
# Use a dict to specifiy multiple
xenobladeXItems = {
    "Key": {
        "Skell License": {"class": ItemClassification.progression}, 
        "Skell Flight Module": {"class": ItemClassification.progression}, 
        "Frontier Nav": {"class": ItemClassification.progression}, 
        "BLADE Terminal": {"class": ItemClassification.progression}, 
        "Overdrive": {}, 
        "Shop Terminal": {}, 
        "Ls Shop": {}, 
        "AM Terminal": {}, 
    },
    "Field Skill": {
        "Mechanical": {"count": 4, "class": ItemClassification.progression},
        "Biological": {"count": 4, "class": ItemClassification.progression},
        "Archaeological": {"count": 4, "class": ItemClassification.progression},
    },
    "Skell": {
        "Urban 20": {"class": ItemClassification.progression},
    },
    "Skell Weapon": {

    },
    "Skell Superweapon": {

    },
    "Skell Augment": {

    },
    "Ground Augment": {

    },
    "Class": {

    },
    "Art": {

    },
    "Skill": {

    },
    "Heart": {
        "Gwin Heart": {"count": 5, "class": ItemClassification.progression},
        "Lao Heart": {"count": 5, "class": ItemClassification.progression},
    },
    # Needs verification, source was not credible
    "Data Probe": {
        "Mining G1": {"count": 20, "class": ItemClassification.progression},
        "Mining G2": {"count": 24},
        "Mining G3": {"count": 7},
        "Mining G4": {"count": 15},
        "Mining G5": {"count": 9},
        "Mining G6": {"count": 9},
        "Mining G7": {"count": 4},
        "Mining G8": {"count": 23},
        "Mining G9": {"count": 10},
        "Mining G10": {"count": 4},

        "Research G1": {"count": 3, "class": ItemClassification.progression},
        "Research G2": {"count": 4},
        "Research G3": {"count": 2},
        "Research G4": {"count": 6},
        "Research G5": {"count": 7},
        "Research G6": {"count": 3},

        "Booster G1": {"count": 3},
        "Booster G2": {"count": 3},
        "Storage": {"count": 11, "class": ItemClassification.progression},
        "Duplicator": {"count": 4},

        "Fuel Recovery": {"count": 3},
        "Melee Attack": {"count": 3},
        "Ranged Attack": {"count": 3},
        "EZ Debuff": {"count": 3},
        "Attribute Resistance": {"count": 3},
    },
}

def create_items(self):
    id = self.base_id
    for itemGroupName, itemGroup in xenobladeXItems.items():
        for itemName, item in itemGroup:
            # itemName = "[" + itemGroupName + "] "
            count = item["count"] if "count" in item else 1
            itemClassification = item["class"] if "class" in item else ItemClassification.useful
            for idx in range(count):
                appendix = " #" + str(idx) if idx > 1 else ""
                self.multiworld.itempool += XenobladeXItem(itemName + appendix, itemClassification, id, self.player)
                id += 1
