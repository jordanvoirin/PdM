; Script to analyse the PSFs made with the python script in order to compare the result of diversity and my algo
;
;instanciate folderPath------------------------------------------------------------------------
resultFolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\PSFforIDLtreatment\IDLajs\'
sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\PSFforIDLtreatment\PSFs\*'
sFolderPaths = file_search(sfolderPath,/Test_Directory)
Nfolders =  n_elements(sFolderPaths)

;run phaseRetrieval----------------------------------------------------------------------------
for iFol = 1, Nfolders-1 do begin
  results = phaseRetrieval(sFolderPaths[iFol]+'\',30,1,1)

  sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
  srmsWFe = sepFolderPath[n_elements(sepFolderPath)-1]
  sepsrmsWFe = strsplit(srmsWFe,'_',/EXTRACT)
  rmsWFe = sepsrmsWFe[n_elements(sepsrmsWFe)-1]
  
  js = results.res.j
  ajsmodal = results.res.a_j
  ajszonal = results.zon.a_j
  
  result = [js,ajsmodal,ajszonal]
  filePath = resultFolderPath+'Ajs_rmsWFe_'+string(rmsWFe)+'.txt'
  GET_LUN, U
  openW,U,filePath
  str = 'js,ajsmodal,ajszonal'
  printf,U,str
  for ij = 0,n_elements(js)-1 do begin
    str = string(js[ij])+','+string(ajsmodal)+','+string(ajszonal)
    printf,U,str
  endfor
  close,U
endfor
end