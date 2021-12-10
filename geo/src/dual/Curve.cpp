#include "Curve.h"

#define CORNERANGLE 30

#define XIND 0
#define YIND 1
#define ZIND 2


#include <fstream>
#include <iostream>

std::ostream& operator<< (std::ostream& stream, const CurvePoint& cp)
{
    stream<<cp.myX<<'\t'<<cp.myY;
    return stream;
}
Curve::Curve(std::string filename)
{
    std::cout<<"Reading in curve from file "<<filename<<std::endl;
    std::ifstream in_file(filename.c_str());

    std::vector<CurvePoint> tmpVec;
     std::string cx,cy;
     double tx,ty;

     bool unset = true;
     in_file>>cx>>cy;
     tx = atof(cx.c_str());
     ty = atof(cy.c_str());

     while(!in_file.fail() && !in_file.eof())
     {
        if(cx != "NaN")
        {
            tmpVec.push_back(CurvePoint(tx,ty));
            if(unset)
            {
                std::get<XIND>(ll)=tx;
                std::get<YIND>(ll)=ty;
                std::get<XIND>(ur)=tx;
                std::get<YIND>(ur)=ty;
                unset=false;
            }
            if(tx < std::get<XIND>(ll))
                 std::get<XIND>(ll)=tx;
            if(tx > std::get<XIND>(ur))
                 std::get<XIND>(ur)=tx;
            if(ty < std::get<YIND>(ll))
                 std::get<YIND>(ll)=ty;
            if(ty > std::get<YIND>(ur))
                 std::get<YIND>(ur)=ty;


        } ///NAN CHECK
        else
        {

            inOrOut.push_back(checkDirectionAndFlip(tmpVec));

            myCurvePoints.push_back(tmpVec);

            tmpVec.resize(0,CurvePoint(0,0));

        }
        in_file>>cx>>cy;
        tx = atof(cx.c_str());
        ty = atof(cy.c_str());
     }

     inOrOut.push_back(checkDirectionAndFlip(tmpVec));
     myCurvePoints.push_back(tmpVec);
    in_file.close();


    ///MOVE THIS TO ITS OWN FUNCTION TO AVOID REWRITING A LOT
    ///JUST ADDED A VECTOR around the VECOTR OF POINTS
    ///NEED TO CHECK FOR +/- CCW OR CW and store that too.
    ///IF CW , need to reverse points
    ///
    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
    std::cout<<(inOrOut[lcv]?"in":"out")<<"Curve with "<<myCurvePoints[lcv].size()<<" points"<<std::endl;

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        fillDerivative(myCurvePoints[lcv]);

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        setTangentAngle(myCurvePoints[lcv]);

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        findCorners(myCurvePoints[lcv]);

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        findFeatures(myCurvePoints[lcv]);


}
Curve::Curve(const std::vector<float> &boundary_x, const std::vector<float> &boundary_y) ///Single curve constructor
{
    std::vector<CurvePoint> tmpVec;
    for(unsigned int lcv =0; lcv < boundary_x.size();++lcv)
        tmpVec.push_back(CurvePoint(boundary_x[lcv],boundary_y[lcv]));

    checkDirectionAndFlip(tmpVec);
    inOrOut.push_back(true);

    myCurvePoints.push_back(tmpVec);

     for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
    std::cout<<(inOrOut[lcv]?"in":"out")<<"Curve with "<<myCurvePoints[lcv].size()<<" points"<<std::endl;

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        fillDerivative(myCurvePoints[lcv]);

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        setTangentAngle(myCurvePoints[lcv]);

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        findCorners(myCurvePoints[lcv]);

    for(unsigned int lcv = 0;lcv < myCurvePoints.size();++lcv)
        findFeatures(myCurvePoints[lcv]);

}

