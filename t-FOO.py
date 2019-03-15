#!/usr/bin/env python

import inspect
import yaml
from util.F import Undefined

class FOO:

 def getLHSName(self,verbose=0):    # ===

  l = inspect.currentframe().f_back.f_back.f_locals

  if verbose >= 3:

   print('inspect.currentframe().f_back.f_back.f_locals ->\n')
   print(yaml.dump(l))

  name = Undefined

  if verbose >= 1: print('\nTARGET ->',self,'\n')

  found = False
  for k, v in l.items():

   if verbose >= 1: print(f'TRY {k:>32s}',end='')
   if v == self:
    if verbose >= 1: print(' ... FOUND',v)
    name = k
    found = True
    break

   if k == 'self':
    for k, v in inspect.getmembers(v):
     if v == self:
      if verbose >= 1: print(' ... FOUND',v)
      name = k
      found = True
      break
     if found: break

   if verbose >= 1: print('')

  if verbose >= 1: print('')

  return name

#///

 def __call__(self,verbose=0):

  return self.getLHSName(verbose)

LHS = FOO()

print(f'LHS = FOO() => {LHS(True)} = {LHS}')
print('')

