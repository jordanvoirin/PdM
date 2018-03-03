;instanciate folderPath------------------------------------------------------------------------
sfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\noise_study\*'

sFolderPaths = file_search(sfolderPath,/Test_Directory)

Nfolders =  n_elements(sFolderPaths)

;get the vector of nbrImgAveraging-------------------------------------------------------------
nbrImgAveraging = []
for iFol = 0, Nfolders-1 do begin
  sepFolderPath = strsplit(sFolderPaths[iFol],'\',/EXTRACT)
  snbrImages = sepFolderPath[n_elements(sepFolderPath)-1]
  nbrImgAveraging = [nbrImgAveraging,long(snbrImages)]
endfor

indSorted = sort(nbrImgAveraging)
nbrImgAveraging = nbrImgAveraging[indSorted]

sFolderPaths[indsorted[iFol]]+'\'

fileExt = '*.fits'

sFilePaths = file_search(filePath+fileExt)
Nfiles =  n_elements(sFilePaths)

