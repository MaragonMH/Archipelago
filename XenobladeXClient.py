import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import BaseServer
from typing import Type
import colorama  # type: ignore


# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils


class XenobladeXHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server: BaseServer) -> None:
        self.items = ""
        self.locations = "Nothing uploaded yet"
        super().__init__(request, client_address, server)

    def upload_item_from_id(self, id):
        pass

    def squash_ids(self):
        pass

    def download_location_ids(self):
        locations = set()
        items = set()
        return (locations, items)

    def get_items(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(self.items.encode())
        self.items = ""

    def post_locations(self):
        locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":","\n")
        if ";" in locations[0]:
            self.locations = ""
            locations = locations[1:]
        self.locations += locations
        print("Received LOCATION: " + locations[0:2] + " Lines: " + str(locations.count('\n')) +
            " FileLines: " +  str(self.locations.count('\n')))
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

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
    want_slot_data = False
    http_server = HTTPServer(('localhost', 45872), XenobladeXHTTPRequestHandler)

    def __init__(self, server_address: str, password: str) -> None:
        super().__init__(server_address, password)


    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(XenobladeXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game


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
        return


    def upload_game_items(self) -> None:
        # Get all the items in locations from the game and
        # Get all the items from the server and
        # Calc the differance between those and 
        # Add items to the game
        # Big problem here is, if you are able to get rid of the items,
        # because there is no way to know which items you already received if you 
        # already disposed them
        return

async def xenoblade_x_sync_task(ctx: XenobladeXContext) -> None:
    logger.info("started xenobladeX sync task")
    while not ctx.exit_event.is_set():
        # ctx.missing_locations
        ctx.download_game_locations()
        ctx.upload_game_items()
        await asyncio.sleep(1)
    logger.info("terminated xenobladeX sync task")

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
