#ifndef MESH_H
#define MESH_H

#include <vector>
#include <list>
#include <set>

#include "NodeList.h"
#include "QuadTree.h"

class Poly
{
public:
    Poly(NodeList* nodes,const std::vector<Node> &myN,int id);

    friend std::ostream& operator<< (std::ostream& stream, const Poly& p);
    unsigned int size()
    {
        return myNodes.size();
    }
    bool active()
    {
        return myActive;
    }
    void active(bool a)
    {
        myActive = a;
    }
    void good()
    {
        std::cout<<"ID "<<myID<<std::endl;
    }
    Node center();
    double shortestSide();
    double longestSide();

private:
    std::vector<Node* > myNodes;
    int myID;
    friend class Dual;
    friend class Mesh;
    bool myActive;
    bool okToSubdivide;

};

class Mesh
{
public:
    Mesh():maxPolySize(0)
    {
        edgeUpToDate=false;
    }

    void addPoly(NodeList* nodes,const std::vector<Node> &nds,int id);
    Poly* getPoly(int id);
    void write(std::string filename,std::string extension);
    void fringeNodes();
    void updateActiveNodes();

protected:
    void out(std::ofstream &of);

    bool edgeUpToDate;
    NodeList* myNodes;
    Curve* myCurve;
    std::list<Poly> myPolys;
    std::map<int,Poly*> idMap;
    unsigned int maxPolySize;


};

class Primal: public Mesh
{
public:

    Primal(QuadTree* QT);
    void qtTraverseAdd(QuadTree* QT,QuadTreeNode_ptr qt);
    int str2ID(std::string locationcode, bool AorB);

private:

    void newtestAdd(const std::vector<std::string> &testLoops,std::string idcode, QuadTree* QT,QuadTreeNode_ptr qt);
    void testAdd(std::string pathcode, std::string startcode,std::string &curcode,std::vector<int> &loop,QuadTree* QT,QuadTreeNode_ptr qt);
    std::string swapEWpathcode(std::string pathcode);
    std::string swapNSpathcode(std::string pathcode);
    std::string swapNSEWpathcode(std::string pathcode);

    void addLoop(int a,int b,int c, int d);

    std::set<std::tuple<int,int,int,int> >  uniqueLoops;
    int maxLevel;
    friend class Dual;

    std::vector<std::string> SquareTestLoops;
    std::vector<std::string> NETestLoops,SETestLoops,SWTestLoops,NWTestLoops;


};
class Dual: public Mesh
{
public:
    Dual(Primal* p);
    void trim();
    void project();
    void snap();
    void smooth();

    void subdivide(Poly* p);
    void subdivide();
    bool split3(Poly* p);

private:
    int count;

    void fixCornerPolys();
    void detangleNodes(Node &A,Node &B, Node &C, Node &D);
    double sumSignAreaNodes(Node A,Node B, Node C, Node D);
    void swap(Node &A, Node &B)
    {
        Node tmp = A;
        A= B;
        B=tmp;
    }
    double cross(Node A,Node B, Node C);
    double angle(Node A,Node B, Node C);
    double dist(Node A, Node B)
    {
        return sqrt(pow(A.X()-B.X(),2.0)+pow(A.Y()-B.Y(),2.0));
    }
    void walkB(Node A,Node &B, Node C);
    double absval(double a)
    {
        if(a<0) return -a;
        else return a;
    }
    bool oblique(double ang)
    {
        return (ang < 20 || ang > 160);
    }
    int badAngleInd(double ang1, double ang2, double ang3, double ang4);
};
#endif
