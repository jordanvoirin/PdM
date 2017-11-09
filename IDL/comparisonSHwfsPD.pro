;script to compare the SH wfs results and the PD results
;

PDwthPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\phaseScreen\wth\cropped\'
PDwoutPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\phaseScreen\wout\cropped\'

SHwthPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wth\'
SHwoutPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wout\'

PDwthPSresults = phaseretrieval(PDwthPSfolderPath,66,1,1)
PDwoutPSresults = phaseretrieval(PDwoutPSfolderPath,66,1,1)

SHwthPSresults = readshwfsdata(SHwthPSfolderPath)
SHwoutPSresults = readshwfsdata(SHwoutPSfolderPath)

