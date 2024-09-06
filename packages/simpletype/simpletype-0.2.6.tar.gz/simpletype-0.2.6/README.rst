
.. image:: https://readthedocs.org/projects/simpletype/badge/?version=latest
    :target: https://simpletype.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/simpletype-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/simpletype-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/simpletype-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/simpletype-project

.. image:: https://img.shields.io/pypi/v/simpletype.svg
    :target: https://pypi.python.org/pypi/simpletype

.. image:: https://img.shields.io/pypi/l/simpletype.svg
    :target: https://pypi.python.org/pypi/simpletype

.. image:: https://img.shields.io/pypi/pyversions/simpletype.svg
    :target: https://pypi.python.org/pypi/simpletype

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/simpletype-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/simpletype-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://simpletype.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://simpletype.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/simpletype-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/simpletype-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/simpletype-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/simpletype#files


Welcome to ``simpletype`` Documentation
==============================================================================
.. image:: https://simpletype.readthedocs.io/en/latest/_static/simpletype-logo.png
    :target: https://simpletype.readthedocs.io/en/latest/

Simple data type system that let many data type systems talk to each other.


Background
------------------------------------------------------------------------------
In the complex world of data processing, defining multiple schemas for a single data structure is a common yet challenging task. Data engineers and analysts often find themselves caught in a web of repetitive schema definitions across various platforms and tools. This is where **simpletype** comes to the rescue.


The Problem
------------------------------------------------------------------------------
Consider a typical scenario: You're working on a project to export data from Amazon DynamoDB to a Data Lake. For this seemingly straightforward task, you find yourself defining and maintaining multiple schemas:

- JSON Schema
- Pandas Schema
- Polars Schema
- Spark Schema
- AWS Glue Schema
- AWS DynamoDB Schema

Each of these schemas serves a crucial purpose in your data pipeline, but the process of creating and maintaining them is:

- Time-consuming
- Prone to errors
- Difficult to keep synchronized


The Solution
------------------------------------------------------------------------------
simpletype is a powerful Python library designed to eliminate the redundancy and potential errors in multi-schema environments. With simpletype, you can:

1. **Define Once, Use Everywhere**: Create a single, unified schema definition.
2. **Automatic Generation**: Let simpletype automatically generate schemas for all your required data processing systems.
3. **Consistency Guaranteed**: Ensure all your schemas remain in sync, reducing errors and inconsistencies.
4. **Save Time and Effort**: Focus on your data and analytics, not on repetitive schema definitions.

simpletype empowers data professionals to streamline their workflow, enhance productivity, and maintain data integrity across diverse data processing ecosystems.


.. _install:

Install
------------------------------------------------------------------------------

``simpletype`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install simpletype

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade simpletype
