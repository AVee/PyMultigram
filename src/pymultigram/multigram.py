'''
This module provides a framework for multi-client Pyrogram programs with 
flexible plugin support.

@author: AVee
'''
import pyrogram
import types
from typing import Iterable
from pyrogram.client.handlers.message_handler import MessageHandler
from functools import partial
from pyrogram.client.client import Client

ALL=lambda client: True
BOTS=lambda client: is_bot(client)
USERS=lambda client: not is_bot(client)

def is_bot(client: Client):
    return client.bot_token #or client. pyrogram.Client.BOT_TOKEN_RE.match(client.session_name)

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
            
    def __get__(self, instance, owner):
        func = partial(self._func, instance)
        func.multigram_onmessagedecorator = self
        return func
       
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
        self._clients = []
        self._bots = []
        self._users = []
        self._handlers = [getattr(self, handler) for handler in dir(self) if hasattr(getattr(self, handler), 'multigram_onmessagedecorator')]
        self._active_handlers = {}
        
    def set_clients(self, clients : Iterable[pyrogram.Client]):
        for client in clients:
            self.add_client(client)
    
    def add_client(self, client: pyrogram.Client):
        if not client in self._clients:
            self._clients.append(client)
            
        if is_bot(client):
            if not client in self._bots:
                self._bots.append(client)
        else:
            if not client in self._users:
                self._users.append(client)
                
        for decorator in self._handlers:
            if decorator.multigram_onmessagedecorator._scope(client):
                handler_ref = client.add_handler(MessageHandler(decorator, decorator.multigram_onmessagedecorator._filters), decorator.multigram_onmessagedecorator._group)
                if not self._active_handlers.__contains__(client):
                    self._active_handlers[client] = []
                self._active_handlers[client].append(handler_ref)

    def remove_all_clients(self):
        for client in self._clients:
            self.remove_client(client)
                
    def remove_client(self, client: pyrogram.Client):
        if self._active_handlers.__contains__(client):
            for handler_ref in self._active_handlers[client]:
                client.remove_handler(handler_ref)
        
        if not client in self._clients:
            self._clients.append(client)
            
        if is_bot(client):
            if not client in self._bots:
                self._bots.append(client)
        else:
            if not client in self._users:
                self._users.append(client)
