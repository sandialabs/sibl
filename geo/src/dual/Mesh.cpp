#include "Mesh.h"
#include <bitset>
#include <cmath>
///23 bits is in the 8M elements...
#define MAXLEVEL 28

#include <fstream>
Poly::Poly(NodeList* nodes,const std::vector<Node> &myN,int id)
{

    for(unsigned int lcv = 0; lcv < myN.size(); ++lcv)
        myNodes.push_back(nodes->addNode(myN[lcv]));

    myID=id;
    myActive = true;
    okToSubdivide=true;
}
std::ostream& operator<< (std::ostream& stream, const Poly& p)
{
    for(unsigned int lcv =0; lcv < p.myNodes.size(); ++lcv)
        stream<<p.myNodes[lcv]->id()<<'\t';//(lcv == p.myNodes.size()-1?'':'\t');
    return stream;

}
Node Poly::center()
{
    Node tmp = *(myNodes[0]);
    for(unsigned int lcv = 1; lcv < myNodes.size(); ++lcv)
        tmp = tmp + *(myNodes[lcv]);
    return  (tmp)/myNodes.size();
}
double Poly::shortestSide()
{
    if(myNodes.size()<2)
        return 0;
    else
    {
        double shortSide = myNodes[0]->dist(*(myNodes[1]));
        for(unsigned int lcv = 0; lcv < myNodes.size(); ++lcv)
        {
            unsigned int lp1 = lcv + 1;
            if(lp1==myNodes.size())
                lp1 = 0;

            double td = myNodes[lcv]->dist(*(myNodes[lp1]));
            if(td < shortSide)
                shortSide=td;
        }
        return shortSide;
    }
}
double Poly::longestSide()
{
    if(myNodes.size()<2)
        return 0;
    else
    {
        double longSide = myNodes[0]->dist(*(myNodes[1]));
        for(unsigned int lcv = 0; lcv < myNodes.size(); ++lcv)
        {
            unsigned int lp1 = lcv + 1;
            if(lp1==myNodes.size())
                lp1 = 0;

            double td = myNodes[lcv]->dist(*(myNodes[lp1]));
            if(td > longSide)
                longSide=td;
        }
        return longSide;
    }
}
void Mesh::write(std::string filename,std::string extension)
{
    if(extension == "")
    {
        std::ofstream out_file((filename+"quads").c_str());
        out(out_file);
        out_file.close();

        myNodes->write(filename+"nodes");
    }
    else if(extension == "inp")
    {

        std::ofstream out_file((filename+".inp").c_str());
        out_file<<"********************************** N O D E S **********************************"<<std::endl;
        out_file<<"*NODE, NSET=ALLNODES"<<std::endl;
        out_file.close();
        myNodes->writeCSVAppend((filename+".inp"));

        out_file.open((filename+".inp").c_str(),std::ios::app);
        out_file<<"********************************** E L E M E N T S ****************************"<<std::endl;
        out_file<<"*ELEMENT, TYPE=CPE4, ELSET=EB1"<<std::endl; ///S4R

        std::list<Poly>::iterator it;
        int counter = 1;
        for(it = myPolys.begin(); it!=myPolys.end(); ++it)
        {
            if(it->active() && it->size() == maxPolySize)
            {
                out_file<<counter<<",    ";
                for(unsigned int lcv =0; lcv < it->myNodes.size(); ++lcv)
                    out_file<<(it->myNodes[lcv])->id()<<(lcv<it->myNodes.size()-1?",    ":"\n");
            }///active poly
        }
        out_file.close();

    }//abaqus if
}
void Mesh::out(std::ofstream &of)
{
    std::list<Poly>::iterator it;
    for(it = myPolys.begin(); it!=myPolys.end(); ++it)
    {
        if(it->active())
        {


            if(it->size() == maxPolySize)
                of<<*(it)<<std::endl;
            else
            {
                of<<*(it);
                for( int lcv = 0; lcv < (int)((maxPolySize-it->size())-1); ++lcv)
                    of<<"-1\t";
                of<<"-1"<<std::endl;
            }
        }///active poly
    }
}
void Mesh::addPoly(NodeList* nodes,const std::vector<Node> &nds,int id)
{
    // std::cout<<"Adding poly with id: "<<id<<std::endl;
    myPolys.push_back(Poly(myNodes,nds,id));
    if(nds.size()>maxPolySize)
        maxPolySize=nds.size();

    std::map<int,Poly*>::iterator mapit;
    mapit = idMap.find(id);
    if(mapit==idMap.end())
        idMap[id]=&(myPolys.back());
    else
        std::cout<<"ERROR - duplicate ID "<<id<<std::endl;

}

