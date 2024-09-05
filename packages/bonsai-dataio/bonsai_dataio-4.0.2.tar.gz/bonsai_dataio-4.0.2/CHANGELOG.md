# Changelog
## version 4.0.2
-Added PropertyOfProducts schema
-Added associated_product to use and supply.
-Confirmed trade is the correct schema
-Added product destination to supply
-Added ExternalDimensionTables

## version 4.0.1
- Added BrokenYearMonetarySUT as external schema which is used for specific type of monetary SUT, for tables with annual data that start on a day other than January 1st. For example for the fiscal year of India.

## version 4.0.0
- added B_Matrix schema to MatrixModel
- updated PPF-fact-schema with units for activities and products

## version 3.3.0
- BREAKING CHANGE: current task name is now required by Config!
- added/updated arg_parser and set_logger from utilities
- fixed bug with loading csv not interpreting nan values correctly
- fixed bug with loading csv didn't parse bool values correctly

## version 3.2.0
- Added feature to save matrices, by specifying the datatype to be .h5 in the location field of a resource
- Also added MatrixModels to schema
  - A_Matrix
  - Inverse
  - IntensitiesMatrix
  
## version 3.1.7
- Added external schema USGSProductionVolume

## version 3.1.6
- Fixed bug where last_update column to resources.csv was not saved and loaded in iso format

## version 3.1.5
- Fixed bug when only single resource was loaded with get_resource_info

## version 3.1.4
- Added external schemas for: external monetary SUT, PRODCOM production volumes, UN and BACI data

## version 3.1.3
- Bugfix that ensures that the resource name and the file name does not need to be identical

## version 3.1.2
- added schemes for classifications
- revisions of names for schemes to synchronize with Bonsai ontology

## version 3.1.1
- changed behaviour of DataResource location. It is now possible to specify a root_location that is used to create absolute paths from relative locations. 
- with this change, location in resources.csv for CSVResourceRepository are now all relative to the resources.csv file!

## version 3.1.0
- feature change: load and all dependent methods now return a dict if more than one file is loaded, otherwise returns just a dataframe.

##  version 3.0.4
- bug fix -> uncertainty columns from get_empty_dataframe not double anymore

## version 3.0.3
- bug fix -> location now stored in relative format
- bug fix -> updating resource now works as expected
- resource_exists function now only works with non-metadata information (e.g. comment field is ignored when checking)

## version 3.0.2 (resource_exists)

- bug fixes
- added resource_repository.resource_exists(resource) -> bool.

## version 3.0.1 (flexible location)

- bug fixes
- added the possibility to use variables in the location name (e.g. `clean/production/{version}/industry.csv`) is now possible.

## version 3.0.0 (rework of dataio)

This version potentially breaks old code that relies on the dataio package.

- **CSV Resource Repository**: Introduced a new `CSVResourceRepository` class to manage data resources stored in CSV files, enabling adding, updating, and listing of resources.
- **Data Validation**: Implemented data validation methods that ensure the integrity of data before it is saved, aligning with predefined schemas.
- **Environment Setup**: Added functionality to set the `BONSAI_HOME` environment variable for specifying the project's home directory.
- **Resource Manipulation Methods**: New methods for adding, updating, and retrieving data resources, including:
  - `add_to_resource_list`
  - `update_resource_list`
  - `get_resource_info`
- **Data Handling Methods**: Developed methods to read and write DataFrame objects directly related to specific tasks and resources, enhancing ease of data manipulation:
  - `write_dataframe_for_task`
  - `get_dataframe_for_task`
- **Test Suite**: A comprehensive test suite has been added to ensure the reliability and performance of the new functionalities.
- **Documentation**: Provided detailed README.md documentation to assist users in understanding and utilizing the new features effectively.


## Version 2.0.3 (fixed bugs)

- read csv files into pandas dataframe properly (e.g. avoid converting `NA` into NaN)
- raise Error when `frictionless.validate` fails


## Version 2.0.2 (minor changes)

- added future work
- changed tox.ini


## Version 2.0.1 (included datapackage dependencies)

- edited validate to check foreign keys to field datapackages in metadata
- implemented dialect handling (delimiter, quotation character and skipinitialvalue)
- edited docs (syntax, future developments, tutorials)
- updated tutorials
- improved user experience (renamed validate report, provided plot output options)


## Version 1.2.7 (small fix)

- create/dump renaming bug
- Layout of create docstring is not good


## Version 1.2.6 (fixed log refs)

- Older terms like dump and visualize were fixed to save and plot


## Version 1.2.5 (log path of saved metadata and tables)

- changed log strings


## Version 1.2.4 (fixed datapackage save index issues)

- 'id' is index, now column exported with proper name


## Version 1.2.3 (fixed datapackage create docstring)

- Concerning tables


## Version 1.2.1 (fixed bug in datapackage create function)

- Indent was misplaced


## Version 1.2.0 (revised tutorials and added metadata syntax)

- Additionaly revised terminology and simplified API of several functions


## Version 1.1.0 (added features to 'dump' and 'describe')

- Added instructions on use of help() and dir() to 'load' toy model
- Added auto-increment option to 'dump'
- Added option to override metadata fields to 'describe'


## Version 1.0.7 (improved user-friendliness)

- Changed version dependency of pandas in setup.cfg install_requires from >= to None
- Changed validate to raise exception only after running all pre-frictionless tests
- Changed describe to accept absolute paths
- Changed all functions to allow both Path and string paths
- Removed output of <name>.datapackage.yaml from describe


## Version 1.0.6 (made dependencies flexible)

- Changed version dependencies in setup.cfg install_requires from == to >=


## Version 1.0.5 (fixed web documentation)

- Renamed subfolder with datapackage
- Reformatted docstrings


## Version 1.0.4 (generate latex documentation)

- Edited several configuration files


## Version 1.0.3 (added jupyter notebooks)

- Added jupyter notebooks to load and dump tutorials
- Added print statements to load and dump tutorials
- Renamed distro to match package name to fix website version number issue


## Version 1.0.2 (fixed instructions)

- Fixed instructions for installing package
- BUG: API is not rendering in website
- BUG: website is showing unknown version


## Version 1.0.0 (datapackage is working)

- Functions describe, validate, visualize, load, dump working for datapackage
- Tests using export illustrations working


