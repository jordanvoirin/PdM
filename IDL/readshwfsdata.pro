function readSHWFSdata, filePath

openr, f, filePath

iLine = 0
line = ''

zernikeCoef = []


while ~EOF(f) do begin
  readf, f, line
  iLine += 1
  if strmatch(line,'* ZERNIKE FIT *')
    subheaderNbrLines = 5
    for isHd =1,subheaderNbrLines do begin
      readf,f,line
    endfor
    sLine = strsplit(line,',',/EXTRACT)
    if stregex(sLine[0],'\d') ne -1 then begin
      
    endif 
  endif
endwhile
free_lun, f


end