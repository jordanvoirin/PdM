function getImgSize, sFilePaths

minSize = 20000

Nfiles =  n_elements(sFilePaths)

imgSizes = make_array([Nfiles],/long,value = 0)

for i = 0, Nfiles-1 do begin
  psf = readfits(sFilePaths[i])
  psfDim = size(psf,/dimension)
  
  imgSizes[i] = psfDim[0]
endfor

return, imgSizes

end