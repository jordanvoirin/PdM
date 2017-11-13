;script to compare the SH wfs results and the PD results
;

PDwthPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\phaseScreen\wth\cropped\PS2\'
PDwoutPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\phaseScreen\wout\cropped\PS2\'

SHwthPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wth\PS2\'
SHwoutPSfolderPath = 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\SHWFS\phaseScreen\wout\PS2\'



jmax = 66 ; jmax of the SH WFS
PDwthPSresult = phaseretrieval(PDwthPSfolderPath,jmax,1,1)
PDwoutPSresult = phaseretrieval(PDwoutPSfolderPath,jmax,1,1)

pdPSresult = PDwthPSresult

SHwthPSresult = readAndAverageSHdata(SHwthPSfolderPath)
SHwthPSresult.zernike = toNoll(SHwthPSresult.zernike)
SHwoutPSresult = readAndAverageSHdata(SHwoutPSfolderPath)
SHwoutPSresult.zernike = toNoll(SHwoutPSresult.zernike)

shPSresult = SHwthPSresult

;Correct for background aberration ------------------------------------------------------------------------------

pdPSresult.res.a_j = (PDwthPSresult.res.a_j -  PDwoutPSresult.res.a_j)*1000
pdPSresult.zon.a_j = (PDwthPSresult.zon.a_j -  PDwoutPSresult.zon.a_j)*1000

pdPSresult.res.wavefront = (PDwthPSresult.res.wavefront -  PDwoutPSresult.res.wavefront)*1000
pdPSresult.zon.wavefront = (PDwthPSresult.zon.wavefront -  PDwoutPSresult.zon.wavefront)*1000

shPSresult.zernike[3,*] = (SHwthPSresult.zernike[3,*]-SHwoutPSresult.zernike[3,*])*1000
shPSresult.wavefront = (SHwthPSresult.wavefront-SHwoutPSresult.wavefront)*1000
;plotting --------------------------------------------------------------------------------
marge = 0.13

;Zernike

MRMSE = rmse(pdPSresult.res.a_j ,shPSresult.zernike[3,3:jmax-1])
ZRMSE = rmse(pdPSresult.zon.a_j ,shPSresult.zernike[3,3:jmax-1])

maxy = max([pdPSresult.res.a_j,pdPSresult.zon.a_j,transpose(shPSresult.zernike[3,3:jmax-1])])
miny = min([pdPSresult.res.a_j,pdPSresult.zon.a_j,transpose(shPSresult.zernike[3,3:jmax-1])])

pdMplot = plot(pdPSresult.res.j,pdPSresult.res.a_j,'b-2',xtitle='Zernike polynome j',ytitle = 'a_j [nm]',$
  name=['PD modal RMSE = ' +string(MRMSE,format='(F5.2)')],xrange=[4,jmax], yrange=[miny-5,maxy+5], MARGIN=marge)
pdZplot = plot(pdPSresult.zon.j,pdPSresult.zon.a_j,'r-2',/overplot,$
  name=['PD zonal RMSE = ' +string(ZRMSE,format='(F5.2)')])
pdSHplot = plot(shPSresult.zernike[0,*],shPSresult.zernike[3,*],'k-2',/overplot,$
    name='SH')
!null = legend(target=[pdMplot,pdZplot,pdSHplot],/DATA)

pdMplot.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\phaseScreen\PS2\ZernikeCoef.pdf', BORDER=10, RESOLUTION=350
pdMplot.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\phaseScreen\PS2\ZernikeCoef.png', BORDER=10, RESOLUTION=350
; Wavefront

abmin=-500
abmax=500


pdMim = image(PDPSresult.res.wavefront,rgb_table=34,min_value=abmin,max_value = abmax,title='PD Modal',position=[0.05,0.55,0.45,0.95])
pdZim = image(PDPSresult.zon.wavefront,rgb_table=34,min_value=abmin,max_value = abmax,title='PD Zonal',/current,position=[0.55,0.55,.95,.95])
pdSHim = image(flipmatrix(shPSresult.wavefront),rgb_table=34,min_value=abmin,max_value = abmax,title='SH',/current,position=[0.33,0.05,.73,.45])
c = COLORBAR(TARGET=pdMim, ORIENTATION=1,position=[.52,.55,.545,.95],TITLE='[nm]',range=[abmin,abmax])

pdMim.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\phaseScreen\PS2\Wavefront.pdf', BORDER=10, RESOLUTION=350
pdMim.save, 'C:\Users\Jojo\Desktop\PdM-HEIG\Science\fig\PD\phaseScreen\PS2\Wavefront.png', BORDER=10, RESOLUTION=350
end