#ifndef DEFINITION_H
#define DEFINITION_H

#include <vector>
#include <Eigen/Core>

namespace uav{

  //definition
  typedef Eigen::Vector3d Point;
  typedef Eigen::Vector4d Point4d;
  typedef std::vector<Point> Polytope;
  typedef Point (*trajectory)(Point, double);
  typedef std::vector<Point4d> Polytope4d;
  typedef Eigen::Matrix<double,8,1> Vector8d;

  //const int INFI = 1e+6; // INFI too big will induce problem with iris
  const double INFI = 1e+4; //for visualization
  
  class Formation{
    public:
      Formation(){}

      Formation(
          std::vector<Polytope> _uavs,
          std::vector<Polytope> _uavShapes,
          Polytope _convexHull,
          double _pref
          );

      std::vector<Polytope> uavs;
      std::vector<Polytope> uavShapes;
      Polytope convexHull;
      double pref;
      double minInterDis;
      double radius;
  };

}

#endif
