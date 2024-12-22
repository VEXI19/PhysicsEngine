.. Physics Engine documentation master file, created by
   sphinx-quickstart on Sat Dec 21 15:52:39 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome page
============================

Welcome to JD Physics Engine Documentation page. Here you can find a full description of all classes and functions used in the Physics Engine.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   GetStarted
   modules

Installation
------------

To install the Physics Engine, use the following command:

.. code-block:: bash

   pip install physics-engine

Usage
-----

Here is a basic example of how to use the Physics Engine:

.. code-block:: python

   from PhysicsEngine import PhysicsEngine, Forces
   from Configs.Rockets.test_rocket import Rocket
   from Configs.Environments.test_env import Environment1 as Environment

   object = Rocket()
   environment = Environment()
   physics_engine = PhysicsEngine(object, environment, 0.1)

   physics_engine.add_force(Forces.gravity)
   physics_engine.add_force(Forces.thrust)
   physics_engine.add_force(Forces.drag)

   # Run the simulation
   physics_engine.run()