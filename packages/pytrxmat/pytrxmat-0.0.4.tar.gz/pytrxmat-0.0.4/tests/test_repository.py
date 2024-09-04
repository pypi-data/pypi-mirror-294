import pytest
import shutil
from pytrxmat.repository import Repository
from pathlib import Path

def add_trx(datetime):
    shutil.copy(Path(__file__).parent/'trx.mat', datetime)

def add_datetimes(protocol):
    d0 = protocol/'00000000_000000'
    d1 = protocol/'00000000_000001'
    d0.mkdir()
    d1.mkdir()
    add_trx(d0)
    add_trx(d1)

def add_protocols(line):
    p0 = line/'p_0'
    p1 = line/'p_1'
    p0.mkdir()
    p1.mkdir()
    add_datetimes(p0)
    add_datetimes(p1)

def add_lines(tracker):
    a = tracker/'a@a'  
    b = tracker/'b@b'
    a.mkdir()
    b.mkdir()
    add_protocols(a)
    add_protocols(b)

@pytest.fixture
def root(tmp_path):
    t1 = tmp_path/'t1'
    t2 = tmp_path/'t2'
    t1.mkdir()
    t2.mkdir()
    add_lines(t1)
    add_lines(t2)
    return tmp_path

def test_repository(root):
    repo = Repository(root, ['t1', 't2'])
    for t in repo.trackers():
        print(t)
    for l in repo.lines():
        print(l)
    for p in repo.protocols():
        print(p)
    for dt in repo.dates():
        print(dt)
    for trx in repo.trx():
        print(trx)

    print(repo['t1']['a@a']['p_0']['00000000_000000'].trx)
