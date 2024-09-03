# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

# determine 1st line of the address
from vipro_python.core.hashing import Hasher

def test_hasher():
  expected = "4dc1a602fada1a08eeecb20a0779b179b60df3dc792996204aa664190308b8b5"
  subject = Hasher(b"123", b"456")
  got = subject.sha256('1234567890')
  assert got == expected

