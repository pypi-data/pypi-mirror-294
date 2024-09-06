/* Copyright (c) 2024 Otto Link. Distributed under the terms of the GNU General
 * Public License. The full license is in the file LICENSE, distributed with
 * this software. */
#define PYBIND11_DETAILED_ERROR_MESSAGES
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "highmap.hpp"

#include "helpers.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pyhighmap, m)
{
  py::enum_<hmap::DistanceFunction>(m, "DistanceFunction")
      .value("CHEBYSHEV", hmap::DistanceFunction::CHEBYSHEV)
      .value("EUCLIDIAN", hmap::DistanceFunction::EUCLIDIAN)
      .value("EUCLISHEV", hmap::DistanceFunction::EUCLISHEV)
      .value("MANHATTAN", hmap::DistanceFunction::MANHATTAN)
      .export_values();

  py::enum_<hmap::NoiseType>(m, "NoiseType")
      .value("PARBERRY", hmap::NoiseType::PARBERRY)
      .value("PERLIN", hmap::NoiseType::PERLIN)
      .value("PERLIN_BILLOW", hmap::NoiseType::PERLIN_BILLOW)
      .value("PERLIN_HALF", hmap::NoiseType::PERLIN_HALF)
      .value("SIMPLEX2", hmap::NoiseType::SIMPLEX2)
      .value("SIMPLEX2S", hmap::NoiseType::SIMPLEX2S)
      .value("VALUE", hmap::NoiseType::VALUE)
      .value("VALUE_CUBIC", hmap::NoiseType::VALUE_CUBIC)
      // .value("VALUE_DELAUNAY", hmap::NoiseType::VALUE_DELAUNAY)
      // .value("VALUE_LINEAR", hmap::NoiseType::VALUE_LINEAR)
      .value("WORLEY", hmap::NoiseType::WORLEY)
      .value("WORLEY_DOUBLE", hmap::NoiseType::WORLEY_DOUBLE)
      .value("WORLEY_VALUE", hmap::NoiseType::WORLEY_VALUE)
      .export_values();

  m.def("biquad_pulse",
        [](py::object shape_obj, float gain)
        {
          hmap::Array array = hmap::biquad_pulse(pyobj_to_vec2<int>(shape_obj),
                                                 gain);
          return array_to_numpy(array);
        });

  m.def(
      "clamp",
      [](py::object array_obj, float vmin, float vmax)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        hmap::clamp(array, vmin, vmax);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("vmin") = 0.f,
      py::arg("vmax") = 1.f);

  m.def(
      "falloff",
      [](py::object array_obj, float strength, hmap::DistanceFunction dist_fct)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        hmap::falloff(array, strength, dist_fct);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("strength") = 1.f,
      py::arg("dist_fct") = hmap::DistanceFunction::EUCLIDIAN);

  m.def(
      "hillshade",
      [](py::object array_obj, float azimuth, float zenith, float talus_ref)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        array = hmap::hillshade(array, azimuth, zenith, talus_ref);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("azimuth"),
      py::arg("zenith"),
      py::arg("talus_ref") = 1.f);

  m.def(
      "hydraulic_particle",
      [](py::object z_obj,
         int        nparticles,
         int        seed,
         float      c_capacity,
         float      c_erosion,
         float      c_deposition,
         float      drag_rate,
         float      evap_rate)
      {
        hmap::Array z = pyobj_to_array(z_obj);
        hmap::Array z_normalized = z;
        hmap::remap(z_normalized);

        hmap::hydraulic_particle(z,
                                 nullptr,
                                 nparticles,
                                 seed,
                                 nullptr,
                                 &z_normalized, // moisture map
                                 nullptr,
                                 nullptr,
                                 0,
                                 c_capacity,
                                 c_erosion,
                                 c_deposition,
                                 drag_rate,
                                 evap_rate);
        return array_to_numpy(z);
      },
      py::arg("z"),
      py::arg("nparticles"),
      py::arg("seed"),
      py::arg("c_capacity") = 10.f,
      py::arg("c_erosion") = 0.05f,
      py::arg("c_deposition") = 0.01f,
      py::arg("drag_rate") = 0.01f,
      py::arg("evap_rate") = 0.001f);

  m.def(
      "hydraulic_stream",
      [](py::object z_obj,
         float      c_erosion,
         float      talus_ref,
         int        ir,
         float      clipping_ratio)
      {
        hmap::Array z = pyobj_to_array(z_obj);
        hmap::Array z_normalized = z;
        hmap::remap(z_normalized);

        hmap::hydraulic_stream(z,
                               &z_normalized, // mask
                               c_erosion,
                               talus_ref,
                               nullptr,
                               nullptr,
                               nullptr,
                               ir,
                               clipping_ratio);
        return array_to_numpy(z);
      },
      py::arg("z"),
      py::arg("c_erosion"),
      py::arg("talus_ref"),
      py::arg("ir") = 1,
      py::arg("clipping_ratio") = 10.f);

  m.def("noise",
        [](hmap::NoiseType noise_type,
           py::object      shape_obj,
           py::object      kw_obj,
           uint            seed)
        {
          hmap::Array array = hmap::noise(noise_type,
                                          pyobj_to_vec2<int>(shape_obj),
                                          pyobj_to_vec2<float>(kw_obj),
                                          seed);
          return array_to_numpy(array);
        });

  m.def(
      "noise_fbm",
      [](hmap::NoiseType noise_type,
         py::object      shape_obj,
         py::object      kw_obj,
         uint            seed,
         int             octaves,
         float           weight,
         float           persistence,
         float           lacunarity)
      {
        hmap::Array array = hmap::noise_fbm(noise_type,
                                            pyobj_to_vec2<int>(shape_obj),
                                            pyobj_to_vec2<float>(kw_obj),
                                            seed,
                                            octaves,
                                            weight,
                                            persistence,
                                            lacunarity);
        return array_to_numpy(array);
      },
      py::arg("noise_type"),
      py::arg("shape_obj"),
      py::arg("kw_obj"),
      py::arg("seed"),
      py::arg("octaves") = 8,
      py::arg("weight") = 0.7f,
      py::arg("persistence") = 0.5f,
      py::arg("lacunarity") = 2.f);

  m.def(
      "noise_pingpong",
      [](hmap::NoiseType noise_type,
         py::object      shape_obj,
         py::object      kw_obj,
         uint            seed,
         int             octaves,
         float           weight,
         float           persistence,
         float           lacunarity)
      {
        hmap::Array array = hmap::noise_pingpong(noise_type,
                                                 pyobj_to_vec2<int>(shape_obj),
                                                 pyobj_to_vec2<float>(kw_obj),
                                                 seed,
                                                 octaves,
                                                 weight,
                                                 persistence,
                                                 lacunarity);
        return array_to_numpy(array);
      },
      py::arg("noise_type"),
      py::arg("shape_obj"),
      py::arg("kw_obj"),
      py::arg("seed"),
      py::arg("octaves") = 8,
      py::arg("weight") = 0.7f,
      py::arg("persistence") = 0.5f,
      py::arg("lacunarity") = 2.f);

  m.def(
      "noise_ridged",
      [](hmap::NoiseType noise_type,
         py::object      shape_obj,
         py::object      kw_obj,
         uint            seed,
         int             octaves,
         float           weight,
         float           persistence,
         float           lacunarity,
         float           k_smoothing)
      {
        hmap::Array array = hmap::noise_ridged(noise_type,
                                               pyobj_to_vec2<int>(shape_obj),
                                               pyobj_to_vec2<float>(kw_obj),
                                               seed,
                                               octaves,
                                               weight,
                                               persistence,
                                               lacunarity,
                                               k_smoothing);
        return array_to_numpy(array);
      },
      py::arg("noise_type"),
      py::arg("shape_obj"),
      py::arg("kw_obj"),
      py::arg("seed"),
      py::arg("octaves") = 8,
      py::arg("weight") = 0.7f,
      py::arg("persistence") = 0.5f,
      py::arg("lacunarity") = 2.f,
      py::arg("k_smoothing") = 0.1f);

  m.def(
      "plateau",
      [](py::object array_obj, int ir, float factor)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        plateau(array, ir, factor);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("ir"),
      py::arg("factor"));

  m.def(
      "remap",
      [](py::object array_obj, float vmin, float vmax)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        hmap::remap(array, vmin, vmax);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("vmin") = 0.f,
      py::arg("vmax") = 1.f);

  m.def(
      "smooth_fill",
      [](py::object array_obj, int ir, float k)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        hmap::smooth_fill(array, ir, k, nullptr);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("ir"),
      py::arg("k") = 0.1f);

  m.def(
      "smoothstep3",
      [](py::object array_obj, float vmin, float vmax)
      {
        hmap::Array array = pyobj_to_array(array_obj);
        hmap::smoothstep3(array, vmin, vmax);
        return array_to_numpy(array);
      },
      py::arg("array"),
      py::arg("vmin") = 0.f,
      py::arg("vmax") = 1.f);

  m.def("warp",
        [](py::object array_obj, py::object dx_obj, py::object dy_obj)
        {
          hmap::Array array = pyobj_to_array(array_obj);
          hmap::Array dx = pyobj_to_array(dx_obj);
          hmap::Array dy = pyobj_to_array(dy_obj);
          hmap::warp(array, &dx, &dy);
          return array_to_numpy(array);
        });
}
