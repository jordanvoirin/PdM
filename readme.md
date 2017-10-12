PdM project
-----------

This project gather all the codes I write for my master thesis in the optical laboratory of the HEIG-VD in Yverdon-les-bains.

Title of the Project : Evaluation of optical aberrations using Phase Diversity (PD)
-----------------------------------------------------------------------------------

First, I will acquire PSF and treat them with an ONERA code which is not shared in this project, contact Laurent Mugnier, ONERA, PARIS
for the code of phase diversity.

The acquisition is done with a Ximea Camera MQ013MG-E2 using the python library https://github.com/pupil-labs/pyximea

Python Code :

- AlignementScriptXimeaCamera.py : Script to align the camera on the focus point of the last lens.
- AcquisAndSaveXimea.py : Script to acquire images using the Ximea camera
- functionsXimea.py : some functions for the ximea 
    - saveImg2Fits()
    - AcquireImg()
    - determineUnsaturatedExposureTime()
    
IDL Code :

- phaseRetrieval.pro  : script to treat the *.fits PSF data in order to retrieve the phase of the wavefront
