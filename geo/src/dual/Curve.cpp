#include "Curve.h"

#define CORNERANGLE 20

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
    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        std::cout<<(inOrOut[lcv]?"in":"out")<<"Curve with "<<myCurvePoints[lcv].size()<<" points"<<std::endl;

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        fillDerivative(myCurvePoints[lcv]);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        setTangentAngle(myCurvePoints[lcv]);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        findCorners(myCurvePoints[lcv]);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        findFeatures(myCurvePoints[lcv]);


}
Curve::Curve(const std::vector<float> &boundary_x, const std::vector<float> &boundary_y) ///Single curve constructor
{
    CurvePoint cp(0,0);
    std::vector<CurvePoint> tmpVec;
    bool unset = true;
    for(unsigned int lcv =0; lcv < boundary_x.size(); ++lcv)
    {
        if(!std::isnan(boundary_x[lcv]))
        {
            tmpVec.push_back(CurvePoint(boundary_x[lcv],boundary_y[lcv]));
            if(unset)
            {
                std::get<XIND>(ll)=boundary_x[lcv];
                std::get<YIND>(ll)=boundary_y[lcv];
                std::get<XIND>(ur)=boundary_x[lcv];
                std::get<YIND>(ur)=boundary_y[lcv];
                unset=false;
            }
            if(boundary_x[lcv] < std::get<XIND>(ll))
                std::get<XIND>(ll)=boundary_x[lcv];
            if(boundary_x[lcv] > std::get<XIND>(ur))
                std::get<XIND>(ur)=boundary_x[lcv];
            if(boundary_y[lcv] < std::get<YIND>(ll))
                std::get<YIND>(ll)=boundary_y[lcv];
            if(boundary_y[lcv] > std::get<YIND>(ur))
                std::get<YIND>(ur)=boundary_y[lcv];
        }
        else
        {
            inOrOut.push_back(checkDirectionAndFlip(tmpVec));
            myCurvePoints.push_back(tmpVec);
            tmpVec.resize(0,cp);
        }

    }

    inOrOut.push_back(checkDirectionAndFlip(tmpVec));
    myCurvePoints.push_back(tmpVec);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        std::cout<<(inOrOut[lcv]?"in":"out")<<"Curve with "<<myCurvePoints[lcv].size()<<" points"<<std::endl;

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        fillDerivative(myCurvePoints[lcv]);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        setTangentAngle(myCurvePoints[lcv]);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        findCorners(myCurvePoints[lcv]);

    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        findFeatures(myCurvePoints[lcv]);

}

