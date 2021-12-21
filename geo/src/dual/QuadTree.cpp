#include "QuadTree.h"
#include <bitset>

///23 bits is in the 8M elements...
#define MAXLEVEL 28

QuadTreeNode::QuadTreeNode(NodeList* nodes,std::tuple<double,double> NE,std::tuple<double,double> NW,std::tuple<double,double> SW,std::tuple<double,double> SE,bool fringe,QuadTreeNode* parent,std::string code)
{
    nNW = nodes->addNode(NW,fringe);
    nNE = nodes->addNode(NE,fringe);
    nSW = nodes->addNode(SW,fringe);
    nSE = nodes->addNode(SE,fringe);
    myParent = parent;
    isLeaf=true;
    locationcode=code;

}
QuadTreeNode::QuadTreeNode(NodeList* nodes,Node NE,Node NW,Node SW,Node SE,QuadTreeNode* parent,std::string code)
{
    nNW = nodes->addNode(NW);
    nNE = nodes->addNode(NE);
    nSW = nodes->addNode(SW);
    nSE = nodes->addNode(SE);
    myParent = parent;
    isLeaf=true;
    locationcode=code;

}
std::ostream& operator<< (std::ostream& stream, const QuadTreeNode& qtn)
{
     stream<<qtn.nNE->id()<<'\t'<<qtn.nNW->id()<<'\t'<<qtn.nSW->id()<<'\t'<<qtn.nSE->id();
    return stream;
}
double QuadTreeNode::width()
{
    double xw = std::get<XIND>(upperRight())-std::get<XIND>(lowerLeft());
    double yw = std::get<YIND>(upperRight())-std::get<YIND>(lowerLeft());

    return (xw<yw?xw:yw);

}
int QuadTreeNode::quadrant() ///1 == NE, 2==NW, 3==SW, 4 == SE
{
    if(locationcode=="")
        return 0;
    std::string lasttwo = locationcode.substr(locationcode.size()-2,2);
    if(lasttwo[0]=='1'&& lasttwo[1]=='1')
        return 1;
    if(lasttwo[0]=='0'&& lasttwo[1]=='1')
        return 2;
    if(lasttwo[0]=='0'&& lasttwo[1]=='0')
        return 3;
    if(lasttwo[0]=='1'&& lasttwo[1]=='0')
        return 4;

        return 0;
}
Node QuadTreeNode::center()
{
    return  (*(nSE)+*(nSW)+*(nNE)+*(nNW))/4.0;
}
QuadTree::QuadTree(Curve* c,NodeList* n,double m)
{
    myCurve=c;
    myNodes=n;
    minimumSize = m;

    if(m<=0)
        std::cout<<"Error -- Minimum size has to be positive and not zero."<<std::endl;

    std::tuple<double,double> ur = myCurve->upperRight();
    std::tuple<double,double> ll = myCurve->lowerLeft();

    if(std::get<XIND>(ur)==std::get<XIND>(ll) && std::get<YIND>(ur)==std::get<YIND>(ll) )
    {
        std::get<XIND>(ur)+=5.1;
        std::get<XIND>(ll)-=5;
        std::get<YIND>(ur)+=5.1;
        std::get<YIND>(ll)-=5;
    }
    else
    {
        std::get<XIND>(ur)+=.01;
        std::get<XIND>(ll)-=.01;
        std::get<YIND>(ur)+=.01;
        std::get<YIND>(ll)-=.01;
    }
    std::tuple<double,double> NE = ur;
    std::tuple<double,double> SW = ll;
    std::tuple<double,double> NW =  std::tuple<double,double>(std::get<XIND>(ll),std::get<YIND>(ur));
    std::tuple<double,double> SE =  std::tuple<double,double>(std::get<XIND>(ur),std::get<YIND>(ll));

    myHead = new QuadTreeNode(myNodes,NE,NW,SW,SE,true,NULL,"");
    //neighborhood["00"]=myHead;
}
void QuadTree::subdivide(QuadTreeNode_ptr qt)
{
    if(qt!=NULL && qt->width() >= minimumSize && qt->isLeaf)
    {
     Node nN = (*(qt->nNW)+*(qt->nNE))/2.0;
    Node nE = (*(qt->nSE)+*(qt->nNE))/2.0;
    Node nS = (*(qt->nSW)+*(qt->nSE))/2.0;
    Node nW = (*(qt->nNW)+*(qt->nSW))/2.0;
    Node nC = (*(qt->nNW)+*(qt->nNE)+*(qt->nSW)+*(qt->nSE))/4.0;
    nC.fringe(false);

    qt->NW=new QuadTreeNode(myNodes,nN,*(qt->nNW),nW,nC,qt,qt->locationcode+"01");
    neighborhood[qt->NW->locationcode]=qt->NW;

    qt->NE=new QuadTreeNode(myNodes,*(qt->nNE),nN,nC,nE,qt,qt->locationcode+"11");
    neighborhood[qt->NE->locationcode]=qt->NE;

    qt->SW=new QuadTreeNode(myNodes,nC,nW,*(qt->nSW),nS,qt,qt->locationcode+"00");
    neighborhood[qt->SW->locationcode]=qt->SW;

    qt->SE=new QuadTreeNode(myNodes,nE,nC,nS,*(qt->nSE),qt,qt->locationcode+"10");
    neighborhood[qt->SE->locationcode]=qt->SE;

    qt->isLeaf=false;

    }

}

