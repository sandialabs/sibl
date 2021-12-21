#include "Surface.h"

#define CORNERANGLE 30

#define XIND 0
#define YIND 1
#define ZIND 2


#include <fstream>
#include <iostream>
#include <sstream>

std::ostream& operator<< (std::ostream& stream, const SurfacePoint& cp)
{
    stream<<cp.myX<<'\t'<<cp.myY<<'\t'<<cp.myZ;
    return stream;
}
Surface::Surface(std::string filename)
{
    std::cout<<"Reading in TRIS from file "<<filename<<std::endl;
    std::ifstream in_file(filename.c_str());

    std::string tmp;
    getline(in_file,tmp);
    while(!in_file.fail() && !in_file.eof()&& tmp.find("*NODE,")==std::string::npos) //tmp != "*NODE,")
    {
        // std::cout<<"tmp: "<<tmp<<std::endl;
        getline(in_file,tmp);
    }


    std::string cx,cy,cz,n;
    double tx,ty,tz;

    bool unset = true;
    getline(in_file,tmp);

    while(!in_file.fail() && !in_file.eof() && tmp.find("*")==std::string::npos)
    {
        stringSplit(tmp,tx,ty,tz);

        // std::cout<<"PTS: "<<tx<<","<<ty<<","<<tz<<std::endl;
        mySurfacePoints.push_back(SurfacePoint(tx,ty,tz));
        if(unset)
        {
            std::get<XIND>(mins)=tx;
            std::get<YIND>(mins)=ty;
            std::get<ZIND>(mins)=tz;
            std::get<XIND>(maxs)=tx;
            std::get<YIND>(maxs)=ty;
            std::get<ZIND>(maxs)=tz;
            unset=false;
        }
        if(tx < std::get<XIND>(mins))
            std::get<XIND>(mins)=tx;
        if(tx > std::get<XIND>(maxs))
            std::get<XIND>(maxs)=tx;

        if(ty < std::get<YIND>(mins))
            std::get<YIND>(mins)=ty;
        if(ty > std::get<YIND>(maxs))
            std::get<YIND>(maxs)=ty;

        if(tz < std::get<ZIND>(mins))
            std::get<ZIND>(mins)=tz;
        if(tz > std::get<ZIND>(maxs))
            std::get<ZIND>(maxs)=tz;

        getline(in_file,tmp);
    }
    in_file.close();
    std::cout<<"Surface with "<<mySurfacePoints.size()<<" points"<<std::endl;
    std::cout<<"Going through second pass for tris..."<<std::endl;

    in_file.open(filename.c_str());
    getline(in_file,tmp);
    while(!in_file.fail() && !in_file.eof() &&  tmp.find("*ELEMENT,")==std::string::npos )
        getline(in_file,tmp);

    double a,b,c;
    getline(in_file,tmp);
    while(!in_file.fail() && !in_file.eof() && tmp.find("*")==std::string::npos)
    {
        stringSplit(tmp,a,b,c);

        //std::cout<<"Tri: "<<a<<","<<b<<","<<c<<std::endl;

        myTris.push_back(std::tuple<unsigned int, unsigned int, unsigned int>(a,b,c));

        getline(in_file,tmp);
    }


    /*
    std::cout<<"Determining derivative... "<<std::endl;
    for(unsigned int lcv = 1;lcv < mySurfacePoints.size()-1;++lcv)
    {
       mySurfacePoints[lcv].DX(  (mySurfacePoints[lcv+1].X() -mySurfacePoints[lcv-1].X() )/2.0 );
       mySurfacePoints[lcv].DY(  (mySurfacePoints[lcv+1].Y() -mySurfacePoints[lcv-1].Y() )/2.0 );
    }
       mySurfacePoints[0].DX(  (-mySurfacePoints[2].X() +4*mySurfacePoints[1].X()-3*mySurfacePoints[0].X() )/2.0 );
       mySurfacePoints[0].DY(   (-mySurfacePoints[2].Y() +4*mySurfacePoints[1].Y()-3*mySurfacePoints[0].Y() )/2.0 );

       mySurfacePoints[mySurfacePoints.size()-1].DX(  (mySurfacePoints[mySurfacePoints.size()-3].X() -4*mySurfacePoints[mySurfacePoints.size()-2].X()+3*mySurfacePoints[mySurfacePoints.size()-1].X() )/2.0 );
       mySurfacePoints[mySurfacePoints.size()-1].DY(  (mySurfacePoints[mySurfacePoints.size()-3].Y() -4*mySurfacePoints[mySurfacePoints.size()-2].Y()+3*mySurfacePoints[mySurfacePoints.size()-1].Y() )/2.0 );

    std::cout<<"Setting tangent and angle... "<<std::endl;
    for(unsigned int lcv = 0;lcv < mySurfacePoints.size();++lcv)
    {
        if(!std::isnan(mySurfacePoints[lcv].DX())&&!std::isnan(mySurfacePoints[lcv].DY()) )
       {
           double magval = sqrt(mySurfacePoints[lcv].DX()*mySurfacePoints[lcv].DX()+mySurfacePoints[lcv].DY()*mySurfacePoints[lcv].DY());
           mySurfacePoints[lcv].tangent(mySurfacePoints[lcv].DX()/magval,mySurfacePoints[lcv].DX()/magval);
       }
       else
       {
           std::cout<<"?"<<std::endl;
           mySurfacePoints[lcv].tangent(1,0);
       }
    }
    std::cout<<"Finding corners... "<<std::endl;
    for(unsigned int lcv = 0;lcv < mySurfacePoints.size();++lcv)
    {
        if(!std::isnan(mySurfacePoints[lcv].DX())&&!std::isnan(mySurfacePoints[lcv].DY()) )
        {


       unsigned int p1 = lcv+1;
       if(p1==mySurfacePoints.size())
           p1 = 0;
       double delAngle = (mySurfacePoints[p1].angle()-mySurfacePoints[lcv].angle())*180/3.14159;
       if(delAngle<0)
           delAngle=delAngle*-1;
       ///ANGLE is in Degrees
       if(delAngle > CORNERANGLE )
       {
         myCorners.push_back(mySurfacePoints[lcv]);
         std::cout<<" Adding corner point at "<<mySurfacePoints[lcv]<<" delAngle "<<delAngle<<" lcv: "<<lcv<<std::endl;
       }
        }


    }*/
}
void Surface::stringSplit(std::string s,double &x,double &y, double &z)
{
    std::stringstream ss;
    for(unsigned int lcv = 0; lcv < s.size(); ++lcv)
        if(s[lcv]==',')
            s[lcv]=' ';

    ss<<s;

    int n;
    ss>>n;
    ss>>x;
    ss>>y;
    ss>>z;
}
bool Surface::inBoundingBox(std::tuple<double,double,double> lb,std::tuple<double,double,double> ub)
{
    ///Check whether any points of the Surface are within the bounding box
    for(auto x : mySurfacePoints)
    {
        if (x.X() <= std::get<XIND>(ub) && x.X() >= std::get<XIND>(lb) &&
                x.Y() <= std::get<YIND>(ub) && x.Y() >= std::get<YIND>(lb) &&
                x.Z() <= std::get<ZIND>(ub) && x.Z() >= std::get<ZIND>(lb) )
            return true;

    }
    return false;
}
void Surface::write(std::string filename)
{
    std::ofstream out_file(filename.c_str());
    for(auto x: mySurfacePoints)
        out_file<<x<<std::endl;
    out_file.close();
}