bool Curve::featureInBoundingBox(std::tuple<double,double> ll,std::tuple<double,double> ur)
{
    ///Check whether any points of the feature are within the bounding box
    ///FEATURE IS A POINT CLOUD REFINEMENT
    ///the other method has been modified to have parametric curve description
    for(auto x : myFeatures)
    {
        if (x.X() <= std::get<XIND>(ur) && x.X() >= std::get<XIND>(ll) && x.Y() <= std::get<YIND>(ur) && x.Y() >= std::get<YIND>(ll) )
            return true;
    }
    return false;
}
bool Curve::inBoundingBox(std::tuple<double,double> ll,std::tuple<double,double> ur)
{
    ///First check to see if any point from the curve is inside the bounding box
    ///During this loop find the point that is nearest the center of the bounding box?
    ///Use this closest point and the 2 next nearest points to draw 2 line segments
    ///Then check to see if either of these line segments pass through the bounding box by splitting it into 2 tris.

    double cx = std::get<XIND>(ll)*0.5+ std::get<XIND>(ur)*0.5;
    double cy = std::get<YIND>(ll)*0.5+ std::get<YIND>(ur)*0.5;
    unsigned int cl=0;
    unsigned int cl2=0;
    double dist = (myCurvePoints[cl][cl2].X()-cx)*(myCurvePoints[cl][cl2].X()-cx) + (myCurvePoints[cl][cl2].Y()-cy)*(myCurvePoints[cl][cl2].Y()-cy) ;

    ///Check whether any points of the curve are within the bounding box
    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
        for(unsigned int lcv2 = 0; lcv2 < myCurvePoints[lcv].size(); ++lcv2)
        {
            if (myCurvePoints[lcv][lcv2].X() <= std::get<XIND>(ur) && myCurvePoints[lcv][lcv2].X() >= std::get<XIND>(ll) && myCurvePoints[lcv][lcv2].Y() <= std::get<YIND>(ur) && myCurvePoints[lcv][lcv2].Y() >= std::get<YIND>(ll) )
                return true;
            double dist2 = (myCurvePoints[cl][cl2].X()-cx)*(myCurvePoints[cl][cl2].X()-cx) + (myCurvePoints[cl][cl2].Y()-cy)*(myCurvePoints[cl][cl2].Y()-cy) ;
            if(dist2 < dist)
            {
                dist = dist2;
                cl = lcv;
                cl2 = lcv2;

            }

        }


    unsigned int cl2p1 = cl2+1;
    if(cl2p1 >= myCurvePoints[cl].size())
        cl2p1=0;
    unsigned int cl2m1;

    if(cl2 ==0)
        cl2m1=myCurvePoints[cl].size()-1;
    else
        cl2m1 = cl2-1;

    std::tuple<double,double,double> A(std::get<XIND>(ll),std::get<YIND>(ll),0);
    std::tuple<double,double,double> B(std::get<XIND>(ur),std::get<YIND>(ll),0);
    std::tuple<double,double,double> C(std::get<XIND>(ur),std::get<YIND>(ur),0);
    std::tuple<double,double,double> D(std::get<XIND>(ll),std::get<YIND>(ur),0);
///Tri 1 A,B,C
    ///Tri 2 A,C,D


    return false;
}
bool Curve::intersects(const std::tuple<double,double,double> &T1,const std::tuple<double,double,double> &T2,const std::tuple<double,double,double> &T3,const std::tuple<double,double,double> &P1,const std::tuple<double,double,double> &P2)
{
    ///Test whether line segment P1 -- P2  crosses through Triangle T1 -- T2 -- T3 (CCW)
    ///2D version, use P1 -- P2 as local x-axis, rotate T1, T2, T3 to this new coordinate system.
    ///Test to see if P1 -- P2 splits y coordinates (2 over 1 under, or 1 over 2 under , along line special cases)

    double P2P1x = std::get<XIND>(P2)-std::get<XIND>(P1);
    double P2P1y = std::get<YIND>(P2)-std::get<YIND>(P1);
    double cx = (std::get<XIND>(P2)+std::get<XIND>(P1))/2.0;
    double cy = (std::get<YIND>(P2)+std::get<YIND>(P1))/2.0;

    double nm = sqrt(P2P1x*P2P1x+P2P1y*P2P1y);
    if(nm ==0)
        return false;

    P2P1x = P2P1x/nm;
    P2P1y = P2P1y/nm;

    double theta = acos(P2P1x);

    ///Rotation matrix : [cos -sin ; sin cos ]
    double nt1y =  (std::get<YIND>(T1)-cy)*cos(theta)+(std::get<XIND>(T1)-cx)*sin(theta);
    double nt2y =  (std::get<YIND>(T2)-cy)*cos(theta)+(std::get<XIND>(T2)-cx)*sin(theta);
    double nt3y =  (std::get<YIND>(T3)-cy)*cos(theta)+(std::get<XIND>(T3)-cx)*sin(theta);

    /*std::cout<<"nt1y : "<<nt1y<<std::endl;
    std::cout<<"nt2y : "<<nt2y<<std::endl;
    std::cout<<"nt3y : "<<nt3y<<std::endl;
*/

    int sum = 0;
    sum= sign(nt1y)+sign(nt2y)+sign(nt3y);

    ///TODO ABS VAL < SMALL NUMBER
    if(nt1y == 0 || nt2y == 0 || nt3y == 0)
        return true;
    if(sum == 1 || sum == -1)
    return true;

    return false;
}


