# -*- coding: utf-8 -*-

#Wrapper to run relion_external_reconstruct and deepEMhancer
#Author: Erney Ramirez-Aportela
#contact: erney.ramirez@gmail.com

#Usage:
# To execute this script in relion_refine it is necessary to use the argument "--external_reconstruct".
# It is also required to set the RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE environment variable 
# to point to this script.

# Sometimes it is also necessary to set dynamic GPU allocation
# using the environment variable TF_FORCE_GPU_ALLOW_GROWTH='true'.

# For example:
# export RELION_EXTERNAL_RECONSTRUCT_EXECUTABLE="python /path/to/relion_deepEMhancer_extRec.py"
# export TF_FORCE_GPU_ALLOW_GROWTH='true'

# In order to run deepEMhancer it is necessary to activate the conda environment. 
# Therefore, the environment is activated from the script. 
# If the script (and RELION) are running from scipion the variable CONDA_ACTIVATION_CMD must exist. 
# If it is run outside of scipion, the variable needs to be set.
# For example:
# export CONDA_ACTIVATION_CMD=" eval "$(/home/user/miniconda3/condabin/conda shell.bash hook)" "


import os
import os.path
import sys
import argparse  
import time
import numpy as np
import fcntl
import errno
import mrcfile


def execute_external_relion(star):

    params = ' relion_external_reconstruct'
    params += ' %s' %star
    os.system(params)     
    
def execute_deep(sampling, dir, var, half): 
               
#     params = 'eval "$(/home/erney/data/miniconda3/condabin/conda shell.bash hook)" && conda activate xmipp_deepEMhancer && ' 
#     params = ' %s && conda activate xmipp_deepEMhancer && ' %CONDA_ACTIVATION_CMD
#     params += ' xmipp_deep_volume_postprocessing'
    params = ' deepemhancer'
    params += ' --sampling_rate %f' %(sampling)  
    params += ' -i %s/relion_it%s_half%s_class001_external_reconstruct.mrc' %(dir, var, half)       
    params += ' -o %s/relion_external_reconstruct_deep%s.mrc' %(dir, half) 
    params += ' -g %s -b 5' %gpu
#     params += ' -p wideTarget'
    os.system(params)
   
    
if __name__=="__main__":  
    paths = sys.argv 
    star = paths[1]
    
    gpu = 0
#     gpu = os.environ['CUDA_VISIBLE_DEVICES'].split(',')[0]
#     print('using gpu: %s' %gpu)
    
    if os.getenv('CONDA_ACTIVATION_CMD'):
        CONDA_ACTIVATION_CMD=os.getenv('CONDA_ACTIVATION_CMD')
    else:
        print('ERROR---The environment variable CONDA_ACTIVATION_CMD must be defined.') 
        print('For example: export CONDA_ACTIVATION_CMD=eval "$(/home/user/miniconda3/condabin/conda shell.bash hook)" ')    
    
    dir=os.path.dirname(star)

    part = star.split('_')
    iter_string = part[2]
    iter_number = int(iter_string[2:5])
    
    #We assume iter < 100   
        
    if int(iter_number) <= 9: 
        var = '00%d' %(iter_number)
        beforeVar = '00%d' %(iter_number-1)
    elif int(iter_number) == 10:
        var = '0%d' %(iter_number)
        beforeVar = '00%d' %(iter_number-1)
    else:
        var = '0%d' %(iter_number)
        beforeVar = '0%d' %(iter_number-1)

    
    with open("%s/relion_it%s_sampling.star" %(dir, beforeVar)) as file:
        for li in file.readlines():
           if "rlnHealpixOrder " in li: 
              healpix = int(li.split()[1]) 
              print("healpix = %s" %healpix)
    
    
#     if iter_number < 1:
    if (healpix < 4):
         
        execute_external_relion(star)   
        time.sleep(5)
           
    else:         
            ###sampling of the images            
        with open("%s/relion_it%s_data.star" %(dir, beforeVar)) as f:
            for line in f.readlines():
                if "opticsGroup1" in line:
                    sampling = float(line.split()[8])
                    print("sampling = %s" %sampling)
        
        
        try:        
            file1=os.path.isfile('%s/relion_external_reconstruct_deep1.mrc' %(dir))
            if file1 is True:
                os.remove('%s/relion_external_reconstruct_deep1.mrc' %(dir))
                file1 = False
        except:
            pass        
        
        try:
            file2=os.path.isfile('%s/relion_external_reconstruct_deep2.mrc' %(dir))
            if file2 is True:
                os.remove('%s/relion_external_reconstruct_deep2.mrc' %(dir)) 
                file2 = False
        except:
            pass        
          
        execute_external_relion(star)   
        
#                     #semaforo
#         x = open('foo', 'w+')
# 
#         try:
#             fcntl.flock(x, fcntl.LOCK_EX | fcntl.LOCK_NB)  
#         except IOError as e:
#             if x:
#                 x.close() 
#             raise 
         
                   
        for i in range (1,15):
            mrc1 = os.path.isfile('%s/relion_it%s_half1_class001_external_reconstruct.mrc' %(dir, var))  
            if mrc1 is True:
                break
            else:
                time.sleep(30)
                
        for i in range (1,15):
            mrc2 = os.path.isfile('%s/relion_it%s_half2_class001_external_reconstruct.mrc' %(dir, var))  
            if mrc2 is True:
                break
            else:
                time.sleep(30)

        check=os.path.isfile('%s/relion_it%s_half1_class001_external_reconstruct.mrc' %(dir, var))        
        
        if check is True:                
        
            #open mrcfile
            with mrcfile.open('%s/relion_it%s_half1_class001_external_reconstruct.mrc' %(dir, var)) as f1:
                emMap1 = f1.data.astype(np.float32).copy()  
            with mrcfile.open('%s/relion_it%s_half2_class001_external_reconstruct.mrc' %(dir, var)) as f2:
                emMap2 = f2.data.astype(np.float32).copy()   
                
            max1_before =  emMap1.max()                  
            max2_before =  emMap2.max()        
            
            try:            
                execute_deep(sampling, dir, var, '1')
            except:
                pass
            
            try:
                execute_deep(sampling, dir, var, '2')
            except:
                pass

            with mrcfile.open('%s/relion_external_reconstruct_deep1.mrc' %(dir)) as d1:
                emDeep1 = d1.data.astype(np.float32).copy() 
            with mrcfile.open('%s/relion_external_reconstruct_deep2.mrc' %(dir)) as d2:
                emDeep2 = d2.data.astype(np.float32).copy()

            max1_after = emDeep1.max()
            max2_after = emDeep2.max()
        
            factor1 = float(max1_after)/float(max1_before) 
            factor2 = float(max2_after)/float(max2_before)
            
            finalMap1 = emDeep1/factor1
            finalMap2 = emDeep2/factor2
            
            #save mrcfile
            with mrcfile.new('%s/relion_it%s_half1_class001_external_reconstruct.mrc' %(dir, var) , overwrite=True) as fMap1:
                fMap1.set_data(finalMap1.astype(np.float32))
                fMap1.voxel_size = tuple([sampling]*3)
            with mrcfile.new('%s/relion_it%s_half2_class001_external_reconstruct.mrc' %(dir, var) , overwrite=True) as fMap2:
                fMap2.set_data(finalMap2.astype(np.float32))
                fMap2.voxel_size = tuple([sampling]*3)

        
