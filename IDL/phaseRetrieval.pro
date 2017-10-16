;Script to retrieve the phase of the wavefront
;

filePath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\'
fileExt = '*.fits'


;Get all the filenames containing the PSF data
sFilePaths = file_search(filePath+fileExt)
Nfiles =  n_elements(sFilePaths)
deltaZ = DINDGEN(Nfiles)

psf = mrdfits(sFilePaths[0],0)

psfDim = size(psf,/dimension)

psfs = make_array([psfDim[0],psfDim[1],Nfiles],/DOUBLE,value = 0.0)
psfs[*,*,1] = psf

sepFilePath = strsplit(sFilePaths[0],'\',/EXTRACT)
sFile = sepFilePath[n_elements(sepFilePath)-1]
sepsFile = strsplit(sFile,"_.",/EXTRACT)
deltaZ[0] = double(sepsFile[n_elements(sepsFile)-2])

;Treat filenames to get the focused or defocused property of the PSFs and fill the vector deltaZ of dimension M for the diversity.pro
for i = 1, n_elements(sFilePaths)-1 do begin
  ;get the deltaZ which is written in the filename
  sepFilePath = strsplit(sFilePaths[i],'\',/EXTRACT)
  sFile = sepFilePath[n_elements(sepFilePath)-1]
  sepsFile = strsplit(sFile,"_.",/EXTRACT)
  deltaZ[i] = double(sepsFile[n_elements(sepsFile)-2])/100
  
  psf = mrdfits(sFilePaths[i],0,header)
  psfs[*,*,i]=psf
endfor


;Run diversity

lambda = 0.6375 ;microns
threshold = 1e-3
D1=3.2*1e-3
D2=0.0
jmax = 66
pxSize = 5.3*1e-6
fdist = 80*1e-3
pxSizeArcSec = pxSize/fdist*!RADEG/3600
mode = 'MODAL'

Phase = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,mode,D1=D1,D2=D2,jmax=jmax)

end