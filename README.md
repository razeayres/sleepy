# SLEEPy - an implementation of the Soil-Landscape Estimation and Evaluation Program using machine learning modeling
###### *Rodrigo de Queiroga Miranda, Rodolfo Luiz Bezerra Nóbrega, Josiclêda Domiciano Galvíncio*
###### Contact: rodrigo.qmiranda@gmail.com

### About
The SLEEPy consists of a a very simple Python implementation of the ArcGIS™ extension SLEEP (Soil–Landscape Estimation and Evaluation Program), added with new machine learning capabilities for modelling soil attributes with high accuracy. The SLEEP is a software, developed by Ziadat et al., 2015, that uses Pedo-transfer functions to provide the spatial distribution of the necessary unmapped soil data needed for SWAT model predictions (http://www.doi.org/10.3965/j.ijabe.20150803.1270). Our code modifies the original modelling techniques to use complex machine learning, turning the whole algorithm into a hybrid approach for soil modelling. The scripts were developed for the interpreter Python 2.7.15 and 3.6.9. The modelling module is built with the dask framework, and scripts can be modified to run in distributed systems or in a single machine.

### Package usage
Usage is still not straightforward. It is divided in two parts, and both involve making changes in the scripts to reflect the actual datasets paths. The first step would be [execute.bat](https://github.com/razeayres/sleepy/blob/master/execute.bat) to do all spatial modelling of soil attrbitutes, and the second part consists in make modifications in the [pedotransfer.py](https://github.com/razeayres/sleepy/blob/master/model/pedotransfer.py) to derive other soil data.

### Development status
![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)