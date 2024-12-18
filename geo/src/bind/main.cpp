#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <math.h>
#include "../dual/Curve.h"
#include "../dual/QuadTree.h"
#include "../dual/NodeList.h"
#include "../dual/Mesh.h"
#include <vector>

// pybind11 STL containers
// https: //pybind11.readthedocs.io/en/stable/advanced/cast/stl.html

// pybind11 casting between C++ and Python types
// https://pybind11.readthedocs.io/en/stable/advanced/cast/overview.html

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int a, int b)
{
    return a + b;
}

float raise_me(float base, float exponent)
{
    return pow(base, exponent);
}

struct Pet
{
    Pet(const std::string &name) : my_name(name) {}
    void setName(const std::string &name_)
    {
        my_name = name_;
    }
    const std::string &getName() const
    {
        return my_name;
    }

    std::string my_name;
};

struct Polygon
{
    /*
    Polygon(
        const std::vector<float> &boundary_x,
        const std::vector<float> &boundary_y)
        : Curve(boundary_x, boundary_y) {}
    */
    Polygon(
        const std::vector<float> &boundary_x,
        const std::vector<float> &boundary_y)
    {
        C = new Curve(boundary_x, boundary_y);
    }

    std::vector<bool> contains(
        const std::vector<float> &probe_x,
        const std::vector<float> &probe_y)
    {
        std::vector<bool> test(probe_x.size(), false);
        for (unsigned int i = 0; i < test.size(); ++i)
            test[i] = C->inCurve(probe_x[i], probe_y[i]);
        return test;
    }

    std::vector<int> inType(const std::vector<int> &probe)
    {
        std::vector<int> test(probe.size(), 0);
        for (unsigned int i = 0; i < test.size(); ++i)
            test[i] = C->in(probe[i]);
        return test;
    }

    Curve *C;
};

struct QT
{
    QT(
        const std::vector<float> &boundary_x,
        const std::vector<float> &boundary_y)
    {
        C = new Curve(boundary_x, boundary_y);
        C->lowerLeft(std::tuple<double, double>(-1, -1));
        C->upperRight(std::tuple<double, double>(1, 1));
        std::cout << "Constructor complete" << std::endl;
    }

    std::vector<int> nodeSize(const std::vector<float> &probe)
    {
        std::cout << "Testing sizes" << std::endl;
        std::vector<int> test(probe.size(), 0);

        for (unsigned int i = 0; i < test.size(); ++i)
        {
            std::cout << "Test resolution: " << probe[i] << std::endl;
            N = new NodeList();
            Q = new QuadTree(C, N, probe[i]);
            Q->subdivide(Q->head());
            Q->balancedRefineCurve(Q->head(), true);
            test[i] = N->size();
            delete Q;
            delete N;
        }
        return test;
    }

    Curve *C;
    QuadTree *Q;
    NodeList *N;
};

struct QuadMesh
{
    ///Provides the basic interface between the C++ engine and python
    QuadMesh()
    {
        featureRefine = false;
        developerOutput = false;
        resolution = 1;
        outputfile = "blank";
    }

    void initialize(
        const std::vector<float> &boundary_x,
        const std::vector<float> &boundary_y,
        bool boundaryRefine,
        double res,
        double lower_bound_x,
        double lower_bound_y,
        double upper_bound_x,
        double upper_bound_y,
        bool devout,
        std::string outfile)
    {
        C = new Curve(boundary_x, boundary_y);
        C->lowerLeft(std::tuple<double, double>(lower_bound_x, lower_bound_y));
        C->upperRight(std::tuple<double, double>(upper_bound_x, upper_bound_y));
        std::cout << "QuadMesh constructor complete" << std::endl;
        featureRefine = !boundaryRefine;
        developerOutput = devout;
        resolution = res;
        outputfile = outfile;
    }

    void compute()
    {
        std::cout << "Computing Mesh" << std::endl;

        N = new NodeList();

        try
        {
            Q = new QuadTree(C, N, resolution);
        }
        catch (std::runtime_error e)
        {
            std::cout << "Runtime error: " << e.what();
            return;
        }
        Q->subdivide(Q->head());
        Q->balancedRefineCurve(Q->head(), !featureRefine);
        Q->assignSplitCode(Q->head());
        if (developerOutput)
            Q->write(outputfile + "_01_quad_tree_");

        P = new Primal(Q);

        if (developerOutput)
            P->write(outputfile + "_02_primal_", "");

        try
        {
            D = new Dual(P);
        }
        catch (std::runtime_error e)
        {
            std::cout << "Runtime error: " << e.what();
            return;
        }
        if (developerOutput)
            D->write(outputfile + "_03_dual_", "");
        D->trim();

        if (developerOutput)
            D->write(outputfile + "_04_d_trim_", "");
        D->project();
        if (developerOutput)
            D->write(outputfile + "_05_dt_project_", "");
        D->snap();
        if (developerOutput)
            D->write(outputfile + "_06_dtp_snap_", "");
        D->subdivide();
        if (developerOutput)
            D->write(outputfile + "_07_dtps_subdivide_", "");
        D->project();
        if (developerOutput)
            D->write(outputfile + "_08_dtpss_project_", "");

        D->snap();
        if (developerOutput)
            D->write(outputfile + "_09_dtpssp_snap_", "");

        D->updateActiveNodes();
        D->write(outputfile, "inp");
        if (developerOutput)
            D->write(outputfile + "_10_mesh_", "");
    }

