#ifndef UTIL_H
#define UTIL_H

#include <vector>
#include <Eigen/Core>
#include "iris/iris.h"
#include "iris/iris_mosek.h"
#include "definition.h"

namespace uav{

  Polytope minkowskiSum(const Polytope &lhs, const Polytope &rhs);

  //return polytope after moving
  Polytope polytopeAfterMove(const Polytope &poly, double time, trajectory m);

  //return poly4d appending x to each vertice in poly3d
  Polytope4d poly3dToPoly4d(const Polytope &poly3d, double x);

  //return bounds generated from lb to ub
  iris::Polyhedron getPolyFromBounds(const Point4d&, const Point4d&);

}

#endif
