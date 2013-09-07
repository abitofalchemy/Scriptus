clear all;
subplot(2,1,1);hold;
csv_files = dir('*Test_3*.csv');
tests_mtrx = [];
for j=1:length(csv_files)
	printf ('%s\n',csv_files(j).name)
	data = csvread(csv_files(j).name);
    
    xyz = [data(:,5), data(:,6), data(:,7)];
    timeVec = data(:,8)-data(1,8);

    N=256;
    nsamp = length(timeVec);
    f_s=(nsamp/max(timeVec));
    y_dat = mean(xyz,2);
	size(y_dat)
	resize(tests_mtrx,i,length(y_dat))
    tests_mtrx(:,j) = y_dat;
	size(tests_mtrx)
    

    K = length(y_dat);
    for (i=0:ceil(K./N)-1)
        if (i == ceil(K./N)-1)
            y_slice = y_dat(i*N+1:length(y_dat));
        else
            y_slice = y_dat(i*N+1:N*(1+i));
        endif
        %printf('i:%d, slice:%d\n',i,length(y_slice));
        c = fft(y_slice,N)./N;            % compute fft of sound data
        
        p = 2*abs( c(2:N/2));         % compute power at each frequency
        p2(:,i+1) = zeros(1,length(p));
        p2(:,i+1) = p;
        
    endfor
endfor

plot(timeVec, tests_mtrx );
subplot(212)
f = (1:N/2-1)*f_s/N;
avg_fft = mean(p2,2);
length(avg_fft)
semilogy(f,avg_fft)