    std::vector<std::vector<float> > nodes()
    {
        return D->getNodes();
    }

    std::vector<std::vector<int> > connectivity()
    {
        return D->getConnectivity();
    }

    Curve *C;
    QuadTree *Q;
    NodeList *N;
    Primal *P;
    Dual *D;
    std::string outputfile;
    bool featureRefine;
    bool developerOutput;
    double resolution;
};

namespace py = pybind11;

// PYBIND11_MODULE(module_name, module_handle)
PYBIND11_MODULE(xybind, m)
{
    m.doc() = "xybind wraps C++ libaries for use in the SIBL Mesh Engine module"; // optional module docstring

    // m.def("cpp_function", &cppmult, "A function that multiplies two numbers.");

    // example with c++ function
    m.def("add", &add, "Add two integers.");

    // example with inline lambda c++ function
    m.def(
        "subtract", [](int a, int b)
        { return a - b; },
        "Subtract two integers.");

    // attributes
    m.attr("the_answer") = 42;
    m.attr("zero") = 0;
    py::object world = py::cast("World");
    m.attr("what") = world;

    // keyword only arguments
    m.def("exponent", &raise_me, py::kw_only(), py::arg("base"), py::arg("exponent"), "Returns base to a power.");

    // struct
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def_property("name", &Pet::getName, &Pet::setName);

    // py::class_<Parade>(m, "Parade")
    //     .def(py::init<const std::vector<float> &, const std::vector<float> &>())
    //     .def("contains", &Parade::contains, py::kw_only(), py::arg("probe_x"), py::kw_only(), py::arg("probe_y"), "Returns a vector with True or False for each element with coordinates probe_x, probe_y.");

    py::class_<Polygon>(m, "Polygon")
        .def(py::init<const std::vector<float> &, const std::vector<float> &>())
        .def("contains", &Polygon::contains, py::kw_only(), py::arg("probe_x"), py::arg("probe_y"), "Returns a vector with True or False for each element with coordinates probe_x, probe_y.")
        .def("inType", &Polygon::inType, py::kw_only(), py::arg("probe"), "Return 1 or -1 if curve at index probe is CCW(1) or CCW(-1) or 0 if out of bounds.");

    py::class_<QT>(m, "QT")
        .def(py::init<const std::vector<float> &, const std::vector<float> &>())
        .def("nodeSize", &QT::nodeSize, py::kw_only(), py::arg("probe"), "Returns a vector of ints with the node count as  a result of probe resolution.");

    py::class_<QuadMesh>(m, "QuadMesh")
        .def(py::init<>())
        .def("initialize", &QuadMesh::initialize, py::kw_only(),
             py::arg("boundary_xs"),
             py::arg("boundary_ys"),
             py::arg("boundary_refine"),
             py::arg("resolution"),
             py::arg("lower_bound_x"),
             py::arg("lower_bound_y"),
             py::arg("upper_bound_x"),
             py::arg("upper_bound_y"),
             py::arg("developer_output"),
             py::arg("output_file"), "Initializes the QuadMesh.")
        .def("compute", &QuadMesh::compute, "Calculates the quad/dual mesh at resolution.")
        .def("nodes", &QuadMesh::nodes, "Returns a matrix of nodes in columns [node number, x, y, z].")
        .def("connectivity", &QuadMesh::connectivity, "Returns a matrix of ints in columns [node number 1, node number 2, node number 3, node number 4].");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}

// The pybind11 module macro:
// Building pybind11 manually
// https://pybind11.readthedocs.io/en/stable/compiling.html#building-manually

/*
From: https://github.com/pybind/pybind11/blob/1376eb0e518ff2b7b412c84a907dd1cd3f7f2dcd/include/pybind11/detail/common.h#L267

    This macro creates the entry point that will be invoked when the Python interpreter
    imports an extension module. The module name is given as the fist argument and it
    should not be in quotes. The second macro argument defines a variable of type
    `py::module` which can be used to initialize the module.
*/
