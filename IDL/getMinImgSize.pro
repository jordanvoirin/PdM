function, sFilePaths

minSize = 20000

Nfiles =  n_elements(sFilePaths)

for i = 1, n_elements(sFilePaths)-1 do begin
  psf = readfits(sFilePaths[i])
  psfDim = size(psf,/dimension)
  if psfDim[0]<minSize then
    minSize = psfDim[0]
  endif
endfor