Poly* Mesh::getPoly(int id)
{
    std::map<int,Poly*>::iterator mapit;
    mapit = idMap.find(id);
    if(mapit!=idMap.end())
        return (idMap[id]);


    return NULL;
}

void Mesh::fringeNodes()
{

    std::map<std::pair<int,int>,int> edgeCount;
    std::map<std::pair<int,int>,int>::iterator mapit;

    ///Loop over Polys, add  counts to the nodes by their number
    ///Once done go through all node counts and assign fringe
    std::list<Poly>::iterator it;
    for(it = myPolys.begin(); it!=myPolys.end(); ++it)
    {
        if(it->active())
            for(unsigned int nn = 0; nn< it->myNodes.size(); ++nn)
            {
                unsigned int np1 = nn+1;
                if(np1>=it->myNodes.size())
                    np1 = 0;

                int id1 = it->myNodes[nn]->id();
                int id2 = it->myNodes[np1]->id();
                if(id1>id2)
                {
                    int tmp = id1;
                    id1 = id2;
                    id2 = tmp;
                }
                std::pair<int,int> edge(id1,id2);
                mapit=edgeCount.find(edge);
                if(mapit==edgeCount.end()) //not found
                    edgeCount[edge]=1;
                else
                    edgeCount[edge]=edgeCount[edge]+1;

            }
    }
    myNodes->resetFringe();
    for(mapit = edgeCount.begin(); mapit!=edgeCount.end(); ++mapit)
    {
//        std::cout<<"map->second: "<<mapit->second<<" nodes : "<<mapit->first.first<<" , "<<mapit->first.second<<std::endl;
        if(mapit->second == 1) //nodes are on the fringe
        {
            myNodes->fringe(mapit->first.first,true);
            myNodes->fringe(mapit->first.second,true);
        }

    }


    /*     std::list<Node>::iterator nodeit;
         for(nodeit = myNodes->nodes.begin();nodeit!=myNodes->nodes.end();++nodeit)
            {
                mapit=idCount.find(nodeit->id());
                if(mapit==idCount.end()) //not found
                    nodeit->active(false);
                else
                {std::cout<<idCount[nodeit->id()]<<std::endl;
                    if(idCount[nodeit->id()]>=4)
                    nodeit->fringe(false);
                    else
                        nodeit->fringe(true);
                        }
            }*/

}
void Mesh::updateActiveNodes()
{
    myNodes->resetActive();
    std::list<Poly>::iterator it;
    for(it = myPolys.begin(); it!=myPolys.end(); ++it)
    {
        if(it->active())
            for(unsigned int nn = 0; nn< it->myNodes.size(); ++nn)
                (it->myNodes[nn])->active(true);

    }

}
Primal::Primal(QuadTree* QT)
{
    myCurve=QT->myCurve;
    myNodes = QT->myNodes;
    maxLevel = QT->maxLevel(QT->head());


    SquareTestLoops = {"N0O_E0O_S0O_W0O_N0O_", "E0O_S0O_W0O_N0O_E0O_","S0O_W0O_N0O_E0O_S0O_","W0O_N0O_E0O_S0O_W0O_" };
    NETestLoops = {"E1O_N0O_W0O_S0T_E1O_","E1O_S0O_W0P_D0T_E1O_","N1O_W0O_S0P_D0T_N1O_",
                   "E1O_N0T_W3O_S0T_E1O_","E1T_N2O_W0O_S0T_E1T_", "D0P_D0T_E1T_D0P_W0O_",
                   "D0T_E1O_N0O_W0T_S4T_",
                   "D0P_D0T_N1T_D0P_S0O_",
                   "D0T_E1T_N2O_W0T_S4T_",   ///270
                   "D0T_E1T_N2T_W3O_S0T_",   ///270
                   "D0T_E1O_N0T_W3T_S4T_",  ///270
                   "D0P_N2O_W0O_S0P_E0O_", ///180
                   "D0P_E4O_S0O_W0P_N0O_" ///180
                  };
    SETestLoops.resize(NETestLoops.size());
    SWTestLoops.resize(NETestLoops.size());
    NWTestLoops.resize(NETestLoops.size());

    // std::cout<<"Square size: "<<SquareTestLoops.size()<<std::endl;
    // std::cout<<"NE Test size: "<<NETestLoops.size()<<std::endl;
    for(unsigned int lcv = 0; lcv < NETestLoops.size(); ++lcv)
    {
        NWTestLoops[lcv] = swapEWpathcode(NETestLoops[lcv]);
        SWTestLoops[lcv] = swapNSEWpathcode(NETestLoops[lcv]);
        SETestLoops[lcv] = swapNSpathcode(NETestLoops[lcv]);
    }
    qtTraverseAdd(QT,QT->head());
}
void Primal::qtTraverseAdd(QuadTree* QT,QuadTreeNode_ptr qt)
{
    // std::cout<<"my sizes: "<<NETestLoops.size()<<" and "<<SquareTestLoops.size()<<std::endl;

    if(qt !=NULL )
    {
        if(qt->isLeaf)
        {
            ///Split codes 270, 180, 90, but then SW, NW, SE, NE


            std::vector<Node> nds;
            std::string splitcode = qt->splitcode;
            int quadrant = qt->quadrant();
            std::string idcode = qt->locationcode;
            //std::cout<<"loc code: "<<qt->locationcode<<" quadrant "<<qt->quadrant()<<std::endl;
            Node NE = *(qt->nNE);
            Node NW = *(qt->nNW);
            Node SE = *(qt->nSE);
            Node SW = *(qt->nSW);
            Node N = (NE+NW)/2.0;
            Node S = (SE+SW)/2.0;
            Node E = (NE+SE)/2.0;
            Node W = (NW+SW)/2.0;
            if(splitcode=="none")
            {
                //  std::cout<<"none case"<<std::endl;
                nds.push_back(NE);
                nds.push_back(NW);
                nds.push_back(SW);
                nds.push_back(SE);

                addPoly(myNodes,nds,str2ID(idcode,false));



            }
            else
            {
                switch(quadrant)
                {

                case 1: ///NE quad, requires SW split
                {
                    // std::cout<<"1 case"<<std::endl;
                    nds.push_back(W);
                    nds.push_back(S);
                    nds.push_back(SW);
                    addPoly(myNodes,nds,str2ID(idcode,true));

                    nds.resize(0);
                    nds.push_back(S);
                    nds.push_back(SE);
                    nds.push_back(NE);
                    nds.push_back(NW);
                    nds.push_back(W);
                    addPoly(myNodes,nds,str2ID(idcode,false));

                    newtestAdd(SWTestLoops,idcode,QT,qt);
                    break;
                }
                case 2: ///NW quad, requires SE split
                {
                    //std::cout<<"2 case"<<std::endl;
                    nds.push_back(E);
                    nds.push_back(S);
                    nds.push_back(SE);
                    addPoly(myNodes,nds,str2ID(idcode,true));
                    nds.resize(0);
                    nds.push_back(E);
                    nds.push_back(NE);
                    nds.push_back(NW);
                    nds.push_back(SW);
                    nds.push_back(S);
                    addPoly(myNodes,nds,str2ID(idcode,false));

                    newtestAdd(SETestLoops,idcode,QT,qt);
                    break;
                }
                case 3: ///SW quad, requires NE split
                {
                    //std::cout<<"3 case"<<std::endl;
                    nds.push_back(NE);
                    nds.push_back(N);
                    nds.push_back(E);
                    addPoly(myNodes,nds,str2ID(idcode,true));
                    nds.resize(0);
                    nds.push_back(N);
                    nds.push_back(NW);
                    nds.push_back(SW);
                    nds.push_back(SE);
                    nds.push_back(E);
                    addPoly(myNodes,nds,str2ID(idcode,false));

                    newtestAdd(NETestLoops,idcode,QT,qt);
                    break;
                }
                case 4: ///SE quad, requires NW split
                {
                    //std::cout<<"4 case"<<std::endl;
                    nds.push_back(N);
                    nds.push_back(NW);
                    nds.push_back(W);
                    addPoly(myNodes,nds,str2ID(idcode,true));
                    nds.resize(0);
                    nds.push_back(W);
                    nds.push_back(SW);
                    nds.push_back(SE);
                    nds.push_back(NE);
                    nds.push_back(N);
                    addPoly(myNodes,nds,str2ID(idcode,false));

                    newtestAdd(NWTestLoops,idcode,QT,qt);
                    break;
                }
                }///SWITCH

            }///ELSE

            newtestAdd(SquareTestLoops,idcode,QT,qt);  //no matter the split code, we always need to check square loops
        }///LEAF IF
        else
        {
            qtTraverseAdd(QT,qt->NW);
            qtTraverseAdd(QT,qt->NE);
            qtTraverseAdd(QT,qt->SW);
            qtTraverseAdd(QT,qt->SE);

        }

    }
}
std::string Primal::swapEWpathcode(std::string pathcode)
{
    std::string newcode = pathcode;
    for(unsigned int lcv =0; lcv < pathcode.size(); ++lcv)
    {
        switch(pathcode[lcv])
        {
        case 'E':
            newcode[lcv]='W';
            break;
        case 'W':
            newcode[lcv]='E';
            break;
        case '1':
            newcode[lcv]='2';
            break;
        case '2':
            newcode[lcv]='1';
            break;
        case '3':
            newcode[lcv]='4';
            break;
        case '4':
            newcode[lcv]='3';
            break;
        default :
            newcode[lcv]=pathcode[lcv];
            break;
        }
    }
    return newcode;
}
std::string Primal::swapNSpathcode(std::string pathcode)
{
    std::string newcode = pathcode;
    for(unsigned int lcv =0; lcv < pathcode.size(); ++lcv)
    {
        switch(pathcode[lcv])
        {
        case 'N':
            newcode[lcv]='S';
            break;
        case 'S':
            newcode[lcv]='N';
            break;
        case '1':
            newcode[lcv]='4';
            break;
        case '4':
            newcode[lcv]='1';
            break;
        case '2':
            newcode[lcv]='3';
            break;
        case '3':
            newcode[lcv]='2';
            break;
        default :
            newcode[lcv]=pathcode[lcv];
            break;
        }
    }
    return newcode;
}
std::string Primal::swapNSEWpathcode(std::string pathcode)
{
    return(swapNSpathcode(swapEWpathcode(pathcode)));
}

