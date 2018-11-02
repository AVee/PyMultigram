# PyMultigram #
The idea behind this library is to create tooling which allows multiple [Pyrogram](https://github.com/pyrogram/pyrogram) clients to run in a single application sharing the same handlers. Ultimately it should be possible to create both handlers and clients from a configuration file which allows to mix and match handlers.

## Why? ##
There are several use cases where this would be useful. Firstly, with even a single client it could provide a way to create an application which can easily be configured to enable or disable certain features. Secondly, it would allow the creation of multiple bots which (partly) share the same functionality. Multi-Tenancy for bots basically. As an added benefit generic handler could be build (and packaged) to be shared between applications.  

But most importantly, it seemed like a fun thing to try ;-)

## Usage ##
To be able to store state for multiple clients and allow for reuse handler methods should be inside a class which inherits from
multigram.MultiHandler. This also means multiple instances of the same handler (with perhaps a different configuration) can exist
within the same application.

The basic flow is to create instances of handler classes and Pyrogram clients. Then on each of the handler classes call 
set_clients() to assign (a selection of) the clients to that handler.

Once the clients are started messages should start to flow into the methods decorated with `@multigram.on_message()`. This decorator is a drop in replacement for the `on_message()` in pyrogram. It adds one named parameter `scope` which may contain a callable to filter clients. You can use the presets `multigram.ALL`, `multigram.BOTS` or `multigram.USERS` (with ALL being the default value), or pass your own client filtering method.

## TODO ##
- Build a pip package and publish to PyPi
- The usual, samples, unit tests, documentation...
- A way to store metadata with clients and use that as a filter or within the handler.
- A way to assign handlers to clients instead of the reverse.
- A way to configure it all without code, config in something like json or yaml.
- A way change add/remove clients or handlers at runtime.
- A way to reload a file based config at runtime.
- Maybe a minimal rest API to make runtime config changes.
- Add a kitchen sink.

## Development ##
Contributions are welcome. I'm following git-flow, so please make pull-requests againts the develop branch. 

I'm using Eclipse with Pydev, project files are included. But it's plain Python so you should be able to use your favorite IDE.
