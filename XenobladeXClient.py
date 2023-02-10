import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import Utils
from typing import NamedTuple, Optional
import colorama

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, logger, get_base_parser
import Utils

CEMU_SETTINGS_NOT_FOUND = "Cemu settings.xml file was not found. Please check your installation directory and Cemu installation"

class GameItem(NamedTuple):
    type: int
    id: int
    level: int = 1

class XenobladeXHttpServer(HTTPServer):
    locations = ""
    items = ""
    upload_in_progress = False

    def upload_item(self, item_game_type:int, item_game_id:int, item_game_level:int = 1):
        if item_game_type == 0:
            self.items += f"K Id={item_game_id:08x} Fg={1:08x}\n"
        elif item_game_type < 0x20:
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
        return re.match(r'^KY Id=0 Fg=1\n', self.locations) is not None


class XenobladeXHTTPRequestHandler(BaseHTTPRequestHandler):
    server:XenobladeXHttpServer

    def get_items(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        # remove duplicate lines
        self.server.items = "\n".join(set(self.server.items.split("\n")))
        self.wfile.write(self.server.items.encode())
        self.server.items = ""

    def post_locations(self):
        locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":","\n")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
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

    def do_GET(self):
        if self.path == '/items':
            self.get_items()

    def do_POST(self):
        if self.path == '/locations':
            self.post_locations()


class XenobladeXContext(CommonContext):
    tags = {"AP", "XenobladeX"}
    game = "XenobladeX"
    items_handling = 0b011  # get items from your own world
    want_slot_data = True
    http_server = XenobladeXHttpServer(('localhost', 45872), XenobladeXHTTPRequestHandler)
    connected = False
    death_link_pending = False
    death_link_enabled = False

    # get from slot data
    options:dict[str,str] = {}
    game_type_item_to_offset:dict[int, int] = {}
    game_type_location_to_offset:dict[int, int] = {}
    

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(XenobladeXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args.get('slot_data', None)
            if slot_data:
                self.game_type_item_to_offset = slot_data.get("game_type_item_to_offset",{})
                self.game_type_location_to_offset = slot_data.get("game_type_location_to_offset", {})
                self.options = slot_data.get("options", {})
                self.death_link_enabled = slot_data.get("death_link_enabled", False)
                self.set_cemu_graphic_packs()
                self.connected = True

    def on_deathlink(self, data: dict):
        if self.connected and self.death_link_enabled:
            self.death_link_pending = True
            self.http_server.upload_item(item_game_type=0, item_game_id=0)
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

    def archipelago_item_to_game_item(self, archipelago_item_id: int) -> GameItem:
        game_item_type = max([id for id in self.game_type_item_to_offset.values() if id <= archipelago_item_id])
        return GameItem(game_item_type, (archipelago_item_id // game_item_type))

    def game_item_to_archipelago_item(self, game_item:GameItem) -> int:
        return self.game_type_item_to_offset[game_item.type] + game_item.id

    def game_location_to_archipelago_location(self, game_location:GameItem) -> int:
        return self.game_type_location_to_offset[game_location.type] + game_location.id


    def download_game_locations(self) -> None:
        # Get all the locations from the game and
        # Calc the differance between those and the server and
        # Send them to the server
        game_locations = {self.game_location_to_archipelago_location(location) for location in self.http_server.download_locations()}
        self.locations_checked.update(game_locations)
        return


    def upload_game_items(self) -> None:
        # Get all the items in locations from the game and
        # Get all the items from the server and
        # Calc the differance between those and
        # Add items to the game
        # Big problem here is, if you are able to get rid of the items,
        # because there is no way to know which items you already received if you
        # already disposed them
        uploaded_items = self.http_server.download_items()
        game_items = {self.game_item_to_archipelago_item(item) for item in uploaded_items if item.level == 1}
        server_items = {network_item.item for network_item in self.items_received if self.slot_concerns_self(network_item.player)}
        missing_items = { item for item in server_items.difference(game_items)}
        for item in missing_items:
            game_item = self.archipelago_item_to_game_item(item)
            self.http_server.upload_item(game_item.type, game_item.id)

        # handle item levels
        for item in uploaded_items: 
            archipelago_level = self.get_level(self.game_item_to_archipelago_item(item))
            if archipelago_level < 1 or archipelago_level <= item.level: continue
            self.http_server.upload_item(item.type, item.id, archipelago_level)

    def set_cemu_graphic_packs(self):
        try:
            cemu_path = Utils.get_options()["xenobladeX_options"]["cemu_path"]
            settings_path = cemu_path + "Settings.xml"
            file_path = Utils.local_path(settings_path)
            with open(file_path, "r") as file :
                filedata = file.read()

            # Cleanup
            for pack_name in {pack.rsplit("/", 1)[0] for pack in self.options}:
                pack_regex = rf'<Entry filename="graphicPacks/downloadedGraphicPacks/XenobladeChroniclesX/Mods/{pack_name}/rules.txt"(/>\n|>.*?</Entry>\n)'
                filedata = re.sub(pack_regex, "", filedata, flags=re.DOTALL)

            cemu_packs = {pack.rsplit("/", 1)[0] : {pack.rsplit("/", 1)[1]: value} for pack, value in self.options.items() if value != "off"}
            cemu_packs["Archipelago"] = {"Active preset": ""}
            # Addition
            for pack_name, categories in cemu_packs.items():
                content = "".join([f'<Preset>\n{f"<category>{pack_category}</category>" if pack_category != "Active preset" else ""}<preset>{category_value}</preset>\n</Preset>\n' 
                    for pack_category, category_value in categories.items()])
                pack_content = (f'<Entry filename="graphicPacks/downloadedGraphicPacks/XenobladeChroniclesX/Mods/'
                    f'{pack_name}/rules.txt">\n{content}</Entry>\n\n')
                filedata = re.sub(rf'</GraphicPack>', f"{pack_content}</GraphicPack>", filedata)
                filedata = re.sub(rf'<GraphicPack/>', f"<GraphicPack>\n{pack_content}</GraphicPack>", filedata)

            with open(settings_path, "w") as file:
                file.write(filedata)
        except FileNotFoundError:
            logger.error(CEMU_SETTINGS_NOT_FOUND)


async def xenoblade_x_sync_task(ctx: XenobladeXContext) -> None:
    logger.debug("started xenobladeX sync task")
    while not ctx.exit_event.is_set():
        if ctx.connected:
            ctx.download_game_locations()
            if ctx.http_server.download_death() and not ctx.death_link_pending:
                await ctx.send_death()
            ctx.upload_game_items()
        await asyncio.sleep(2)
    logger.debug("terminated xenobladeX sync task")


async def main() -> None:
    parser = get_base_parser()
    args = parser.parse_args()

    ctx = XenobladeXContext(args.connect, args.password)
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
    Utils.init_logging("XenobladeXClient", exception_logger="Client")

    colorama.init()
    asyncio.run(main())
    colorama.deinit()
