from http.server import HTTPServer, BaseHTTPRequestHandler

ITEMS = ""
LOCATIONS = "Nothing uploaded yet"
# Example: Invoke-WebRequest http://localhost:45872/items -Method POST -Body "I Tp=00000008 Id=00000039`n"

def get_items(self):
    global ITEMS
    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.end_headers()
    self.wfile.write(ITEMS.encode())
    ITEMS = ""

def get_locations(self):
    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.end_headers()
    self.wfile.write(LOCATIONS.encode())

def post_items(self):
    global ITEMS
    items = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":","\n")
    if ";" in items[0]:
        ITEMS = ""
        items = items[1:]
    ITEMS += items
    print("Received ITEM: " + items[0:2] + " Lines: " + str(items.count('\n')) +
        " FileLines: " +  str(ITEMS.count('\n')))
    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.end_headers()

def post_locations(self):
    global LOCATIONS
    locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":","\n")
    if ";" in locations[0]:
        LOCATIONS = ""
        locations = locations[1:]
    LOCATIONS += locations
    print("Received LOCATION: " + locations[0:2] + " Lines: " + str(locations.count('\n')) +
        " FileLines: " +  str(LOCATIONS.count('\n')))
    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.end_headers()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/items':
            get_items(self)
        elif self.path == '/locations':
            get_locations(self)

    def do_POST(self):
        if self.path == '/items':
            post_items(self)
        elif self.path == '/locations':
            post_locations(self)


print("Starting...")

try:
    httpServer = HTTPServer(('localhost', 45872), SimpleHTTPRequestHandler)
    httpServer.serve_forever()
except KeyboardInterrupt:
    httpServer.shutdown()
