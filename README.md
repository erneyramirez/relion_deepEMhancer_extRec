# relion_deepEMhancer_extRec

This repository contains code used to run deepEMhancer in relion_refine using the external reconstruction funtionality with `--external_reconstruct` argument.

For information on the installation and use of deepEMhancer you can visit the page: https://github.com/rsanchezgarc/deepEMhancer. 


---
* **Steps before executing the script (relion_deepEMhancer_extRec.py) in relion_refine**

 1. Activate conda enviroment for deepEMhancer 
 
 `conda activate deepEMhancer_env`
   
 2. Setting the environmental variable RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE to the command that executes the script.

`export RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE="python /path/to/relion_deepEMhancer_extRec.py"`

3. Set the CUDA_VISIBLE_DEVICES environment variable to the gpu to be used. It is recommended that it is the same one used in relion. If this variable does not appear, GPU 0 will be used.

`export CUDA_VISIBLE_DEVICES=0`

4. In some cases, it is recommended to set dynamic GPU allocation using the environment variable TF_FORCE_GPU_ALLOW_GROWTH='true'

`export TF_FORCE_GPU_ALLOW_GROWTH='true'`

---
* **EXAMPLE**

