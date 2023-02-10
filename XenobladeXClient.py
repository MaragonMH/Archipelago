import asyncio
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import colorama  # type: ignore

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, logger, get_base_parser
import Utils


class XenobladeXHTTPRequestHandler(BaseHTTPRequestHandler):
    def get_items(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        # remove duplicate lines
        self.server.items = "\n".join(list(OrderedDict.fromkeys(self.server.items.split("\n")))) # type: ignore
        self.wfile.write(self.server.items.encode()) # type: ignore
        self.server.items = "" # type: ignore

    def post_locations(self):
        locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":","\n")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        upload_ended = "$" in locations[-1]
        if "^" in locations[0]:
            self.server.upload_in_progress = True # type: ignore
            self.server.locations = "" # type: ignore
            locations = locations[1:]
        if upload_ended:
            locations = locations[0:-2]
        self.server.locations += locations # type: ignore
        if upload_ended:
            self.server.upload_in_progress = False # type: ignore
        logger.debug("Received LOCATION: " + locations[0:2] + " Lines: " + str(locations.count('\n')) +
            " FileLines: " +  str(self.server.locations.count('\n'))) # type: ignore

    def do_GET(self):
        if self.path == '/items':
            self.get_items()

    def do_POST(self):
        if self.path == '/locations':
            self.post_locations()

