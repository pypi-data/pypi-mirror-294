
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include "Eigen/Dense"

#include "polyscope/point_light.h"
#include "polyscope/polyscope.h"

#include "utils.h"

namespace py = pybind11;
namespace ps = polyscope;

// For overloaded functions, with C++11 compiler only
template <typename... Args>
using overload_cast_ = pybind11::detail::overload_cast_impl<Args...>;

// clang-format off
void bind_point_light(py::module& m) {

  bindLight<ps::PointLight>(m, "PointLight");

  // Static adders and getters
  m.def("register_point_light", &ps::registerPointLight,
      py::arg("name"), py::arg("position"), py::arg("color"), "Register a point light",
      py::return_value_policy::reference);
}
// clang-format on

