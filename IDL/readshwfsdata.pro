function readSHWFSdata, filePath

openr, f, filePath, /GET_LUN

iLine = 0
line = ''


coefficient = []
index = []
order = []
frequency = []
wavefront = []

while ~EOF(f) do begin
  readf, f, line
  iLine += 1
  
  ;get the zernike coefficient
  if strmatch(line,'* ZERNIKE FIT *') then begin
    subheaderNbrLines = 5
    for isHd =1,subheaderNbrLines do begin
      readf, f, line
      iLine += 1
    endfor
    
    readf, f, line
    iLine += 1
    sLine = strsplit(line,',',/EXTRACT)
    
    while stregex(sLine[0],'[0-9]+') ne -1 and ~EOF(f) do begin
      index = [[[index]],[[long(sLine[0])]]]
      order = [[[order]],[[long(sLine[1])]]]
      frequency = [[[frequency]],[[long(sLine[2])]]]
      coefficient = [[[coefficient]],[[double(sLine[3])]]]
      readf, f, line
      iLine += 1
      sLine = strsplit(line,',',/EXTRACT)
    endwhile
  endif
  
  if strmatch(line,'\*\*\* WAVEFRONT \*\*\*')  then begin
    subheaderNbrLines = 11
    for isHd =1,subheaderNbrLines do begin
      readf, f, line
      iLine += 1
    endfor
    readf, f, line
    iLine += 1
    sLine = strsplit(line,',',/EXTRACT)
    nel = n_elements(sLine)
    while stregex(sLine[0],'[0-9]+') ne -1 and ~EOF(f) do begin
      wavefront = [[wavefront],[double(sLine[1:nel-1])]]
      readf, f, line
      iLine += 1
      sLine = strsplit(line,',',/EXTRACT)
    endwhile
    
  endif
endwhile
free_lun, f

zernike = {index:index,order:order,frequency:frequency,coefficient:coefficient}

return, {zernike:zernike,wavefront:wavefront}

end