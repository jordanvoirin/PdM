function readSHWFSdata, filePath

openr, f, filePath

iLine = 0
line = ''

zernike.coefficient = []
zernike.index = []
zernike.order = []
zernike.frequency = []

while ~EOF(f) do begin
  readf, f, line
  iLine += 1
  
  ;get the zernike coefficient
  if strmatch(line,'* ZERNIKE FIT *')
    subheaderNbrLines = 5
    for isHd =1,subheaderNbrLines do begin
      readf, f, line
      iLine += 1
    endfor
    
    readf, f, line
    iLine += 1
    sLine = strsplit(line,',',/EXTRACT)
    
    while stregex(sLine[0],'\d') ne -1 then begin
      zernike.index = [zernike.index,long(sLine[0])]
      zernike.order = [zernike.order,long(sLine[1])]
      zernike.frequency = [zernike.frequency,long(sLine[2])]
      zernike.coefficient = [zernike.coefficient,long(sLine[3])]
      readf, f, line
      iLine += 1
      sLine = strsplit(line,',',/EXTRACT)
    endwhile 
  endif
endwhile
free_lun, f

return, zernike

end