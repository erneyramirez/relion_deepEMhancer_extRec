# relion_deepEMhancer_extRec

This repository contains code used to run deepEMhancer in relion_refine using the external reconstruction funtionality with `--external_reconstruct` argument.

For information on the installation and use of deepEMhancer you can visit the page: https://github.com/rsanchezgarc/deepEMhancer. 


---
* **Steps before executing the script (relion_deepEMhancer_extRec.py) in relion_refine**

*It is assumed that the user already has deepEMhancer installed.*


 1. Setting the environment variable CONDA_ENV to the conda enviroment created for deepEMhancer. This variable is used by the script to activate the deepEMhancer conda environment.   
 
 `export CONDA_ENV="deepEMhancer_env"`
   
 2. Setting the environment variable RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE to the command that executes the script.

`export RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE="python /path/to/relion_deepEMhancer_extRec.py"`

3. Set the CUDA_VISIBLE_DEVICES environment variable to the gpu to be used. It is recommended that it is the same one used in relion. If this variable does not appear, GPU 0 will be used.

`export CUDA_VISIBLE_DEVICES=0`

4. In some cases, it is recommended to set dynamic GPU allocation using the environment variable TF_FORCE_GPU_ALLOW_GROWTH='true'

`export TF_FORCE_GPU_ALLOW_GROWTH='true'`

---
* **Example**
 
```
wget https://github.com/erneyramirez/relion_deepEMhancer_extRec/blob/master/relion_deepEMhancer_extRec.py
export CONDA_ENV="deepEMhancer_env"
export RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE="python /path/to/relion_deepEMhancer_extRec.py"
export CUDA_VISIBLE_DEVICES=0
export TF_FORCE_GPU_ALLOW_GROWTH='true'
mpirun -n 3 relion_refine_mpi --auto_refine  ...  --external_reconstruct
```