bool Curve::featureInBoundingBox(std::tuple<double,double> ll,std::tuple<double,double> ur)
{
     ///Check whether any points of the feature are within the bounding box

   for(auto x : myFeatures)
   {
       if (x.X() <= std::get<XIND>(ur) && x.X() >= std::get<XIND>(ll) && x.Y() <= std::get<YIND>(ur) && x.Y() >= std::get<YIND>(ll) )
        return true;
   }
   return false;
}
bool Curve::inBoundingBox(std::tuple<double,double> ll,std::tuple<double,double> ur)
{

    ///Check whether any points of the curve are within the bounding box
   for(unsigned int lcv = 0; lcv < myCurvePoints.size();++lcv)
   for(auto x : myCurvePoints[lcv])
   {
       if (x.X() <= std::get<XIND>(ur) && x.X() >= std::get<XIND>(ll) && x.Y() <= std::get<YIND>(ur) && x.Y() >= std::get<YIND>(ll) )
        return true;
   }
   return false;
}
void Curve::write(std::string filename)
{

    std::ofstream out_file(filename.c_str());
    for(unsigned int lcv = 0; lcv < myCurvePoints.size();++lcv)
    {
        for(auto x: myCurvePoints[lcv])
            out_file<<x<<std::endl;
        if(lcv != myCurvePoints.size()-1)
            out_file<<"NaN\tNaN"<<std::endl;
    }

    out_file.close();

    out_file.open((filename+"features").c_str());
    for(unsigned int lcv = 0; lcv < myFeatures.size();++lcv)
    {
            out_file<<myFeatures[lcv]<<std::endl;
    }
    out_file.close();

    out_file.open((filename+"curvature").c_str());
    for(unsigned int lcv = 0; lcv < myCurvePoints.size();++lcv)
    {
         for(auto x: myCurvePoints[lcv])
            out_file<<x.X()<<"\t"<<x.Y()<<"\t"<<x.DX()<<"\t"<<x.DY()<<"\t"<<x.D2X()<<"\t"<<x.D2Y()<<"\t"<<x.curvature()<<std::endl;
            if(lcv != myCurvePoints.size()-1)
            out_file<<"NaN\tNaN"<<std::endl;
    }
    out_file.close();

}

