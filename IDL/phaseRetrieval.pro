;function to retrieve the phase of the wavefront
;
function phaseRetrieval, filePath, jmax, modal, zonal
;filePath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\astigmatism\'
fileExt = '*.fits'


;Get all the filenames containing the PSF data
sFilePaths = file_search(filePath+fileExt)
Nfiles =  n_elements(sFilePaths)
deltaZ = DINDGEN(Nfiles)

imgSizes = getImgSize(sFilePaths)

minSize = min(imgSizes[where(imgSizes ge 118)])

if minSize mod 2 ne 0 then begin
  minSize = minSize - 1
endif

print, 'Image size = ' + string(minSize) + 'x' + string(minSize)

psf = readfits(sFilePaths[0])
psfDim = size(psf,/dimension)

psfs = []
deltaZ = []

if psfDim[0] ge minSize and psfDim[1] ge minSize then begin

  ;get the deltaZ which is written in the filename
  sepFilePath = strsplit(sFilePaths[0],'\',/EXTRACT)
  sFile = sepFilePath[n_elements(sepFilePath)-1]
  sepsFile = strsplit(sFile,"_.",/EXTRACT)
  deltaZ = [deltaZ,double(sepsFile[n_elements(sepsFile)-2])/100]
  
  psfs=[[[psfs]],[[psf[psfDim[0]/2-minSize/2:psfDim[0]/2+minSize/2-1,psfDim[1]/2-minSize/2:psfDim[1]/2+minSize/2-1]]]]

endif else begin
  print, 'img0 is to small and is not taken into account for the phase retrieval'
endelse

;Treat filenames to get the focused or defocused property of the PSFs and fill the vector deltaZ of dimension M for the diversity.pro
for i = 1, n_elements(sFilePaths)-1 do begin
  
  psf = readfits(sFilePaths[i])
  psfDim = size(psf,/dimension)
  
  if psfDim[0] ge minSize and psfDim[1] ge minSize then begin
  
    ;get the deltaZ which is written in the filename
    sepFilePath = strsplit(sFilePaths[i],'\',/EXTRACT)
    sFile = sepFilePath[n_elements(sepFilePath)-1]
    sepsFile = strsplit(sFile,"_.",/EXTRACT)
    deltaZ = [deltaZ,double(sepsFile[n_elements(sepsFile)-2])/100]
  
    psfs=[[[psfs]],[[psf[psfDim[0]/2-minSize/2:psfDim[0]/2+minSize/2-1,psfDim[1]/2-minSize/2:psfDim[1]/2+minSize/2-1]]]]
  endif else begin
    print, 'img'+string(i)+' is to small and is not taken into account for the phase retrieval'
  endelse
  
endfor


;Run diversity

lambda = 0.6375d ;microns
threshold = 1e-3
D1=3.2*1e-3
D2=0.d
jmax = jmax
pxSize = 5.3e-6
fdist = 80e-3
pxSizeArcSec = pxSize/fdist*!RADEG*3600.d

if modal eq 1 and zonal ne 1 then begin
  res = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,'modal',d1=D1,d2=D2,jmax=jmax)
  return, {res:res}
endif
if modal ne 1 and zonal eq 1 then begin
  zon = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,'zonal',d1=D1,d2=D2,jmax=jmax)
  return, {zon:zon}
endif
if modal eq 1 and zonal eq 1 then begin
  res = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,'modal',d1=D1,d2=D2,jmax=jmax)
  zon = diversity(psfs,deltaZ,lambda,fdist,pxSizeArcSec,threshold,'zonal',d1=D1,d2=D2,jmax=jmax)
  return, {res:res, zon:zon}
endif


end
