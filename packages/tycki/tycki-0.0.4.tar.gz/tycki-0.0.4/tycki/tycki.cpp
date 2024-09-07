/*################################################################################
  ##
  ##   Copyright (C) 2011-2023 Keith O'Hara
  ##
  ##   This file is part of the MCMC C++ library.
  ##
  ##   Licensed under the Apache License, Version 2.0 (the "License");
  ##   you may not use this file except in compliance with the License.
  ##   You may obtain a copy of the License at
  ##
  ##       http://www.apache.org/licenses/LICENSE-2.0
  ##
  ##   Unless required by applicable law or agreed to in writing, software
  ##   distributed under the License is distributed on an "AS IS" BASIS,
  ##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ##   See the License for the specific language governing permissions and
  ##   limitations under the License.
  ##
  ################################################################################*/
 
/*
 * Sampling from a Gaussian distribution using sampler_t
 */

// $CXX -Wall -std=c++14 -O3 -mcpu=native -ffp-contract=fast -I$EIGEN_INCLUDE_PATH -I./../../include/ rwmh_normal_mean.cpp -o rwmh_normal_mean.out -L./../.. -lmcmc

#define MCMC_ENABLE_EIGEN_WRAPPERS
#include "mcmc.hpp"

#include <optional>
#include <sstream>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

namespace py = pybind11;

struct rng_t {
    size_t seed;
    mcmc::rand_engine_t rand_engine;

    rng_t(size_t seed) {
        this->rand_engine = mcmc::rand_engine_t(seed);
    }
};

struct rwmh_t {
    mcmc::algo_settings_t settings;
    std::optional<Eigen::VectorXd> current_val;
};

struct mala_t {
    mcmc::algo_settings_t settings;
    std::optional<Eigen::VectorXd> current_val;
};

struct hmc_t {
    mcmc::algo_settings_t settings;
    std::optional<Eigen::VectorXd> current_val;
};

struct nuts_t {
    mcmc::algo_settings_t settings;
    std::optional<Eigen::VectorXd> current_val;
};

//template<typename settings_t>
Eigen::MatrixXd sample_nuts(
        nuts_t& sampler, 
        std::function<double (const Eigen::VectorXd& vals_inp)> log_density,
        std::function<Eigen::VectorXd (const Eigen::VectorXd& vals_inp)> grad_log_density,
        std::optional<Eigen::VectorXd> initial_val,
        std::optional<size_t> n_samples,
        std::optional<size_t> n_burnin,
        std::optional<size_t> n_adapt
        ) {
    Eigen::MatrixXd draws_out;

    if (!initial_val and !sampler.current_val) throw std::invalid_argument("No starting point supplied.");
    auto _initial_val = ( initial_val ? *initial_val : *sampler.current_val );

    if (n_samples) sampler.settings.nuts_settings.n_keep_draws = *n_samples;
    if (n_burnin) sampler.settings.nuts_settings.n_burnin_draws = *n_burnin;
    if (n_adapt) sampler.settings.nuts_settings.n_adapt_draws = *n_adapt;

    mcmc::nuts(_initial_val, [&](auto x, auto* grad, auto d) { 
                if(grad) 
                    *grad = grad_log_density(x); 
                return log_density(x); 
            }, draws_out, nullptr, sampler.settings);

    sampler.current_val = draws_out.row(draws_out.rows() - 1);

    return draws_out;
}

Eigen::MatrixXd sample_mala(
        mala_t& sampler, 
        std::function<double (const Eigen::VectorXd& vals_inp)> log_density,
        std::function<Eigen::VectorXd (const Eigen::VectorXd& vals_inp)> grad_log_density,
        std::optional<Eigen::VectorXd> initial_val,
        std::optional<size_t> n_samples,
        std::optional<size_t> n_burnin
        ) {
    Eigen::MatrixXd draws_out;

    if (!initial_val and !sampler.current_val) throw std::invalid_argument("No starting point supplied.");
    auto _initial_val = ( initial_val ? *initial_val : *sampler.current_val );

    if (n_samples) sampler.settings.mala_settings.n_keep_draws = *n_samples;
    if (n_burnin) sampler.settings.mala_settings.n_burnin_draws = *n_burnin;

    mcmc::mala(_initial_val, [&](auto x, auto* grad, auto d) { 
                if(grad) 
                    *grad = grad_log_density(x); 
                return log_density(x); 
            }, draws_out, nullptr, sampler.settings);

    sampler.current_val = draws_out.row(draws_out.rows() - 1);

    return draws_out;
}

