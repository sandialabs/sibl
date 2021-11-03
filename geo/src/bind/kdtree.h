#ifndef KDTREE_H
#define KDTREE_H

#include <vector>
#include <memory>
#include <map>
#include "intersectionprimitives.h"

class KDTreeNode
{
	public:
		KDTreeNode(std::vector<IntersectionPrimitives::PolygonSegment const*> const& segs);
		IntersectionPrimitives::IntersectionCounter	numIntersections(IntersectionPrimitives::CartesianRay const& ray) const;
		std::size_t node_size() const;
		std::size_t seg_size() const;
	private:
		std::vector<std::unique_ptr<KDTreeNode>> m_children;
		IntersectionPrimitives::BoundingBox m_bbox;
		std::vector<IntersectionPrimitives::PolygonSegment const*> m_segs;
// Hidden copy ctors
	private:
		KDTreeNode(KDTreeNode const&);
		KDTreeNode(KDTreeNode&&);
		KDTreeNode& operator=(KDTreeNode const&);
		KDTreeNode& operator=(KDTreeNode&&);
};

//! KDTree for fast intersection detection
/*! Adapted from https://blog.frogslayer.com/kd-trees-for-faster-ray-tracing-with-triangles/
 */
class KDTree
{
	public:
		KDTree(std::vector<IntersectionPrimitives::PolygonSegment> segs);
		IntersectionPrimitives::IntersectionCounter	numIntersections(IntersectionPrimitives::CartesianRay const& ray) const 
			{return m_rootNode->numIntersections(ray);}
		std::size_t node_size() const;
		std::size_t seg_size() const;
	private:
		std::vector<IntersectionPrimitives::PolygonSegment> const m_segs;
		std::unique_ptr<KDTreeNode> m_rootNode;
// Hidden copy ctors
	private:
		KDTree(KDTree const&); 
		KDTree(KDTree&&);
		KDTree& operator=(KDTree const&);
		KDTree& operator=(KDTree&&);
};

#endif