bool Curve::checkDirectionAndFlip(std::vector<CurvePoint> &CurvePoints)
{
    std::vector<CurvePoint> tmp = CurvePoints;

    bool in = true;

    if(area(CurvePoints)<0)
        in=false;

    std::cout<<"deciding this loop is : "<<(in?"in":"out")<<std::endl;
    return in;
}
double Curve::area(std::vector<CurvePoint> &CurvePoints)
{
    double area = 0;
    for(unsigned int lcv = 0; lcv < CurvePoints.size();++lcv)
    {
        int lp1 = lcv+1;
        if(lp1 == CurvePoints.size())
            lp1 = 0;
        double crs = CurvePoints[lp1].Y()*CurvePoints[lcv].X()-CurvePoints[lcv].Y()*CurvePoints[lp1].X();
        area+=crs;
    }
    return area;
}
double Curve::cross(CurvePoint &A, CurvePoint &B, CurvePoint &C)
{
double fx = B.X()-A.X();
double fy = B.Y()-A.Y();
double tx = C.X()-B.X();
double ty = C.Y()-B.Y();

return fy*tx-fx*ty;

}
void Curve::fillDerivative(std::vector<CurvePoint> &CurvePoints)
{
     std::cout<<"Determining derivative... "<<std::endl;
    for(unsigned int lcv = 0;lcv < CurvePoints.size();++lcv)
    {
        int lp1 = lcv+1;
        int lm1 = lcv-1;
        if(lcv == 0)
            lm1=CurvePoints.size()-1;
        if(lcv == CurvePoints.size()-1)
            lp1=0;
        CurvePoints[lcv].DX(  (CurvePoints[lp1].X() -CurvePoints[lm1].X() )/2.0 );
        CurvePoints[lcv].DY(  (CurvePoints[lp1].Y() -CurvePoints[lm1].Y() )/2.0 );

        CurvePoints[lcv].D2X(  (-2*CurvePoints[lcv].X() +CurvePoints[lp1].X() +CurvePoints[lm1].X() ) );
        CurvePoints[lcv].D2Y(  (-2*CurvePoints[lcv].Y() + CurvePoints[lp1].Y() +CurvePoints[lm1].Y() ) );

        //std::cout<<"D2X : "<<CurvePoints[lcv].D2X()<<" D2Y: "<<CurvePoints[lcv].D2Y()<<std::endl;

            //if( (CurvePoints[lcv].D2X() < 1e-15 && CurvePoints[lcv].D2X() > -1e-15 ) || ( CurvePoints[lcv].D2Y() < 1e-15 && CurvePoints[lcv].D2Y() > -1e-15 )  )
              //  CurvePoints[lcv].curvature(std::infinity);
            //else
                CurvePoints[lcv].curvature(pow(CurvePoints[lcv].DX()*CurvePoints[lcv].DX()+CurvePoints[lcv].DY()*CurvePoints[lcv].DY(),3.0/2.0)/pow(pow(CurvePoints[lcv].DX()*CurvePoints[lcv].D2Y()-CurvePoints[lcv].DY()*CurvePoints[lcv].D2X(),2),.50));
    }
}
void Curve::setTangentAngle(std::vector<CurvePoint> &CurvePoints)
{
 std::cout<<"Setting tangent and angle... "<<std::endl;
    for(unsigned int lcv = 0;lcv < CurvePoints.size();++lcv)
    {
         if(!std::isnan(CurvePoints[lcv].DX())&&!std::isnan(CurvePoints[lcv].DY()) )
        {
            double magval = sqrt(CurvePoints[lcv].DX()*CurvePoints[lcv].DX()+CurvePoints[lcv].DY()*CurvePoints[lcv].DY());
            CurvePoints[lcv].tangent(CurvePoints[lcv].DY()/magval,CurvePoints[lcv].DX()/magval);
        }
        else
        {
            std::cout<<"?"<<std::endl;
            CurvePoints[lcv].tangent(1,0);
        }
    }
}
void Curve::findCorners(std::vector<CurvePoint> &CurvePoints)
{
    std::cout<<"Finding corners... "<<std::endl;
    for(unsigned int lcv = 0;lcv < CurvePoints.size();++lcv)
    {
         if(!std::isnan(CurvePoints[lcv].DX())&&!std::isnan(CurvePoints[lcv].DY()) )
         {


        unsigned int p1 = lcv+1;
        if(p1==CurvePoints.size())
            p1 = 0;
        double delAngle = (CurvePoints[p1].angle()-CurvePoints[lcv].angle())*180/3.14159;
        if(delAngle<0)
            delAngle=delAngle*-1;
        if(delAngle > 180 ) ///180 flip error??? noise in derivative???
            delAngle = delAngle-180;

        if(delAngle > 170 && delAngle < 190) ///180 flip error??? noise in derivative???
            delAngle = 0;


        ///ANGLE is in Degrees
        if(delAngle > CORNERANGLE )
        {
          myCorners.push_back(CurvePoints[lcv]);
          std::cout<<" Adding corner point at "<<CurvePoints[lcv]<<" delAngle "<<delAngle<<" lcv: "<<lcv<<std::endl;
        }
         }
         else
            std::cout<<"How did a nan slip in?"<<std::endl;


    }
}
void Curve::findFeatures(std::vector<CurvePoint> &CurvePoints)
{
      std::cout<<"Finding features... "<<std::endl;
    for(unsigned int lcv = 0;lcv < CurvePoints.size();++lcv)
    {
         if(!std::isnan(CurvePoints[lcv].DX())&&!std::isnan(CurvePoints[lcv].DY()) )
         {

            double kurv = CurvePoints[lcv].curvature();
            if(kurv < 0)
                kurv =kurv *-1;

        if(kurv <= 2.75 && kurv > 0.1250 )//&& notACorner(CurvePoints[lcv]))
        {
          myFeatures.push_back(CurvePoints[lcv]);
          std::cout<<" Adding feature point at "<<CurvePoints[lcv]<<" kurvature  "<<kurv<<" lcv: "<<lcv<<std::endl;
        }
         } //if
         else
            std::cout<<"How did a nan slip in?"<<std::endl;


    }
}
bool Curve::notACorner(CurvePoint &cp)
{
    for(unsigned int lcv =0; lcv < myCorners.size();++lcv)
        if(cp.X() == myCorners[lcv].X() && cp.Y() == myCorners[lcv].Y() )
        return false;
return true;
}
std::tuple<double,double> Curve::nearestPt(double x, double y)
{
    double nx,ny;
    double dist=1e9;
    int lind,pind;
    for(unsigned int lcv = 0; lcv < myCurvePoints.size();++lcv)
    {
        for(unsigned int pt=0; pt < myCurvePoints[lcv].size();++pt)
        {
            double tdist = ( myCurvePoints[lcv][pt].X()-x)*( myCurvePoints[lcv][pt].X()-x)+( myCurvePoints[lcv][pt].Y()-y)*( myCurvePoints[lcv][pt].Y()-y);
            if(lcv == 0 && pt == 0)
            {
                nx = myCurvePoints[lcv][pt].X();
                ny = myCurvePoints[lcv][pt].Y();
                dist = (nx-x)*(nx-x)+(ny-y)*(ny-y);
                lind = 0;pind=0;
            }
            else
            {
                if(tdist < dist)
            {
                 nx = myCurvePoints[lcv][pt].X();
                ny = myCurvePoints[lcv][pt].Y();
                dist = tdist;
                lind = lcv;
                pind = pt;
            }
            }

        }
    }

    return std::tuple<double,double> (nx,ny);
}
std::tuple<double,double> Curve::nextNearestPt(double x, double y,int direction)
{

    double nx,ny;
    double dist=1e9;
    int lind,pind;
    for(unsigned int lcv = 0; lcv < myCurvePoints.size();++lcv)
    {
        for(unsigned int pt=0; pt < myCurvePoints[lcv].size();++pt)
        {
            double tdist = ( myCurvePoints[lcv][pt].X()-x)*( myCurvePoints[lcv][pt].X()-x)+( myCurvePoints[lcv][pt].Y()-y)*( myCurvePoints[lcv][pt].Y()-y);
            if(lcv == 0 && pt == 0)
            {
                nx = myCurvePoints[lcv][pt].X();
                ny = myCurvePoints[lcv][pt].Y();
                dist = (nx-x)*(nx-x)+(ny-y)*(ny-y);
                lind = 0;pind=0;
            }
            else
            {
                if(tdist < dist)
            {
                 nx = myCurvePoints[lcv][pt].X();
                ny = myCurvePoints[lcv][pt].Y();
                dist = tdist;
                lind = lcv;
                pind = pt;
            }
            }

        }
    }
//std::cout<<"pind before: "<<pind<<std::endl;
  //  if(inOrOut[lind]==false )
    //    direction = -1*direction;
    if(direction > 0)
    { ///CCW // pt+1

        pind++;
        if(pind == myCurvePoints[lind].size())
            pind = 0;
    }
    else
    {
        pind--;
        if(pind<0)
            pind = myCurvePoints[lind].size()-1;
    }
    nx = myCurvePoints[lind][pind].X();
    ny = myCurvePoints[lind][pind].Y();
//    std::cout<<"pind after: "<<pind<<std::endl;
    return std::tuple<double,double> (nx,ny);
}
//**********************************************************************************//
//"isLeft" "crossingNumber" and "windingNumber"  function take from pg 48 of Practical Geometry Algorithms by Daniel Sunday PhD
//We use his algorithm for Winding number
//Copyright 2001, 2012, 2021 Dan Sunday
//This code may be freely used and modified for any purpose
//providing that this copyright notice is included with it.
//There is no warranty for this code, and the author of it cannot
//be held liable for any real or imagined damage from its use.
//Users of this code must verify correctness for their application.
//isLeft : tests if a point is Left|On|Right of an infinite line.
//Input is three points P0, P1, P2
//Return:  >0 for P2 eft of the line through P0 and P1
//            =0 for P2 on the line
//          <0 for P2 right of the line
inline double isLeft(CurvePoint &P0,CurvePoint &P1,CurvePoint &P2)
{
    return ( (P1.X()-P0.X())*(P2.Y()-P0.Y()) - (P2.X()-P0.X())*(P1.Y()-P0.Y())      );
}