void QuadTree::balancedRefineCurve(QuadTreeNode_ptr qt,bool boundaryOrFeature)
{
     if(qt!=NULL && !qt->isLeaf)
    {
            balancedRefineCurve(qt->NE,boundaryOrFeature);
            balancedRefineCurve(qt->SE,boundaryOrFeature);
            balancedRefineCurve(qt->SW,boundaryOrFeature);
            balancedRefineCurve(qt->NW,boundaryOrFeature);
    }

    bool inq;
    if(boundaryOrFeature)
     inq = myCurve->inBoundingBox(qt->lowerLeft(),qt->upperRight());
    else
    inq = myCurve->featureInBoundingBox(qt->lowerLeft(),qt->upperRight());
    double width = qt->width();

    if(  inq  && width>minimumSize)
    {
        subdivide(qt);
        fullSetTestAndSubdivide(qt);
        balancedRefineCurve(qt->NE,boundaryOrFeature);
        balancedRefineCurve(qt->SE,boundaryOrFeature);
        balancedRefineCurve(qt->SW,boundaryOrFeature);
        balancedRefineCurve(qt->NW,boundaryOrFeature);
    }
}

void QuadTree::write(std::string filename)
{
    std::ofstream out_file((filename+"quads").c_str());
    out(myHead,out_file);
    out_file.close();

    myNodes->write(filename+"nodes");
}
void QuadTree::out(QuadTreeNode_ptr qt,std::ofstream &of)
{
    if(qt->isLeaf)
        of<<*(qt)<<std::endl;
    else
    {
        out(qt->NE,of);
        out(qt->NW,of);
        out(qt->SW,of);
        out(qt->SE,of);
    }
}

std::string QuadTree::direction(std::string c, bool isX,bool isPlus)
{

    if(c == "NULL"|| c=="")
        return "NULL";

    std::string tmp="";
    for(unsigned int lcv = (isX?0:1);lcv<c.size();lcv=lcv+2)
        tmp=tmp+c[lcv];

    std::bitset<MAXLEVEL> mybits(tmp);
    unsigned long int code = mybits.to_ulong();


    if(isPlus && code == std::pow(2,tmp.size())-1 )
        return "NULL";
    if(!isPlus && code == 0 )
        return "NULL";
    if(isPlus)
        code++;
    else
        code--;

    std::bitset<MAXLEVEL> mybits2(code);
    std::string newcode = mybits2.to_string();

    ///newcode has only the y's need to merge it with the preexisting x's of c.
    ///newcode is much longer (maxlevel) and not the same as c.
    tmp = c;

     int loc =(isX?tmp.size()-2:tmp.size()-1);

    for(unsigned int lcv = newcode.size()-1; loc >=0 ; --lcv)
    {
        //std::cout<<"loc: "<<loc<<" and lcv: "<<lcv<<std::endl;
        tmp[loc]=newcode[lcv];
        loc=loc-2;
    }

    return tmp;

}

