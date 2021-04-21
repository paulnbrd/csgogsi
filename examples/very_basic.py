import csgogsi

server = csgogsi.Server()
server.run(blocking=False)

while True:
    print(server.payload)
