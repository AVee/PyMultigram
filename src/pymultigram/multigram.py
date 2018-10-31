'''
This module provides a framework for multi-client Pyrogram programs with 
flexible plugin support.

@author: AVee
'''
import pyrogram
import types
from typing import Iterable
from pyrogram.client.handlers.message_handler import MessageHandler

ALL=-1
BOTS=-2
USERS=-3

class OnMessageDecorator(object):
    '''
    Callable class which is used to track decorated methods in handler classes.
    
    Using the Multigram.on_message decorator replaces the method with this object,
    so we can find all decorated objects later during initialization of the Handler
    class. When the object is called we still call the original method, so the Handler
    object doesn't have any unexpected behavior. 
    '''
    def __init__(self, scope, filters, group):
        '''
        @see: on_message
        '''
        self._func = None
        self._scope = scope
        self._filters = filters
        self._group = group
        
    def wrapper(self, func):
        self._func = func
        return self
        
    def __call__(self, *args, **kwargs):
        return self._func(self, *args, **kwargs)
       
def on_message(scope=ALL, filters=None, group: int = 0):
    '''
    This is the MultiGram replacement for the Pyrogram on_message
    decorator. For the filter and groups parameters see the 
    Pyrogram documentation.
    
    The added scope variable defines on which clients this handler
    will be applied. Values can be:
    - multigram.ALL:     Apply to all clients
    - multigram.BOTS:    Apply to all bot clients
    - multigram.USERS:   Apply to normal user clients
    Additionally a iterator or callback method can be passed which
    should produce a list of clients on which the handler should 
    be applied. 
    '''
    decorator = OnMessageDecorator(scope, filters, group)
    return decorator.wrapper

class MultiHandler(object):
    '''
    classdocs
    '''
    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        super().__init__()
        self._clients: int = None
        self._bots = None
        self._users = None
        
    def set_clients(self, clients : Iterable[pyrogram.Client]):
        self._clients = clients
        self._bots = (client for client in clients if pyrogram.Client.BOT_TOKEN_RE.match(client.session_name))
        self._users = (client for client in clients if not pyrogram.Client.BOT_TOKEN_RE.match(client.session_name))

        handlers = (getattr(self, handler) for handler in dir(self) if isinstance(getattr(self, handler), OnMessageDecorator))
        
        for handler in handlers:
            if callable(handler._scope):
                applies_to = handler._scope()
            elif isinstance(handler._scope, Iterable):
                applies_to = handler._scope
            elif handler._scope == BOTS:
                applies_to = self._bots
            elif handler._scope == USERS:
                applies_to = self._users
            elif handler._scope == ALL:
                applies_to = self._clients
             
            for client in applies_to:
                client.add_handler(MessageHandler(handler, handler._filters), handler._group)