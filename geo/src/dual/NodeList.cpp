#include "NodeList.h"
#include <sstream>

bool areEqual(const std::tuple<double,double>& first, const std::tuple<double,double>& second)
{
    return (std::get<XIND>(first)-std::get<XIND>(second))*(std::get<XIND>(first)-std::get<XIND>(second))   +  (std::get<YIND>(first)-std::get<YIND>(second))*(std::get<YIND>(first)-std::get<YIND>(second))<TOLERANCE*TOLERANCE;
}
bool areEqual(const std::tuple<double,double,double>& first, const std::tuple<double,double,double>& second)
{
    return (std::get<XIND>(first)-std::get<XIND>(second))*(std::get<XIND>(first)-std::get<XIND>(second))   +  (std::get<YIND>(first)-std::get<YIND>(second))*(std::get<YIND>(first)-std::get<YIND>(second))    +  (std::get<ZIND>(first)-std::get<ZIND>(second))*(std::get<ZIND>(first)-std::get<ZIND>(second))<TOLERANCE*TOLERANCE;
}
Node& Node::operator=(const Node& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    x=rhs.x;y=rhs.y;z=rhs.z;
    isActive=rhs.isActive;
    isFringe=rhs.isFringe;
    myID = rhs.myID;

    return *this;
}
Node Node::operator + ( const Node& A ) const
{
    return Node( std::tuple<double,double,double>(x + A.x, y + A.y,z+A.z),A.isFringe&&isFringe );
}
Node Node::operator / ( const double A ) const
{
    return Node( std::tuple<double,double,double>(x /A, y / A, z/A),isFringe );
}
bool Node::operator ==( const Node& A ) const
{
    return (A.x - x)*(A.x - x)+(A.y - y)*(A.y - y)+(A.z - z)*(A.z - z) < TOLERANCE*TOLERANCE;
}
bool Node::operator<(const Node& rhs)
{
    return (x<rhs.x && y<rhs.y && z<rhs.z);
}
std::ostream& operator<<(std::ostream& stream, const Node& n)
{
    stream<<n.myID<<'\t'<<n.x<<'\t'<<n.y<<'\t'<<n.z<<'\t'<<n.isActive<<'\t'<<n.isFringe;
    return stream;
}
std::string Node::print()
{
    std::stringstream ss;
    ss<<myID<<'\t'<<x<<'\t'<<y<<'\t'<<z<<'\t'<<isActive<<'\t'<<isFringe;
    return ss.str();
}
Node* NodeList::addNode(Node N)
{
    std::tuple<double,double,double> pt = N.xyz();
    bool fringe = N.fringe();

    std::list<Node>::iterator it;
    for (it=nodes.begin(); it!=nodes.end();++it)
        if(areEqual(it->xyz(),pt))
        return &(*it);

    count++;
    nodes.push_back(Node(pt,fringe,count));

    return &(nodes.back());

}

Node* NodeList::addNode(std::tuple<double,double,double> pt,bool fringe)
{
    std::list<Node>::iterator it;
    for (it=nodes.begin(); it!=nodes.end();++it)
        if(areEqual(it->xyz(),pt))
        return &(*it);

        ++count;
    nodes.push_back(Node(pt,fringe,count));

    return &(nodes.back());

}
Node* NodeList::addNode(std::tuple<double,double> pt,bool fringe)
{
 std::list<Node>::iterator it;
    for (it=nodes.begin(); it!=nodes.end();++it)
        if(areEqual(it->xy(),pt))
        return &(*it);

++count;
    nodes.push_back(Node(pt,fringe,count));

    return &(nodes.back());
}
Node* NodeList::addNode(double tx,double ty,bool fringe)
{
    return addNode(std::tuple<double,double>(tx,ty),fringe);
}
Node* NodeList::addNode(double tx,double ty,double tz,bool fringe)
{
    return addNode(std::tuple<double,double,double>(tx,ty,tz),fringe);
}
void NodeList::print()
{
    for(auto x : nodes)
        std::cout<<x<<std::endl;
}
void NodeList::write(std::string filename)
{
    std::ofstream out_file(filename.c_str());
    for(auto x : nodes)
        out_file<<x<<std::endl;
    out_file.close();
}
void NodeList::writeCSVAppend(std::string filename)
{
    std::ofstream out_file(filename.c_str(),std::ios::app);
    for(auto n : nodes)
        out_file<<n.id()<<",\t"<<n.x<<",\t"<<n.y<<",\t"<<n.z<<std::endl;
    out_file.close();

    //out_file<<x.id()<<',\t'<<x.X()<<',\t'<<x.Y()<<',\t'<<x.Z()<<std::endl;
}
void NodeList::writeTABAppend(std::string filename)
{
 std::ofstream out_file(filename.c_str(),std::ios::app);
    for(auto n : nodes)
        out_file<<"\t"<<n.x<<"\t"<<n.y<<"\t"<<n.z<<std::endl;
    out_file.close();
}
void NodeList::fringe(int id,bool f)
{
    ///set node that has given id, fringe status f
     std::list<Node>::iterator it;
    for(it = nodes.begin();it!=nodes.end();++it)
        if(it->id()==id)
            it->fringe(f);
}
void NodeList::resetFringe()
{
    std::list<Node>::iterator it;
    for(it = nodes.begin();it!=nodes.end();++it)
            it->fringe(false);
}
Node* NodeList::near(double x,double y)
{
    double dist=1e9;

    Node* closep=NULL;

     std::list<Node>::iterator it;
    for(it = nodes.begin();it!=nodes.end();++it)
    {
        double tdist = (it->X()-x)*(it->X()-x)+(it->Y()-y)*(it->Y()-y);
        if(it==nodes.begin())
        {
            closep=&(*it);
            dist = (it->X()-x)*(it->X()-x)+(it->Y()-y)*(it->Y()-y);
        }
        else if(tdist < dist)
            {
                closep=&(*it);
                dist = tdist;
            }
    }
    return closep;
}
