import asyncio
import os
import shutil
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import re
import Utils
from typing import NamedTuple, Optional
import colorama

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, logger, get_base_parser
import Utils

from worlds.xenobladeX import XenobladeXWorld
from worlds.xenobladeX.drops.item import dropItemData
from worlds.xenobladeX.drops.lot import dropLotData
from worlds.xenobladeX.drops.skill import dropSkillsData
from worlds.xenobladeX.items.groundAugments import ground_augments_data
from worlds.xenobladeX.Items import game_type_item_to_offset
from worlds.xenobladeX.Locations import game_type_location_to_offset

CEMU_GRAPHIC_PACK_MISSING = "Unable to add the necessary graphic pack to Cemu. Please check your installation directory and Cemu installation"
CEMU_SETTINGS_NOT_FOUND = "Cemu settings.xml file was not found. Please check your installation directory and Cemu installation"
CEMU_NOT_FOUND = "Cemu was not found. Please check your installation directory and Cemu installation"

class GameItem(NamedTuple):
    type: int
    id: int
    level: int = 1

class XenobladeXHttpServer(HTTPServer):
    locations = ""
    items = ""
    upload_in_progress = False

    def __init__(self, server_address, bind_and_activate = True, debug:bool = False) -> None:
        self.debug = debug
        super().__init__(server_address, XenobladeXHTTPRequestHandler, bind_and_activate)

    class Gear(NamedTuple):
        affix_1: int = 0
        affix_2: int = 0
        affix_3: int = 0
        slots: int = 0

    def generate_gear(self, item_name:Optional[str], seed_name:Optional[str]) -> Optional[Gear]:
        if not seed_name or not item_name or item_name not in dropItemData: return None
        random.seed(seed_name + item_name)

        affix_lot = dropItemData[item_name].affixLot
        affix_num_lot = dropItemData[item_name].affixNumLot
        slot_lot = dropItemData[item_name].slotNumLot
        # set good lot at 5%, which is the minimum value used in game
        # it is way to complex to calculate the exact rate, because that depends on the enemy that droped it
        # check gold lot https://xenoblade.github.io/xbx/bdat/common_local_us/DRP_LotRankTable.html for all values
        if random.random() < 0.05:
            affix_lot = dropItemData[item_name].affixLotGood
            affix_num_lot = dropItemData[item_name].affixNumLotGood
            slot_lot = dropItemData[item_name].slotNumLotGood
        
        affix_num = 0
        if random.random() < dropLotData[affix_num_lot].lot1Prob / 100: affix_num += 1
        if random.random() < dropLotData[affix_num_lot].lot2Prob / 100: affix_num += 1
        if random.random() < dropLotData[affix_num_lot].lot3Prob / 100: affix_num += 1

        affixes = [0,0,0]
        for affix in range(affix_num):
            for skill in dropSkillsData[affix_lot]:
                if random.random() < skill.prob / 100 and affixes[affix] == 0:
                    affix_id = [x.name for x in ground_augments_data].index(skill.name)
                    if affix_id not in affixes: affixes[affix] = affix_id

        slot_num = 0
        if random.random() < dropLotData[slot_lot].lot1Prob / 100: slot_num += 1
        if random.random() < dropLotData[slot_lot].lot2Prob / 100: slot_num += 1
        if random.random() < dropLotData[slot_lot].lot3Prob / 100: slot_num += 1

        return self.Gear(affixes[0], affixes[1], affixes[2], slot_num)

    def adjustTypeRange(self, item_game_type: int) -> int:
        if item_game_type == 0x1: return 5
        if item_game_type == 0x6: return 2
        if item_game_type == 0xa: return 5
        if item_game_type == 0xf: return 5
        if item_game_type == 0x14: return 2
        if item_game_type == 0x16: return 3
        return 1

    def upload_item(self, item_game_type:int, item_game_id:int, seed_name:Optional[str], item_name:Optional[str], item_game_level:int = 1):
        if item_game_type == 0:
            self.items += f"K Id={item_game_id:08x} Fg={1:08x}\n"
        elif item_game_type < 0x20:
            # Currently the exact type for multitype tables is not saved, so we need to distribute all possible types
            # This requires the game to reject every invalid type + item combination
            for item_game_type in range(item_game_type, item_game_type + self.adjustTypeRange(item_game_type)):
                gear = self.generate_gear(item_name, seed_name)
                if gear:
                    self.items += f"G Tp={item_game_type:08x} Id={item_game_id:08x} A1={gear.affix_1:08x} A2={gear.affix_2:08x} A3={gear.affix_3:08x} Sc={gear.slots:08x}\n"
                else:
                    self.items += f"I Tp={item_game_type:08x} Id={item_game_id:08x}\n"
        elif item_game_type < 0x21:
            self.items += f"A Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x22:
            self.items += f"S Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x23:
            self.items += f"F Id={item_game_id:08x} Lv={item_game_level*10:08x}\n"
        elif item_game_type < 0x24:
            self.items += f"D Id={item_game_id:08x} Lv={item_game_level:08x}\n"
        elif item_game_type < 0x25:
            self.items += f"C Id={item_game_id:08x} Lv={10:08x}\n"

    def _match_line(self, data:list[GameItem], game_type:Optional[int], regex:str, min:int = 1, 
            max:int = 0xFFFF, has_lvl:bool = False):
        match = re.findall(regex, self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        data += [GameItem(game_type if game_type is not None else entry[1], entry[0], 1 if not has_lvl else entry[1]) 
            for entry in match if min <= entry[1] <= max]

    def download_locations(self) -> list[GameItem]:
        locations = []
        if self.upload_in_progress:
            return locations

        self._match_line(locations, 0, r'^CP Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(locations, 1, r'^EN Id=([0-9a-fA-F]{3}) Dc=([0-9a-fA-F]{1})\n', min=2)
        self._match_line(locations, 2, r'^FN Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n')
        self._match_line(locations, 3, r'^SG Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n')
        self._match_line(locations, 4, r'^LC Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) Tp=[0-9a-fA-F]{1}\n')

        return locations

    def _match_line_augment(self, data:list[GameItem], game_type:int, regex:str, lower:int = 1, upper:int = 0xFFFF,
            has_type: bool = False):
        starting_index = 1 if has_type else 0
        match = re.findall(regex, self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        data += [GameItem(game_type, entry[i]) for entry in match if not has_type or lower <= entry[0] <= upper
            for i in range(starting_index + 3) if 0 < entry[i] < 0xFFFF]

    def download_items(self) -> list[GameItem]:
        items = []
        if self.upload_in_progress:
            return items

        self._match_line(items, 0, r'^KY Id=([1-9a-fA-F]{1}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(items, None, r'^IT Id=([0-9a-fA-F]{3}) Tp=([0-9a-fA-F]{2})(?:\n| S1Id)')
        self._match_line(items, 0x1c, r'^IT Id=([0-9a-fA-F]{3}) Tp=1[cC] Cn=([0-9a-fA-F]{2})', has_lvl=True)
        equip_regex = r'^EQ CId=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})'
        self._match_line(items, 0x6, equip_regex, min=0, max=2)
        self._match_line(items, 0x1, equip_regex, min=3)
        doll_regex = r'^DL GIx=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})'
        self._match_line(items, 0xf, doll_regex, min=0, max=0x9)
        self._match_line(items, 0x9, doll_regex, min=0xa, max=0xa)
        self._match_line(items, 0xa, doll_regex, min=0xb)
        augment_regex = r'^IT .*Tp=([0-9a-fA-F]{2}).*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})'
        self._match_line_augment(items, 0x14, augment_regex, lower=1, upper=7)
        self._match_line_augment(items, 0x14, r'^EQ .*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})')
        self._match_line_augment(items, 0x16, augment_regex, lower=0xa, upper=0x13)
        self._match_line_augment(items, 0x16, r'^DL .*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})')
        self._match_line(items, 0x20, r'^AT Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')
        self._match_line(items, 0x21, r'^SK Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')
        self._match_line(items, 0x22, r'^FS Id=([0-9a-fA-F]{1}) Lv=([0-9a-fA-F]{1})\n', has_lvl=True)
        self._match_line(items, 0x23, r'^FD Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{2}) Ch=.*\n', has_lvl=True)
        self._match_line(items, 0x24, r'^CL Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')

        return items

    def download_death(self) -> bool:
        if self.upload_in_progress:
            return False
        pattern = r'^KY Id=6 .*\n'
        result:bool = re.match(pattern, self.locations) is not None
        re.sub(pattern, "", self.locations)
        return result


class XenobladeXHTTPRequestHandler(BaseHTTPRequestHandler):
    server:XenobladeXHttpServer

    def respond_success(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def get_items(self):
        self.respond_success()
        # remove duplicate lines
        self.server.items = "\n".join(set(self.server.items.split("\n")))
        self.wfile.write(self.server.items.encode())
        self.server.items = ""

    def post_locations(self):
        locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":","\n")
        self.respond_success()
        if "^" in locations[0]:
            self.server.upload_in_progress = True
            self.server.locations = ""
            locations = locations[1:]
        upload_ended = "$" in locations[-1]
        if upload_ended:
            locations = locations[0:-2]
        self.server.locations += locations
        if upload_ended:
            self.server.upload_in_progress = False
        logger.debug("Received LOCATION: " + locations[0:2] + " Lines: " + str(locations.count('\n')) +
            " FileLines: " +  str(self.server.locations.count('\n')))

    # Silence connection request logging
    def log_request(self, code='-', size='-'): return

    def debug_get_locations(self):
        self.respond_success()
        self.wfile.write(self.server.locations.encode())

    def debug_post_items(self):
        self.server.items = (self.rfile.read(int(self.headers['content-length']))).decode('cp437')
        self.respond_success()

    def do_GET(self):
        if self.path == "/items":
            self.get_items()
        if self.path == "/locations" and self.server.debug:
            self.debug_get_locations()

    def do_POST(self):
        if self.path == "/locations":
            self.post_locations()
        if self.path == "/items" and self.server.debug:
            self.debug_post_items()



class XenobladeXContext(CommonContext):
    tags = {"AP", "XenobladeX"}
    game = "XenobladeX"
    items_handling = 0b111  # get items from your own world
    want_slot_data = True

    def __init__(self, server_address: Optional[str], password: Optional[str], debug: bool) -> None:
        self.http_server = XenobladeXHttpServer(('localhost', 45872), debug=debug)
        super().__init__(server_address, password)

    # get from slot data
    options:dict[str,str] = {}

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(XenobladeXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args.get('slot_data', None)
            if slot_data:
                self.options = slot_data.get("options", {})
                if slot_data.get("death_link", False): self.tags.add("DeathLink")
                else: self.tags.discard("DeathLink")
                self.prepare_cemu()

    def on_deathlink(self, data: dict):
        if "DeathLink" in self.tags:
            self.http_server.upload_item(item_game_type=0, item_game_id=6, seed_name=self.seed_name, item_name=None)
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager
        class XenobladeXManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Xenoblade X Client"

        self.ui = XenobladeXManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


    def get_level(self, archipelago_item_id: int) -> int:
        return len([item.item for item in self.items_received if item.item == archipelago_item_id])
    
    def archipelago_item_to_name(self, archipelago_item_id:int) -> str:
        return re.sub(r"^[A-Z]*?: ", "",XenobladeXWorld.item_id_to_name[archipelago_item_id])
    
    def archipelago_item_to_game_item(self, archipelago_item_id: int) -> GameItem:
        game_item_type = max([id for id in game_type_item_to_offset.values() if id <= archipelago_item_id - XenobladeXWorld.base_id])
        return GameItem(game_item_type, ((archipelago_item_id - XenobladeXWorld.base_id) // game_item_type))

    def game_item_to_archipelago_item(self, game_item:GameItem) -> int:
        return XenobladeXWorld.base_id + game_type_item_to_offset[game_item.type] + game_item.id

    def game_location_to_archipelago_location(self, game_location:GameItem) -> int:
        return XenobladeXWorld.base_id + game_type_location_to_offset[game_location.type] + game_location.id


    def download_game_locations(self) -> None:
        game_locations = {self.game_location_to_archipelago_location(location) for location in self.http_server.download_locations()}
        self.locations_checked.update(game_locations)


    def upload_game_items(self) -> None:
        uploaded_items = self.http_server.download_items()
        server_items = {network_item.item for network_item in self.items_received if self.slot_concerns_self(network_item.player)}
        for item in server_items:
            game_level = next(itm for itm in uploaded_items if item == self.game_item_to_archipelago_item(itm)).level
            archipelago_level = self.get_level(item)
            if archipelago_level <= game_level: continue
            game_item = self.archipelago_item_to_game_item(item)
            self.http_server.upload_item(game_item.type, game_item.id, self.seed_name, self.archipelago_item_to_name(item), archipelago_level)

    def prepare_cemu(self):
        cemu_path = Utils.get_options()["xenobladeX_options"]["cemu_path"]
        mod_path = "graphicPacks/downloadedGraphicPacks/XenobladeChroniclesX/Mods/"
        self.copy_cemu_files(cemu_path, mod_path)
        self.set_cemu_graphic_packs(cemu_path, mod_path)
        self.open_cemu(cemu_path)

    def copy_cemu_files(self, cemu_path:str, mod_path:str):
        archipelago_graphic_pack_path = "worlds/xenobladeX/cemuGraphicPack/"
        if not os.path.exists(archipelago_graphic_pack_path): 
            archipelago_graphic_pack_path = "lib/" + archipelago_graphic_pack_path
            if not os.path.exists(archipelago_graphic_pack_path):
                logger.error(CEMU_GRAPHIC_PACK_MISSING)
                return
        try:
            shutil.copytree(archipelago_graphic_pack_path, cemu_path + mod_path + "AP/", dirs_exist_ok=True)
        except:
            logger.error(CEMU_GRAPHIC_PACK_MISSING)

    def set_cemu_graphic_packs(self, cemu_path:str, mod_path:str):
        settings_path = cemu_path + "Settings.xml"
        try:
            file_path = Utils.local_path(settings_path)
            with open(file_path, "r") as file :
                filedata = file.read()

            # Cleanup
            for pack_name in {pack.rsplit("/", 1)[0] for pack in self.options}:
                pack_regex = rf'<Entry filename="{mod_path}{pack_name}/rules.txt"(/>\n|>.*?</Entry>\n)'
                filedata = re.sub(pack_regex, "", filedata, flags=re.DOTALL)

            cemu_packs = {pack.rsplit("/", 1)[0] : {pack.rsplit("/", 1)[1]: value} for pack, value in self.options.items() if value != "off"}

            # Addition
            for pack_name, categories in cemu_packs.items():
                content = "".join([f'<Preset>\n{f"<category>{pack_category}</category>" if pack_category != "Active preset" else ""}<preset>{category_value}</preset>\n</Preset>\n' 
                    for pack_category, category_value in categories.items()])
                pack_content = (f'<Entry filename="{mod_path}{pack_name}/rules.txt">\n{content}</Entry>\n\n')
                filedata = re.sub(rf'</GraphicPack>', f"{pack_content}</GraphicPack>", filedata)
                filedata = re.sub(rf'<GraphicPack/>', f"<GraphicPack>\n{pack_content}</GraphicPack>", filedata)

            with open(settings_path, "w") as file:
                file.write(filedata)
        except FileNotFoundError:
            logger.error(CEMU_SETTINGS_NOT_FOUND)

    def open_cemu(self, cemu_path):
        try: 
            subprocess.Popen(cemu_path + "Cemu")
        except FileNotFoundError:
            logger.error(CEMU_NOT_FOUND)


async def xenoblade_x_sync_task(ctx: XenobladeXContext) -> None:
    while not ctx.exit_event.is_set():
        if "DeathLink" in ctx.tags and ctx.http_server.download_death():
            await ctx.send_death()
        ctx.download_game_locations()
        ctx.upload_game_items()
        await asyncio.sleep(0.5)


async def main() -> None:
    parser = get_base_parser()
    parser.add_argument('--log_level', default='info', help='Sets log level')
    parser.add_argument("-d", "--debug", action="store_true", help="Enable full server exposure for debugging purposes")
    args = parser.parse_args()

    Utils.init_logging("XenobladeXClient", exception_logger="Client", loglevel=args.log_level)

    ctx = XenobladeXContext(args.connect, args.password, args.debug)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    asyncio.get_event_loop().run_in_executor(None, ctx.http_server.serve_forever)
    sync_task = asyncio.create_task(xenoblade_x_sync_task(ctx))

    await ctx.exit_event.wait()

    ctx.server_address = None
    logger.debug("waiting for game server task to end")
    await asyncio.get_event_loop().run_in_executor(None, ctx.http_server.shutdown)
    logger.debug("waiting for sync task to end")
    await sync_task
    await ctx.shutdown()


if __name__ == "__main__":
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
