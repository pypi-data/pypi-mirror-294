Flow Cytometer Simulation Code Documentation
============================================

This document provides the API documentation for the Flow Cytometer simulation code, which models
the flow of particles through a flow cytometer and generates particle arrival times based on a
Poisson process. The classes and functions documented here are automatically generated from the
codebase using Sphinx `autoclass` directives.

Classes and Methods
===================

Below are the primary classes and methods used in the flow cytometer simulation.

Flow Class
----------

.. autoclass:: FlowCyPy.Flow
   :members:
   :undoc-members:
   :show-inheritance:

ScattererDistribution Class
---------------------------

.. autoclass:: FlowCyPy.ScattererDistribution
   :members:
   :undoc-members:
   :show-inheritance:


FlowCytometer Class
-------------------

.. autoclass:: FlowCyPy.FlowCytometer
   :members:
   :undoc-members:
   :show-inheritance:


Additional Notes
================

This documentation is auto-generated from the code's docstrings using `autoclass` and `automethod`
directives in Sphinx. To build the documentation, run the following command in your project directory:

.. code-block:: bash

    sphinx-build -b html source/ build/
