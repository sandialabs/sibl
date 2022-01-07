#ifndef SURFACE_H
#define SURFACE_H

#define XX 0
#define YY 0
#define ZZ 0
#include <string>
#include <tuple>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <iostream>

class SurfacePoint
{
public:
    SurfacePoint(double xx,double yy,double zz)
    {
        myX=xx;
        myY=yy;
        myZ=zz;
    }

    double Y()
    {
        return myY;
    }
    double X()
    {
        return myX;
    }
    double Z()
    {
        return myZ;
    }
    void DX(double d)
    {
        myDX = d;
    }
    double DX()
    {
        return myDX;
    }
    void DY(double d)
    {
        myDY = d;
    }
    double DY()
    {
        return myDY;
    }
    void DZ(double d)
    {
        myDZ = d;
    }
    double DZ()
    {
        return myDZ;
    }

    //void tangent(double tx,double ty){myTanX=tx;myTanY=ty;myAngle=std::atan2(ty,tx);}
    //double angle(){return myAngle;}
    friend std::ostream& operator<< (std::ostream& stream, const SurfacePoint& cp);


private:
    double myX,myY,myZ;
    double myDX,myDY,myDZ;
    //double myTanX,myTanY,myAngle;
    ///double angle,normal,tangent,curvature; <<<< WERE ANY OF THESE ACTUALLY NEEDED IN THE END?
};
inline std::tuple<double,double,double> crossProduct(const std::tuple<double,double,double> &A,const  std::tuple<double,double,double> &B)
{
    std::tuple<double,double,double> C;

    double ax,ay,az;
    double bx,by,bz;

    ax = std::get<XX>(A);
    ay = std::get<YY>(A);
    az = std::get<ZZ>(A);
    bx = std::get<XX>(B);
    by = std::get<YY>(B);
    bz = std::get<ZZ>(B);

    std::get<XX>(C)=(ay*bz-az*by);
    std::get<YY>(C)=(az*bx-ax*bz);
    std::get<ZZ>(C)=(ax*by-ay*bx);

    return C;
}
inline double dotProduct(const std::tuple<double,double,double> &A,const  std::tuple<double,double,double> &B)
{
    double ax,ay,az;
    double bx,by,bz;

    ax = std::get<XX>(A);
    ay = std::get<YY>(A);
    az = std::get<ZZ>(A);
    bx = std::get<XX>(B);
    by = std::get<YY>(B);
    bz = std::get<ZZ>(B);

    return ax*bx+ay*by+az*bz;
}

inline std::tuple<double,double,double> subtract(const std::tuple<double,double,double> &A,const  std::tuple<double,double,double> &B)
{
    std::tuple<double,double,double> C;

    double ax,ay,az;
    double bx,by,bz;

    ax = std::get<XX>(A);
    ay = std::get<YY>(A);
    az = std::get<ZZ>(A);
    bx = std::get<XX>(B);
    by = std::get<YY>(B);
    bz = std::get<ZZ>(B);

    std::get<XX>(C)=(ax-bx);
    std::get<YY>(C)=(ay-by);
    std::get<ZZ>(C)=(az-bz);

    return C;
}

inline std::tuple<double,double,double> hat(const std::tuple<double,double,double> &A)
{
    std::tuple<double,double,double> C;

    double ax,ay,az;

    ax = std::get<XX>(A);
    ay = std::get<YY>(A);
    az = std::get<ZZ>(A);

    double nm =std::sqrt( ax*ax+ay*ay+az*az);
    if(nm == 0)
        return A;
    else
    {
    std::get<XX>(C)=(ax/nm);
    std::get<YY>(C)=(ay/nm);
    std::get<ZZ>(C)=(az/nm);

    return C;
    }
}
inline std::tuple<double,double,double> multiply(const std::tuple<double,double,double> &A,double B)
{
    std::tuple<double,double,double> C;

    double ax,ay,az;

    ax = std::get<XX>(A);
    ay = std::get<YY>(A);
    az = std::get<ZZ>(A);

    std::get<XX>(C)=(ax*B);
    std::get<YY>(C)=(ay*B);
    std::get<ZZ>(C)=(az*B);

    return C;

}



inline double signedVolume(const std::tuple<double,double,double> &A,const  std::tuple<double,double,double> &B,const  std::tuple<double,double,double> &C,const  std::tuple<double,double,double> &D)
{//SignedVolume(a,b,c,d) = (1.0/6.0)*dot(cross(b-a,c-a),d-a)

    return 1.0/6.0*dotProduct(crossProduct(subtract(B,A),subtract(C,A)),subtract(D,A));

}

 /*unsigned int cl2p1 = cl2+1;
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


    std::tuple<double,double,double> P(myCurvePoints[cl][cl2].X(),myCurvePoints[cl][cl2].Y(),0);
    std::tuple<double,double,double> Pp1(myCurvePoints[cl][cl2p1].X(),myCurvePoints[cl][cl2p1].Y(),0);
    std::tuple<double,double,double> Pm1(myCurvePoints[cl][cl2m1].X(),myCurvePoints[cl][cl2m1].Y(),0);

    std::tuple<double,double,double> PP1 = multiply(hat(subtract(P,Pp1)),10.0);
    std::tuple<double,double,double> PP2 = multiply(hat(subtract(Pp1,P)),10.0);

    std::tuple<double,double,double> PM1 = multiply(hat(subtract(P,Pm1)),10.0);
    std::tuple<double,double,double> PM2 = multiply(hat(subtract(Pm1,P)),10.0);


    ///Tri 1 A,B,C
    ///Tri 2 A,C,D
    if(intersects(A,B,C,PP1,PP2))
        return true;
    if(intersects(A,B,C,PM1,PM2))
        return true;
    if(intersects(A,C,D,PP1,PP2))
        return true;
    if(intersects(A,C,D,PM1,PM2))
        return true;
*/
/*
 ///Test whether line segment P1 -- P2  crosses through Triangle T1 -- T2 -- T3 (CCW)

    if(sign(signedVolume(P1,T1,T2,T3)) != sign(signedVolume(P2,T1,T2,T3)))
        if( sign(signedVolume(P1,P2,T1,T2)) == sign(signedVolume(P1,P2,T2,T3)) && sign(signedVolume(P1,P2,T2,T3)) == sign(signedVolume(P1,P2,T3,T1)) )
            return true;

    return false;*/
class Surface
{
public:
    Surface(std::string filename);
    std::tuple<double,double,double> upperBound()
    {
        return maxs;
    }
    std::tuple<double,double,double> lowerBound()
    {
        return mins;
    }

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

