Dataset for manuscript "Ensembler: Enabling high-throughput molecular simulations at the superfamily scale" - Daniel L. Parton, Patrick B. Grinaway, Sonya M. Hanson, Kyle A. Beauchamp, John D. Chodera
========

Data from an Ensembler project used to generate models for all 93 known human tyrosine kinase (TK) catalytic domains, using all 4433 structures of protein kinase catalytic domains of any species as templates.

Manifest
--------

* Target data:
  * targets-IDs.txt - newline-separated list of target IDs
  * targets-data.csv - detailed target info in CSV format
  * targets-data.txt - detailed target info in ASCII-format table 
* Template data:
  * templates-data.csv - detailed template info in CSV format
  * templates-data.txt - detailed template info in ASCII-format table 
* models/
  * [target ID]/
    * topology.pdb - PDB-format coordinate file, used to provide model topology
    * models.xtc - Gromacs XTC-format trajectory; each frame represents the coordinates of a model
      * models have been subjected to 100 ps implicit solvent molecular dynamics refinement
      * only models which successfully completed the implicit solvent MD stage are included in the trajectory
    * models-data.csv - data for each model (in same order as the trajectory file), including template ID, sequence identity relative to the target sequence, and RMSD relative to the highest sequence identity model
