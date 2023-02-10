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


class XenobladeXCommandProcessor(ClientCommandProcessor):
    ctx: "XenobladeXContext"


class XenobladeXContext(CommonContext):
    game = "XenobladeX"
    command_processor: Type[ClientCommandProcessor] = XenobladeXCommandProcessor
    items_handling = 0b011  # get items from your own world
    http_server = HTTPServer(('localhost', 45872), XenobladeXHTTPRequestHandler)

    def __init__(self, server_address: str, password: str) -> None:
        super().__init__(server_address, password)


    def download_game_locations(self) -> None:
        return


    def upload_game_items(self) -> None:
        return


async def main() -> None:
    parser = get_base_parser()

    args = parser.parse_args()
    print(args)

    ctx = XenobladeXContext(args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    asyncio.get_event_loop().run_in_executor(None, ctx.http_server.serve_forever)

    await ctx.exit_event.wait()

    ctx.server_address = None
    logger.debug("waiting for game server task to end")
    await asyncio.get_event_loop().run_in_executor(None, ctx.http_server.shutdown)

    await ctx.shutdown()


if __name__ == "__main__":
    Utils.init_logging("XenobladeXClient", exception_logger="Client")

    colorama.init()
    asyncio.run(main())
    colorama.deinit()