/*https://stackoverflow.com/questions/42740765/intersection-between-line-and-triangle-in-3d
1) If you just want to know whether the line intersects the triangle (without needing the actual intersection point):

Let p1,p2,p3 denote your triangle

Pick two points q1,q2 on the line very far away in both directions.

Let SignedVolume(a,b,c,d) denote the signed volume of the tetrahedron a,b,c,d.

If SignedVolume(q1,p1,p2,p3) and SignedVolume(q2,p1,p2,p3) have different signs AND SignedVolume(q1,q2,p1,p2), SignedVolume(q1,q2,p2,p3) and SignedVolume(q1,q2,p3,p1) have the same sign, then there is an intersection.
*/

void Curve::write(std::string filename)
{

    std::ofstream out_file(filename.c_str());
    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
    {
        for(auto x: myCurvePoints[lcv])
            out_file<<x<<std::endl;
        if(lcv != myCurvePoints.size()-1)
            out_file<<"NaN\tNaN"<<std::endl;
    }

    out_file.close();

    out_file.open((filename+"features").c_str());
    for(unsigned int lcv = 0; lcv < myFeatures.size(); ++lcv)
    {
        out_file<<myFeatures[lcv]<<std::endl;
    }
    out_file.close();

    out_file.open((filename+"curvature").c_str());
    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
    {
        for(auto x: myCurvePoints[lcv])
            out_file<<x.X()<<"\t"<<x.Y()<<"\t"<<x.DX()<<"\t"<<x.DY()<<"\t"<<x.D2X()<<"\t"<<x.D2Y()<<"\t"<<x.curvature()<<std::endl;
        if(lcv != myCurvePoints.size()-1)
            out_file<<"NaN\tNaN"<<std::endl;
    }
    out_file.close();
    out_file.open((filename+"corners").c_str());
    for(unsigned int lcv = 0; lcv < myCorners.size(); ++lcv)
    {

        out_file<<myCorners[lcv].X()<<"\t"<<myCorners[lcv].Y()<<std::endl;

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
    /// #warning "This is not an actual area calculation"
    ///just for sign not actual area
    double area = 0;
    for(unsigned int lcv = 0; lcv < CurvePoints.size(); ++lcv)
    {
        int lp1 = lcv+1;
        if(lp1 == (int)CurvePoints.size())
            lp1 = 0;
        double crs = CurvePoints[lp1].Y()*CurvePoints[lcv].X()-CurvePoints[lcv].Y()*CurvePoints[lp1].X();
        area+=crs;
    }
    return area;
}
///TODO Rename this function to something more descriptive and propagate changes
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
    for(unsigned int lcv = 0; lcv < CurvePoints.size(); ++lcv)
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
    for(unsigned int lcv = 0; lcv < CurvePoints.size(); ++lcv)
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
    bool firstcorneriszero =false;
    unsigned int lastCorner = CurvePoints.size();
    //std::ofstream out_file("delangles");
    std::cout<<"Finding corners... "<<std::endl;
    for(unsigned int lcv = 0; lcv < CurvePoints.size(); ++lcv)
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

            //out_file<<delAngle<<std::endl;
            ///ANGLE is in Degrees
            if(delAngle > CORNERANGLE )
            {
                if(lcv == 0)
                    firstcorneriszero=true;
                unsigned int lp1 = lastCorner+1;
                if(lp1 > CurvePoints.size())
                    lp1 = lp1-CurvePoints.size();
                if(lp1!=lcv )
                {
                    if( !(lcv == CurvePoints.size()-1 && firstcorneriszero ))
                    {
                        myCorners.push_back(CurvePoints[lcv]);
                        std::cout<<" Adding corner point at "<<CurvePoints[lcv]<<" delAngle "<<delAngle<<" lcv: "<<lcv<<std::endl;
                        lastCorner=lcv;
                    }
                }

            }
        }
        else
            std::cout<<"How did a nan slip in?"<<std::endl;


    }
    //out_file.close();
}
void Curve::findFeatures(std::vector<CurvePoint> &CurvePoints)
{
    std::cout<<"Finding features... "<<std::endl;
    for(unsigned int lcv = 0; lcv < CurvePoints.size(); ++lcv)
    {
        if(!std::isnan(CurvePoints[lcv].DX())&&!std::isnan(CurvePoints[lcv].DY()) )
        {

            double kurv = CurvePoints[lcv].curvature();


            if(kurv < 0)
                kurv =kurv *-1;

            if(kurv <= 2.75 && kurv > 0.1250 )//&& notACorner(CurvePoints[lcv]))
            {
                myFeatures.push_back(CurvePoints[lcv]);
                //std::cout<<" Adding feature point at "<<CurvePoints[lcv]<<" kurvature  "<<kurv<<" lcv: "<<lcv<<std::endl;
            }
        } //if
        else
            std::cout<<"How did a nan slip in?"<<std::endl;


    }
    std::cout<<"Done with features."<<std::endl;
}
bool Curve::notACorner(CurvePoint &cp)
{
    for(unsigned int lcv =0; lcv < myCorners.size(); ++lcv)
        if(cp.X() == myCorners[lcv].X() && cp.Y() == myCorners[lcv].Y() )
            return false;
    return true;
}
std::tuple<double,double> Curve::nearestPt(double x, double y)
{
    /// #warning "This function depends on the curve resolution"
    double nx,ny;
    double dist=1e9;
    int lind=0;
    int pind=0;
    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
    {
        for(unsigned int pt=0; pt < myCurvePoints[lcv].size(); ++pt)
        {
            double tdist = ( myCurvePoints[lcv][pt].X()-x)*( myCurvePoints[lcv][pt].X()-x)+( myCurvePoints[lcv][pt].Y()-y)*( myCurvePoints[lcv][pt].Y()-y);
            if(lcv == 0 && pt == 0)
            {
                nx = myCurvePoints[lcv][pt].X();
                ny = myCurvePoints[lcv][pt].Y();
                dist = (nx-x)*(nx-x)+(ny-y)*(ny-y);
                lind = 0;
                pind=0;
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


    unsigned int pindp1 = pind+1;
    if(pindp1 >= myCurvePoints[lind].size())
        pindp1=0;
    unsigned int pindm1;
    if(pind == 0)
        pindm1 = myCurvePoints[lind].size()-1;
    else
        pindm1 = pind-1;

    double distp1 = sqrt(( x-myCurvePoints[lind][pindp1].X())*( x-myCurvePoints[lind][pindp1].X())
                    +( y-myCurvePoints[lind][pindp1].Y())*( y-myCurvePoints[lind][pindp1].Y()));

    double distm1 = sqrt(( x-myCurvePoints[lind][pindm1].X())*( x-myCurvePoints[lind][pindm1].X())
                    +( y-myCurvePoints[lind][pindm1].Y())*( y-myCurvePoints[lind][pindm1].Y()));


     dist = sqrt(dist);

    if(distp1 < distm1)
    {
        double sum = dist+distp1;

       // std::cout<<"Sum : "<<sum<<" dist "<<dist<<" distp1 "<<distp1<<" ratio "<<dist/sum<<" ratio "<<distp1/sum<<std::endl;

        nx = distp1/sum*(myCurvePoints[lind][pind].X())+dist/sum*(myCurvePoints[lind][pindp1].X());
        ny = distp1/sum*(myCurvePoints[lind][pind].Y())+dist/sum*(myCurvePoints[lind][pindp1].Y());
    }
    else
    {
     double sum = dist+distm1;

     //std::cout<<"Sum : "<<sum<<" dist "<<dist<<" distm1 "<<distm1<<" ratio "<<dist/sum<<" ratio "<<distm1/sum<<std::endl;
        nx = distm1/sum*(myCurvePoints[lind][pind].X())+dist/sum*(myCurvePoints[lind][pindm1].X());
        ny = distm1/sum*(myCurvePoints[lind][pind].Y())+dist/sum*(myCurvePoints[lind][pindm1].Y());

    }




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
    for(unsigned int i=0; i<V.size()-1; ++i)
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
    for(unsigned int i=0; i<V.size(); ++i)
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
    int count=0;
    CurvePoint p(x,y);
    for(unsigned int lcv = 0; lcv < myCurvePoints.size(); ++lcv)
    {
        if(windingNumber(p,myCurvePoints[lcv])!=0) ///Inside the loop
        {
            if(inOrOut[lcv]) ///this loops says it's in
                count+=1;
            else
                count= count-1;
        }
    }


    return (count>0);
}
