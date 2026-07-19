from rule_builder.rules import Has, Rule

important_item_rules: dict[str, Rule] = {
    "Conners Comm Device": Has("IMPIT: Conners Comm Device"),
    "Windshield Glass": Has("IMPIT: Windshield Glass"),
    "Bobbys Watch": Has("IMPIT: Bobbys Watch"),
    "Gnarlbranch Sap": Has("IMPIT: Gnarlbranch Sap"),
    "Legen-dar": Has("IMPIT: Legen-dar"),
    "Smelly Legen-dar": Has("IMPIT: Smelly Legen-dar"),
    "Slice of Bread": Has("IMPIT: Slice of Bread"),
    "Deep Blue Gem": Has("IMPIT: Deep Blue Gem"),
    "Stuffed Lobster": Has("IMPIT: Stuffed Lobster", 99),
    "Gold Nopopotamus Card": Has("IMPIT: Gold Nopopotamus Card"),
    "Natural Pearl": Has("IMPIT: Natural Pearl", 10),
    "White Gold Ore": Has("IMPIT: White Gold Ore"),
    "Briggss Key": Has("IMPIT: Briggss Key"),
    # "Fosdykes Key": Has("IMPIT: Fosdykes Key"),  # after the celeste three
    # "Moorehouses Key": Has("IMPIT: Moorehouses Key"),  # after the celeste three
    "Queggas Note": Has("IMPIT: Queggas Note"),
    "Keycard Lakeside Getaway": Has("IMPIT: Keycard - Lakeside Getaway"),
    "Ajoas ID Card": Has("IMPIT: Ajoas ID Card"),
    "Ice Cream Cake": Has("IMPIT: Ice Cream Cake"),
    "Malyteths Bottle": Has("IMPIT: Malyteths Bottle"),
    "Nopon Contract": Has("IMPIT: Nopon Contract", 4),
    "Nopon Gemstone": Has("IMPIT: Nopon Gemstone"),
    "Vi Sezhas Bracelet": Has("IMPIT: Vi Sezhas Bracelet"),
    "Ge Jewhes Dagger": Has("IMPIT: Ge Jewhes Dagger"),
    "Ringstone": Has("IMPIT: Ringstone"),
    "Zazazans Package": Has("IMPIT: Zazazans Package"),
    "Hazardous Container": Has("IMPIT: Hazardous Container"),
    "Hazardous Fuel Cell": Has("IMPIT: Hazardous Fuel Cell"),
    "Nios IOU": Has("IMPIT: Nios IOU"),
    "Sapphire Ring": Has("IMPIT: Sapphire Ring"),
    "Lumenoa Leaf": Has("IMPIT: Lumenoa Leaf"),
    "Gorkwa": Has("IMPIT: Gorkwa"),
    "Runtonams Right Arm": Has("IMPIT: Runtonams Right Arm"),
    "Troylans Gorkwa Fake": Has("IMPIT: Troylans Gorkwa Fake"),
    "White Whale Parts": Has("IMPIT: White Whale Parts", 3),
    "Ians ID Card": Has("IMPIT: Ians ID Card"),
    "Nalus Present": Has("IMPIT: Nalus Present"),
    "Dadapons Sunglasses": Has("IMPIT: Dadapons Sunglasses"),
    "Dodonga Treaty": Has("IMPIT: Dodonga Treaty"),
    "Dorian Treaty": Has("IMPIT: Dorian Treaty"),
    "Wrothian Part": Has("IMPIT: Wrothian Part", 3),
    "Med Kit NLA": Has("IMPIT: Med Kit NLA", 5),
    "Internment Camp Key": Has("IMPIT: Internment Camp Key"),
    # "Skell License": Has("IMPIT: Skell License"),  # after the skell license
    # "White Whale Parts_2": Has("IMPIT: White Whale Parts_2"),  # probably unused
    "L-002 Power Cable": Has("IMPIT: L-002 Power Cable", 3),
    "Skell License Certificate": Has("IMPIT: Skell License Certificate", 8),
    "Tissue Sample": Has("IMPIT: Tissue Sample"),
    "Mias Comm Device": Has("IMPIT: Mias Comm Device"),
    "Phosphorus-Tree Seed": Has("IMPIT: Phosphorus-Tree Seed", 6),
    "Container Key": Has("IMPIT: Container Key"),
    "Grenade Pizza": Has("IMPIT: Grenade Pizza"),
    "Frozen Pizza": Has("IMPIT: Frozen Pizza"),
    "Ajibas Key": Has("IMPIT: Ajibas Key"),
    "Mujibas Key": Has("IMPIT: Mujibas Key"),
    "Dancers Clothes": Has("IMPIT: Dancers Clothes"),
    "Crimson Tear": Has("IMPIT: Crimson Tear"),
    "New Weapon Blueprint": Has("IMPIT: New Weapon Blueprint"),
    "Summoning Goggles": Has("IMPIT: Summoning Goggles"),
    "Senirapa Water": Has("IMPIT: Senirapa Water"),
    "Zirtodiamond": Has("IMPIT: Zirtodiamond"),
    "Golboggas Disk": Has("IMPIT: Golboggas Disk"),
    "Tykki Sap": Has("IMPIT: Tykki Sap"),
    "Gray Keycard": Has("IMPIT: Gray Keycard"),
    "Rectangular Chest": Has("IMPIT: Rectangular Chest"),
    "Kutas Cargo": Has("IMPIT: Kutas Cargo"),
    "Aerozium": Has("IMPIT: Aerozium"),
    "Guardian Etherscale": Has("IMPIT: Guardian Etherscale"),
    "Mimeosome Left Arm": Has("IMPIT: Mimeosome Left Arm"),  # affinity mission arms and the men
    "L-002 Experimental Plant": Has("IMPIT: L-002 Experimental Plant"),
    "Reverends Journal": Has("IMPIT: Reverends Journal"),
    "Flemtide": Has("IMPIT: Flemtide", 5),
    "Floatstone Shard": Has("IMPIT: Floatstone Shard"),
    "Blood-Soaked Beast Fur": Has("IMPIT: Blood-Soaked Beast Fur"),
    "Laws Pendant": Has("IMPIT: Laws Pendant"),
    "Three Swords": Has("IMPIT: Three Swords"),
    "Data Unit FN093": Has("IMPIT: Data Unit FN093"),
    "Repair Kit": Has("IMPIT: Repair Kit"),
    "Aganeba Alloy": Has("IMPIT: Aganeba Alloy"),
    "Cockpit Wreckage": Has("IMPIT: Cockpit Wreckage"),
    "Engine Wreckage": Has("IMPIT: Engine Wreckage"),
    "Zu Pharg Wreckage": Has("IMPIT: Zu Pharg Wreckage", 3),
    "Data Unit FN094": Has("IMPIT: Data Unit FN094"),
    # "Mimeosome Head": Has("IMPIT: Mimeosome Head"),  # obtainable after yelvs partner
    # "Mimeosome Torso": Has("IMPIT: Mimeosome Torso"),  # obtainable after yelvs partner
    # required for yelvs partner. obtainable after arms and the man
    "Mimeosome Left Leg": Has("IMPIT: Mimeosome Left Leg"),
    # required for yelvs partner. obtainable after arms and the man
    "Mimeosome Right Leg": Has("IMPIT: Mimeosome Right Leg"),
    "First Barrier Key": Has("IMPIT: First Barrier Key"),
    "Cleansing Moss": Has("IMPIT: Cleansing Moss"),  # basic mission clean and green
    "Locket": Has("IMPIT: Locket"),  # basic mission lost memento
    "Star Sand": Has("IMPIT: Star Sand"),  # basic mission star sand seeker
    "Violet Crystal": Has("IMPIT: Violet Crystal"),  # basic mission a hard pill to swallow
    "Emerian Relic": Has("IMPIT: Emerian Relic"),  # basic mission the emerian battlegrounds
    "Missing Drive": Has("IMPIT: Missing Drive"),  # basic mission data recovery
    "Broken Data Probe": Has("IMPIT: Broken Data Probe"),  # basic mission a probing issue
    "Heart Stone": Has("IMPIT: Heart Stone"),  # basic mission straight from the heart
    "Mount Mgando Stone": Has("IMPIT: Mount Mgando Stone"),  # basic mission mount mgando mineralogy
    "Jelly Weeds": Has("IMPIT: Jelly Weeds"),  # basic mission in a jam
    "New-Weapon Remains": Has("IMPIT: New-Weapon Remains"),  # basic mission test data retrieval
    "Sampling Bottle": Has("IMPIT: Sampling Bottle"),
    # required for proficiency exam 4, which itself is just a skell license certificate
    "Solar Starship Map": Has("IMPIT: Solar Starship Map"),
    "Hamburger": Has("IMPIT: Hamburger"),
    "Hot Dog": Has("IMPIT: Hot Dog"),
    "Data Unit FN095": Has("IMPIT: Data Unit FN095"),
    "Data Unit FN096": Has("IMPIT: Data Unit FN096"),
    "Data Unit FN097": Has("IMPIT: Data Unit FN097"),
    "Practice Data Probe": Has("IMPIT: Practice Data Probe"),
    "Toxic Chemical Bomb": Has("IMPIT: Toxic Chemical Bomb"),
    "Med Kit Ganglion": Has("IMPIT: Med Kit Ganglion", 5),
    "Noble Silk": Has("IMPIT: Noble Silk"),
    "Data Unit FN098": Has("IMPIT: Data Unit FN098"),
    "Sword of Legendaryness": Has("IMPIT: Sword of Legendaryness"),
    "Unbreakable Sword": Has("IMPIT: Unbreakable Sword"),
    # "Voltant": Has("IMPIT: Voltant"),  # probably not required for the good thief
    "Keycard House of Cards": Has("IMPIT: Keycard - House of Cards"),
    "Troylans Gorkwa": Has("IMPIT: Troylans Gorkwa"),
    "Traditional Orphean Drug": Has("IMPIT: Traditional Orphean Drug"),
    "Weapon Test Data": Has("IMPIT: Weapon Test Data"),
    "Second Barrier Key": Has("IMPIT: Second Barrier Key"),
    "Third Barrier Key": Has("IMPIT: Third Barrier Key"),
    "Phogrium": Has("IMPIT: Phogrium"),
    "Massive Ring Fragment": Has("IMPIT: Massive Ring Fragment"),
    "Butte Ruin Fragments": Has("IMPIT: Butte Ruin Fragments"),
    "North Coast Riddle Rock": Has("IMPIT: North Coast Riddle Rock"),
    "Communication Data": Has("IMPIT: Communication Data"),
    "Medical Data": Has("IMPIT: Medical Data"),
}
