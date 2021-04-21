import csgogsi

server = csgogsi.Server()

#  I want to observe the changes to this:
#  server.payload.played_map.round_no
#  It is easy:
@server.add_observer("played_map", "round_no")
def on_new_round():  # If the server observed a change to the payload subattribute round_no (of the attribute played_map), it will call this function
    print("The server observed a change to the payload ! We are now in the round {} !".format(server.payload.played_map.round_no))

@server.add_observer("player", "match_stats", "kills")
def on_kill_number_changed():
    print("New kill (or suicide) ! Now {} kill(s)".format(server.payload.player.match_stats.kills))

@server.add_observer("player", "match_stats", "deaths")
def on_deaths_number_changed():
    print("New death ! Now {} death(s)".format(server.payload.player.match_stats.deaths))

server.run()
