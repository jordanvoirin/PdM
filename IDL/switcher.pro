function switcher, arr
  yDim = n_elements(arr[0,*])
  
  if n_elements(yDim) gt 1 then ydim = ydim[1]

  tmparr = arr

  for iy = 0,yDim-1 do begin
    tmparr[*,iy] = arr[*,yDim-(1+iy)]
  endfor
  
  return, tmparr
end