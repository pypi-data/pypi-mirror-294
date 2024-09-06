import asyncio
from typing import Any, Callable
from deccom.cryptofuncs.hash import SHA256
from deccom.peers.peer import Peer
from deccom.protocols.defaultprotocol import DefaultProtocol
from deccom.protocols.wrappers import *


class AbstractProtocol(object):

    required_lower = ["sendto", "start", "callback"]

    offers = {  
                "sendto": "sendto",
                "callback": "callback",
                "datagram_received": "datagram_received",
                }
    bindings = dict({"_lower_start":  "start", "_lower_sendto":  "sendto", "datagram_received": "callback"})
    
   
    def check_if_have(submodule, attr, name = None)->bool:
        if name != None and submodule.__class__.__name__ != name:
            return AbstractProtocol.check_if_have(submodule.submodule,attr,name)
        if not hasattr(submodule,attr):
            if hasattr(submodule,"offers"):
                if isinstance(submodule.offers, dict):
                    if submodule.offers.get(attr) != None:
                        if submodule._taken.get(submodule.offers.get(attr)) != None:
                            raise Exception(attr,"of", submodule,"already taken by",submodule._taken.get(submodule.offers.get(attr)))
                        return True
            if not hasattr(submodule,"submodule") or submodule.submodule == None:
                return False
            else:
                return AbstractProtocol.check_if_have(submodule.submodule,attr,name)
            
        else:
            if submodule._taken.get(attr) != None:
                
                raise Exception(attr,"of", submodule,"already taken by",submodule._taken.get(attr))
            return True
        
        
        return True
    @bindto("stop")
    async def _lower_stop(self):
        return
    async def stop(self):
        if not self.started:
            return
        self.started = False

        return await self._lower_stop()
    def get_if_have(submodule: Any, attr, name = None)->bool:
        if name != None and submodule.__class__.__name__ != name:
            return AbstractProtocol.get_if_have(submodule.submodule,attr,name)
        if not hasattr(submodule,attr):
            if hasattr(submodule,"offers"):
                if isinstance(submodule.offers, dict):
                    if submodule.offers.get(attr) != None:
                        return getattr(submodule,submodule.offers.get(attr))
            if not hasattr(submodule,"submodule") or submodule.submodule == None:
                return None
            else:
                return AbstractProtocol.get_if_have(submodule.submodule,attr,name)
        else:
            return getattr(submodule,attr)
        return None
    
    def process_datagram(self, addr, data):
        
        return self.callback(addr,data)
    
    async def send_datagram(self, msg: bytes, addr: tuple[str,int]):
        if not self.started:
            return
        await self._lower_sendto(self.uniqueid + msg, addr)

    
    def set_if_have(submodule,attr,val,name = None):
        if name != None and submodule.__class__.__name__ != name:
            return AbstractProtocol.set_if_have(submodule.submodule,attr,val,name)
        if not hasattr(submodule,attr):
            if hasattr(submodule,"offers"):
                if isinstance(submodule.offers, dict):
                    if submodule.offers.get(attr) != None:
                        if submodule._taken.get(submodule.offers.get(attr)) != None:
                            raise Exception(attr,"already taken by",submodule._taken.get(attr),"while setting",val)
                        
                        setattr(submodule,submodule.offers.get(attr),val)
                        submodule._taken[submodule.offers.get(attr)] = val
                        return
            if not hasattr(submodule,"submodule") or submodule.submodule == None:
                raise Exception("Cannot find any method to bind to",attr,"asked to be bound to",val)
            else:
                AbstractProtocol.set_if_have(submodule.submodule,attr,val,name)
                return
        else:
            if submodule._taken.get(attr) != None:
                
                raise Exception(attr,"already taken by",submodule._taken.get(attr),"while setting",val)
            
            setattr(submodule,attr,val)
            submodule._taken[attr] = val
            return
        raise Exception("Cannot find any method to bind to",attr,"asked to be bound to",val,"bottom")
    
    def __init__(self, submodule = None, callback: Callable[[tuple[str, int], bytes], None] = lambda addr, data: ...):
        self.started = False
        self.submodule = submodule
        self.callback = callback
        self._taken = dict()
        self.uniqueid = SHA256(self.__class__.__name__)[-8:]
    
    @bindfrom("callback")    
    def datagram_received(self, addr:tuple[str,int],data:bytes):
        if not self.started:
            return
        if data[:8] == self.uniqueid:
            return self.process_datagram(addr, data[8:])
        else:
            return self.callback(addr,data)
        
    
    @bindto("sendto")
    async def _lower_sendto(self, msg:bytes, addr:tuple[str,int]):
        return
    
    @bindto("start")
    async def _lower_start(self, p: Peer):
        return
        
    async def start(self, p: Peer):
        await self._lower_start(p)
        print("started")
        self.peer = p
        self.started = True
    def recursive_check(obj, mtd, attr):
        if not hasattr(obj, mtd):
            return None
        if hasattr(getattr(obj, mtd), attr):
            return obj
        elif obj.__class__.__base__ != None and issubclass(obj.__class__.__base__,AbstractProtocol):
            return AbstractProtocol.recursive_check(obj.__class__.__base__, mtd, attr)
        else:
            return None
    def inform_lower(self):
        
        for name in dir(self):            
            if callable(getattr(self, name)):
                if hasattr(getattr(self, name), "nobind"):
                    continue
                ret = AbstractProtocol.recursive_check(self,name,"bindfrom")
                if ret != None:
                
                    method = self.__class__.check_if_have(self.submodule,getattr(ret, name).bindfrom)
                    if not method:
                        
                        continue
                    self.__class__.set_if_have(self.submodule,getattr(ret, name).bindfrom,getattr(self,name))
                
                ret = AbstractProtocol.recursive_check(self,name,"bindto")
                if ret != None:
                
                    method = self.__class__.get_if_have(self.submodule,getattr(ret, name).bindto)
                    if method == None:
                        continue
                    setattr(self,name,method)
                    # self._taken[name] = method

                    

    def set_lower(self, submodule):
        self.submodule = submodule
        
        for method in self.__class__.required_lower:
            if not self.__class__.check_if_have(submodule,method): 
                raise Exception("MISSING REQUIRED!",method," in the protocol chain by ",type(self))
        
        self.inform_lower()
    
    def get_lowest(self):
        return self.submodule.get_lowest()
    
    def set_callback(self, callback):
        self.callback = callback
    
    async def sendto(self,msg,addr):
        await self._lower_sendto(msg,addr)
    def __getattribute__(self, __name: str) -> Any:
        
            
        try:
                # print("looking for", __name,self)
                return object.__getattribute__(self, __name)
        except AttributeError:
                if not self.started:
                    raise AttributeError()
                else:
                    # print("missing",self, __name)
                    return self.submodule.__getattribute__(__name)
        