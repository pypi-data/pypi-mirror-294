from pathlib import Path
from typing import Dict, List
from .trx import TRX

class DateTime:
    def __init__(self, name:str, path:Path):
        self.name = name
        self.path = path
        assert(str(path.name) == name)
    
    @property
    def trx(self)->TRX:
        return TRX(self.path/'trx.mat')

class Protocol:
    def __init__(self, name:str, root:Path):
        self.name = name
        self.root = root
        assert(str(root.name) == name)
        self._dates:Dict[str, DateTime] = {dt.name:DateTime(dt.name, dt) for dt in self.root.glob(8*'[0-9]'+'_'+6*'[0-9]') if dt.is_dir()}

    def __getitem__(self, dt:str)->DateTime:
        return self._dates[dt]
    
    def dates(self):
        return self._dates.values()

    def trx(self):
        for dt in self.dates():
            yield dt.trx
    
class Line:
    def __init__(self, name:str, root:Path):
        self.name = name
        self.root = root
        assert(str(root.name) == name)
        self._protocols:Dict[str, Protocol] = {p.name:Protocol(p.name, p) for p in self.root.glob('p_*') if p.is_dir()}

    def __getitem__(self, protocol:str)->Protocol:
        return self._protocols[protocol]
    
    def protocols(self):
        return self._protocols.values()
    
    def dates(self):
        for p in self.protocols():
            for dt in p.dates():
                yield dt
    
    def trx(self):
        for p in self.protocols():
            for trx in p.trx():
                yield trx

class Tracker:
    def __init__(self, name:str, root:Path):
        self.name = name
        self.root = root
        assert(str(root.name) == name)
        self._lines:Dict[str, Line] = {l.name:Line(l.name, l) for l in self.root.glob('*@*') if l.is_dir()}

    def __getitem__(self, line:str)->Line:
        return self._lines[line]
    
    def lines(self):
        return self._lines.values()
    
    def protocols(self):
        for l in self.lines():
            for p in l.protocols():
                yield p
    
    def dates(self):
        for l in self.lines():
            for dt in l.dates():
                yield dt

    def trx(self):
        for l in self.lines():
            for trx in l.trx():
                yield trx


class Repository:
    def __init__(self, root:Path, trackers:List[str]):
        self.root = root
        self._trackers:Dict[str, Tracker] = {t:Tracker(t, self.root/t) for t in trackers if (self.root/t in self.root.iterdir()) and (self.root/t).is_dir()}

    def __getitem__(self, tracker:str)->Tracker:
        return self._trackers[tracker]
    
    def trackers(self):
        return self._trackers.values()
    
    def lines(self):
        for t in self.trackers():
            for l in t.lines():
                yield l

    def protocols(self):
        for t in self.trackers():
            for p in t.protocols():
                yield p
    
    def dates(self):
        for t in self.trackers():
            for dt in t.dates():
                yield dt

    def trx(self):
        for t in self.trackers():
            for trx in t.trx():
                yield trx