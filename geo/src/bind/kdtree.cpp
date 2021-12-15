#include "kdtree.h"
#include <iostream>

namespace
{
	IntersectionPrimitives::Point midpoint(std::vector<IntersectionPrimitives::PolygonSegment const *> const &segs)
	{
		IntersectionPrimitives::Point mp(0., 0.);
		for (auto pCurSeg : segs)
			mp += pCurSeg->midpoint();
		mp /= static_cast<double>(segs.size());
		return mp;
	}
}

KDTree::KDTree(std::vector<IntersectionPrimitives::PolygonSegment> segs) : m_segs(std::move(segs))
{
	// Set up a vector of pointers to segments
	std::vector<IntersectionPrimitives::PolygonSegment const *> segPs;
	segPs.reserve(m_segs.size());
	for (auto segIt = m_segs.begin(); segIt != m_segs.end(); ++segIt)
		segPs.push_back(&(*segIt));
	// Construct the tree
	m_rootNode = std::unique_ptr<KDTreeNode>(new KDTreeNode(segPs));
}

KDTreeNode::KDTreeNode(std::vector<IntersectionPrimitives::PolygonSegment const *> const &segs) : m_bbox(segs)
{
	using namespace IntersectionPrimitives;
	if (segs.size() <= 10) // Stop if list is small
	{
		m_segs = segs;
		return;
	}
	// Full check
	// First get mid point
	Point mp = midpoint(segs);
	// Get longer axis and coordinate access function
	CartesianDirection dir = m_bbox.orientation();
	std::unique_ptr<coordAccessor> upC = coordAccessor::parallelToDirection(dir);
	coordAccessor const &c = *upC;
	// Split segments into two groups
	std::vector<PolygonSegment const *> rightSegs, leftSegs;
	rightSegs.reserve(segs.size() / 2 + 3);
	leftSegs.reserve(segs.size() / 2 + 3);
	for (auto pCurSeg : segs)
		c(pCurSeg->midpoint()) < c(mp) ? leftSegs.push_back(pCurSeg) : rightSegs.push_back(pCurSeg);
	// Build new nodes
	m_children.push_back(std::unique_ptr<KDTreeNode>(new KDTreeNode(rightSegs)));
	m_children.push_back(std::unique_ptr<KDTreeNode>(new KDTreeNode(leftSegs)));
}

IntersectionPrimitives::IntersectionCounter KDTreeNode::numIntersections(IntersectionPrimitives::CartesianRay const &ray) const
{
	IntersectionPrimitives::IntersectionCounter curIntersections;
	if (m_bbox.intersects(ray))
	{
		for (unsigned k = 0; k < m_children.size(); ++k)
			curIntersections += m_children[k]->numIntersections(ray);
		for (auto pCurSeg : m_segs)
			curIntersections += pCurSeg->intersects(ray);
	}
	return curIntersections;
}

std::size_t KDTree::node_size() const
{
	return m_rootNode->node_size();
}

std::size_t KDTree::seg_size() const
{
	return m_rootNode->seg_size();
}

std::size_t KDTreeNode::node_size() const
{
	std::size_t nnodes = 1;
	for (unsigned k = 0; k < m_children.size(); ++k)
		nnodes += m_children[k]->node_size();
	return nnodes;
}

std::size_t KDTreeNode::seg_size() const
{
	std::size_t nsegs = m_segs.size();
	for (unsigned k = 0; k < m_children.size(); ++k)
		nsegs += m_children[k]->seg_size();
	return nsegs;
}
