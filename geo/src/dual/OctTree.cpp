#include "OctTree.h"
#include <bitset>
#define MAXLEVEL 28

OctTreeNode::OctTreeNode(NodeList* nodes,std::vector<std::tuple<double,double,double> > &N,
                         bool fringe,OctTreeNode* parent,std::string code)
{
    myNodes.resize(8,NULL);
    myChildren.resize(8,NULL);

    for(unsigned int lcv = 0; lcv < 8; ++lcv)
        myNodes[lcv]  = nodes->addNode(N[lcv],fringe);


    myParent = parent;
    isLeaf=true;
    locationcode=code;
}
OctTreeNode::OctTreeNode(NodeList* nodes,std::vector<Node> &N,
                         OctTreeNode* parent,std::string code)
{
    myNodes.resize(8,NULL);
    myChildren.resize(8,NULL);

    for(unsigned int lcv = 0; lcv < 8; ++lcv)
        myNodes[lcv]  = nodes->addNode(N[lcv]);


    myParent = parent;
    isLeaf=true;
    locationcode=code;
}
double OctTreeNode::width()
{
    double xw = std::get<XIND>(upperBound())-std::get<XIND>(lowerBound());
    double yw = std::get<YIND>(upperBound())-std::get<YIND>(lowerBound());
    double zw = std::get<ZIND>(upperBound())-std::get<ZIND>(lowerBound());

    double minv = (xw<yw?xw:yw);
    minv = (minv<zw?minv:zw);
    return minv;

}
std::tuple<double,double,double> OctTreeNode::lowerBound()
{
    std::tuple<double,double,double> lb = myNodes[0]->xyz();
    for(unsigned int lcv = 1; lcv < 8; ++lcv)
    {
        if(std::get<XIND>(lb) > std::get<XIND>(myNodes[lcv]->xyz()) )
            std::get<XIND>(lb)=std::get<XIND>(myNodes[lcv]->xyz());
        if(std::get<YIND>(lb) > std::get<YIND>(myNodes[lcv]->xyz()) )
            std::get<YIND>(lb)=std::get<YIND>(myNodes[lcv]->xyz());
        if(std::get<ZIND>(lb) > std::get<ZIND>(myNodes[lcv]->xyz()) )
            std::get<ZIND>(lb)=std::get<ZIND>(myNodes[lcv]->xyz());
    }
    return lb;

}
std::tuple<double,double,double> OctTreeNode::upperBound()
{

    std::tuple<double,double,double> ub = myNodes[0]->xyz();
    for(unsigned int lcv = 1; lcv < 8; ++lcv)
    {
        if(std::get<XIND>(ub) < std::get<XIND>(myNodes[lcv]->xyz()) )
            std::get<XIND>(ub)=std::get<XIND>(myNodes[lcv]->xyz());
        if(std::get<YIND>(ub) < std::get<YIND>(myNodes[lcv]->xyz()) )
            std::get<YIND>(ub)=std::get<YIND>(myNodes[lcv]->xyz());
        if(std::get<ZIND>(ub) < std::get<ZIND>(myNodes[lcv]->xyz()) )
            std::get<ZIND>(ub)=std::get<ZIND>(myNodes[lcv]->xyz());
    }
    return ub;
}
int OctTreeNode::octant() ///follows subdivide code: [0]="111",[1]="011",[2]="101",[3]="001",[4]="110",[5]="010",[6]="100",[7]="000";
{
    if(locationcode.size()<3)
        return -1;
    std::string lastthree = locationcode.substr(locationcode.size()-3,3);
    if(lastthree=="111")
        return 0;
    if(lastthree=="011")
        return 1;
    if(lastthree=="101")
        return 2;
    if(lastthree=="001")
        return 3;
    if(lastthree=="110")
        return 4;
    if(lastthree=="010")
        return 5;
    if(lastthree=="100")
        return 6;
    if(lastthree=="000")
        return 7;

    return -1;
}
std::ostream& operator<< (std::ostream& stream, const OctTreeNode& qtn)
{
    for(unsigned int lcv = 0; lcv < 8; ++lcv)
        stream<<qtn.myNodes[lcv]->id()<<(lcv<7?',':' ');
    //stream<<qtn.nNEU->id()<<','<<qtn.nNWU->id()<<','<<qtn.nSWU->id()<<','<<qtn.nSEU->id()<<','<<qtn.nNED->id()<<','<<qtn.nNWD->id()<<','<<qtn.nSWD->id()<<','<<qtn.nSED->id();
    return stream;
}