//crossingNumber : tests for a point in a polygon
// Input:   P a point, V[] vertex points of a polygon V[n+1] with V[n] = V[0]
// Return: 0 = outside , 1 = inside
//This code is patterned after [Wm Randolph Franklin, "PNPOLY - Point Inclusion in Polygon Test" Web Page 2000
inline int crossingNumber(CurvePoint P,std::vector<CurvePoint> V)
{
int cn= 0;
//loop through edges of polygon
for(unsigned int i=0; i<V.size()-1;++i)
{
    if(  (( V[i].Y()<=P.Y()) && (V[i+1].Y() > P.Y() ))
         || ( ((V[i].Y()>P.Y()) && (V[i+1].Y()<=P.Y()))    ))
    {
        float vt = (float)(P.Y()-V[i].Y())/(V[i+1].Y()-V[i].Y());
        float x_intersect = V[i].X()+vt*(V[i+1].X()-V[i].X());
        if(P.X() < x_intersect)
            ++cn;
    }
}
return (cn&1); // 0 if even (out), 1 if odd (in)
}

//windingNumber
// Input P point
//      V[] vertex of points of polygon with   V[n+1] with V[n] = V[0]
// Return wn the winding number (=0 only when P is outside )
inline int windingNumber(CurvePoint P,  std::vector<CurvePoint> &V)
{
    int wn=0;
    //loop through edges of polygon
    for(unsigned int i=0; i<V.size();++i)
    {
        unsigned int ip1 = i+1;
        if(ip1==V.size())
            ip1 = 0;
        if(V[i].Y()<=P.Y())
        {
            if(V[ip1].Y() > P.Y())
            if(isLeft(V[i],V[ip1],P)>0)
                ++wn;
        }
        else
        {
            if(V[ip1].Y()<=P.Y())
                if(isLeft(V[i],V[ip1],P)<0)
                --wn;
        }
    }
    return wn;
}
//**********************************************************************************//
bool Curve::inCurve(double x, double y)
{
 bool in=false;
     CurvePoint p(x,y);
     for(unsigned int lcv = 0; lcv < myCurvePoints.size();++lcv)
     {
            if(windingNumber(p,myCurvePoints[lcv])!=0) ///Inside the loop
            {
                 if(inOrOut[lcv])
                    in = true;
                 else
                    in=false;
            }
     }


     return in;
}
