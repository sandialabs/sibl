#ifndef NODELIST_H
#define NODELIST_H

#include <list>
#include <tuple>
#include <map>
#include <iostream>
#include <fstream>
#include <string>
#include "Curve.h"

#define XIND 0
#define YIND 1
#define ZIND 2
#define UNSET -1
#define TOLERANCE 1e-8

class Node
{
 public:
    Node(){isFringe=false;isActive=false;x=0;y=0;z=0;myID=UNSET;fx=0;fy=0;fz=0;}
    Node(std::tuple<double,double,double> pt,bool fringe){x=std::get<XIND>(pt);y=std::get<YIND>(pt);z=std::get<ZIND>(pt);isFringe=fringe;isActive=true;myID=UNSET;}
    Node(std::tuple<double,double,double> pt,bool fringe,int id){x=std::get<XIND>(pt);y=std::get<YIND>(pt);z=std::get<ZIND>(pt);isFringe=fringe;isActive=true;myID=id;}

    Node(std::tuple<double,double> pt,bool fringe){x=std::get<XIND>(pt);y=std::get<YIND>(pt);z=0;isFringe=fringe;isActive=true;myID=UNSET;}
    Node(std::tuple<double,double> pt,bool fringe,int id){x=std::get<XIND>(pt);y=std::get<YIND>(pt);z=0;isFringe=fringe;isActive=true;myID=id;}

    void fringe(bool f){isFringe=f;}
    bool fringe(){return isFringe;}
    void active(bool a){isActive=a;}
    bool active(){return isActive;}


    double dist(const Node &A){return std::pow((x-A.x)*(x-A.x)+(y-A.y)*(y-A.y)+(z-A.z)*(z-A.z),0.5);}
    double magnitude(){return std::pow(x*x+y*y+z*z,0.5);}
    Node direction(const Node &A){Node N; N.x = x-A.x;N.y = y-A.y;N.z = z-A.z; double m = N.magnitude(); N.x/=m;N.y/=m; N.z/=m;return N; }
    double X(){return x;}
    double Y(){return y;}
    double Z(){return z;}
    void X(double d){x=d;}
    void Y(double d){y=d;}
    void Z(double d){z=d;}
    int id(){return myID;}
    void id(int i){myID=i;}

    std::tuple<double,double> xy(){return std::tuple<double,double>(x,y);}
    std::tuple<double,double,double> xyz(){return std::tuple<double,double,double>(x,y,z);}

    std::string print();

    double fx,fy,fz;
    Node operator + ( const Node& A ) const;
    Node operator / ( const double A ) const;
    Node& operator=(const Node& other);
    bool operator ==( const Node& A ) const;
    bool operator<(const Node& rhs);
    friend std::ostream& operator<< (std::ostream& stream, const Node& n);

 private:
     double x,y,z;

     bool isFringe,isActive;
     int myID;
     friend class NodeList;
};



class NodeList
{
    public:
        NodeList(){count = 0;}

        Node* addNode(Node N);
        Node* addNode(std::tuple<double,double,double> pt,bool fringe);
        Node* addNode(std::tuple<double,double> pt,bool fringe);
        Node* addNode(double tx,double ty,bool fringe);
        Node* addNode(double tx,double ty,double tz,bool fringe);
        int size(){return nodes.size();}

        Node* near(double x,double y);
        void fringe(int id,bool f);
        void resetFringe();
        void resetForce();
        void resetActive();
        void moveByForce();
        void print();
        void write(std::string filename);
        void writeCSVAppend(std::string filename);
        void writeTABAppend(std::string filename);


    private:
        std::list<Node> nodes;
        int count;
        friend class Mesh;
        friend class Dual;


};
#endif
