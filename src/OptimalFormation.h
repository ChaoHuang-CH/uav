#ifndef OPTIMAL_FORMATION_H
#define OPTIMAL_FORMATION_H

#include <Eigen/Core>
#include <vector>
#include "util.h"
#include "definition.h"
#include <exception>

namespace uav{
  class OptimalFormationError: public std::exception{
    public:
      const char* what() const throw(){
        return "OptimalFormation's static variables haven't been initialized, call OptimalFormation::init() first";
      }
  };

  class OptimalFormation{
    public:

      OptimalFormation(){}

      OptimalFormation(
          const std::vector<Formation> &_formations
          ):
        formations_(_formations)
    {

    }

    public:

      // getter
      std::vector<Formation> getFormations(){
        return formations_;
      }

      // setter
      void setFormations(const std::vector<Formation> &_formations){
        formations_ = _formations;
      }

      // all formations
      std::vector<Formation> formations_;

      // return index of optimal formation
      // deviation is passed through param
      int optimalFormation(Vector8d &param);

      // return minimal loss
      // the optimal param is passed through param
      double optimalDeviation(const Formation &formation, Vector8d &param);

      // for snopt
      static void init(const Eigen::MatrixXd &_A, const Eigen::VectorXd &_b,
          const Point &_gPref, const double &_sPref, const Eigen::Vector4d &_qPref,
          const double &_wT, const double &_wS, const double &_wQ,
          const double &_timeInterval){
        sA_ = _A;
        sB_ = _b;
        sG_ = _gPref;
        sS_ = _sPref;
        sQ_ = _qPref;
        sWT_ = _wT;
        sWS_ = _wS;
        sWQ_ = _wQ;
        sTimeInterval_ = _timeInterval;
        sInitialized_ = true;
      }

      // for a specific formation
      static Formation sFormation_;

      // for all formations
      static bool sInitialized_;

      static Point sG_;
      static double sS_;
      static Eigen::Vector4d sQ_;
      static double sWT_, sWS_, sWQ_;
      static double sTimeInterval_;

      static Eigen::MatrixXd sA_;
      static Eigen::VectorXd sB_;

      static void sUsrfg_( int    *Status, int *n,    double x[],
          int    *needF,  int *neF,  double F[],
          int    *needG,  int *neG,  double G[],
          char      *cu,  int *lencu,
          int    iu[],    int *leniu,
          double ru[],    int *lenru );

  };
}

#endif