class XenobladeXHttpServer(HTTPServer):
    locations = ""
    items = ""
    upload_in_progress = False

    def get_item_type(self, base_id, archipelago_item_id, max_type_count):
        return (archipelago_item_id - base_id) % max_type_count

    def get_item_lvl_ids(self, base_id, archipelago_item_id, max_type_count) -> set[int]:
        item_game_type:int = self.get_item_type(base_id, archipelago_item_id, max_type_count)
        item_game_id:int = (archipelago_item_id - base_id) // max_type_count

        # Handle Lvl aka progressive powerups
        lvl_count = 1
        if item_game_type == 0x22:
            lvl_count = 5
        elif item_game_type == 0x23:
            lvl_count = 4
        else:
            return set(archipelago_item_id)

        item_game_first_id:int = item_game_id - item_game_id % lvl_count
        
        result = set()
        for item_game_offset in range(lvl_count):
            result.add(base_id + item_game_type * max_type_count + item_game_first_id + item_game_offset)
        return result

    def upload_item(self, base_id, archipelago_item_id, max_type_count, item_game_level = 0):
        item_game_type:int = (archipelago_item_id - base_id) % max_type_count
        item_game_id:int = (archipelago_item_id - base_id) // max_type_count

        if item_game_type == 0:
            self.items += f"K Id={item_game_id:08x} Fg={1:08x}\n"
        elif item_game_type < 0x20:
            self.items += f"I Tp={item_game_type:08x} Id={item_game_id:08x}\n"
        elif item_game_type < 0x21:
            self.items += f"A Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x22:
            self.items += f"S Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x23:
            self.items += f"F Id={item_game_id:08x} Lv={item_game_level:08x}\n"
        elif item_game_type < 0x24:
            self.items += f"D Id={item_game_id:08x} Lv={item_game_level:08x}\n"
        elif item_game_type < 0x25:
            self.items += f"C Id={item_game_id:08x} Lv={10:08x}\n"

    def _get_lvl_ids(self, data: set[int], base_id: int, type_id: int, game_id: int, max_type_count: int, game_lvl:int = 1, max_lvl:int = 1):
        offset_id:int = game_id * max_lvl
        type_offset_id:int = type_id * max_type_count
        for location_id in range(game_lvl):
            data.add(base_id + type_offset_id + offset_id + location_id)
        return data

    def download_item_ids(self, base_id, max_type_count) -> set[int]:
        locations = set()
        locations_count = max_type_count
        if self.upload_in_progress:
            return locations

        match = re.findall(r'^CP Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for collepedia_entry in match:
            if collepedia_entry[1] > 0:
                locations = self._get_lvl_ids(locations, base_id, 0, collepedia_entry[0], base_id, locations_count)
        match = re.findall(r'^EN Id=([0-9a-fA-F]{3}) Dc=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for enemy_book_entry in match:
            if enemy_book_entry[1] > 1:
                locations = self._get_lvl_ids(locations, base_id, 1, enemy_book_entry[0], base_id, locations_count)
        match = re.findall(r'^FN Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for fn_node_entry in match:
            if fn_node_entry[1] > 0:
                locations = self._get_lvl_ids(locations, base_id, 2, fn_node_entry[0], base_id, locations_count)
        match = re.findall(r'^SG Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for segment_entry in match:
            if segment_entry[1] > 0:
                locations = self._get_lvl_ids(locations, base_id, 3, segment_entry[0], base_id, locations_count)
        match = re.findall(r'^LC Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) Tp=[0-9a-fA-F]{1}\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for location_entry in match:
            if location_entry[1] > 0:
                locations = self._get_lvl_ids(locations, base_id, 4, location_entry[0], base_id, locations_count)

        return locations

    def download_location_ids(self, base_id, max_type_count) -> set[int]:
        items = set()
        items_count = max_type_count
        if self.upload_in_progress:
            return items

        match = re.findall(r'^KY Id=([0-9a-fA-F]{1}) Fg=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for key_entry in match:
            if key_entry[1] > 0:
                items = self._get_lvl_ids(items, base_id, 0, key_entry[0], base_id, items_count)
        match = re.findall(r'^IT Id=([0-9a-fA-F]{3}) Tp=([0-9a-fA-F]{2})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for item_entry in match:
            items = self._get_lvl_ids(items, base_id, item_entry[1], item_entry[0], base_id, items_count)
        match = re.findall(r'^IT Id=([0-9a-fA-F]{3}) Tp=([0-9a-fA-F]{2}) S1Id=[0-9a-fA-F]{3} U1=[0-9a-fA-F]{1} S2Id=[0-9a-fA-F]{3} U2=[0-9a-fA-F]{1} S3Id=[0-9a-fA-F]{3} U3=[0-9a-fA-F]{1} A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4}) Na=.*\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for item_entry in match:
            items = self._get_lvl_ids(items, base_id, item_entry[1], item_entry[0], base_id, items_count)
            for idx in range(2,5):
                if item_entry[idx] != 0 and item_entry[idx] != 0xFFFF: # Check for empty or disabled augment slot
                    # use player character augment type for these
                    items = self._get_lvl_ids(items, base_id, item_entry[idx], 0x14, base_id, items_count)
        match = re.findall(r'^EQ CId=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=[0-9a-fA-F]{1} S1Id=[0-9a-fA-F]{3} U1=[0-9a-fA-F]{1} S2Id=[0-9a-fA-F]{3} U2=[0-9a-fA-F]{1} S3Id=[0-9a-fA-F]{3} U3=[0-9a-fA-F]{1} A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4}) Na=.*\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for equip_entry in match:
            if equip_entry[1] < 3:
                items = self._get_lvl_ids(items, base_id, 0x6, equip_entry[0], base_id, items_count)
            else:
                items = self._get_lvl_ids(items, base_id, 0x1, equip_entry[0], base_id, items_count)
            for idx in range(2,5):
                if equip_entry[idx] != 0 and equip_entry[idx] != 0xFFFF: # Check for empty or disabled augment slot
                    # use player character augment type for these
                    items = self._get_lvl_ids(items, base_id, equip_entry[idx], 0x14, base_id, items_count)
        match = re.findall(r'^DL GIx=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1}) S1Id=[0-9a-fA-F]{3} U1=[0-9a-fA-F]{1} S2Id=[0-9a-fA-F]{3} U2=[0-9a-fA-F]{1} S3Id=[0-9a-fA-F]{3} U3=[0-9a-fA-F]{1} A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4}) Na=.*\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for doll_entry in match:
            if doll_entry[1] < 0xA:
                items = self._get_lvl_ids(items, base_id, 0xF, doll_entry[0], base_id, items_count)
            elif doll_entry[1] == 0xA:
                items = self._get_lvl_ids(items, base_id, 0x9, doll_entry[0], base_id, items_count)
            else:
                items = self._get_lvl_ids(items, base_id, 0xA, doll_entry[0], base_id, items_count)
            for idx in range(2,5):
                if doll_entry[idx] != 0 and doll_entry[idx] != 0xFFFF: # Check for empty or disabled augment slot
                    # use player doll augment type for these
                    items = self._get_lvl_ids(items, base_id, doll_entry[idx], 0x16, base_id, items_count)
        match = re.findall(r'^AT Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for art_entry in match:
            if art_entry[1] > 0:
                items = self._get_lvl_ids(items, base_id, 0x20, art_entry[0], items_count)
        match = re.findall(r'^SK Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for skill_entry in match:
            if skill_entry[1] > 0:
                items = self._get_lvl_ids(items, base_id, 0x21, skill_entry[0], items_count)
        match = re.findall(r'^FS Id=([0-9a-fA-F]{1}) Lv=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for field_skill_entry in match:
            items = self._get_lvl_ids(items, base_id, 0x22, field_skill_entry[0], items_count, field_skill_entry[1] - 1, 4)
        match = re.findall(r'^FD Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{2}) Ch=.*\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for friend_entry in match:
            items = self._get_lvl_ids(items, base_id, 0x23, friend_entry[0], items_count, friend_entry[1] // 10, 5)
        match = re.findall(r'^CL Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n', self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        for class_entry in match:
            if class_entry[1] > 9:
                items = self._get_lvl_ids(items, base_id, 0x24, class_entry[0], items_count)

        return items


class XenobladeXContext(CommonContext):
    tags = {"AP", "XenobladeX"}
    game = "XenobladeX"
    items_handling = 0b011  # get items from your own world
    want_slot_data = False
    http_server = XenobladeXHttpServer(('localhost', 45872), XenobladeXHTTPRequestHandler)
    base_id = 0 # get from slot data
    max_type_count = 5000 # get from slot data

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(XenobladeXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game # type: ignore


    def run_gui(self):
        from kvui import GameManager
        class XenobladeXManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Xenoblade X Client"

        self.ui = XenobladeXManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


    def download_game_locations(self) -> None:
        # Get all the locations from the game and
        # Calc the differance between those and the server and
        # Send them to the server
        game_locations = self.http_server.download_location_ids(self.base_id, self.max_type_count)
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
        game_items = self.http_server.download_item_ids(self.base_id, self.max_type_count)
        server_items = {network_item.item for network_item in self.items_received if self.slot_concerns_self(network_item.player)}
        for network_item in self.items_received:
            if self.slot_concerns_self(network_item.player) and network_item.item not in game_items:
                lvl = len(self.http_server.get_item_lvl_ids(self.base_id, network_item.item, self.max_type_count).intersection(server_items))
                self.http_server.upload_item(self.base_id, network_item.item, self.max_type_count, lvl)


async def xenoblade_x_sync_task(ctx: XenobladeXContext) -> None:
    logger.debug("started xenobladeX sync task")
    while not ctx.exit_event.is_set():
        ctx.download_game_locations()
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