void Primal::newtestAdd(const std::vector<std::string> &testLoops, std::string idcode, QuadTree* QT,QuadTreeNode_ptr qt)
{
    for(unsigned int lcv = 0; lcv < testLoops.size(); ++lcv)
    {
        std::vector<int> loop;
        std::string tcode = idcode;
        testAdd(testLoops[lcv],idcode,tcode,loop,QT,qt);
    }
}
void Primal::testAdd(std::string pathcode, std::string startcode,std::string &curcode,std::vector<int> &loop,QuadTree* QT,QuadTreeNode_ptr qt)
{

    if(pathcode.size()==0 && loop.size()==5 && loop[0] == loop[4])
    {
        addLoop(loop[0],loop[1],loop[2],loop[3]);
    }
    else if(pathcode.size()>=4)
    {
        std::string code = pathcode.substr(0,3);
        pathcode = pathcode.substr(4,pathcode.size()-1);

        char step_direction = code[0];
        char fictitious_code = code[1];
        char destination_code = code[2];

        if(curcode!="NULL")
            switch(fictitious_code)
            {
            case '0':
                curcode=curcode;
                break;
            case '1':
                curcode=curcode+"11";
                break;
            case '2':
                curcode=curcode+"01";
                break;
            case '3':
                curcode=curcode+"00";
                break;
            case '4':
                curcode=curcode+"10";
                break;
            default :
                curcode=curcode;
                break;
            }

        if(curcode!="NULL")
            switch (step_direction)
            {
            case 'N':
                curcode = QT->north(curcode);
                break;
            case 'S':
                curcode = QT->south(curcode);
                break;
            case 'E':
                curcode = QT->east(curcode);
                break;
            case 'W':
                curcode = QT->west(curcode);
                break;
            case 'D':
                curcode = curcode;
                break;
            default :
                curcode = QT->north(curcode);
                break;

            }

        if(curcode!="NULL" && step_direction!='D')
            switch(destination_code)
            {
            case 'O':
                curcode = curcode;
                break;
            case 'P':
                curcode = QT->parent(curcode);
                break;
            case 'T':
                curcode = QT->parent(curcode);
                break;
            default :
                curcode = curcode;
                break;
            }

        if(QT->existsAndLeaf(curcode))
        {
            bool TorF =  destination_code == 'T'  ;
            loop.push_back(str2ID(curcode,TorF ));
            testAdd(pathcode,startcode,curcode,loop,QT,qt);
        }

    } ///else







}