OctTree::OctTree(Surface* s,NodeList* n,double m)
{
    mySurface=s;
    myNodes=n;
    minimumSize=m;
    count = 0;
    subdivideNodeOrder.resize(8);
    subdivideNodeOrder[0] = {8,9,10,11,12,13,6,14};
    subdivideNodeOrder[1] = { 15,8,11,16,17,12,14,7 };
    subdivideNodeOrder[2] = {18,19,9,8,20,5,13,12 };
    subdivideNodeOrder[3] = { 21,18,8,15,4,20,12,17};

    subdivideNodeOrder[4] = { 22,23,2,24,8,9,10,11};
    subdivideNodeOrder[5] = { 25,22,24,3,15,8,11,16};
    subdivideNodeOrder[6] = { 26,1,23,22,18,19,9,8};
    subdivideNodeOrder[7] = { 0,26,22,25,21,18,8,15};

    subdivideNodeCode.resize(8);
    subdivideNodeCode[0]="111";
    subdivideNodeCode[1]="011";
    subdivideNodeCode[2]="101";
    subdivideNodeCode[3]="001";
    subdivideNodeCode[4]="110";
    subdivideNodeCode[5]="010";
    subdivideNodeCode[6]="100";
    subdivideNodeCode[7]="000";


    std::vector<std::tuple<double,double,double> > N;

    std::tuple<double,double,double> ur = mySurface->upperBound();
    std::tuple<double,double,double> ll = mySurface->lowerBound();


    std::tuple<double,double,double> NEU = ur;
    std::tuple<double,double,double> NWU =  std::tuple<double,double,double>(std::get<XIND>(ll),std::get<YIND>(ur),std::get<ZIND>(ur));
    std::tuple<double,double,double> SEU =  std::tuple<double,double,double>(std::get<XIND>(ur),std::get<YIND>(ll),std::get<ZIND>(ur));
    std::tuple<double,double,double> SWU =  std::tuple<double,double,double>(std::get<XIND>(ll),std::get<YIND>(ll),std::get<ZIND>(ur));


    std::tuple<double,double,double> NED =  std::tuple<double,double,double>(std::get<XIND>(ur),std::get<YIND>(ur),std::get<ZIND>(ll));
    std::tuple<double,double,double> NWD =  std::tuple<double,double,double>(std::get<XIND>(ll),std::get<YIND>(ur),std::get<ZIND>(ll));
    std::tuple<double,double,double> SED =  std::tuple<double,double,double>(std::get<XIND>(ur),std::get<YIND>(ll),std::get<ZIND>(ll));
    std::tuple<double,double,double> SWD = ll;

///ABAQUS DOES bottom loop starting nearest the origin on a (1,2,3) axis, and goes CCW. Then does the same on the uppers.
///My 000 is the lower left SWD
    N = {SWD,SED, NED,NWD, SWU,SEU, NEU,NWU};

    myHead = new OctTreeNode(myNodes,N,true,NULL,"");
}
void OctTree::subdivide(OctTreeNode_ptr qt)
{
    if(qt!=NULL  && qt->width() > minimumSize && qt->isLeaf)
    {


        std::vector<Node> N;
        N.resize(27);


        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            N[lcv]=*(qt->myNodes[lcv]);

///CENTER POINT 1
        N[8]= (N[0]+N[1]+N[2]+N[3]+N[4]+N[5]+N[6]+N[7])/8.0;
        N[8].fringe(false);

        ///CENTER FACES 6
        N[9]= (N[1]+N[2]+N[5]+N[6])/4.0;
        N[12]= (N[5]+N[6]+N[7]+N[4])/4.0;
        N[15]= (N[0]+N[4]+N[7]+N[3])/4.0;
        N[22]= (N[0]+N[1]+N[2]+N[3])/4.0;
        N[18]= (N[0]+N[1]+N[5]+N[4])/4.0;
        N[11]= (N[2]+N[3]+N[6]+N[7])/4.0;

        ///CENTER EDGES 12
        N[26]= (N[0]+N[1])/2.0;
        N[19]= (N[1]+N[5])/2.0;
        N[20]= (N[5]+N[4])/2.0;
        N[21]= (N[4]+N[0])/2.0;

        N[13]= (N[5]+N[6])/2.0;
        N[17]= (N[4]+N[7])/2.0;
        N[25]= (N[0]+N[3])/2.0;
        N[23]= (N[1]+N[2])/2.0;

        N[14]= (N[7]+N[6])/2.0;
        N[16]= (N[3]+N[7])/2.0;
        N[24]= (N[2]+N[3])/2.0;
        N[10]= (N[6]+N[2])/2.0;

        ///The ones with pointers are NWU, NEU , SWU , SEU ,NWD, NED , SWD , SED

        for(unsigned int lcv = 0; lcv < 8; ++lcv)
        {
            std::vector<Node> Nt;
            Nt.resize(8);
            for(unsigned int nn= 0; nn < 8; ++nn)
                Nt[nn]=N[subdivideNodeOrder[lcv][nn]];

            qt->myChildren[lcv]=new OctTreeNode(myNodes,Nt,qt,qt->locationcode+subdivideNodeCode[lcv]);
            neighborhood[qt->locationcode+subdivideNodeCode[lcv]]=qt->myChildren[lcv];
        }
        qt->isLeaf=false;
    }
}


