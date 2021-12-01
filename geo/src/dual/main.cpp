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
    cout<<"Version : "<<compilation_date<<endl;
    string filename = argv[2];
    minsize = atof(argv[1]);
    int bnds = atoi(argv[3]);



    Curve* myCurve;
    myCurve = new Curve(filename);
    myCurve->write("line");
    if(bnds == 1)
    {
        myCurve->lowerLeft(std::tuple<double,double>(-1,-1));
        myCurve->upperRight(std::tuple<double,double>(1,1));
    }
    NodeList* myNodes;
    myNodes = new NodeList();
    cout<<"Nodes size: "<<myNodes->size()<<endl;
    QuadTree* myQuadTree;
    myQuadTree=new QuadTree(myCurve,myNodes,minsize);
    myQuadTree->subdivide(myQuadTree->head());



    cout<<"Nodes size: "<<myNodes->size()<<endl;
    //myQuadTree->write("qt");

    myQuadTree->balancedRefineCurve(myQuadTree->head(),false);
    cout<<"Nodes size: "<<myNodes->size()<<endl;
    myQuadTree->write("qt1");

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
   // myDual->write("trimmeddual","");
    myDual->project();
    myDual->write("projecteddual","");
      cout<<"projection done"<<endl;
      myDual->snap();

   // myDual->write("snappeddual","");
     cout<<"snap done"<<endl;
     myDual->subdivide();
  //  myDual->write("subdivideddual","");
    cout<<"subdivide done"<<endl;
    myDual->project();
   // myDual->write("projected2dual","");
    myDual->snap();
    myDual->write("snapped2dual","");
    ///    TODO ADD SMOOTHING function
   /// TODO ADD ABAQUS output
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
    return 0;
}
