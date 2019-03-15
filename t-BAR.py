#!/usr/bin/env python

from util.F import F

def BAR(_0,_1,_2=2,_3=3,*args,_4=4,_5=5,**kargs):

 return (_0,_1,_2,_3,args,_4,_5,kargs)

#
# - swap arg 0 & 1
# - change default value for _5
#

BAR_alt      = F(BAR).order('_1','_0').default(_5=105).unhold()

#
# - swap arg 1 & 2
# - change default value for _5
# - positional _0 -> named _0
#

BAR_alt_held = F(BAR).order('_2','_1').default(_0=100,_5=105).  hold()

print("\nOriginal:")
print(BAR(0,1))

print("\nModified: reordered & redefined")
print(BAR_alt(0,1))

print("\nModified: reordered & redefined [HELD] -> lambda")
print(BAR_alt_held(0,1))

print("\n        : \"call\" it again!")
print(BAR_alt_held(0,1)())

print('')