void OctTree::refineSurface(OctTreeNode_ptr qt)
{
    if(  qt!=NULL && !qt->isLeaf)
    {
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            refineSurface(qt->myChildren[lcv]);
    }

    bool inq = mySurface->inBoundingBox(qt->lowerBound(),qt->upperBound());
    double width = qt->width();

    //  std::cout<<"IN Q query: "<<inq<<std::endl;
    // std::cout<<"WIDTH: "<<width<<" minsize : "<<minsize<<std::endl;
    if(  inq  && width>minimumSize)
    {

        subdivide(qt);
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            refineSurface(qt->myChildren[lcv]);
    }
}
void OctTree::balancedRefineSurface(OctTreeNode_ptr qt)
{
    if(  qt!=NULL && !qt->isLeaf)
    {
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            balancedRefineSurface(qt->myChildren[lcv]);
    }
    bool inq = mySurface->inBoundingBox(qt->lowerBound(),qt->upperBound());
    double width = qt->width();

    //  std::cout<<"IN Q query: "<<inq<<std::endl;
    // std::cout<<"WIDTH: "<<width<<" minsize : "<<minsize<<std::endl;
    if(  inq  && width>minimumSize)
    {

        subdivide(qt);
        fullSetTestAndSubdivide(qt);
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            balancedRefineSurface(qt->myChildren[lcv]);
    }
}
void OctTree::write(std::string filename,std::string extension)
{
    if(extension == "inp")
    {
        std::ofstream out_file((filename).c_str());
        out_file<<"********************************** N O D E S **********************************"<<std::endl;
        out_file<<"*NODE, NSET=ALLNODES"<<std::endl;
        out_file.close();

        myNodes->writeCSVAppend(filename);

        out_file.open((filename).c_str(),std::ios::app);
        out_file<<"********************************** E L E M E N T S ****************************"<<std::endl;
        out_file<<"*ELEMENT, TYPE=C3D8R, ELSET=EB1"<<std::endl;
        count = 1;
        out(myHead,out_file);
        out_file.close();
    }
    else
    {
        std::ofstream out_file((filename).c_str());
        out_file<<"# vtk DataFile Version 3.1\nMCVE VTK file\nASCII\nDATASET UNSTRUCTURED_GRID\n"<<std::endl;

        out_file<<"POINTS      "<<myNodes->size()<<" float"<<std::endl;

        out_file.close();

        myNodes->writeTABAppend(filename);

        out_file.open((filename).c_str(),std::ios::app);
        int mysize = size(head());
        out_file<<"CELLS "<<mysize<<" "<<mysize*9<<std::endl;

        count = 0;
        outVTK(myHead,out_file);

        out_file<<"CELL_TYPES        "<<mysize<<std::endl;
        for( int lcv = 0; lcv < mysize; ++lcv)
            out_file<<"12\t";
        out_file<<std::endl;

        out_file<<"CELL_DATA        "<<mysize<<std::endl;
        out_file<<"SCALARS elem_val float\nLOOKUP_TABLE default\n"<<std::endl;
        for(int lcv = 0; lcv < mysize; ++lcv)
            out_file<<lcv+1<<"\n";
        out_file<<std::endl;

        out_file.close();
    }


}
int OctTree::size(OctTreeNode_ptr qt)
{
    if(qt->isLeaf)
    {
        return 1;
    }
    else
    {
        int sum=0;
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            sum+=size(qt->myChildren[lcv]);

        return sum;
    }
}
void OctTree::out(OctTreeNode_ptr qt,std::ofstream &of)
{
    if(qt->isLeaf)
    {
        of<<count<<",\t"<<*(qt)<<std::endl;
        count++;
    }
    else
    {
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            out(qt->myChildren[lcv],of);

    }
}
void OctTree::outVTK(OctTreeNode_ptr qt,std::ofstream &of)
{
    if(qt->isLeaf)
    {
        of<<"8"<<"\t";
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            of<<(qt->myNodes[lcv]->id())-1<<"\t";
        of<<std::endl;
        //count++;
    }
    else
    {
        for(unsigned int lcv = 0; lcv < 8; ++lcv)
            outVTK(qt->myChildren[lcv],of);

    }
}


