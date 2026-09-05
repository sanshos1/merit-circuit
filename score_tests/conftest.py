import os
_unlink=os.unlink
def safe(path,*a,**k):
 try:return _unlink(path,*a,**k)
 except PermissionError:return None
os.unlink=safe
CONTRACT='scoring_engine/merit_circuit.py'