Eigen::MatrixXd sample_hmc(
        hmc_t& sampler, 
        std::function<double (const Eigen::VectorXd& vals_inp)> log_density,
        std::function<Eigen::VectorXd (const Eigen::VectorXd& vals_inp)> grad_log_density,
        std::optional<Eigen::VectorXd> initial_val,
        std::optional<size_t> n_samples,
        std::optional<size_t> n_burnin
        ) {
    Eigen::MatrixXd draws_out;

    if (!initial_val and !sampler.current_val) throw std::invalid_argument("No starting point supplied.");
    auto _initial_val = ( initial_val ? *initial_val : *sampler.current_val );

    if (n_samples) sampler.settings.hmc_settings.n_keep_draws = *n_samples;
    if (n_burnin) sampler.settings.hmc_settings.n_burnin_draws = *n_burnin;

    mcmc::hmc(_initial_val, [&](auto x, auto* grad, auto d) { 
                if(grad) 
                    *grad = grad_log_density(x); 
                return log_density(x); 
            }, draws_out, nullptr, sampler.settings);

    sampler.current_val = draws_out.row(draws_out.rows() - 1);

    return draws_out;
}

Eigen::MatrixXd sample_rwmh(
        rwmh_t& sampler, 
        std::function<double (const Eigen::VectorXd& vals_inp)> log_density,
        std::optional<std::function<Eigen::VectorXd (const Eigen::VectorXd& vals_inp)>> grad_log_density,
        std::optional<Eigen::VectorXd> initial_val,
        std::optional<size_t> n_samples,
        std::optional<size_t> n_burnin
        ) {
    Eigen::MatrixXd draws_out;

    if (!initial_val and !sampler.current_val) throw std::invalid_argument("No starting point supplied.");
    auto _initial_val = ( initial_val ? *initial_val : *sampler.current_val );

    if (n_samples) sampler.settings.rwmh_settings.n_keep_draws = *n_samples;
    if (n_burnin) sampler.settings.rwmh_settings.n_burnin_draws = *n_burnin;

    mcmc::rwmh(_initial_val, [&](auto x, auto d) { return log_density(x); }, draws_out, nullptr, sampler.settings);

    sampler.current_val = draws_out.row(draws_out.rows() - 1);

    return draws_out;
}