std::string OctTree::direction(std::string c, int idx,bool isPlus)
{
    if(idx > 2 || idx < 0)
        return "NULL";

    if(c == "NULL"|| c=="")
        return "NULL";

    std::string tmp="";
    for(unsigned int lcv = idx; lcv<c.size(); lcv=lcv+3)
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

    ///idx 0 -> -3
    ///idx 1 -> -2
    ///idx 2 -> -1
    int loc = tmp.size()- (3-idx);

    for(unsigned int lcv = newcode.size()-1; loc >=0 ; --lcv)
    {
        //std::cout<<"loc: "<<loc<<" and lcv: "<<lcv<<std::endl;
        tmp[loc]=newcode[lcv];
        loc=loc-3;
    }

    return tmp;

}

std::string OctTree::parent(std::string c)
{
    if(c == "NULL"|| c=="")
        return "NULL";
    if(c.size()==2)
        return "NULL";

    return c.substr(0,c.size()-2);
}

void OctTree::testAndSubdivide(OctTreeNode_ptr qt,  int cardinal)
{
    int myLevel = maxLevel(qt);
    std::map<std::string,OctTreeNode_ptr>::iterator it;
    std::string test;

    switch(cardinal)
    {
    case 1:
        test= ip1(qt->locationcode);
        break;
    case 2:
        test= im1(qt->locationcode);
        break;
    case 3:
        test= jp1(qt->locationcode);
        break;
    case 4:
        test= jm1(qt->locationcode);
        break;
    case 5:
        test= kp1(qt->locationcode);
        break;
    case 6:
        test= km1(qt->locationcode);
        break;
    default:
        test= ip1(qt->locationcode);
        break;
    }

    it = neighborhood.find(test);
    if(test!="NULL" && it!=neighborhood.end()) //then it actually has an east neighbor
    {
        int nbrMaxLevel = maxLevel(neighborhood[test]);
        int diff =  myLevel-nbrMaxLevel; ///We are possibly going to refine the neighbor but not this node so sign is important

        bool sameParents = (parent(test) == parent(qt->locationcode));

        if( (sameParents && diff>=1) || (!sameParents && diff>=2))
        {
            subdivide(neighborhood[test]);
            fullSetTestAndSubdivide(neighborhood[test]);
        }
    }
    else
    {
        ///The hypothetical node does not exist , so check for a hypotehical parent
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
int OctTree::maxLevel(OctTreeNode_ptr qt)
{
    if(qt==NULL)
        return 0;
    if(qt->isLeaf)
        return 1;
    else
    {
        int maxl = 0;
        for(unsigned int lcv=0; lcv < qt->myChildren.size(); ++lcv)
        {
            int level = maxLevel(qt->myChildren[lcv]);
            if(level > maxl)
                maxl=level;
        }

        return maxl+1;
    }

}
void OctTree::fullSetTestAndSubdivide(OctTreeNode_ptr qt)
{
    for(unsigned int lcv = 1; lcv <=6; ++lcv)
        testAndSubdivide(qt,lcv);
}
