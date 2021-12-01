#ifndef SURFACE_H
#define SURFACE_H

#include <string>
#include <tuple>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <iostream>

class SurfacePoint
{
public:
    SurfacePoint(double xx,double yy,double zz){myX=xx;myY=yy;myZ=zz;}

    double Y(){return myY;}
    double X(){return myX;}
    double Z(){return myZ;}
    void DX(double d){myDX = d;}
    double DX(){return myDX;}
    void DY(double d){myDY = d;}
    double DY(){return myDY;}
    void DZ(double d){myDZ = d;}
    double DZ(){return myDZ;}

    //void tangent(double tx,double ty){myTanX=tx;myTanY=ty;myAngle=std::atan2(ty,tx);}
    //double angle(){return myAngle;}
    friend std::ostream& operator<< (std::ostream& stream, const SurfacePoint& cp);


private:
    double myX,myY,myZ;
    double myDX,myDY,myDZ;
   //double myTanX,myTanY,myAngle;
    ///double angle,normal,tangent,curvature; <<<< WERE ANY OF THESE ACTUALLY NEEDED IN THE END?
};

class Surface
{
    public:
       Surface(std::string filename);
        std::tuple<double,double,double> upperBound(){return maxs;}
        std::tuple<double,double,double> lowerBound(){return mins;}

        bool inBoundingBox(std::tuple<double,double,double> lb,std::tuple<double,double,double> ub);
        void write(std::string filename);
    private:
        std::vector<SurfacePoint> mySurfacePoints;
        std::vector<SurfacePoint> myCorners;
        std::tuple<double,double,double> mins,maxs;
        std::vector<std::tuple<unsigned int,unsigned int,unsigned int> > myTris;
        void stringSplit(std::string s,double &x,double &y, double &z);

};

#endif

