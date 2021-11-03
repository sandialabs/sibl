#include "intersectionprimitives.h"
#include <cmath>

namespace IntersectionPrimitives
{
	namespace
	{
		// Helper functions for constructing a bounding box
		void replaceIfLesser(double& cmin, double c)
		{
			if(c < cmin)
				cmin = c;
		}
		void replaceIfGreater(double& cmax, double c)
		{
			if(c > cmax)
				cmax = c;
		}
	}

	IntersectionCounter::IntersectionCounter()
	{
		nintersections[IntersectionType::interior] = 0;
		nintersections[IntersectionType::vertex] = 0;
		nintersections[IntersectionType::collinear] = 0;
	}

	bool IntersectionCounter::any() const
	{
		return nintersections.at(IntersectionType::interior) > 0 
				|| nintersections.at(IntersectionType::vertex) > 0
				|| nintersections.at(IntersectionType::collinear) > 0;
	}
	
	bool IntersectionCounter::badIntersections() const
	{
		return nintersections.at(IntersectionType::vertex) != 0 || nintersections.at(IntersectionType::collinear) != 0;
	}

	IntersectionCounter& IntersectionCounter::operator+=(IntersectionCounter const& rhs)
	{
		nintersections[IntersectionType::interior] += rhs[IntersectionType::interior];
		nintersections[IntersectionType::vertex] += rhs[IntersectionType::vertex];
		nintersections[IntersectionType::collinear] += rhs[IntersectionType::collinear];
		return *this;
	}
	
	IntersectionCounter& IntersectionCounter::operator+=(IntersectionType const& rhs)
	{
		if(rhs != IntersectionType::none)
			nintersections[rhs] += 1;
		return *this;
	}

	BoundingBox::BoundingBox(std::vector<PolygonSegment const*> const& polySegs) :
		m_bottomLeft(0., 0.),
		m_topRight(0., 0.)
	{
		if(polySegs.empty())
			return;
		double xmin = polySegs[0]->p0().x();
		double ymin = polySegs[0]->p0().y();
		double xmax = polySegs[0]->p0().x();
		double ymax = polySegs[0]->p0().y();
		for(auto pcurseg : polySegs)
		{
			// First point in segment
			replaceIfLesser(xmin, pcurseg->p0().x());
			replaceIfLesser(ymin, pcurseg->p0().y());
			replaceIfGreater(xmax, pcurseg->p0().x());
			replaceIfGreater(ymax, pcurseg->p0().y());
			// Second point in segment
			replaceIfLesser(xmin, pcurseg->p1().x());
			replaceIfLesser(ymin, pcurseg->p1().y());
			replaceIfGreater(xmax, pcurseg->p1().x());
			replaceIfGreater(ymax, pcurseg->p1().y());
		}
		m_bottomLeft.x() = xmin;
		m_bottomLeft.y() = ymin;
		m_topRight.x() = xmax;
		m_topRight.y() = ymax;
	}

	bool BoundingBox::intersects(CartesianRay const& ray) const
	{
		bool res = false;
		// Get coordinate accessors
		std::unique_ptr<coordAccessor> upU = coordAccessor::parallelToDirection(ray.direction());
		std::unique_ptr<coordAccessor> upV = coordAccessor::perpToDirection(ray.direction());
		coordAccessor const& u = *upU;
		coordAccessor const& v = *upV;
		// Do checks
		res = v(ray.origin()) >= v(m_bottomLeft);
		res &= v(ray.origin()) <= v(m_topRight);
		res &= u(ray.origin()) <= u(m_topRight);
		return res;
	}

	bool BoundingBox::has(PolygonSegment const& seg) const
	{
		Point const mp = seg.midpoint();
		bool res = mp.x() > m_bottomLeft.x();
		res &= mp.x() < m_topRight.x();
		res &= mp.y() > m_bottomLeft.y();
		res &= mp.y() < m_topRight.y();
		return res;
	}

	IntersectionType PolygonSegment::intersects(CartesianRay const& ray) const
	{
		double tol = 1e-13*sqrt(len2());
		// Get coordinate accessors
		std::unique_ptr<coordAccessor> upU = coordAccessor::parallelToDirection(ray.direction());
		std::unique_ptr<coordAccessor> upV = coordAccessor::perpToDirection(ray.direction());
		coordAccessor const& u = *upU;
		coordAccessor const& v = *upV; 
		// First check for axis-aligned segment
		double td = v(m_p1) - v(m_p0);
		if(fabs(td) < tol)
		{
			if(fabs(v(m_p0) - v(ray.origin())) < tol && (u(ray.origin()) < u(m_p0) || u(ray.origin()) < u(m_p1)))
				return IntersectionType::collinear;
			return IntersectionType::none;
		}
		// Check t* and xi*
		double tstar = (v(ray.origin()) - v(m_p0))/td;
		double xistar = tstar*(u(m_p1) - u(m_p0)) + u(m_p0) - u(ray.origin());
		if(xistar > 0.)
		{
			if(tstar == 0. || tstar == 1.)
				return IntersectionType::vertex;
			else if(tstar > 0. && tstar < 1.)
				return IntersectionType::interior;
		}
		return IntersectionType::none;
	}

	Point& Point::operator+=(Point const& p)
	{
		m_x += p.x();
		m_y += p.y();
		return *this;
	}

	Point Point::operator+(Point p)
	{
		p += *this;
		return p;
	}

	Point& Point::operator/=(double s)
	{
		m_x /= s;
		m_y /= s;
		return *this;
	}

	std::unique_ptr<coordAccessor> coordAccessor::parallelToDirection(CartesianDirection dir)
	{
		if(dir == CartesianDirection::x)
			return std::unique_ptr<coordAccessor>(new xAccessor());
		return std::unique_ptr<coordAccessor>(new yAccessor());
	}

	std::unique_ptr<coordAccessor> coordAccessor::perpToDirection(CartesianDirection dir)
	{
		if(dir == CartesianDirection::y)
			return std::unique_ptr<coordAccessor>(new xAccessor());
		return std::unique_ptr<coordAccessor>(new yAccessor());
	}

	double polygonArea(std::vector<PolygonSegment> const& segs)
	{
		double area = 0.;
		for(auto curSeg : segs)
			area += curSeg.p0().x()*curSeg.p1().y() - curSeg.p1().x()*curSeg.p0().y();
		return area*0.5;
	}
}