std::string QuadTree::parent(std::string c)
{
    if(c == "NULL"|| c=="")
        return "NULL";
    if(c.size()==2)
        return "NULL";

    return c.substr(0,c.size()-2);
}

void QuadTree::testAndSubdivide(QuadTreeNode_ptr qt,  int cardinal)
{
    int myLevel = maxLevel(qt);
    std::map<std::string,QuadTreeNode_ptr>::iterator it;
    std::string test;

   switch(cardinal)
   {
       case 1: test= north(qt->locationcode);break;
       case 2: test= east(qt->locationcode);break;
       case 3: test= south(qt->locationcode);break;
       case 4: test= west(qt->locationcode);break;
       default: test= east(qt->locationcode);break;
   }

    it = neighborhood.find(test);
    if(test!="NULL" && it!=neighborhood.end()) //then it actually has an east neighbor
          {
              int nbrMaxLevel = maxLevel(neighborhood[test]);
              int diff =  myLevel-nbrMaxLevel; ///We are possibly going to refine the neighbor but not this node so sign is important

              bool sameParents = (parent(test) == parent(qt->locationcode));

              if( (sameParents && diff>=2) || (!sameParents && diff>=1))
              {
                  subdivide(neighborhood[test]);
                 fullSetTestAndSubdivide(neighborhood[test]);
              }
          }
        else
            {  ///The hypothetical node does not exist , so check for a hypotehical parent
                it = neighborhood.find(parent(test));

                if(parent(test)!="NULL" && it!=neighborhood.end()) //then it might have a parent that needs more than 1 refinement
                {
                    subdivide(neighborhood[parent(test)]);
                    subdivide(neighborhood[test]);
                    fullSetTestAndSubdivide(neighborhood[parent(test)]);
                    fullSetTestAndSubdivide(neighborhood[test]);
                }
        }//Else (no direct neighbor, checked parent )

}
int QuadTree::maxLevel(QuadTreeNode_ptr qt)
{
    if(qt==NULL)
        return 0;
    if(qt->isLeaf)
         return 1;
    else
    {
        int NElevel = maxLevel(qt->NE);
        int NWlevel = maxLevel(qt->NW);
        int SElevel = maxLevel(qt->SE);
        int SWlevel = maxLevel(qt->SW);

        int level = NElevel;
        if(NWlevel>level)
            level = NWlevel;
        if(SWlevel>level)
            level = SWlevel;
        if(SElevel>level)
            level = SElevel;

        return level+1;
    }


}
void QuadTree::fullSetTestAndSubdivide(QuadTreeNode_ptr qt)
{
        testAndSubdivide(qt,1);
        testAndSubdivide(qt,2);
        testAndSubdivide(qt,3);
        testAndSubdivide(qt,4);
}
void QuadTree::assignSplitCode(QuadTreeNode_ptr qt)
{
    if(qt!=NULL)
    {
        if(qt->isLeaf)
        {
          splitCodeStarter(qt);
        }
        else
        {
        assignSplitCode(qt->NE);
        assignSplitCode(qt->NW);
        assignSplitCode(qt->SW);
        assignSplitCode(qt->SE);
        }
    }
}
void QuadTree::splitCodeStarter(QuadTreeNode_ptr qt)
{
        std::vector<int> neighborsToTest;
        std::vector<int> count={0,0,0};
        int sum = 0;
       /// std::cout<<"Location code: "<<qt->locationcode<<" and quadrant: "<<qt->quadrant()<<std::endl;
            switch(qt->quadrant())
            {
                case 1: neighborsToTest={2,3,4};break;
                case 2: neighborsToTest={1,3,4};break;
                case 3: neighborsToTest={1,2,4};break;
                case 4: neighborsToTest={1,2,3};break;
                default : neighborsToTest={};break;
            }
            for(unsigned int lcv = 0; lcv < neighborsToTest.size();++lcv)
            {
                    std::string nbr;
                    if(qt->quadrant() == 1 && neighborsToTest[lcv] == 2) //i am NE, neighbor is NW, so I go west
                        nbr = west(qt->locationcode);
                    else if(qt->quadrant() == 1 && neighborsToTest[lcv] == 3) //i am NE, neighbor is SW, so I go southwest
                        nbr = southwest(qt->locationcode);
                    else if(qt->quadrant() == 1 && neighborsToTest[lcv] == 4) //i am NE, neighbor is SE, so I go south
                        nbr = south(qt->locationcode);
                    else if(qt->quadrant() == 2 && neighborsToTest[lcv] == 1) //i am NW, neighbor is NE, so I go east
                        nbr = east(qt->locationcode);
                    else if(qt->quadrant() == 2 && neighborsToTest[lcv] == 3) //i am NW, neighbor is SW, so I go south
                        nbr = south(qt->locationcode);
                    else if(qt->quadrant() == 2 && neighborsToTest[lcv] == 4) //i am NW, neighbor is SE, so I go southeast
                        nbr = southeast(qt->locationcode);
                    else if(qt->quadrant() == 3 && neighborsToTest[lcv] == 1) //i am SW, neighbor is NE, so I go northeast
                        nbr = northeast(qt->locationcode);
                    else if(qt->quadrant() == 3 && neighborsToTest[lcv] == 2) //i am SW, neighbor is NW, so I go north
                        nbr = north(qt->locationcode);
                    else if(qt->quadrant() == 3 && neighborsToTest[lcv] == 4) //i am SW, neighbor is SE, so I go east
                        nbr = east(qt->locationcode);
                    else if(qt->quadrant() == 4 && neighborsToTest[lcv] == 1) //i am SE, neighbor is NE, so I go north
                        nbr = north(qt->locationcode);
                    else if(qt->quadrant() == 4 && neighborsToTest[lcv] == 2) //i am SE, neighbor is NW, so I go northwest
                        nbr = northwest(qt->locationcode);
                    else if(qt->quadrant() == 4 && neighborsToTest[lcv] == 3) //i am SE, neighbor is SW, so I go west
                        nbr = west(qt->locationcode);

                    std::map<std::string,QuadTreeNode_ptr>::iterator it;
                    it=neighborhood.find(nbr);

                    if(it!=neighborhood.end()) ///actual neighbor
                    {
                        count[lcv]=maxLevel(neighborhood[nbr])-1;
                    }
                    sum+=count[lcv];
            }
//            std::cout<<"Total count : "<<sum;
            if(sum == 0)
                qt->splitcode="none";
            else if(sum == 1)
                qt->splitcode="270";
            else if(sum == 2)
                qt->splitcode = "180";
            else if(sum == 3)
                qt->splitcode = "90";
    if(sum!=0)
    switch(qt->quadrant())
    {
        case 1: qt->splitcode+="SW";break;
        case 2: qt->splitcode+="SE";break;
        case 3: qt->splitcode+="NE";break;
        case 4: qt->splitcode+="NW";break;
    }


}
bool QuadTree::parentExists(std::string locCode)
{
    return exists(parent(locCode));
}
bool QuadTree::exists(std::string locCode)
{
    std::map<std::string,QuadTreeNode_ptr>::iterator it;
    it= neighborhood.find(locCode);
    return it!=neighborhood.end();
}
bool QuadTree::existsAndLeaf(std::string locCode)
{
    std::map<std::string,QuadTreeNode_ptr>::iterator it;
    it= neighborhood.find(locCode);

    if (it==neighborhood.end()) ///DNE
        return false;

    return neighborhood[locCode]->isLeaf;
}
bool QuadTree::existsAndLeafAndNoSplit(std::string locCode)
{
    std::map<std::string,QuadTreeNode_ptr>::iterator it;
    it= neighborhood.find(locCode);

    if (it==neighborhood.end()) ///DNE
        return false;

    if(!neighborhood[locCode]->isLeaf) ///NOT LEAF
        return false;

    if(neighborhood[locCode]->splitcode=="none")
        return true;
    else
        return false;
}
std::string QuadTree::splitcode(std::string locCode)
{
     std::map<std::string,QuadTreeNode_ptr>::iterator it;
    it= neighborhood.find(locCode);

    if (it==neighborhood.end()) ///DNE
        return "NULL";

    if(!neighborhood[locCode]->isLeaf) ///NOT LEAF
        return "NULL";

    return neighborhood[locCode]->splitcode;
}
