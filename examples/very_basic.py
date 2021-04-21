import csgogsi

server = csgogsi.Server()
server.run()

while True:
    print(server.payload)
