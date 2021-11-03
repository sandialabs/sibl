#ifndef GENERALPOLYGON_H
#define GENERALPOLYGON_H

#include <vector>
#include <memory>
//#include "REP/cgal_types.h"
#include "kdtree.h"

class GeneralizedPolygon //: public std::enable_shared_from_this<GeneralizedPolygon> { };
{
	public:
		GeneralizedPolygon(std::pair<std::vector<double>, std::vector<double>> const& nanSepPoly);
		GeneralizedPolygon(std::pair<std::vector<float>, std::vector<float>> const& nanSepPoly);


		//GeneralizedPolygon(std::vector<Topologies::Mesh_Segment_2> const& CGALSegmentSoup); // For CGAL data types
		bool inpoly(std::pair<double,double> const& pt) const;
		bool inpoly(float x,float y) const; ///Ugly for Python binding
		double area() const {return m_area;}

	private:
		std::unique_ptr<KDTree> m_kdtree;
		double m_area;
	private:
		GeneralizedPolygon(GeneralizedPolygon const&);
		GeneralizedPolygon(GeneralizedPolygon&&);
		GeneralizedPolygon& operator=(GeneralizedPolygon const&);
		GeneralizedPolygon& operator=(GeneralizedPolygon&&);
};

#endif

