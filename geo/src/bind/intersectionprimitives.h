#ifndef INTERSECTIONPRIMITIVES_H
#define INTERSECTIONPRIMITIVES_H

#include <vector>
#include <memory>
#include <map>

namespace IntersectionPrimitives
{
	enum class CartesianDirection{x, y};
	enum class IntersectionType{none, interior, vertex, collinear};

	class IntersectionCounter
	{
		public:
			IntersectionCounter();
			unsigned operator[](IntersectionType it) const {return nintersections.at(it);}
			bool any() const;
			bool badIntersections() const;
			IntersectionCounter& operator+=(IntersectionCounter const& rhs);
			IntersectionCounter& operator+=(IntersectionType const& rhs);
		private:
			std::map<IntersectionType, unsigned> nintersections;
	};

	class Point
	{
		public:
			Point(double x, double y) : m_x(x), m_y(y) {}
			Point(std::pair<double,double> const& p) : m_x(p.first), m_y(p.second) {}
			double& x() {return m_x;}
			double& y() {return m_y;}
			double x() const {return m_x;}
			double y() const {return m_y;}
			Point& operator+=(Point const& p);
			Point operator+(Point p);
			Point& operator/=(double s);
		private:
			double m_x, m_y;
	};

	struct coordAccessor
	{
		virtual double operator()(Point const& p) const = 0;
		virtual double& operator()(Point& p) const = 0;
		static std::unique_ptr<coordAccessor> parallelToDirection(CartesianDirection dir);
		static std::unique_ptr<coordAccessor> perpToDirection(CartesianDirection dir);
	};

	struct xAccessor : public coordAccessor
	{
		virtual double operator()(Point const& p) const {return p.x();}
		virtual double& operator()(Point& p) const {return p.x();}
	};

	struct yAccessor : coordAccessor
	{
		virtual double operator()(Point const& p) const {return p.y();}
		virtual double& operator()(Point& p) const {return p.y();}
	};

	class CartesianRay
	{
		public:
			CartesianRay(double x0, double y0, CartesianDirection dir) :
				m_p(x0, y0), m_dir(dir) {}
			CartesianRay(std::pair<double, double> p, CartesianDirection dir) :
				m_p(p), m_dir(dir) {}
			CartesianRay(Point p, CartesianDirection dir) : 
				m_p(std::move(p)), m_dir(dir) {}

			CartesianDirection direction() const {return m_dir;}
			Point const& origin() const {return m_p;}
		private:
			Point m_p;
			CartesianDirection m_dir;
	};

	class PolygonSegment
	{
		public:
			PolygonSegment(double p0x, double p0y, double p1x, double p1y) :
				m_p0(p0x, p0y), m_p1(p1x, p1y) {}
			PolygonSegment(Point p0, Point p1) :
				m_p0(std::move(p0)), m_p1(std::move(p1)) {}

			Point const& p0() const {return m_p0;}
			Point const& p1() const {return m_p1;}
			Point midpoint() const {return Point(0.5*(m_p0.x() + m_p1.x()), 0.5*(m_p0.y() + m_p1.y()));}
			double len2() const {return (m_p1.x() - m_p0.x())*(m_p1.x() - m_p0.x()) + (m_p1.y() - m_p0.y())*(m_p1.y() - m_p0.y());}
			IntersectionType intersects(CartesianRay const& ray) const; 
		private:
			Point m_p0, m_p1;
	};

	double polygonArea(std::vector<PolygonSegment> const& segs);

	class BoundingBox
	{
		public:
			BoundingBox(double x0, double y0, double width, double height) :
				m_bottomLeft(x0, y0), m_topRight(x0 + width, y0 + height) {}
			BoundingBox(Point bottomLeft, double width, double height) :
				m_bottomLeft(std::move(bottomLeft)), m_topRight(m_bottomLeft.x() + width, m_bottomLeft.y() + height) {}
			BoundingBox(Point bottomLeft, Point topRight) : 
				m_bottomLeft(std::move(bottomLeft)), m_topRight(std::move(topRight)) {}
			BoundingBox(std::vector<PolygonSegment const*> const& polySegs);
			//! Get length along x dimension
			double xlen() const {return m_topRight.x() - m_bottomLeft.x();}
			//! Get length along y dimension
			double ylen() const {return m_topRight.y() - m_bottomLeft.y();}
			//! Returns the direction along which the BoundingBox is longer
			CartesianDirection orientation() const {return xlen() > ylen() ? CartesianDirection::x : CartesianDirection::y;}
			//! Returns true if the ray @param ray intersects with this bounding box
			bool intersects(CartesianRay const& ray) const;
			//! Returns true if the midpoint of the segment @param seg is within this bounding box
			bool has(PolygonSegment const& seg) const;
		private:
			Point m_bottomLeft, m_topRight;
	};
}
#endif

