import asyncio
from typing import Any, Callable
import os

from deccom.protocols.abstractprotocol import AbstractProtocol


class HolePuncher(AbstractProtocol):
    REQUEST_RELAY = int.from_bytes(b'\xff', byteorder="big")
    INFORM_RELAY = int.from_bytes(b'\x43', byteorder="big")
    INFORM_EXTERNAL = int.from_bytes(b'\x13', byteorder="big")
    REQUEST_EXTERNAL = int.from_bytes(b'\x23', byteorder="big")
    def __init__(self, submodule=None, callback: Callable[[tuple[str, int], bytes], None] = ...):
        super().__init__(submodule, callback)
        self.heard_data = dict()
        self.successful = set()
        self.outstanding: dict[tuple[str,int], tuple[int, list[bytes]]] = dict()
        
    async def stop(self):
        self.outstanding.clear()
        self.heard_data.clear()
        for _,v in self.outstanding.items():
            v[1].clear()
        self.outstanding.clear()
        return await super().stop()
    def heard_from(self,add1, add2):
        print("adding", add2,"from",add1)
        if self.heard_data.get(add2) == None:
            self.heard_data[add2] = []
        self.heard_data[add2].append(add1)
        self.heard_data[add2] = self.heard_data[add2][-5:]

    def datagram_received(self, addr:tuple[str,int],data:bytes):
        self.successful.add(addr)
        if self.outstanding.get(addr) != None:
            print("outstanding from them")
            loop = asyncio.get_event_loop()
            for msg in self.outstanding.get(addr)[1]:
                
                loop.create_task(self._lower_sendto(msg,addr))
            del self.outstanding[addr]
        if data[:8] == self.uniqueid:
            return self.process_datagram(addr, data[8:])
        else:
            return self.callback(addr,data)
    def process_datagram(self, addr: tuple[str, int], data: bytes):
        if len(data) < 2:
            return
        if data[0] == HolePuncher.REQUEST_RELAY:
            print("they requested relay ",addr,self.peer.addr)
            loop = asyncio.get_event_loop()
            msg = bytearray([HolePuncher.INFORM_RELAY])
            baddrs = addr[0].encode("utf-8")
            msg += len(baddrs).to_bytes(4, byteorder="big")
            msg += baddrs
            msg += addr[1].to_bytes(2, byteorder="big")
            l_their = int.from_bytes(data[1:5], byteorder="big")
            ip_their = data[5:5+l_their].decode(encoding="utf-8")
            p_their = int.from_bytes(data[5+l_their: 7+l_their], byteorder="big")
        
            loop.create_task(self.send_datagram(bytes(msg),(ip_their, p_their)))
            return
        elif data[0] == HolePuncher.INFORM_RELAY:
            
            l_their = int.from_bytes(data[1:5], byteorder="big")
            ip_their = data[5:5+l_their].decode(encoding="utf-8")
            p_their = int.from_bytes(data[5+l_their: 7+l_their], byteorder="big")
            loop = asyncio.get_event_loop()
            print("informed of relay to ",p_their)
            loop.create_task(self.send_datagram(b'\x01',(ip_their, p_their)))
            return
        return super().process_datagram(addr, data[1:])
    def timeout(self, addr):
        if self.outstanding.get(addr) == None:
            return
        if self.outstanding[addr][0] == 0:
            del self.outstanding[addr]
            return
        self.outstanding[addr] = (self.outstanding[addr][0] - 1, self.outstanding[addr][1])
        msg = bytearray([HolePuncher.REQUEST_RELAY])
        baddrs = addr[0].encode("utf-8")
        msg += len(baddrs).to_bytes(4, byteorder="big")
        msg += baddrs
        msg += addr[1].to_bytes(2, byteorder="big")
                
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_datagram(msg,self.heard_data[addr][-1]))
        loop.call_later(10,
                                      self.timeout, addr)
    async def sendto(self, msg, addr):
        if addr not in self.successful and self.heard_data.get(addr) != None:
            print("havent heard")
            if self.outstanding.get(addr) == None:
                self.outstanding[addr] = (3,[msg])
                loop = asyncio.get_event_loop()
                loop.call_later(10,
                                      self.timeout, addr)
                msg = bytearray([HolePuncher.REQUEST_RELAY])
                baddrs = addr[0].encode("utf-8")
                msg += len(baddrs).to_bytes(4, byteorder="big")
                msg += baddrs
                msg += addr[1].to_bytes(2, byteorder="big")
                await self.send_datagram(b'\x01',addr)
                for add in self.heard_data.get(addr):
                    await self.send_datagram(bytes(msg),add)
            else:
                # print(self.outstanding[addr])
                # self.outstanding[addr] = (self.outstanding[addr][0], self.outstanding[addr][1])
                self.outstanding[addr][1].append(msg)
        else:
            
            await self._lower_sendto(msg,addr)

        