int Primal::str2ID(std::string locationcode, bool AorB)
{

//std::cout<<"loc code: "<<locationcode<<'\t'<<"level: "<<locationcode.size()/2;

    std::bitset<8> levelbit(locationcode.size()/2+1);
    std::string levelbitstring = levelbit.to_string();
//if(locationcode.size() > maxLevel*2)
    //  std::cout<<"WE GOT ISSUES"<<std::endl;
    locationcode.resize(maxLevel*2,'0');
    //for(unsigned int lcv = 0; lcv < maxLevel*2-locationcode.size()-1;++lcv)
    //  locationcode=locationcode+'0';


//std::cout<<"padded :"<<levelbitstring<<" "<<locationcode<<std::endl;
    locationcode=levelbitstring+locationcode;

    if(AorB)
    {
        locationcode="1"+locationcode;
        //mybits[MAXLEVEL-maxLevel*2-3]=1;

    }


    std::bitset<MAXLEVEL> mybits(locationcode);


    return (int) mybits.to_ulong();
}
void Primal::addLoop(int a,int b,int c, int d)
{
    //std::cout<<"a,b,c,d "<<a<<" "<<b<<" "<<c<<" "<<d<<std::endl;
    std::set<int> tmp;
    tmp.insert(a);
    tmp.insert(b);
    tmp.insert(c);
    tmp.insert(d);
    std::tuple<int,int,int,int> tmptup;
    std::set<int>::iterator it;
    int i = 0;

    for(it = tmp.begin(); it!=tmp.end(); ++it)
    {

        switch(i)
        {
        case 0:
            std::get<0>(tmptup)=*it;
            break;
        case 1:
            std::get<1>(tmptup)=*it;
            break;
        case 2:
            std::get<2>(tmptup)=*it;
            break;
        case 3:
            std::get<3>(tmptup)=*it;
            break;
        default :
            std::get<0>(tmptup)=*it;
            break;
        }
        i++;
    }
    uniqueLoops.insert(tmptup);
    // std::cout<<"tuple 0123 "<<std::get<0>(tmptup)<<" "<<std::get<1>(tmptup)<<" "<<std::get<2>(tmptup)<<" "<<std::get<3>(tmptup)<<std::endl;
}
Dual::Dual(Primal* p)
{
    count = 0;
    myNodes= new NodeList();
    myCurve=p->myCurve;
    std::cout<<"Size of my nodes: "<<myNodes->size()<<std::endl;
    std::cout<<"Size of my Primal nodes: "<<p->myNodes->size()<<std::endl;
    std::cout<<"Size of my Primal Polys: "<<p->myPolys.size()<<std::endl;
    //QT->maxLevel(QT->head());
    //qtTraverseAdd(QT->head());
    std::cout<<"Unique loop size: "<<p->uniqueLoops.size()<<std::endl;
    std::set<std::tuple<int,int,int,int> >::iterator it;

    for(it = p->uniqueLoops.begin(); it !=p->uniqueLoops.end(); ++it)
    {
        std::tuple<int,int,int,int> tmptup = *it;
        // std::cout<<std::get<0>(tmptup)<<" "<<std::get<1>(tmptup)<<" "<<std::get<2>(tmptup)<<" "<<std::get<3>(tmptup)<<std::endl;

        // Poly* ptr = p->getPoly(std::get<0>(tmptup));


        count++;

        Node NW = (p->idMap[std::get<0>(tmptup)])->center();
        Node NE =  (p->idMap[std::get<1>(tmptup)])->center();
        Node SW =  (p->idMap[std::get<2>(tmptup)])->center();
        Node SE = (p->idMap[std::get<3>(tmptup)])->center();

        detangleNodes(NE,NW,SW,SE);

        std::vector<Node> nds;
        nds.push_back(NE);
        nds.push_back(NW);
        nds.push_back(SW);
        nds.push_back(SE);
        addPoly(myNodes,nds,count);
    }

}

