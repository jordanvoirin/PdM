function flipMatrix, M
;takes a 2d array and flip along x and y
dims = size(M,/Dimensions)

for ix = 0, (dims[0]-1) do begin
  for iy = 0, ceil((dims[1]-1)/2) do begin
    tmp = M[ix,iy]
    M[ix,iy] = M[dims[0]-1-ix,dims[1]-1-iy]
    M[dims[0]-1-ix,dims[1]-1-iy] = tmp 
  endfor
endfor

return, M

end