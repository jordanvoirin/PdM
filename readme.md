# PdM project : Evaluation of optical aberrations using Phase Diversity (PD)
____________________________________________________________________________

This project gathers all the codes I write for my master thesis in the optical laboratory of the HEIG-VD in Yverdon-les-bains.

## 1st part
--------
The first part of my project is to acquire PSF in/out of focus and treat them with an ONERA code which is not shared in this project, contact Laurent Mugnier, ONERA, PARIS for the code of phase diversity.

The acquisition is done with a Ximea Camera MQ013MG-E2 using the python library https://github.com/pupil-labs/pyximea

### Python Code :

- AlignementScriptXimeaCamera.py : Script to align the camera on the focus point of the last lens.
- AcquisAndSaveXimea.py : Script to acquire images using the Ximea camera
- functionsXimea.py : some functions for the ximea
    - saveImg2Fits()
    - AcquireImg()
    - determineUnsaturatedExposureTime()
    - TwoDGaussian()
    - getPSFCentroid()
    - cropAroundPSF()
    - cropAndCenterPSF()

### IDL Code :

- phaseRetrieval.pro  : script to treat the \*.fits PSF data in order to retrieve the phase of the wavefront
- getImgSize.pro : function that returns the img size of the given sFilenames

## 2nd part
--------
The second part of my project is more theoretical on the subject of phase diversity.

I found a package for the zernike polynomials used as the basis for the aberrations (libtim-py, https://github.com/tvwerkhoven/libtim-py)

###Python Code :

- phaseDiversity.py : Class phaseDiversity that we instantiate an object which will do the phase phaseRetrieval
- fs.py : functions to construct the matricial system which will be minimized
- myExceptions.py : new exceptions I use to let know the users on what he could have done wrong
- phasor.py : Class phasor that construct a phasor with the desired characteristic.
- some test codes to check if everything runs smoothly
