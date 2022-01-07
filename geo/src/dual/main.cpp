#include <iostream>
#include <tuple>
#include <cstdlib>
#include "NodeList.h"
#include "Curve.h"
#include "QuadTree.h"
#include "Surface.h"

#include "OctTree.h"
#include "Mesh.h"

using namespace std;

int main(int argc, char *argv[])
{
    if(argc > 1)
    {
        double minsize;
        const std::string compilation_date = __DATE__;
        cout<<"Build Date : "<<compilation_date<<endl;
        string filename = argv[2];
        minsize = atof(argv[1]);
        int bnds = atoi(argv[3]);
        int featureRefine = atoi(argv[4]);

        cout<<"Filename : "<<filename<<endl;
        cout<<"Resolution: "<<minsize<<endl;
        cout<<"Bnds: "<<bnds<<endl;
        cout<<"Refine on the feature only: "<<featureRefine<<endl;


        Curve* myCurve;
        myCurve = new Curve(filename);
        filename = filename.substr(0,filename.length()-4);
        myCurve->write("line");
        if(bnds == 1)
        {
            cout<<"Using unit bounds"<<endl;
            myCurve->lowerLeft(std::tuple<double,double>(-1,-1));
            myCurve->upperRight(std::tuple<double,double>(1,1));
        }
        NodeList* myNodes;
        myNodes = new NodeList();
        //cout<<"Nodes size: "<<myNodes->size()<<endl;
        QuadTree* myQuadTree;
        myQuadTree=new QuadTree(myCurve,myNodes,minsize);
        myQuadTree->subdivide(myQuadTree->head());



        //cout<<"Nodes size: "<<myNodes->size()<<endl;
        //myQuadTree->write("qt");

        myQuadTree->balancedRefineCurve(myQuadTree->head(),(featureRefine!=1));
        cout<<"Nodes size: "<<myNodes->size()<<endl;

        myQuadTree->assignSplitCode(myQuadTree->head());

        Primal* myPrimal = new Primal(myQuadTree);

        myPrimal->write("primal","");


        //std::cout<<"00 :" <<myPrimal->str2ID("00",false)<<std::endl;
        //std::cout<<"00 00 :" <<myPrimal->str2ID("0000",false)<<std::endl;
        cout<<"Dual"<<endl;
        Dual* myDual = new Dual(myPrimal);
        cout<<"traverse done"<<endl;
        myDual->write("dual","");
        if(bnds == 0)
        {
            myDual->trim();
            myDual->write("trimmeddual","");
            myDual->project();
            myDual->write("projecteddual","");
            cout<<"projection done"<<endl;
            myDual->snap();

            myDual->write("snappeddual","");
            cout<<"snap done"<<endl;
            myDual->subdivide();
            //myDual->write("subdivideddual","");
            cout<<"subdivide done"<<endl;
            myDual->project();
            //myDual->write("projected2dual","");
            myDual->snap();
            myDual->write("snapped2dual","");
            myDual->updateActiveNodes();
            myDual->write(filename,"inp");
        }


        cout<<"execution done"<<endl;
        /*
        Surface* mySurface;
        mySurface = new Surface("sphere.inp");
        mySurface->write("sph");

        NodeList* myNodes3;
        myNodes3 = new NodeList();

        OctTree* myOctTree;
        myOctTree= new OctTree(mySurface,myNodes3,.5);
        myOctTree->balancedRefineSurface(myOctTree->head());
        //myOctTree->refineSurface(myOctTree->head());
        myOctTree->write("test.inp","inp");
        myOctTree->write("test.vtk","vtk");
        cout<<"Nodes size: "<<myNodes3->size()<<endl;
        //myNodes3->print();

        */
    }
    else
    {
        ///Run some tests:
        Node A,B;
        B.X(1);
        B.Y(1);

        Node direction = A.direction(B);
        double dist = A.dist(B);
        cout<<direction<<endl;
        cout<<dist<<endl;

        Curve* myCurve = new Curve();

        myCurve->lowerLeft(std::tuple<double,double>(-1,-1));
        myCurve->upperRight(std::tuple<double,double>(1,1));

        std::tuple<double,double,double> T1(0,0,0);
        std::tuple<double,double,double> T2(1,0,0);
        std::tuple<double,double,double> T3(1,1,0);
        std::tuple<double,double,double> T4(0,1,0);
        std::tuple<double,double,double> P1(0,.5,0);
        std::tuple<double,double,double> P2(1,.5,0);
        std::tuple<double,double,double> P3(0,1.5,0);
        std::tuple<double,double,double> P4(1,1.5,0);
        std::tuple<double,double,double> P5(0,0,0);
        std::tuple<double,double,double> P6(1,0,0);
        std::tuple<double,double,double> P7(1,1,0);
        std::tuple<double,double,double> P8(0,1,0);
        std::tuple<double,double,double> P9(1,2,0);
        std::tuple<double,double,double> P10(0,-1,0);
        std::tuple<double,double,double> P11(1,0,0);


        cout<<"intersection (true): "<<myCurve->intersects(T1,T2,T3,P1,P2)<<endl;
        cout<<"intersection (false): "<<myCurve->intersects(T1,T2,T3,P3,P4)<<endl;
        cout<<"intersection (true): "<<myCurve->intersects(T1,T2,T3,P5,P6)<<endl;
        cout<<"intersection (true): "<<myCurve->intersects(T1,T2,T3,P5,P7)<<endl;
        cout<<"intersection (false): "<<myCurve->intersects(T1,T2,T3,P8,P9)<<endl;
        cout<<"intersection (true): "<<myCurve->intersects(T1,T2,T3,P10,P11)<<endl;



        NodeList* myNodes;
        myNodes = new NodeList();

        QuadTree* myQuadTree;
        myQuadTree=new QuadTree(myCurve,myNodes,1);
        myQuadTree->subdivide(myQuadTree->head());
        myQuadTree->assignSplitCode(myQuadTree->head());
        Primal* myPrimal = new Primal(myQuadTree);
        myPrimal->write("primal","");
        Dual* myDual = new Dual(myPrimal);
        myDual->write("dual","");




    }
    return 0;
}