PYBIND11_MODULE(tycki, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

	py::class_<rwmh_t>(m, "RWMH")
        .def(py::init([] (
                        std::optional<Eigen::VectorXd> initial_val,
                        size_t n_burnin_draws, 
                        size_t n_keep_draws, 
                        size_t seed, 
                        double par_scale, 
                        std::optional<Eigen::MatrixXd> cov_mat) { 
                    rwmh_t* rwmh = new rwmh_t();
                    rwmh->current_val = initial_val;

                    rwmh->settings.rng_seed_value = seed;
                    rwmh->settings.rand_engine = mcmc::rand_engine_t(seed);

                    rwmh->settings.rwmh_settings.n_burnin_draws = n_burnin_draws;
                    rwmh->settings.rwmh_settings.n_keep_draws = n_keep_draws;
                    rwmh->settings.rwmh_settings.omp_n_threads = 1;
                    rwmh->settings.rwmh_settings.par_scale = par_scale;

                    if (cov_mat)
                        rwmh->settings.rwmh_settings.cov_mat = *cov_mat;

                    return rwmh;
                }),
                py::arg("x0") = std::optional<Eigen::VectorXd>(),
                py::arg("n_burnin") = 0,
                py::arg("n_samples") = int(1E03),
                py::arg("seed") = 42,
                py::arg("scale") = 1.0,
                py::arg("cov") = std::optional<Eigen::MatrixXd>()
            )
        .def_property("x0", 
                [](const rwmh_t& rwmh){ return rwmh.current_val; }, 
                [](rwmh_t& rwmh, Eigen::VectorXd x0){ rwmh.current_val = x0; }
            )
        .def_property("n_burnin", 
                [](const rwmh_t& rwmh){ return rwmh.settings.rwmh_settings.n_burnin_draws; }, 
                [](rwmh_t& rwmh, int n){ rwmh.settings.rwmh_settings.n_burnin_draws = n; }
            )
        .def_property("n_samples", 
                [](const rwmh_t& rwmh){ return rwmh.settings.rwmh_settings.n_keep_draws; }, 
                [](rwmh_t& rwmh, int n){ rwmh.settings.rwmh_settings.n_keep_draws = n; }
            )
        .def_property("scale", 
                [](const rwmh_t& rwmh){ return rwmh.settings.rwmh_settings.par_scale; }, 
                [](rwmh_t& rwmh, double scale){ rwmh.settings.rwmh_settings.par_scale = scale; }
            )
        .def_property("cov", 
                [](const rwmh_t& rwmh){ return rwmh.settings.rwmh_settings.cov_mat; }, 
                [](rwmh_t& rwmh, const Eigen::MatrixXd& cov){ rwmh.settings.rwmh_settings.cov_mat = cov; }
            )
        .def_property("n_accept", 
                [](const rwmh_t& rwmh){ return rwmh.settings.rwmh_settings.n_accept_draws; }, 
                nullptr
            )
        .def_property("seed", 
                [](const rwmh_t& rwmh){ return rwmh.settings.rng_seed_value; }, 
                [](rwmh_t& rwmh, size_t seed){ 
                    rwmh.settings.rng_seed_value = seed; 
                    rwmh.settings.rand_engine = mcmc::rand_engine_t(seed); 
                }
            )
        .def("sample", sample_rwmh, 
                py::arg("log_density"), 
                py::arg("grad_log_density") = std::optional<std::function<Eigen::VectorXd (const Eigen::VectorXd& vals_inp)>>(),
                py::arg("x0") = std::optional<Eigen::VectorXd>(), 
                py::arg("n_samples") = std::optional<size_t>(), 
                py::arg("n_burnin") = std::optional<size_t>()
            )
		.def(py::pickle(
			[](const rwmh_t &rwmh) { // __getstate__
				std::stringstream str;
                str << rwmh.settings.rand_engine;

				return py::make_tuple(
                        str.str(), 
                        rwmh.settings.rng_seed_value,
                        rwmh.current_val,
                        rwmh.settings.rwmh_settings.n_burnin_draws,
                        rwmh.settings.rwmh_settings.n_keep_draws,
                        rwmh.settings.rwmh_settings.par_scale,
                        rwmh.settings.rwmh_settings.cov_mat,
                        rwmh.settings.rwmh_settings.n_accept_draws
                    );
			},
			[](py::tuple t) { // __setstate__
                rwmh_t* rwmh = new rwmh_t();

                std::stringstream ss(t[0].cast<std::string>());
                ss >> rwmh->settings.rand_engine;
                rwmh->settings.rng_seed_value = t[1].cast<size_t>();

                rwmh->current_val = t[2].cast<Eigen::VectorXd>();

                rwmh->settings.rwmh_settings.n_burnin_draws = t[3].cast<size_t>();
                rwmh->settings.rwmh_settings.n_keep_draws = t[4].cast<size_t>();

                rwmh->settings.rwmh_settings.omp_n_threads = 1;

                rwmh->settings.rwmh_settings.par_scale = t[5].cast<double>();
                rwmh->settings.rwmh_settings.cov_mat = t[6].cast<Eigen::MatrixXd>();

                rwmh->settings.rwmh_settings.n_accept_draws = t[7].cast<size_t>();

				return rwmh;
			})
		)
    ;

	py::class_<mala_t>(m, "MALA")
        .def(py::init([] (
                        std::optional<Eigen::VectorXd> initial_val,
                        size_t n_burnin_draws, 
                        size_t n_keep_draws, 
                        size_t seed, 
                        double par_scale, 
                        std::optional<Eigen::MatrixXd> cov_mat) { 
                    mala_t* mala = new mala_t();
                    mala->current_val = initial_val;

                    mala->settings.rng_seed_value = seed;
                    mala->settings.rand_engine = mcmc::rand_engine_t(seed);

                    mala->settings.mala_settings.n_burnin_draws = n_burnin_draws;
                    mala->settings.mala_settings.n_keep_draws = n_keep_draws;
                    mala->settings.mala_settings.omp_n_threads = 1;
                    mala->settings.mala_settings.step_size = par_scale;

                    if (cov_mat)
                        mala->settings.mala_settings.precond_mat = *cov_mat;

                    return mala;
                }),
                py::arg("x0") = std::optional<Eigen::VectorXd>(),
                py::arg("n_burnin") = 0,
                py::arg("n_samples") = int(1E03),
                py::arg("seed") = 42,
                py::arg("scale") = 1.0,
                py::arg("precond") = std::optional<Eigen::MatrixXd>()
            )
        .def_property("x0", 
                [](const mala_t& mala){ return mala.current_val; }, 
                [](mala_t& mala, Eigen::VectorXd x0){ mala.current_val = x0; }
            )
        .def_property("n_burnin", 
                [](const mala_t& mala){ return mala.settings.mala_settings.n_burnin_draws; }, 
                [](mala_t& mala, int n){ mala.settings.mala_settings.n_burnin_draws = n; }
            )
        .def_property("n_samples", 
                [](const mala_t& mala){ return mala.settings.mala_settings.n_keep_draws; }, 
                [](mala_t& mala, int n){ mala.settings.mala_settings.n_keep_draws = n; }
            )
        .def_property("n_threads", 
                [](const mala_t& mala){ return mala.settings.mala_settings.omp_n_threads; }, 
                [](mala_t& mala, int n){ mala.settings.mala_settings.omp_n_threads = n; }
            )
        .def_property("scale", 
                [](const mala_t& mala){ return mala.settings.mala_settings.step_size; }, 
                [](mala_t& mala, double scale){ mala.settings.mala_settings.step_size = scale; }
            )
        .def_property("precond", 
                [](const mala_t& mala){ return mala.settings.mala_settings.precond_mat; }, 
                [](mala_t& mala, const Eigen::MatrixXd& cov){ mala.settings.mala_settings.precond_mat = cov; }
            )
        .def_property("n_accept", 
                [](const mala_t& mala){ return mala.settings.mala_settings.n_accept_draws; }, 
                nullptr
            )
        .def_property("seed", 
                [](const mala_t& mala){ return mala.settings.rng_seed_value; }, 
                [](mala_t& mala, size_t seed){ 
                    mala.settings.rng_seed_value = seed; 
                    mala.settings.rand_engine = mcmc::rand_engine_t(seed); 
                }
            )
        .def("sample", sample_mala, 
                py::arg("log_density"), 
                py::arg("grad_log_density"), 
                py::arg("x0") = std::optional<Eigen::VectorXd>(), 
                py::arg("n_samples") = std::optional<size_t>(), 
                py::arg("n_burnin") = std::optional<size_t>()
            )
		.def(py::pickle(
			[](const mala_t &mala) { // __getstate__
				std::stringstream str;
                str << mala.settings.rand_engine;

				return py::make_tuple(
                        str.str(), 
                        mala.settings.rng_seed_value,
                        mala.current_val,
                        mala.settings.mala_settings.n_burnin_draws,
                        mala.settings.mala_settings.n_keep_draws,
                        mala.settings.mala_settings.step_size,
                        mala.settings.mala_settings.precond_mat,
                        mala.settings.mala_settings.n_accept_draws
                    );
			},
			[](py::tuple t) { // __setstate__
                mala_t* mala = new mala_t();

                std::stringstream ss(t[0].cast<std::string>());
                ss >> mala->settings.rand_engine;
                mala->settings.rng_seed_value = t[1].cast<size_t>();

                mala->current_val = t[2].cast<Eigen::VectorXd>();

                mala->settings.mala_settings.n_burnin_draws = t[3].cast<size_t>();
                mala->settings.mala_settings.n_keep_draws = t[4].cast<size_t>();

                mala->settings.mala_settings.omp_n_threads = 1;

                mala->settings.mala_settings.step_size = t[5].cast<double>();
                mala->settings.mala_settings.precond_mat = t[6].cast<Eigen::MatrixXd>();

                mala->settings.mala_settings.n_accept_draws = t[7].cast<size_t>();

				return mala;
			})
		)
    ;

	py::class_<hmc_t>(m, "HMC")
        .def(py::init([] (
                        std::optional<Eigen::VectorXd> initial_val,
                        size_t n_burnin_draws, 
                        size_t n_keep_draws, 
                        size_t seed, 
                        size_t n_steps, 
                        double par_scale, 
                        std::optional<Eigen::MatrixXd> cov_mat) { 
                    hmc_t* hmc = new hmc_t();
                    hmc->current_val = initial_val;

                    hmc->settings.rng_seed_value = seed;
                    hmc->settings.rand_engine = mcmc::rand_engine_t(seed);

                    hmc->settings.hmc_settings.n_burnin_draws = n_burnin_draws;
                    hmc->settings.hmc_settings.n_keep_draws = n_keep_draws;
                    hmc->settings.hmc_settings.omp_n_threads = 1;
                    hmc->settings.hmc_settings.n_leap_steps = n_steps;
                    hmc->settings.hmc_settings.step_size = par_scale;

                    if (cov_mat)
                        hmc->settings.hmc_settings.precond_mat = *cov_mat;

                    return hmc;
                }),
                py::arg("x0") = std::optional<Eigen::VectorXd>(),
                py::arg("n_burnin") = 0,
                py::arg("n_samples") = int(1E03),
                py::arg("seed") = 42,
                py::arg("n_leap") = 32,
                py::arg("scale") = 1.0,
                py::arg("precond") = std::optional<Eigen::MatrixXd>()
            )
        .def_property("x0", 
                [](const hmc_t& hmc){ return hmc.current_val; }, 
                [](hmc_t& hmc, Eigen::VectorXd x0){ hmc.current_val = x0; }
            )
        .def_property("n_burnin", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.n_burnin_draws; }, 
                [](hmc_t& hmc, int n){ hmc.settings.hmc_settings.n_burnin_draws = n; }
            )
        .def_property("n_samples", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.n_keep_draws; }, 
                [](hmc_t& hmc, int n){ hmc.settings.hmc_settings.n_keep_draws = n; }
            )
        .def_property("n_threads", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.omp_n_threads; }, 
                [](hmc_t& hmc, int n){ hmc.settings.hmc_settings.omp_n_threads = n; }
            )
        .def_property("scale", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.step_size; }, 
                [](hmc_t& hmc, double scale){ hmc.settings.hmc_settings.step_size = scale; }
            )
        .def_property("n_leap", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.n_leap_steps; }, 
                [](hmc_t& hmc, int n_steps){ hmc.settings.hmc_settings.n_leap_steps = n_steps; }
            )
        .def_property("precond", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.precond_mat; }, 
                [](hmc_t& hmc, const Eigen::MatrixXd& cov){ hmc.settings.hmc_settings.precond_mat = cov; }
            )
        .def_property("n_accept", 
                [](const hmc_t& hmc){ return hmc.settings.hmc_settings.n_accept_draws; }, 
                nullptr
            )
        .def_property("seed", 
                [](const hmc_t& hmc){ return hmc.settings.rng_seed_value; }, 
                [](hmc_t& hmc, size_t seed){ 
                    hmc.settings.rng_seed_value = seed; 
                    hmc.settings.rand_engine = mcmc::rand_engine_t(seed); 
                }
            )
        .def("sample", sample_hmc, 
                py::arg("log_density"), 
                py::arg("grad_log_density"), 
                py::arg("x0") = std::optional<Eigen::VectorXd>(), 
                py::arg("n_samples") = std::optional<size_t>(), 
                py::arg("n_burnin") = std::optional<size_t>()
            )
		.def(py::pickle(
			[](const hmc_t &hmc) { // __getstate__
				std::stringstream str;
                str << hmc.settings.rand_engine;

				return py::make_tuple(
                        str.str(), 
                        hmc.settings.rng_seed_value,
                        hmc.current_val,
                        hmc.settings.hmc_settings.n_burnin_draws,
                        hmc.settings.hmc_settings.n_keep_draws,
                        hmc.settings.hmc_settings.n_leap_steps,
                        hmc.settings.hmc_settings.step_size,
                        hmc.settings.hmc_settings.precond_mat,
                        hmc.settings.hmc_settings.n_accept_draws
                    );
			},
			[](py::tuple t) { // __setstate__
                hmc_t* hmc = new hmc_t();

                std::stringstream ss(t[0].cast<std::string>());
                ss >> hmc->settings.rand_engine;
                hmc->settings.rng_seed_value = t[1].cast<size_t>();

                hmc->current_val = t[2].cast<Eigen::VectorXd>();

                hmc->settings.hmc_settings.n_burnin_draws = t[3].cast<size_t>();
                hmc->settings.hmc_settings.n_keep_draws = t[4].cast<size_t>();

                hmc->settings.hmc_settings.omp_n_threads = 1;

                hmc->settings.hmc_settings.n_leap_steps = t[5].cast<size_t>();
                hmc->settings.hmc_settings.step_size = t[6].cast<double>();
                hmc->settings.hmc_settings.precond_mat = t[7].cast<Eigen::MatrixXd>();

                hmc->settings.hmc_settings.n_accept_draws = t[8].cast<size_t>();

				return hmc;
			})
		)
    ;

	py::class_<nuts_t>(m, "NUTS")
        .def(py::init([] (
                        std::optional<Eigen::VectorXd> initial_val,
                        size_t n_burnin_draws, 
                        size_t n_keep_draws, 
                        size_t n_adapt_draws, 
                        size_t seed, 
                        double target_accept, 
                        size_t max_tree_depth,
                        double gamma, 
                        size_t t0,
                        double kappa, 
                        double par_scale, 
                        std::optional<Eigen::MatrixXd> cov_mat) { 
                    nuts_t* nuts = new nuts_t();
                    nuts->current_val = initial_val;

                    nuts->settings.rng_seed_value = seed;
                    nuts->settings.rand_engine = mcmc::rand_engine_t(seed);

                    nuts->settings.nuts_settings.n_burnin_draws = n_burnin_draws;
                    nuts->settings.nuts_settings.n_keep_draws = n_keep_draws;
                    nuts->settings.nuts_settings.n_adapt_draws = n_adapt_draws;
                    nuts->settings.nuts_settings.omp_n_threads = 1;
                    nuts->settings.nuts_settings.step_size = par_scale;
                    nuts->settings.nuts_settings.target_accept_rate = target_accept; 
                    nuts->settings.nuts_settings.max_tree_depth = max_tree_depth;
                    nuts->settings.nuts_settings.gamma_val = gamma; 
                    nuts->settings.nuts_settings.t0_val = t0;
                    nuts->settings.nuts_settings.kappa_val = kappa;

                    if (cov_mat)
                        nuts->settings.nuts_settings.precond_mat = *cov_mat;

                    return nuts;
                }),
                py::arg("x0") = std::optional<Eigen::VectorXd>(),
                py::arg("n_burnin") = int(5E02),
                py::arg("n_samples") = int(1E03),
                py::arg("n_adapt") = int(5E02),
                py::arg("seed") = 42,
                py::arg("target_accept") = 0.55,
                py::arg("max_tree_depth") = 10,
                py::arg("gamma") = 0.05, 
                py::arg("t0") = 10,
                py::arg("kappa") = 0.75,
                py::arg("scale") = 1.0,
                py::arg("precond") = std::optional<Eigen::MatrixXd>()
            )
        .def_property("x0", 
                [](const nuts_t& nuts){ return nuts.current_val; }, 
                [](nuts_t& nuts, Eigen::VectorXd x0){ nuts.current_val = x0; }
            )
        .def_property("n_burnin", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.n_burnin_draws; }, 
                [](nuts_t& nuts, int n){ nuts.settings.nuts_settings.n_burnin_draws = n; }
            )
        .def_property("n_samples", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.n_keep_draws; }, 
                [](nuts_t& nuts, int n){ nuts.settings.nuts_settings.n_keep_draws = n; }
            )
        .def_property("n_adapt", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.n_adapt_draws; }, 
                [](nuts_t& nuts, int n){ nuts.settings.nuts_settings.n_keep_draws = n; }
            )
        .def_property("n_threads", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.omp_n_threads; }, 
                [](nuts_t& nuts, int n){ nuts.settings.nuts_settings.omp_n_threads = n; }
            )
        .def_property("scale", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.step_size; }, 
                [](nuts_t& nuts, double scale){ nuts.settings.nuts_settings.step_size = scale; }
            )
        .def_property("precond", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.precond_mat; }, 
                [](nuts_t& nuts, const Eigen::MatrixXd& cov){ nuts.settings.nuts_settings.precond_mat = cov; }
            )
        .def_property("target_accept", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.target_accept_rate; }, 
                [](nuts_t& nuts, double target_accept){ nuts.settings.nuts_settings.target_accept_rate = target_accept; }
            )
        .def_property("max_tree_depth", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.max_tree_depth; }, 
                [](nuts_t& nuts, size_t max_tree_depth){ nuts.settings.nuts_settings.max_tree_depth = max_tree_depth; }
            )
        .def_property("gamma", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.gamma_val; }, 
                [](nuts_t& nuts, double gamma){ nuts.settings.nuts_settings.gamma_val = gamma; }
            )
        .def_property("t0", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.t0_val; }, 
                [](nuts_t& nuts, double t0){ nuts.settings.nuts_settings.t0_val = t0; }
            )
        .def_property("kappa", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.kappa_val; }, 
                [](nuts_t& nuts, double kappa){ nuts.settings.nuts_settings.kappa_val = kappa; }
            )
        .def_property("n_accept", 
                [](const nuts_t& nuts){ return nuts.settings.nuts_settings.n_accept_draws; }, 
                nullptr
            )
        .def_property("seed", 
                [](const nuts_t& nuts){ return nuts.settings.rng_seed_value; }, 
                [](nuts_t& nuts, size_t seed){ 
                    nuts.settings.rng_seed_value = seed; 
                    nuts.settings.rand_engine = mcmc::rand_engine_t(seed); 
                }
            )
        .def("sample", sample_nuts, 
                py::arg("log_density"), 
                py::arg("grad_log_density"), 
                py::arg("x0") = std::optional<Eigen::VectorXd>(), 
                py::arg("n_samples") = std::optional<size_t>(), 
                py::arg("n_burnin") = std::optional<size_t>(),
                py::arg("n_adapt") = std::optional<size_t>()
            )
		.def(py::pickle(
			[](const nuts_t &nuts) { // __getstate__
				std::stringstream str;
                str << nuts.settings.rand_engine;

				return py::make_tuple(
                        str.str(), 
                        nuts.settings.rng_seed_value,

                        nuts.current_val,

                        nuts.settings.nuts_settings.n_burnin_draws,
                        nuts.settings.nuts_settings.n_keep_draws,

                        nuts.settings.nuts_settings.n_adapt_draws,
                        nuts.settings.nuts_settings.target_accept_rate,

                        nuts.settings.nuts_settings.step_size,
                        nuts.settings.nuts_settings.gamma_val,
                        nuts.settings.nuts_settings.t0_val,
                        nuts.settings.nuts_settings.kappa_val,
                        nuts.settings.nuts_settings.precond_mat,

                        nuts.settings.nuts_settings.n_accept_draws
                    );
			},
			[](py::tuple t) { // __setstate__
                nuts_t* nuts = new nuts_t();

                std::stringstream ss(t[0].cast<std::string>());
                ss >> nuts->settings.rand_engine;
                nuts->settings.rng_seed_value = t[1].cast<size_t>();

                nuts->current_val = t[2].cast<Eigen::VectorXd>();

                nuts->settings.nuts_settings.n_burnin_draws = t[3].cast<size_t>();
                nuts->settings.nuts_settings.n_keep_draws = t[4].cast<size_t>();

                nuts->settings.nuts_settings.n_adapt_draws = t[5].cast<size_t>();
                nuts->settings.nuts_settings.target_accept_rate = t[6].cast<size_t>();

                nuts->settings.nuts_settings.omp_n_threads = 1;

                nuts->settings.nuts_settings.step_size = t[7].cast<double>();
                nuts->settings.nuts_settings.gamma_val = t[8].cast<double>();
                nuts->settings.nuts_settings.t0_val = t[9].cast<double>();
                nuts->settings.nuts_settings.kappa_val = t[10].cast<double>();
                nuts->settings.nuts_settings.precond_mat = t[11].cast<Eigen::MatrixXd>();

                nuts->settings.nuts_settings.n_accept_draws = t[12].cast<size_t>();

				return nuts;
			})
		)
    ;
}

