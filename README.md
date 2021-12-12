# DIP
DIP project

DataSets:
1. MIT CBCL
2. BioID
3. Yale
4. Caltech
5. SoF
6. Orl
7. Non - Face Dataset (Collected Heterogeneously)

----------------------------------------------------------------------------------------
Pre-Processing Methods Studied:
* Low Pass Filters:

1. gaussian blur
2. bilateral filter


* Deconvolutions
1. Blind Deconvolution (richardson lucy)
2. tv_chambolle
3. BMD (partially implemented , not converging yet)

* Retinex

1. SSR
2. MSR
3. retinex FM
4. NMBM

* Normalization

1. HOMO

* Histogram Manipulation

1. CLAHE
2. HE
3. log intensity stretch
4. full scale intensity stretch
----------------------------------------------------------------------------------------

The pipeline is as:
Step 1: Download the DataSets (from their owner sites) and use the scripts in the dataset_helper_scripts directory to convert all to greyscale and change extensions like (.gif and .pgm) to common extensions. Also arrange all images of a dataset in a single folder using these scripts.

Step 2: Arrange the data   directory like shown
has 2 subdirectories: faces     non-faces
These further have their particular sub-directories with name of the DATASET


----! Important, for illuastration "data" folder has the desired structure, just that it has few images 

Step 3: Run all the "driver scripts" in the root directory of this repository.
This will create an "output" directory with the result of all preprocessing methods.

Step 4: Use "csv_scripts" directory to get the performance metrics from the "output" directory

Step 5: "analysis" directory has the final performance csv files of each pre-procesing method

Step 6: Published report  directory has the final findings in form of csv file.