double Dual::sumSignAreaNodes(Node A,Node B, Node C, Node D)
{
    std::vector<double> crs = {cross(A,B,C),cross(B,C,D),cross(C,D,A),cross(D,A,B)};

    double sum =0;
    for(unsigned int lcv = 0; lcv < crs.size(); ++lcv)
    {
        sum=sum+(crs[lcv]>0?1:-1);
    }
    return sum;
}
void Dual::detangleNodes(Node &A,Node &B, Node &C, Node &D)
{

    double sum = sumSignAreaNodes(A,B,C,D);
    if(sum == 0 )
    {
        if(sumSignAreaNodes(A,B,D,C) ==4 )
            swap(C,D);
        else if(sumSignAreaNodes(A,C,B,D)==4)
            swap(B,C);
        else if(sumSignAreaNodes(A,C,D,B)==4)
        {
            swap(B,D);
            swap(B,C);
        }
        else if(sumSignAreaNodes(A,D,B,C)==4)
        {
            swap(B,D);
            swap(C,D);
        }
        else if (sumSignAreaNodes(A,D,C,B)==4)
            swap(B,D);
        else
            std::cout<<"WARNING -- Dual Detangle Nodes, this is a case that I hadn't thought of."<<'\n'<<A<<'\n'<<B<<'\n'<<C<<'\n'<<D<<'\n'<<std::endl;
    }
    else if(sum == -4 )
    {
        swap(A,D);
        swap(B,C);
    }

}

