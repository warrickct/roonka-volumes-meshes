# random dev notes 

## todo
- [ ] refactor modifier additions
- [ ] convert to filetype suitable for use
- [ ] investigate removing erosion or large protusions e.g. in F142 vs F142b

## original approach
* bpy.ops.mesh.subdivide(number_cuts=3)
## curent method
* remesh up with increased octo-tree (around 8+), apply, shrinkwrap + apply -> smooth in various ways but most importantly using regular smooth, high repititions, factor that seemed to work nicely was /0.8
* tl;dr: remesh(octo=8, type=smooth) -> shrinkwrap(mode=surface) -> smooth(factor=0.8, repeat=30-100)
* sometimes smooth way more than that even

## other potential methods

* create a cube, remesh, have it encapsulate the target shape, shrinkwrap. Doing so creates a different output due to the way the remeshing creates vertices.
* Josh asked if stepping could be removed. Using nearest vertex shrinkwrapping could be a potential solution.

