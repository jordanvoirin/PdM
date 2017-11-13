function readAndAverageSHdata, folderPath

fileExt='*.csv'

files = file_search(folderPath+fileExt)

r = readshwfsdata(files[0])

NFiles = n_elements(files)

for ifile = 1,Nfiles-1 do begin
  
  rtmp = readshwfsdata(files[ifile])
  
  r.wavefront = r.wavefront+rtmp.wavefront
  r.zernike[3,*] = r.zernike[3,*]+rtmp.zernike[3,*]
  
endfor

r.wavefront = r.wavefront / NFiles
r.zernike[3,*] = r.zernike[3,*] / Nfiles

return, r
end