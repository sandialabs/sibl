#ifndef OCTTREE_H
#define OCTTREE_H

#include "NodeList.h"
#include "Surface.h"

#include <list>
#include <tuple>
#include <map>
#include <iostream>
#include <string>
#include <fstream>

#define x111 0
#define x011 1
#define x001 2
#define x101 3
#define x110 4
#define x010 5
#define x000 6
#define x100 7


class OctTreeNode;
typedef class OctTreeNode *OctTreeNode_ptr;

class OctTreeNode
{
public:
    OctTreeNode(NodeList* nodes,std::vector<std::tuple<double,double,double> > &N,
                bool fringe,OctTreeNode* parent,std::string code);
    OctTreeNode(NodeList* nodes, std::vector<Node> &N,
                OctTreeNode* parent,std::string code);

    friend std::ostream& operator<< (std::ostream& stream, const OctTreeNode& qtn);
    std::tuple<double,double,double> lowerBound();//{return myNodes[x000]->xyz();}
    std::tuple<double,double,double> upperBound();//{return myNodes[x111]->xyz();}
    double width();
    int octant(); ///follows subdivide code: [0]="111",[1]="011",[2]="101",[3]="001",[4]="110",[5]="010",[6]="100",[7]="000";
private:

    std::vector<OctTreeNode_ptr> myChildren;


    OctTreeNode_ptr myParent;
    std::vector<Node* > myNodes;

    std::string locationcode,splitcode;
    bool isLeaf;
    friend class OctTree;
};



class OctTree
{
public:
    OctTree(Surface* s,NodeList* n,double m);
    OctTreeNode* head()
    {
        return myHead;
    }
    NodeList* nodes()
    {
        return myNodes;
    }

    void subdivide(OctTreeNode_ptr qt);

    void refineSurface(OctTreeNode_ptr qt);
    void balancedRefineSurface(OctTreeNode_ptr qt);

    int size(OctTreeNode_ptr qt);
    void write(std::string filename,std::string extension);

    int maxLevel(OctTreeNode_ptr qt);

private:
    void out(OctTreeNode_ptr qt,std::ofstream &of);
    void outVTK(OctTreeNode_ptr qt,std::ofstream &of);
    std::vector<std::vector<unsigned int> > subdivideNodeOrder;
    std::vector<std::string > subdivideNodeCode;
    double minimumSize;
    std::map<std::string,OctTreeNode_ptr> neighborhood;
    OctTreeNode* myHead;
    NodeList* myNodes;
    Surface* mySurface;
    int count;
    std::string direction(std::string c, int idx,bool isPlus);
    std::string parent(std::string c);
    std::string ip1(std::string c)
    {
        return direction(c,0,true);
    }
    std::string im1(std::string c)
    {
        return direction(c,0,false);
    }
    std::string jp1(std::string c)
    {
        return direction(c,1,true);
    }
    std::string jm1(std::string c)
    {
        return direction(c,1,false);
    }
    std::string kp1(std::string c)
    {
        return direction(c,2,true);
    }
    std::string km1(std::string c)
    {
        return direction(c,2,false);
    }
    void fullSetTestAndSubdivide(OctTreeNode_ptr qt);
    void testAndSubdivide(OctTreeNode_ptr qt,  int cardinal);

};
#endif


