import inspect

def GenConstClass(name,auto=True):  # ===

 class _: pass

 _.__qualname__ = 'FOO'

 if auto:
  globals()[name] = _
 else:
  return _

#///

ConstClass_List = ['Undefined','NotDefined','Default','Auto']

for each in ConstClass_List: GenConstClass(each)

class F:    # = =

 def __init__(self,func,*args,**krgs):  # ===

  #
  # Keep track of the callable object and its argument specification
  #
  self._func      = func
  self._spec      = inspect.getfullargspec(func)
  self._signature = inspect.signature(self._func)

  #
  # Reorder non-keyword-only arguments. Specify only those that you are interested
  # in and they will be place at the start in the order in which they are specified.
  #
  
  self._opt = { 'order': [] } # default to no reordering

  #
  # Parameter names prefixed with ':' are used to pass information to instances of class F
  #
  for k, v in krgs.items():

   if re.match('^:.*',k):

    self._opt[re.sub('^:','',k)] = v

  #
  # Delete parameters whose names prefixed with ':'
  #
  for k in krgs.keys():

   if re.match('^:.*',k):

    del krgs[k]

  #
  # Suppress debug messages
  #
  self.debug(-1)

  #
  # True implies returning the closure of the callable evaluated with given arguments
  #
  self.hold(True)

  #
  # True implies user's default values take precedence while processing the positional arguments
  # in order of their appearence in the argument list.
  #
  self.user_default_priority(True)

  self.default(*args,**krgs)

#///

 def info(self):                        # ===

  print(self._func)
  print(self._spec)
  print(self._signature)

#///

 def hold(self,hold=True):              # ===

  self._hold = hold

  return self

#///
 def unhold(self):                      # ===

  self._hold = False

  return self

#///

 def debug(self,debug=0):               # ===

  self._debug = debug

  return self

#///

 def default(self,*args,**krgs):        # ===

  if not getattr(self,'_default',None):

   self._default = { '.internal': { '.original': { 'args': [], 'krgs': {} } } }

  #
  # Attempt to bind the parameters. Not all parameters can be satisfied hence "partial".
  #
  self._default = self.parse(partial=True,args=args,krgs=krgs)

  return self

#///
 def user_default_priority(self,priority=True): # ===

  self._user_default_priority = priority

#///
 def order(self,*args):                 # ===

  #
  # Reorder positional parameters.
  #
  self._opt['order'] = []

  [ self._opt['order'].extend( _ if isinstance(_,(tuple,list)) else [_] ) for _ in args ]

  return self

#///

 def parse(self,partial=False,args=[],krgs={}):          # ===

  _args       = {}  # ===

  # === explicitly named parameter values

  for k, v in krgs.items():

   if k in self._spec.args:

    _args[k] = v

#///
  # === user default

  if self._user_default_priority:

   for k, v in self._default['.internal']['.original']['krgs'].items():

    _args[k] = v

#///
  # === positional parameters

  # === (partial) reordering of 'args' arguments

  if 'order' in self._opt:

   _spec_args = [ *self._opt['order'], *[ _ for _ in self._spec.args if _ not in self._opt['order'] ] ]

  else:

   _spec_args = self._spec.args

#///

  # === skip positional parameters already supplied with values
  for _ in ( set(_spec_args) & set(krgs.keys()) ):

   _spec_args.remove(_)

  if self._user_default_priority:

   for _ in ( set(_spec_args) & set(self._default['.internal']['.original']['krgs'].keys()) ):

    _spec_args.remove(_)

#///

  _args_i = 0
  for k, v in zip(_spec_args,args):

   if k not in _args or _args[k] is Undefined:

    _args[k] = v

    _args_i += 1

#///
  # === user default

  if not self._user_default_priority:

   for k, v in self._default['.internal']['args'].items():

    if k not in _args or _args[k] is Undefined:

     _args[k] = v

#///
  # === original default

  if self._spec.defaults is not None:

   for k, v in zip(self._spec.args[-1::-1],self._spec.defaults[-1::-1]):

    if k not in _args:

     _args[k] = v

#///

  #
  # In original order, before passing to the callable
  #
  _args = { k: ( _args[k] if k in _args else Undefined ) for k in self._spec.args }

#///

  #
  # ... rest of the non-keyword-only arguments
  #
  _varargs    = args[_args_i:]

  _kwonlyargs = {}
  _varkw      = {}  # ===

  for k, v in krgs.items():

   #
   # skip non-keyword-only parameters
   #
   if k not in self._spec.args:

    { True: _kwonlyargs, False: _varkw } [k in self._spec.kwonlyargs] [k] = v

#///

  parsed = \
  {
    'args': [  *_args.values(),  *_varargs ]
  , 'krgs': { **_kwonlyargs   , **_varkw   }
  , '.internal':
    {
      'args'      : _args
    , 'varargs'   : _varargs
    , 'kwonlyargs': _kwonlyargs
    , 'varkw'     : _varkw
    , '.original' :
      {
        'args': args
      , 'krgs': krgs
      }
    }
  , 'bind': None
  }

  try:

   _rgs = getattr(self._signature,{True: 'bind_partial', False: 'bind'}[partial])(*parsed['args'], **parsed['krgs'])
   _rgs.apply_defaults()

   parsed['bind'] = _rgs

  except Exception as e:

   print(f'[ERROR] :: F.parse ::',e)

  #
  # Expect all parameters with default values except those at the beginning of the para,eter list
  #
  complete = not any([ _ == Undefined for _ in [*parsed['args'],*parsed['krgs'].values()]])

  parsed['complete'] = complete

  return parsed

#///
 def parse_only(self,*args,**krgs):       # ===

  parsed = self.parse(args=args,krgs={**self._default['.internal']['kwonlyargs'],**krgs})

  return parsed

#///
 def __call__(self,*args,**krgs):       # ===

  parsed = self.parse(args=args,krgs={**self._default['.internal']['kwonlyargs'],**krgs})

 #print(parsed)

  if parsed['bind'] is None:

   hold = lambda : None

  else:

   hold = lambda : self._func(*parsed['bind'].args,**parsed['bind'].kwargs)

  return hold if self._hold else hold()

#///

#///
