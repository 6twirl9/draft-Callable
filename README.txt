
Take advantage of Python's introspection, specifically, the inspect module.

- Redefine the parameter list

  Constantly repeating "dtype = tf.float32" is annoying.

  => t-BAR.py

- A reparametrized callable is still a callable. While in its "held"
  state, we can inject info from its environment. Constantly, specifying
  or restricted to using the default "name" is also annoying.

  With inspect, one can find out what the left hand side is!

  => t-FOO.py

VIM required to "see" the code as intended with fold merkers === & ///.

