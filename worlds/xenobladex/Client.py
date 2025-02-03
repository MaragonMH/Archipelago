import asyncio
import os
import pathlib
import shutil
import sys
import zipfile
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import BaseServer
import socket
import random
import re
import urllib.parse
import Utils
from NetUtils import NetworkItem
from typing import Counter, List, NamedTuple, Optional, Set, cast
from itertools import groupby
import colorama

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, logger, get_base_parser
from settings import get_settings

from worlds.xenobladex import XenobladeXWorld
from .drops.item import dropItemData
from .drops.lot import dropLotData
from .drops.skill import dropSkillsData
from .items.dollFrames import doll_frame_ids
from .items.groundAugments import ground_augments_data
from .Items import game_type_item_to_offset
from .Locations import game_type_location_to_offset
from .Options import XenobladeXOption

CEMU_MODS_NOT_FOUND = "Unable to find the Cemu Mods please make sure to download the community mods" \
                      "within Cemu settings first"
CEMU_APPDATA_NOT_FOUND = "Unable to find the Cemu Appdata folder, please make sure to start Cemu once beforehand"
CEMU_APWORLD_NOT_FOUND = "Unable to find the Xenoblade X *.apworld"
CEMU_GRAPHIC_PACK_MISSING = "Unable to add the necessary graphic pack to Cemu." \
                            "Please check your installation directory and Cemu installation"
CEMU_SETTINGS_NOT_FOUND = "Cemu settings.xml file was not found." \
                          "Please check your installation directory and Cemu installation"
CEMU_NOT_FOUND = "Cemu was not found. Please check your installation directory and Cemu installation"


class GameItem(NamedTuple):
    type: int
    id: int
    level: int = 1


