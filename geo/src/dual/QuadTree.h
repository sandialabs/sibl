#ifndef QUADTREE_H
#define QUADTREE_H

#include "NodeList.h"
#include "Curve.h"


#include <list>
#include <tuple>
#include <map>
#include <iostream>
#include <string>
#include <fstream>



class QuadTreeNode;
typedef class QuadTreeNode *QuadTreeNode_ptr;

class QuadTreeNode
{
 public:
     QuadTreeNode(NodeList* nodes,std::tuple<double,double> NE,std::tuple<double,double> NW,std::tuple<double,double> SW,std::tuple<double,double> SE,bool fringe,QuadTreeNode* parent,std::string code);
     QuadTreeNode(NodeList* nodes,Node NE,Node NW,Node SW,Node SE,QuadTreeNode* parent,std::string code);

     friend std::ostream& operator<< (std::ostream& stream, const QuadTreeNode& qtn);
     std::tuple<double,double> lowerLeft(){return nSW->xy();}
     std::tuple<double,double> upperRight(){return nNE->xy();}

     int level(){return locationcode.size()/2;}
     double width();
     int quadrant(); ///1 == NE, 2==NW, 3==SW, 4 == SE
     Node center();

 private:
     QuadTreeNode_ptr NW;
     QuadTreeNode_ptr NE;
     QuadTreeNode_ptr SW;
     QuadTreeNode_ptr SE;
     QuadTreeNode_ptr myParent;
     Node* nNW;
     Node* nNE;
     Node* nSW;
     Node* nSE;
     std::string locationcode,splitcode;
     bool isLeaf;

    friend class QuadTree;
    friend class Primal;
    friend class Dual;
};



class QuadTree
{
    public:
        QuadTree(Curve* c,NodeList* n,double m);
        QuadTreeNode* head(){return myHead;}
        NodeList* nodes(){return myNodes;}

        void subdivide(QuadTreeNode_ptr qt);

        void balancedRefineCurve(QuadTreeNode_ptr qt,bool boundaryOrFeature);
        void assignSplitCode(QuadTreeNode_ptr qt);

        int maxLevel(QuadTreeNode_ptr qt);

        void write(std::string filename);

        std::string splitcode(std::string locCode);
        bool parentExists(std::string locCode);
        bool exists(std::string locCode);
        bool existsAndLeaf(std::string locCode);
        bool existsAndLeafAndNoSplit(std::string locCode);
std::string east(std::string c){return direction(c,true,true);}
        std::string west(std::string c){return direction(c,true,false);}
        std::string south(std::string c){return direction(c,false,false);}
        std::string north(std::string c){return direction(c,false,true);}
        std::string northeast(std::string c){return north(east(c));}
        std::string northwest(std::string c){return north(west(c));}
        std::string southeast(std::string c){return south(east(c));}
        std::string southwest(std::string c){return south(west(c));}
  std::string direction(std::string c, bool isX,bool isPlus);

        std::string parent(std::string c);
    private:
        void out(QuadTreeNode_ptr qt,std::ofstream &of);

        QuadTreeNode* myHead;
        NodeList* myNodes;
        Curve* myCurve;
        double minimumSize;
        std::map<std::string,QuadTreeNode_ptr> neighborhood;
        void testAndSubdivide(QuadTreeNode_ptr qt,  int cardinal);
        void fullSetTestAndSubdivide(QuadTreeNode_ptr qt);
        void splitCodeStarter(QuadTreeNode_ptr qt);


        friend class Primal;
};
#endif

