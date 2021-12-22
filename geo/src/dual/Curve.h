#ifndef CURVE_H
#define CURVE_H

#include <string>
#include <tuple>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <iostream>

class CurvePoint
{
public:
    CurvePoint(double xx, double yy)
    {
        myX = xx;
        myY = yy;
        myDX = 0;
        myDY = 0;
        myD2X = 0;
        myD2Y = 0;
    }

    double Y()
    {
        return myY;
    }
    double X()
    {
        return myX;
    }
    void DX(double d)
    {
        myDX = d;
    }
    double DX()
    {
        return myDX;
    }
    void DY(double d)
    {
        myDY = d;
    }
    double DY()
    {
        return myDY;
    }

    void D2X(double d)
    {
        myD2X = d;
    }
    double D2X()
    {
        return myD2X;
    }
    void D2Y(double d)
    {
        myD2Y = d;
    }
    double D2Y()
    {
        return myD2Y;
    }

    void tangent(double tx, double ty)
    {
        myTanX = tx;
        myTanY = ty;
        myAngle = std::atan2(ty, tx);
    }
    double angle()
    {
        return myAngle;
    }
    double curvature()
    {
        return myCurvature;
    }
    void curvature(double c)
    {
        myCurvature = c;
    }
    friend std::ostream &operator<<(std::ostream &stream, const CurvePoint &cp);

private:
    double myX, myY;
    double myDX, myDY;
    double myD2X, myD2Y;
    double myTanX, myTanY, myAngle, myCurvature;
};

class Curve
{
public:
    Curve(std::string filename);
    Curve() {};
    Curve(const std::vector<float> &boundary_x, const std::vector<float> &boundary_y); ///Single curve constructor

    std::tuple<double, double> upperRight()
    {
        return ur;
    }
    std::tuple<double, double> lowerLeft()
    {
        return ll;
    }
    void upperRight(std::tuple<double, double> tp)
    {
        ur = tp;
    }
    void lowerLeft(std::tuple<double, double> tp)
    {
        ll = tp;
    }

    ///TODO: Add check for line segment within a bounding box, not just the point cloud
    bool inBoundingBox(std::tuple<double, double> ll, std::tuple<double, double> ur);
    bool featureInBoundingBox(std::tuple<double, double> ll, std::tuple<double, double> ur);
    bool inCurve(double x, double y);
    std::tuple<double, double> nearestPt(double x, double y);
    int in(unsigned int ind)
    {
        if(ind >= inOrOut.size())
            return 0;
        else if(ind < 0)
            return 0;
        else
            return (inOrOut[ind]?1:-1);
    }
    std::vector<CurvePoint> corners()
    {
        return myCorners;
    };
    void write(std::string filename);

private:
    void fillDerivative(std::vector<CurvePoint> &CurvePoints);
    void setTangentAngle(std::vector<CurvePoint> &CurvePoints);
    void findCorners(std::vector<CurvePoint> &CurvePoints);
    void findFeatures(std::vector<CurvePoint> &CurvePoints);
    bool notACorner(CurvePoint &cp);
    bool checkDirectionAndFlip(std::vector<CurvePoint> &CurvePoints);
    double cross(CurvePoint &A, CurvePoint &B, CurvePoint &C);
    double area(std::vector<CurvePoint> &CurvePoints);
    std::vector<std::vector<CurvePoint> > myCurvePoints;
    std::vector<bool> inOrOut;
    std::vector<CurvePoint> myCorners;
    std::vector<CurvePoint> myFeatures; ///TODO MAKE FEATURES a vector of vector, eventually we will use analytical line segment in quad test
    std::tuple<double, double> ur, ll;
};

#endif
