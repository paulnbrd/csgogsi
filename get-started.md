# Get started

First thing first, you need a configuration file in the cfg folder of the person who will send the data from CS:GO. In Windows, it's usually here: ``` C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg ```

In this folder, you will need to create a file named `gamestate_integration_<name>.cfg` where `<name>` can be whatever you want (in lowercase and no special characters pls). In this file, you need to copy [this](https://raw.githubusercontent.com/paulnbrd/csgogsi/master/examples/gamestate_integration_paulinux.cfg) for a basic setup. Official Steam documentation [here](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration)

Then, restart or start CS:GO to begin to use `csgogsi` !

If `csgogsi` is not installed, please refer to [this](installation)

# Basic example

Here is a basic example which will `print` the payload sent from CS:GO to the program ([this example](https://github.com/paulnbrd/csgogsi/blob/master/examples/very_basic.py))

```python
import csgogsi  # Import the module

server = csgogsi.Server()  # Create a Server object
server.run(blocking=False)  # Run the server without blocking the main thread

while True:
    print(server.payload)  # Print what the server got from CS:GO. If it's None, please verify your .cfg.
```

Tadaa ! You learned to use `csgogsi` ! But what if you want to print something (or do whatever you want) when the player get a kill ? Or die ? Or when a new round begins ? Easy !

[File here](https://github.com/paulnbrd/csgogsi/blob/master/examples/event_introduction.py)
```python
import csgogsi

server = csgogsi.Server()

#  I want to observe the changes to this:
#  server.payload.played_map.round_no
#  It is easy:
@server.add_observer("played_map", "round_no")
def on_new_round():  # If the server observed a change to the payload subattribute round_no (of the attribute played_map), it will call this function
    print("The server observed a change to the payload ! We are now in the round {} !".format(server.payload.played_map.round_no))

@server.add_observer("player", "match_stats", "kills")  # Say to the server to execute this function when it detects a change to the kills of the player
def on_kill_number_changed():
    print("New kill (or suicide) ! Now {} kill(s)".format(server.payload.player.match_stats.kills))

@server.add_observer("player", "match_stats", "deaths")
def on_deaths_number_changed():
    print("New death ! Now {} death(s)".format(server.payload.player.match_stats.deaths))
    
"""
To know what things you can observer (strings in the decorator), search in the payload object in state-parser.py.
I will maybe, one day, make a documentation about it, with all you can observe.

Note that if your are not spectator, there are things that you can't see
"""

server.run()  # By default, server blocks the main thread
```

Tadaa ! Now you can use `csgogsi` !