double Dual::cross(Node A, Node B, Node C)
{
    double fx = B.X()-A.X();
    double fy = B.Y()-A.Y();
    double tx = C.X()-B.X();
    double ty = C.Y()-B.Y();

    return fy*tx-fx*ty;

}
double Dual::angle(Node A,Node B, Node C)
{
    double fx = B.X()-A.X();
    double fy = B.Y()-A.Y();
    double fmag = sqrt(fx*fx+fy*fy);
    fx=fx/fmag;
    fy=fy/fmag;
    double tx = C.X()-B.X();
    double ty = C.Y()-B.Y();
    double tmag = sqrt(tx*tx+ty*ty);
    tx = tx/tmag;
    ty = ty/tmag;

    double ang =acos(fx*tx + fy*ty)*180/3.14159;
///if(ang<0)
    ///  ang=ang+360; //ang*(-1);
    return ang;
}
void Dual::trim()
{
    edgeUpToDate=false;
    std::list<Poly>::iterator it;
    for(it = myPolys.begin(); it!=myPolys.end(); ++it)
    {
        Node temp = it->center();
        if(!myCurve->inCurve(temp.X(),temp.Y()))
            it->active(false);

        /* double sum = 0;
         for(auto x : it->myNodes)
             if(myCurve->inCurve(x->X(),x->Y()))
                 sum++;
         if(sum != it->myNodes.size())
         it->active(false);*/

    }

}
void Dual::fixCornerPolys()
{
    ///THIS FUNCTION DOES NOT WORK
    std::list<Poly>::iterator it;
    for(it = myPolys.begin(); it!=myPolys.end(); ++it)
    {
        int sum =0;
        std::vector<Node*> nds;
        for(auto n : it->myNodes)
            if(n->fringe())
            {
                sum++;
                nds.push_back(n);
            }

        if(sum == 3) ///Three fringe nodes
        {
            ///THIS DOES NOT WORK
            std::cout<<"Sum of 3"<<std::endl;
            Node *a,*b,*c;
            if(nds[0]->id()!=-1)
            {
                b = nds[0];
                a = nds[1];
                c = nds[2];
            }
            else if(nds[1]->id()!=-1)
            {
                b = nds[1];
                a = nds[2];
                c = nds[0];
            }
            else //if(nds[2]->id()!=-1)
            {
                b = nds[2];
                a = nds[1];
                c = nds[0];
            }
            b->X((a->X()+c->X())/2.0);
            b->Y((a->Y()+c->Y())/2.0);

        }
    }

}
void Dual::project()
{
    if(!edgeUpToDate)
        fringeNodes(); ///UPDATE ACTIVE AND FRINGE NODES

    //fixCornerPolys();

    std::list<Node>::iterator it;
    for(it = myNodes->nodes.begin(); it!=myNodes->nodes.end(); ++it)
    {
        if(it->fringe())
        {
            std::tuple<double,double> np = myCurve->nearestPt(it->X(),it->Y());
            it->X(std::get<XIND>(np));
            it->Y(std::get<YIND>(np));
        }
    }
}
void Dual::snap()
{

    std::vector<CurvePoint> corners = myCurve->corners();
    ///snap nearest node to a corner
    for(unsigned int lcv =0; lcv < corners.size(); ++lcv)
    {
        Node* np = myNodes->near(corners[lcv].X(),corners[lcv].Y());
        np->X(corners[lcv].X());
        np->Y(corners[lcv].Y());
    }
}
int Dual::badAngleInd(double ang1, double ang2, double ang3, double ang4)
{
    if(ang1  > 90)
        ang1 = absval(ang1 - 180);
    if(ang2  > 90)
        ang2 = absval(ang2 - 180);
    if(ang3  > 90)
        ang3 = absval(ang3 - 180);
    if(ang4  > 90)
        ang4 = absval(ang4 - 180);

    int mini = 1;
    double minval = ang1;

    if(ang2 < minval)
    {
        minval=ang2;
        mini=2;
    }
    if(ang3 < minval)
    {
        minval=ang3;
        mini=3;
    }
    if(ang4 < minval)
    {
        minval=ang4;
        mini=4;
    }
    return mini;
}
bool Dual::split3(Poly* p)
{
    ///check 4 angles to see if this quad should be split into three, if true do so and return true,  otherwise return false.
    if(p!=NULL && p->myNodes.size()==4 && p->active() && p->okToSubdivide)
    {
        Node A = *(p->myNodes[0]);
        Node B = *(p->myNodes[1]);
        Node C = *(p->myNodes[2]);
        Node D = *(p->myNodes[3]);

        Node AB = (A+B)/2.0;
        Node BC = (B+C)/2.0;
        Node CD = (C+D)/2.0;
        Node DA = (D+A)/2.0;


        double angABC = angle(A,B,C);
        double angBCD = angle(B,C,D);
        double angCDA = angle(C,D,A);
        double angDAB = angle(D,A,B);

        if(oblique(angABC) || oblique(angBCD) || oblique(angCDA) || oblique(angDAB ))
        {
            p->active(false);
            p->okToSubdivide=false;
            std::vector<Node> nds;

            int badAngIndex =  badAngleInd(angABC,angBCD,angCDA,angDAB);

            switch(badAngIndex)
            {
            case 1:  ///angle ABC is bad meaning B is the oblique point
            {
                Node M = (A+C+D)/3.0;
                walkB(A,B,C);
                count++;
                nds.resize(0);
                detangleNodes(B,C,CD,M);
                nds.push_back(B);
                nds.push_back(C);
                nds.push_back(CD);
                nds.push_back(M);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(B,M,DA,A);
                nds.push_back(B);
                nds.push_back(M);
                nds.push_back(DA);
                nds.push_back(A);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(M,CD,D,DA);
                nds.push_back(M);
                nds.push_back(CD);
                nds.push_back(D);
                nds.push_back(DA);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                break;
            }
            case 2:   ///angle BCD is bad meaning C is the oblique point
            {
                Node M = (A+B+D)/3.0;
                walkB(B,C,D);
                count++;
                nds.resize(0);
                detangleNodes(C,M,AB,B);
                nds.push_back(C);
                nds.push_back(M);
                nds.push_back(AB);
                nds.push_back(B);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(C,D,DA,M);
                nds.push_back(C);
                nds.push_back(D);
                nds.push_back(DA);
                nds.push_back(M);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(M,DA,A,AB);
                nds.push_back(M);
                nds.push_back(DA);
                nds.push_back(A);
                nds.push_back(AB);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                break;
            }
            case 3:   ///angle CDA is bad meaning D is the oblique point
            {
                Node M = (A+B+C)/3.0;
                walkB(C,D,A);
                count++;
                nds.resize(0);
                detangleNodes(D,A,AB,M);
                nds.push_back(D);
                nds.push_back(A);
                nds.push_back(AB);
                nds.push_back(M);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(D,M,BC,C);
                nds.push_back(D);
                nds.push_back(M);
                nds.push_back(BC);
                nds.push_back(C);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(M,AB,B,BC);
                nds.push_back(M);
                nds.push_back(AB);
                nds.push_back(B);
                nds.push_back(BC);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                break;
            }
            case 4:   ///angle DAB is bad meaning A is the oblique point
            {
                Node M = (D+B+C)/3.0;
                walkB(D,A,B);
                count++;
                nds.resize(0);
                detangleNodes(A,B,BC,M);
                nds.push_back(A);
                nds.push_back(B);
                nds.push_back(BC);
                nds.push_back(M);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(A,M,CD,D);
                nds.push_back(A);
                nds.push_back(M);
                nds.push_back(CD);
                nds.push_back(D);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                count++;
                nds.resize(0);
                detangleNodes(M,BC,C,CD);
                nds.push_back(M);
                nds.push_back(BC);
                nds.push_back(C);
                nds.push_back(CD);
                addPoly(myNodes,nds,count);
                getPoly(count)->okToSubdivide=false;
                break;
            }
            default :
                return false;
                break;
            } ///switch

            return true;
        } ///if



    }
    return false;
}
void Dual::subdivide(Poly* p)
{
    if(p!=NULL && p->myNodes.size()==4 && p->active() && p->okToSubdivide)
    {
        Node A = *(p->myNodes[0]);
        Node B = *(p->myNodes[1]);
        Node C = *(p->myNodes[2]);
        Node D = *(p->myNodes[3]);

        Node AB = (A+B)/2.0;
        Node BC = (B+C)/2.0;
        Node CD = (C+D)/2.0;
        Node DA = (D+A)/2.0;
        Node M = (A+B+C+D)/4.0;

        p->active(false);
        std::vector<Node> nds;
        count++;
        nds.resize(0);

        detangleNodes(A,AB,M,DA);
        nds.push_back(A);
        nds.push_back(AB);
        nds.push_back(M);
        nds.push_back(DA);
        addPoly(myNodes,nds,count);
        count++;
        nds.resize(0);
        detangleNodes(AB,B,BC,M);
        nds.push_back(AB);
        nds.push_back(B);
        nds.push_back(BC);
        nds.push_back(M);
        addPoly(myNodes,nds,count);
        count++;
        nds.resize(0);
        detangleNodes(BC,C,CD,M);
        nds.push_back(BC);
        nds.push_back(C);
        nds.push_back(CD);
        nds.push_back(M);
        addPoly(myNodes,nds,count);

        count++;
        nds.resize(0);
        detangleNodes(CD,D,DA,M);
        nds.push_back(CD);
        nds.push_back(D);
        nds.push_back(DA);
        nds.push_back(M);
        addPoly(myNodes,nds,count);
    }
}
void Dual::subdivide()
{
    std::list<Poly>::iterator it;
    int current = 1;
    int maxcount = count;
    for(it=myPolys.begin(); it!=myPolys.end(); ++it)
    {
        //  std::cout<<"subidividing poly: "<<current<<std::endl;

        if(!split3(&(*it)))
            subdivide(&(*it));
        current++;
        if(current>maxcount)
            break;
    }
    edgeUpToDate=false;
}
void Dual::smooth()
{
    /*
    This function still doesn't work as intended
    need to really figure out a robust method for smoothing.
            */

    /*
        std::list<Poly>::iterator it;
        myNodes->resetForce();

        double k = 0.05;
        double kdiag = 0.1;

        double shortLen=1e9;
        double longLen = 0;
        for(it=myPolys.begin();it!=myPolys.end();++it)
        {
            double ss = it->shortestSide();
            double ls = it->longestSide();
            if(ss<shortLen)
                shortLen=ss;
            if(ls>longLen)
                longLen = ls;
        }

        for(it=myPolys.begin();it!=myPolys.end();++it)
        {
            //double ss = (it->longestSide()+it->shortestSide())/2.0;
           for(int a = 0; a <4;++a)
           {
                int b = a+1;
                if(b ==4)
                    b=0;

           double dist  = it->myNodes[a]->dist(*(it->myNodes[b]));
           double scl = 1-(dist-shortLen)/(longLen-shortLen);

           double func = (dist*(scl+1.0));

           Node direction = it->myNodes[a]->direction(*(it->myNodes[b]));

           double nx = direction.X();
           double ny = direction.Y();
            it->myNodes[a]->fx+=nx*func*k;
            it->myNodes[a]->fy+=ny*func*k;
            it->myNodes[b]->fx-=nx*func*k;
            it->myNodes[b]->fy-=ny*func*k;
           }


            int a = 0;
            int b = 2;
           double distAC  = it->myNodes[a]->dist(*(it->myNodes[b]));
           Node directionAC = it->myNodes[a]->direction(*(it->myNodes[b]));
             a = 3;
             b = 1;
           double distBD  = it->myNodes[a]->dist(*(it->myNodes[b]));
           Node directionBD = it->myNodes[a]->direction(*(it->myNodes[b]));
            Node direction;
            double dist;
           if(distAC > distBD)
           {
              direction = directionAC;
             a=0;b=2;dist = distAC-distBD;
           }
           else
            { direction = directionBD;
            a=3;b=1;
            dist = distBD-distAC;
            }

            double nx = direction.X();
            double ny = direction.Y();
            it->myNodes[a]->fx+=nx*dist*kdiag;
            it->myNodes[a]->fy+=ny*dist*kdiag;
            it->myNodes[b]->fx-=nx*dist*kdiag;
            it->myNodes[b]->fy-=ny*dist*kdiag;


        }
        myNodes->moveByForce();*/
}

