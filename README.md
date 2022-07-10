# SLEEPy - an implementation of the Soil-Landscape Estimation and Evaluation Program using machine learning modeling
###### *Rodrigo de Queiroga Miranda, Rodolfo Luiz Bezerra Nóbrega, Josiclêda Domiciano Galvíncio*
###### Contact: rodrigo.qmiranda@gmail.com

### About
The SLEEPy consists of a a very simple Python implementation of the ArcGIS™ extension SLEEP (Soil–Landscape Estimation and Evaluation Program), added with new machine learning capabilities for modelling soil attributes with high accuracy. The SLEEP is a software, developed by Ziadat et al., 2015, that uses Pedo-transfer functions to provide the spatial distribution of the necessary unmapped soil data needed for SWAT model predictions (http://www.doi.org/10.3965/j.ijabe.20150803.1270). Our code modifies the original modelling techniques to use complex machine learning, turning the whole algorithm into a hybrid approach for soil modelling. The scripts were developed for the interpreter Python 2.7.15 and 3.6.9. The modelling module is built with the dask framework, and scripts can be modified to run in distributed systems or in a single machine.

### Package usage
Usage protocol is divided in two parts, and both involve making changes in the scripts to reflect the actual datasets paths:

1. The first step would be [execute.bat](https://github.com/razeayres/sleepy/blob/master/execute.bat) to do all spatial modelling of soil attrbitutes. Here, the paths of two Python interpreters must be entered. One of them must be the Python instalations that holds the Arcpy module, and the other one is a second instalation which can be easily customized, e.g., an Anaconda distro.
2. Then, the path to the input data must be defined as [workfolder](https://github.com/razeayres/sleepy/blob/2e99c9a85ea134d741416a80b1a66c9ab502ad56/main.py#L5) variable in [main.py](https://github.com/razeayres/sleepy/blob/master/main.py).
3. The third and final part consists in make modifications in the [pedotransfer.py](https://github.com/razeayres/sleepy/blob/master/model/pedotransfer.py) to derive other soil data. Here the user must change the input and output filenames in [line 302](https://github.com/razeayres/sleepy/blob/2e99c9a85ea134d741416a80b1a66c9ab502ad56/model/pedotransfer.py#L302) and [line 8](https://github.com/razeayres/sleepy/blob/2e99c9a85ea134d741416a80b1a66c9ab502ad56/model/pedotransfer.py#L8) repectively. All the differents PTFs can be configured in the function [run()](https://github.com/razeayres/sleepy/blob/2e99c9a85ea134d741416a80b1a66c9ab502ad56/model/pedotransfer.py#L287).

### Development status
![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)