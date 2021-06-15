import csgogsi

server = csgogsi.Server()  # Default is host: 127.0.0.1, port: 3000
csgogsi.disable_log()


@server.add_observer("current_round", "bomb")  # On bomb state changed
def on_bomb_state_changed():
    print("Bomb sate changed ! Now {}".format(server.payload.current_round.bomb))


server.disable_on_start_event_triggering = True
server.run()
print("This will never be printed because the csgogsi server is blocking the thread (blocking argument is True by "
      "default)")