class XenobladeXHttpServer(HTTPServer):
    address_family = socket.AF_INET6
    locations = ""
    items = ""
    death_link = ""
    messages: List[str] = []
    upload_in_progress = False
    upload_count = 0
    upload_limit = 25

    def __init__(self, server_address, bind_and_activate=True, debug: bool = False) -> None:
        self.debug = debug
        super().__init__(server_address, XenobladeXHTTPRequestHandler, bind_and_activate)

    class Gear(NamedTuple):
        affix_1: int = 0
        affix_2: int = 0
        affix_3: int = 0
        slots: int = 0

    def generate_gear(self, item_name: Optional[str], seed_name: Optional[str]) -> Optional[Gear]:
        if not seed_name or not item_name or item_name not in dropItemData:
            return None
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
        if random.random() < dropLotData[affix_num_lot].lot1Prob / 100:
            affix_num += 1
        if random.random() < dropLotData[affix_num_lot].lot2Prob / 100:
            affix_num += 1
        if random.random() < dropLotData[affix_num_lot].lot3Prob / 100:
            affix_num += 1

        affixes = [0, 0, 0]
        for affix in range(affix_num):
            for skill in dropSkillsData[affix_lot]:
                if random.random() < skill.prob / 100 and affixes[affix] == 0:
                    affix_id = [x.name for x in ground_augments_data].index(skill.name)
                    if affix_id not in affixes:
                        affixes[affix] = affix_id

        slot_num = 0
        if random.random() < dropLotData[slot_lot].lot1Prob / 100:
            slot_num += 1
        if random.random() < dropLotData[slot_lot].lot2Prob / 100:
            slot_num += 1
        if random.random() < dropLotData[slot_lot].lot3Prob / 100:
            slot_num += 1

        return self.Gear(affixes[0], affixes[1], affixes[2], slot_num)

    def adjustTypeRange(self, item_game_type: int) -> int:
        if item_game_type == 0x1:
            return 5
        if item_game_type == 0x6:
            return 2
        if item_game_type == 0xa:
            return 5
        if item_game_type == 0xf:
            return 5
        if item_game_type == 0x14:
            return 2
        if item_game_type == 0x16:
            return 3
        return 1

    def clear_uploaded_items(self):
        self.items = ""
        self.upload_count = 0

    # Example: Invoke-WebRequest http://localhost:45872/items -Method POST -Body "I Tp=00000007 Id=00000039`n"
    def upload_item(self, item_game_type: int, item_game_id: int, seed_name: Optional[str],
                    item_name: str, player_name: str, item_game_level: int = 1):
        if self.upload_count > self.upload_limit:
            return
        self.upload_count += 1

        self.items += self._generate_message(f"From {player_name}", item_name)

        if item_game_type == 0:
            self.items += f"K Id={item_game_id:08x} Fg={1:08x}\n"
        elif item_game_type < 0x20:
            # Currently the exact type for multitype tables is not saved, so we need to distribute all possible types
            # This requires the game to reject every invalid type + item combination
            for item_game_type in range(item_game_type, item_game_type + self.adjustTypeRange(item_game_type)):
                gear = self.generate_gear(item_name, seed_name)
                if gear:
                    self.items += f"G Tp={item_game_type:08x} Id={item_game_id:08x} A1={gear.affix_1:08x}" \
                                  f"A2={gear.affix_2:08x} A3={gear.affix_3:08x} Sc={gear.slots:08x}\n"
                else:
                    if item_game_type == 0x9 and item_name in doll_frame_ids:
                        item_game_id = doll_frame_ids[item_name]
                    self.items += f"I Tp={item_game_type:08x} Id={item_game_id:08x}\n"
        elif item_game_type < 0x21:
            self.items += f"A Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x22:
            self.items += f"S Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x23:
            self.items += f"F Id={item_game_id:08x} Lv={item_game_level * 10:08x}\n"
        elif item_game_type < 0x24:
            self.items += f"D Id={item_game_id:08x} Lv={item_game_level + 1:08x}\n"
        elif item_game_type < 0x25:
            self.items += f"C Id={item_game_id:08x} Lv={10:08x}\n"

    def _match_line(self, data: list[GameItem], game_type: Optional[int], regex: str, min: int = 1,
                    max: int = 0xFFFF, has_lvl: bool = False, lvl_change=lambda lvl: lvl):
        match = re.findall(regex, self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        data += [GameItem(game_type if game_type is not None else entry[1], entry[0], 1000 if not has_lvl
                          else lvl_change(entry[1])) for entry in match if min <= entry[1] <= max]

    def upload_death(self):
        self.death_link += f"K Id={6:08x} Fg={1:08x}\n"

    def upload_message(self, heading: str, body: str):
        self.messages += [self._generate_message(heading, body)]

    def _sanitize_message(self, message: str) -> str:
        return re.sub(r"[^\w ]", "", message)

    def _generate_message(self, heading: str, body: str):
        return f"M {self._sanitize_message(heading)}\r{(self._sanitize_message(body))[:60]}\n"

    def download_locations(self) -> list[GameItem]:
        locations: list[GameItem] = []
        if self.upload_in_progress:
            return locations

        self._match_line(locations, 0, r'^CP Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(locations, 1, r'^EN Id=([0-9a-fA-F]{3}) Dc=([0-9a-fA-F]{1})\n', min=2)
        self._match_line(locations, 2, r'^FN Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n')
        self._match_line(locations, 3, r'^SG Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n', min=2)
        self._match_line(locations, 4, r'^LC Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) Tp=[0-9a-fA-F]{1}\n')

        return locations

    def _match_line_augment(self, data: list[GameItem], game_type: int, regex: str, lower: int = 1, upper: int = 0xFFFF,
                            has_type: bool = False):
        starting_index = 1 if has_type else 0
        match = re.findall(regex, self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        data += [GameItem(game_type, entry[i]) for entry in match if not has_type or lower <= entry[0] <= upper
                 for i in range(starting_index + 3) if 0 < entry[i] < 0xFFFF]

    def download_items(self) -> list[GameItem]:
        items: list[GameItem] = []
        if self.upload_in_progress:
            return items

        self._match_line(items, 0, r'^KY Id=([1-9a-fA-F]{1}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(items, None, r'^IT Id=([0-9a-fA-F]{3}) Tp=([0-9a-fA-F]{2})(?:\n| S1Id)')
        self._match_line(items, 0x1c, r'^IT Id=([0-9a-fA-F]{3}) Tp=1[cC] Cn=([0-9a-fA-F]{3})', has_lvl=True)
        equip_regex = r'^EQ CId=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})'
        self._match_line(items, 0x6, equip_regex, min=0, max=2)
        self._match_line(items, 0x1, equip_regex, min=3)
        doll_regex = r'^DL GIx=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})'
        self._match_line(items, 0xf, doll_regex, min=0, max=0x9)
        self._match_line(items, 0x9, doll_regex, min=0xa, max=0xa)
        self._match_line(items, 0xa, doll_regex, min=0xb)
        augment_regex = r'^IT .*Tp=([0-9a-fA-F]{2}).*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})'
        self._match_line_augment(items, 0x14, augment_regex, lower=1, upper=7)
        self._match_line_augment(items, 0x14,
                                 r'^EQ .*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})')
        self._match_line_augment(items, 0x16, augment_regex, lower=0xa, upper=0x13)
        self._match_line_augment(items, 0x16,
                                 r'^DL .*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})')
        self._match_line(items, 0x20, r'^AT Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')
        self._match_line(items, 0x21, r'^SK Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')
        self._match_line(items, 0x22, r'^FD Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{2}) Ch=.*\n',
                         has_lvl=True, lvl_change=lambda lvl: lvl / 10 if lvl else 0)
        self._match_line(items, 0x23, r'^FS Id=([0-9a-fA-F]{1}) Lv=([0-9a-fA-F]{1})\n',
                         has_lvl=True, lvl_change=lambda lvl: lvl - 1)
        self._match_line(items, 0x24, r'^CL Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')

        return items

    def download_death(self) -> bool:
        if self.upload_in_progress:
            return False
        pattern = r'^KY Id=6 .*\n'
        result: bool = re.match(pattern, self.locations) is not None
        re.sub(pattern, "", self.locations)
        if result:
            self.upload_message("Deathlink", "Sent death")
        return result


class XenobladeXHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server: BaseServer) -> None:
        self.http_server: XenobladeXHttpServer = cast(XenobladeXHttpServer, server)
        super().__init__(request, client_address, server)

    def respond_success(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def get_items(self):
        self.respond_success()
        messages = "".join(self.http_server.messages[-4:])
        self.http_server.messages = self.http_server.messages[:-4]
        items_text = self.http_server.items + self.http_server.death_link + messages
        self.wfile.write(items_text.encode())
        self.http_server.items = ""
        self.http_server.death_link = ""

    def post_locations(self):
        locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":", "\n")
        self.respond_success()
        if "^" in locations[0]:
            self.http_server.upload_in_progress = True
            self.http_server.locations = ""
            locations = locations[1:]
        upload_ended = "$" in locations[-1]
        if upload_ended:
            locations = locations[0:-2]
        self.http_server.locations += locations
        if upload_ended:
            self.http_server.upload_in_progress = False

    # Silence connection request logging
    def log_request(self, code='-', size='-'):
        return

    def debug_get_locations(self):
        self.respond_success()
        self.wfile.write(self.http_server.locations.encode())

    def debug_post_items(self):
        self.http_server.items += (self.rfile.read(int(self.headers['content-length']))).decode('cp437')
        self.respond_success()

    def do_GET(self):
        if self.path == "/items":
            self.get_items()
        if self.path == "/locations" and self.http_server.debug:
            self.debug_get_locations()

    def do_POST(self):
        if self.path == "/locations":
            self.post_locations()
        if self.path == "/items" and self.http_server.debug:
            self.debug_post_items()


class XenobladeXContext(CommonContext):
    game = "Xenoblade X"
    items_handling = 0b111  # get items from your own world
    want_slot_data = True

    connected = False
    cemu_process: Optional[subprocess.Popen[bytes]] = None
    locations_checked: Set[int]

    def __init__(self, server_address: Optional[str], password: Optional[str], debug: bool = False) -> None:
        self.http_server = XenobladeXHttpServer(('::', 45872), debug=debug)
        super().__init__(server_address, password)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(XenobladeXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super(XenobladeXContext, self).disconnect(allow_autoreconnect)
        self.connected = False

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args.get('slot_data', None)
            if slot_data:
                cemu_options: list[XenobladeXOption] = [XenobladeXOption(**option)
                                                        for option in slot_data["cemu_options"]]
                options: dict[str, int] = slot_data["options"]
                if options["death_link"]:
                    self.tags.add("DeathLink")
                else:
                    self.tags.discard("DeathLink")
                self.prepare_cemu(cemu_options)
                self.connected = True

    def on_deathlink(self, data: dict):
        if "DeathLink" in self.tags:
            death_source = data["source"]
            self.http_server.upload_death()
            self.http_server.upload_message(f"From {death_source}", "Death")
        super().on_deathlink(data)

    def on_print_json(self, args: dict):
        print_type = args.get("type", "")
        if print_type in ["ItemSend", "ItemCheat", "Hint"]:
            item: NetworkItem = args["item"]
            sender = item.player
            receiver = args["receiving"]
            if (not self.slot_concerns_self(receiver)) and self.slot_concerns_self(sender):
                self.http_server.upload_message(f"To {self.player_names[receiver]}",
                                                self.archipelago_item_to_name(item.item))
        elif print_type == "Chat":
            chatting_player = self.player_names[args["slot"]]
            self.http_server.upload_message(f"From {chatting_player}", args["message"])
        elif print_type == "ServerChat":
            self.http_server.upload_message("From Server", args["message"])
        elif print_type == "Join":
            self.http_server.upload_message("Joined", self.player_names[args["slot"]])
        elif print_type == "Part":
            self.http_server.upload_message("Disconnected", self.player_names[args["slot"]])
        elif print_type == "Goal":
            self.http_server.upload_message("Reached Goal", self.player_names[args["slot"]])
        super(XenobladeXContext, self).on_print_json(args)

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

    def archipelago_item_to_name(self, archipelago_item_id: int) -> str:
        return re.sub(r"^[A-Z]*?: ", "", XenobladeXWorld.item_id_to_name[archipelago_item_id])

    def archipelago_item_to_game_item(self, archipelago_item_id: int) -> GameItem:
        game_item_type_offset = max([id for id in game_type_item_to_offset.values()
                                     if id < archipelago_item_id - XenobladeXWorld.base_id])
        game_item_type = min([key for key, offset in game_type_item_to_offset.items()
                              if offset == game_item_type_offset])
        return GameItem(game_item_type, (archipelago_item_id - XenobladeXWorld.base_id) - game_item_type_offset)

    def game_item_to_archipelago_item(self, game_item: GameItem) -> int:
        return XenobladeXWorld.base_id + game_type_item_to_offset[game_item.type] + game_item.id

    def game_location_to_archipelago_location(self, game_location: GameItem) -> int:
        return XenobladeXWorld.base_id + game_type_location_to_offset[game_location.type] + game_location.id

    async def download_game_locations(self) -> None:
        game_locations = {self.game_location_to_archipelago_location(location)
                          for location in self.http_server.download_locations()}
        new_locations = game_locations.difference(self.locations_checked)
        if new_locations:
            await self.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])
            self.locations_checked = game_locations

    def upload_game_items(self) -> None:
        self.http_server.clear_uploaded_items()
        uploaded_server_items = self.http_server.download_items()
        uploaded_items = {self.game_item_to_archipelago_item(itm): itm.level for itm in uploaded_server_items}
        player_item_names = {net_item.item: self.player_names[net_item.player] for net_item in self.items_received}
        server_items = Counter(network_item.item for network_item in self.items_received)
        for item, level in server_items.items():
            uploaded_level = uploaded_items.get(item, 0)
            if level <= uploaded_level:
                continue
            game_item = self.archipelago_item_to_game_item(item)
            item_name = self.archipelago_item_to_name(item)
            self.http_server.upload_item(game_item.type, game_item.id, self.seed_name,
                                         item_name, player_item_names[item], level)

    def prepare_cemu(self, options: list[XenobladeXOption]):
        try:
            mod_path = "graphicPacks/downloadedGraphicPacks/XenobladeChroniclesX/Mods/"
            appdata = None
            if Utils.is_windows:
                appdata = os.getenv('APPDATA')
            elif Utils.is_linux:
                appdata = os.path.join(pathlib.Path.home(), ".local/share")
            if not appdata:
                raise Exception(CEMU_APPDATA_NOT_FOUND)
            cemu_appdata_path = os.path.join(appdata, "Cemu")
            if not os.path.isdir(cemu_appdata_path):
                raise Exception(CEMU_SETTINGS_NOT_FOUND)
            else:
                self.copy_cemu_files(cemu_appdata_path, mod_path)
                self.set_cemu_graphic_packs(cemu_appdata_path, mod_path, options)
                self.open_cemu()
        except Exception as e:
            logger.exception(str(e))
            logger.error(str(e))
            self.gui_error(str(e), e)
            self.exit_event.set()

    def copy_cemu_files(self, cemu_path: str, mod_path: str):
        archipelago_graphic_pack_path = "worlds/xenobladex/cemu_graphicpack/"
        cemu_mod_path = os.path.join(cemu_path, mod_path)
        cemu_ap_path = os.path.join(cemu_mod_path, "AP")
        if not os.path.isdir(cemu_mod_path):
            raise Exception(CEMU_MODS_NOT_FOUND)
        if not os.path.exists(cemu_ap_path):
            os.makedirs(cemu_ap_path)
        if not os.path.isdir(archipelago_graphic_pack_path):
            self.copy_from_apworld(cemu_ap_path)
            return
        try:
            shutil.copytree(archipelago_graphic_pack_path, cemu_ap_path, dirs_exist_ok=True)
        except Exception:
            raise Exception(CEMU_GRAPHIC_PACK_MISSING)

    def copy_from_apworld(self, cemu_ap_path: str):
        try:
            zip_path = XenobladeXWorld.zip_path
            if not zip_path:
                raise
            with zipfile.ZipFile(zip_path, "r") as z:
                for file in z.namelist():
                    filename = os.path.basename(file)
                    if file.startswith("xenobladex/cemu_graphicpack/") and filename:
                        z.getinfo(file).filename = filename
                        z.extract(file, cemu_ap_path)
        except Exception:
            raise Exception(CEMU_APWORLD_NOT_FOUND)

    def set_cemu_graphic_packs(self, cemu_path: str, mod_path: str, options: list[XenobladeXOption]):
        settings_path = os.path.join(cemu_path, "settings.xml")
        try:
            with open(settings_path, "r") as file:
                filedata = file.read()

            # Group by cemu pack
            sorted_options = sorted(options, key=lambda option: option.cemu_pack)
            grouped_options = [list(result) for key, result
                               in groupby(sorted_options, key=lambda option: option.cemu_pack)]

            for settings in grouped_options:
                cemu_pack: str = settings[0].cemu_pack

                # Cleanup
                pack_regex = rf'<Entry filename="{mod_path}{cemu_pack}/rules.txt"(/>\n|>.*?</Entry>\n)'
                filedata = re.sub(pack_regex, "", filedata, flags=re.DOTALL)

                # Abort whenever a single setting of a pack is off
                if any(setting.cemu_selection == "off" for setting in settings):
                    continue

                # Addition
                content = ""
                for setting in settings:
                    if setting.cemu_option != "":
                        category = f"<category>{setting.cemu_option}</category>" \
                                   if setting.cemu_option != "Active preset" else ""
                        content += f"<Preset>\n{category}<preset>{setting.cemu_selection}</preset>\n</Preset>\n"
                pack_content = (f'<Entry filename="{mod_path}{cemu_pack}/rules.txt">\n{content}</Entry>\n\n')
                filedata = re.sub(r'</GraphicPack>', f"{pack_content}</GraphicPack>", filedata)

            with open(settings_path, "w") as file:
                file.write(filedata)
        except Exception:
            raise Exception(CEMU_SETTINGS_NOT_FOUND)

    def open_cemu(self):
        try:
            cemu_exe = get_settings()["xenobladex_options"]["executable"]
            if not self.cemu_process or self.cemu_process.poll() is not None:
                self.cemu_process = subprocess.Popen(cemu_exe)
        except Exception:
            raise Exception(CEMU_NOT_FOUND)


async def xenoblade_x_sync_task(ctx: XenobladeXContext) -> None:
    while not ctx.exit_event.is_set():
        if ctx.connected:
            if "DeathLink" in ctx.tags and ctx.http_server.download_death():
                await ctx.send_death()
            await ctx.download_game_locations()
            ctx.upload_game_items()
        await asyncio.sleep(0.5)


async def main(args) -> None:
    Utils.init_logging("XenobladeXClient", exception_logger="Client")

    # handle if launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            args.connect = url.netloc
            if url.username:
                args.name = urllib.parse.unquote(url.username)
            if url.password:
                args.password = urllib.parse.unquote(url.password)
        else:
            logger.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    ctx = XenobladeXContext(args.connect, args.password, args.debug)
    ctx.auth = args.name
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    asyncio.get_event_loop().run_in_executor(None, ctx.http_server.serve_forever)
    sync_task = asyncio.create_task(xenoblade_x_sync_task(ctx))

    await ctx.exit_event.wait()

    ctx.server_address = None
    await asyncio.get_event_loop().run_in_executor(None, ctx.http_server.shutdown)
    await sync_task
    await ctx.shutdown()


def launch(*args) -> None:
    parser = get_base_parser()
    parser.add_argument("-d", "--debug", action="store_true", help="Enable full server exposure for debugging purposes")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    launch(*sys.argv[1:])
