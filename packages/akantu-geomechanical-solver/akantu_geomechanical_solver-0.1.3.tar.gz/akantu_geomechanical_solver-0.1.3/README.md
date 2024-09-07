
[![Project Status](https://img.shields.io/badge/status-under%20development-yellow)](https://gitlab.com/hsolleder/akantu-geomechanical-solver)
![GitLab License](https://img.shields.io/gitlab/license/hsolleder%2Fakantu-geomechanical-solver)

# Akantu Geomechanical solver

This package contains a geomechanical simulator based on the open-source FEM library [Akantu].

## Install

Start by cloning the repository, for instance using

```bash
git clone git@gitlab.com:hsolleder/akantu-geomechanical-solver.git
```

To set up the backend environment, you need [pip](https://pip.pypa.io/en/stable/installation/). The akantu software can be installed using two different approaches:

### Serial

To install the serial version of akantu, run

``` bash
pip install .[serial] --index-url https://gitlab.com/api/v4/projects/15663046/packages/pypi/simple
```

### Parallel (WIP)

To install the parallel version of akantu, using the `installation.sh` script or the Docker image