void Dual::walkB(Node A,Node &B, Node C)
{
    B = (A+C)/2.0;
    std::tuple<double,double> nn =myCurve->nearestPt(B.X(),B.Y());
    B.X(std::get<XIND>(nn));
    B.Y(std::get<YIND>(nn));
}
std::vector<std::vector<int> > Dual::getConnectivity()
{
    std::vector<std::vector<int> > con;
    std::list<Poly>::iterator it;
    for(it=myPolys.begin(); it!=myPolys.end(); ++it)
    {
        if(it->active())
        {
            std::vector<int> tmp;
            tmp.push_back((it->myNodes[0])->id());
            tmp.push_back((it->myNodes[1])->id());
            tmp.push_back((it->myNodes[2])->id());
            tmp.push_back((it->myNodes[3])->id());
            con.push_back(tmp);
        }
    }
    return con;
}
std::vector<std::vector<float> > Dual::getNodes()
{
    std::vector<std::vector<float> > nds;
    std::list<Node>::iterator it;
    for(it = myNodes->nodes.begin(); it!=myNodes->nodes.end(); ++it)
    {
        if(it->active())
        {
            std::vector<float> tmp(4,0);
            tmp[0] = it->id();
            tmp[1] = it->X();
            tmp[2] = it->Y();
            tmp[3] = it->Z();
            nds.push_back(tmp);
        }
    }
    return nds;

}
