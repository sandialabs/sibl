#include <cinolib/meshes/drawable_trimesh.h>
#include <cinolib/gl/glcanvas.h>

int main()
{
    using namespace cinolib;
    DrawableTrimesh<> m("bunny.obj");
    GLcanvas gui;
    gui.push(&m);
    return gui.launch();
}