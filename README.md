# HospitalGeneratorRDF_V2
**HospitalGeneratorRDF_V2** is an updated version of the software presented in [HospitalGeneratorRDF](https://github.com/LorenaPujante/HospitalGeneratorRDF). Compared to the previous version, the changes are related to achieving a hospital design with some specific characteristics. This software has been used in the work "TODO: HACER PAPER" with DOI [~~doi: TODO~~](NULL) to create the dataset used for the experiments. 

As its previous version, **HospitalGeneratorRDF_V2** is a software that, based on the output of [_H-Outbreak_](https://github.com/denissekim/Simulation-Model) (a simulation model of the movements of patients inside a hospital), creates a knowledge graph (KG) in RDF and RDF* according to the data model presented in "_Spatiotemporal Data Modelling for Epidemiological Research in Hospitals_" ([10.1109/JBHI.2024.3417224](https://ieeexplore.ieee.org/document/10568325)) with the little changes presented in [HospitalKG_changes](https://github.com/LorenaPujante/HospitalKG_Changes).

Since H-Outbreak does not cover all the classes and relations from the data model, HospitalGeneratorRDF completes it by adding _Floors_, _Areas_, _Corridors_, _Rooms_, _Beds_, _Services_ and _HospitalizationUnits_, and the relations between them. It also creates different subclasses of _Events_: _Hospitalization_, _Radiology_, _Surgery_ and _Death_.

## 0. Related Repositories
Below, we present some other related repositories that may be of interest to you:
- [**HospitalKG_changes**](https://github.com/LorenaPujante/HospitalKG_Changes): It is also linked to [~~doi: TODO~~](NULL).
- [**HospitalEdgeWeigths**](https://github.com/LorenaPujante/HospitalEdgeWeigths): It is also linked to [~~doi: TODO~~](NULL).
- [**HospitalGeneratorRDF**](https://github.com/LorenaPujante/HospitalGeneratorRDF): Previous version of this software. In the folder _Description_ of this repository, there is an exhaustive description of how the process of generating random hospitals works.


## 1. Changes over HospitalGeneratorRDF
We have based several characteristics of the hospital on the main building of the Virgen de la Arrixaca University Clinical Hospital, Region of Murcia, Spain. These characteristics are:
- Number of _Services_ for hospitalisations
- Number of _HospitalizationUnits_ (_HU_) per _Service_
- Number of operating theatres.
- Number of rooms for radiology and other diagnostic imaging techniques (we will call all of them as _radiology_).
- Number of beds for A&E
- Number of beds for Intensive Care (IC)

The hospital will have four _Floors_:
- _**Ground Floor**_: In thi _Floor_ there will be: ICU rooms, A&E rooms, radiology rooms and operating theatres.
- _**Upper Floor**_: These 3 _Floors_ will be used for hospitalisations.   

Next, there is a brief description of the services and each kind of _Floor_.

### 1.1. Services
The hospital will have:
- **17** Services for _Hospitalisations_.
- **1** Service for _Radiology_.
- **1** Service for _A&E_.
- **1** Service for _IC_.
- There isn't a _Service_ for only surgeries. Each _Service_ will be in charge of its own surgeries.

Below, we present the distribution of _HospitalizationUnits_ per _Service_:
- The 17 _Services_ for hospitalisations, the A&E _Service_ and the IC _Service_ will have each **1** _HU_ for **surgeries**.
- _A&E Service_ will have **1** _HU_ for patient stays.
- _IC Service_ will have **1** _HU_ for patient stays.
- _Radiology Service_ will have **6** _HU_.
- The _Services for hospitalisations_ will have a certain number of _HospitalizationUnits_. There will be:
  - **8** Services with **1** _HU_. These _Services_ are: _S0_, _S1_, _S2_, _S10_, _S11_, _S12_ and _S13_.
  - **3** Services with **2** _HU_. These _Services_ are: _S2_, _S6_ and _S8_.
  - **4** Services with **3** _HU_. These _Services_ are: _S3_, _S4_, _S9_ and _S16_.
  - **1** Services with **4** _HU_. This _Service_ is: _S7_.
  - **1** Services with **5** _HU_. This _Service_ is: _S15_.
  - **1** Services with **6** _HU_. This _Service_ is: _S14_.





### 1.2. Ground Floor
This _Floor_ has a layout with **2 rows** (_Units_) and _5 columns_ (_Blocks_). In this _Floor_ there will be:
- _Operating theatres_: **27**
  - There will be  


  
## 2. Installation
The source code is currently hosted on [github.com/LorenaPujante/HospitalGeneratorRDF](https://github.com/LorenaPujante/HospitalGeneratorRDF_V2).

The program is in Python 3.10, and no external packages are needed.


## 3. Input
aaa


## 4. Execution and Configuration Params
aaa


## 5. Output
aaaa




