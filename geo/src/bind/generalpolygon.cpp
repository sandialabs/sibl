#include "generalpolygon.h"
#include "intersectionprimitives.h"
#include <iostream>
#include <cmath>
GeneralizedPolygon::GeneralizedPolygon(std::pair<std::vector<float>, std::vector<float>> const& nanSepPoly)
{
	using namespace IntersectionPrimitives;
	if(nanSepPoly.first.empty() || nanSepPoly.second.empty() || (nanSepPoly.first.size() != nanSepPoly.second.size()))
		return; // Invalid input
	std::vector<PolygonSegment> segs;
	segs.reserve(nanSepPoly.first.size());
	std::size_t firstk = 0;
	for(std::size_t k = 1; k < nanSepPoly.first.size(); ++k)
	{
		if(std::isnan(nanSepPoly.first[k]))
		{
			segs.push_back(PolygonSegment(nanSepPoly.first[k - 1], nanSepPoly.second[k - 1],
																		nanSepPoly.first[firstk], nanSepPoly.second[firstk]));
			firstk = k + 1; // Reset the first point
			++k; // Need to pass the NAN for next iteration
		}
		else
			segs.push_back(PolygonSegment(nanSepPoly.first[k - 1], nanSepPoly.second[k - 1],
                                    nanSepPoly.first[k], nanSepPoly.second[k]));
	}
	// Add last segment
	segs.push_back(PolygonSegment(nanSepPoly.first.back(), nanSepPoly.second.back(),
																nanSepPoly.first[firstk], nanSepPoly.second[firstk]));
	// Compute area
	m_area = polygonArea(segs);
	// Set up tree
	m_kdtree = std::unique_ptr<KDTree>(new KDTree(std::move(segs)));
}

GeneralizedPolygon::GeneralizedPolygon(int len, float x[],float y[])
{
    std::vector<double> xv(len,0);
    std::vector<double> yv(len,0);
    for(unsigned int lcv = 0; lcv < len; ++lcv)
    {
        xv[lcv]=x[lcv];
        yv[lcv]=y[lcv];
		std::cout<<"(X,Y) "<<x[lcv]<<","<<y[lcv]<<std::endl;
    }
    std::pair<std::vector<double>, std::vector<double>> nanSepPoly;
    nanSepPoly.first=xv;
    nanSepPoly.second=yv;
	using namespace IntersectionPrimitives;
	if(nanSepPoly.first.empty() || nanSepPoly.second.empty() || (nanSepPoly.first.size() != nanSepPoly.second.size()))
		return; // Invalid input
	std::vector<PolygonSegment> segs;
	segs.reserve(nanSepPoly.first.size());
	std::size_t firstk = 0;
	for(std::size_t k = 1; k < nanSepPoly.first.size(); ++k)
	{
		if(std::isnan(nanSepPoly.first[k]))
		{
			segs.push_back(PolygonSegment(nanSepPoly.first[k - 1], nanSepPoly.second[k - 1],
																		nanSepPoly.first[firstk], nanSepPoly.second[firstk]));
			firstk = k + 1; // Reset the first point
			++k; // Need to pass the NAN for next iteration
		}
		else
			segs.push_back(PolygonSegment(nanSepPoly.first[k - 1], nanSepPoly.second[k - 1],
                                    nanSepPoly.first[k], nanSepPoly.second[k]));
	}
	// Add last segment
	segs.push_back(PolygonSegment(nanSepPoly.first.back(), nanSepPoly.second.back(),
																nanSepPoly.first[firstk], nanSepPoly.second[firstk]));
	// Compute area
	m_area = polygonArea(segs);
	// Set up tree
	m_kdtree = std::unique_ptr<KDTree>(new KDTree(std::move(segs)));


}
GeneralizedPolygon::GeneralizedPolygon(std::pair<std::vector<double>, std::vector<double>> const& nanSepPoly)
{
	using namespace IntersectionPrimitives;
	if(nanSepPoly.first.empty() || nanSepPoly.second.empty() || (nanSepPoly.first.size() != nanSepPoly.second.size()))
		return; // Invalid input
	std::vector<PolygonSegment> segs;
	segs.reserve(nanSepPoly.first.size());
	std::size_t firstk = 0;
	for(std::size_t k = 1; k < nanSepPoly.first.size(); ++k)
	{
		if(std::isnan(nanSepPoly.first[k]))
		{
			segs.push_back(PolygonSegment(nanSepPoly.first[k - 1], nanSepPoly.second[k - 1],
																		nanSepPoly.first[firstk], nanSepPoly.second[firstk]));
			firstk = k + 1; // Reset the first point
			++k; // Need to pass the NAN for next iteration
		}
		else
			segs.push_back(PolygonSegment(nanSepPoly.first[k - 1], nanSepPoly.second[k - 1],
                                    nanSepPoly.first[k], nanSepPoly.second[k]));
	}
	// Add last segment
	segs.push_back(PolygonSegment(nanSepPoly.first.back(), nanSepPoly.second.back(),
																nanSepPoly.first[firstk], nanSepPoly.second[firstk]));
	// Compute area
	m_area = polygonArea(segs);
	// Set up tree
	m_kdtree = std::unique_ptr<KDTree>(new KDTree(std::move(segs)));
}
/* // This is for converting CGAL data types, won't compile w/o CGAL
GeneralizedPolygon::GeneralizedPolygon(std::vector<Topologies::Mesh_Segment_2> const& CGALSegmentSoup)
{
	using namespace IntersectionPrimitives;
	std::vector<PolygonSegment> segs;
	segs.reserve(CGALSegmentSoup.size());
	for(auto const& curCGALSeg : CGALSegmentSoup)
	{
		segs.push_back(PolygonSegment(curCGALSeg.source().x(), curCGALSeg.source().y(),
																	curCGALSeg.target().x(), curCGALSeg.target().y()));
	}
	// Compute area
	m_area = polygonArea(segs);
	// Set up tree
	m_kdtree = std::unique_ptr<KDTree>(new KDTree(std::move(segs)));
}
*/
bool GeneralizedPolygon::inpoly(float x,float y) const
{
    return inpoly(std::pair<double,double>(x,y));
}
bool GeneralizedPolygon::inpoly(std::pair<double,double> const& pairPt) const
{
	using namespace IntersectionPrimitives;
	Point pt(pairPt);
	IntersectionCounter numIntersections = m_kdtree->numIntersections(CartesianRay(pt, CartesianDirection::x));
	if(numIntersections.badIntersections())
	{
		// An ambiguous result was found, so try with a y-directed ray
		numIntersections = m_kdtree->numIntersections(CartesianRay(pt, CartesianDirection::y));
		if(numIntersections.badIntersections())
		{
			// Still found an ambiguous result
			// The best solution to this issue is probably to use a ray with an arbitrary slope.
			// Using a more general ray introduces additional complications (dealing with infinite slope)
			// and makes the ray/bbox intersection more difficult.  So for now, perturb the point slightly and check again
			double tol = sqrt(m_area)*1e-12;
			Point perturbPt(pt.x() + tol, pt.y() + tol);
			numIntersections = m_kdtree->numIntersections(CartesianRay(perturbPt, CartesianDirection::x));
		}
	}
	return (numIntersections[IntersectionType::interior] % 2) == 1;
}

