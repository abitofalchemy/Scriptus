clear all;
clf
csvStr = 'Bailey*Accel_Test_3*';
csv_files = dir( csvStr );
tests_mtrx = [];
for j=1:length(csv_files)
    %printf ('%s\n',csv_files(j).name)
    data = csvread(csv_files(j).name);
columns = size(data);:
    if (columns(2)< 8)
        break;
    else
        xyz = [data(:,5), data(:,6), data(:,7)];
        timeVec = data(:,8)-data(1,8);

        N=256;
        nsamp = length(timeVec);
        f_s=(nsamp/max(timeVec));
        y_dat = mean(xyz,2);
    %size(y_dat)
    %size(tests_mtrx)
        tests_mtrx = resize(tests_mtrx,length(y_dat),j+1);
    %size(tests_mtrx)
        tests_mtrx(:,j) = y_dat;
    

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
    endif
endfor

printf('Processed:%d files\n',length(csv_files));
printf('size of: %d(timeVec), %d(min(tests_mtrx))\n',length(timeVec), length(tests_mtrx));
subplot(2,1,1);hold;
%plot(timeVec, mean(tests_mtrx,2),'r-' );
plot(timeVec, min(tests_mtrx'),'r:' );
plot(timeVec, max(tests_mtrx'),'c:' );
errorbar(timeVec,mean(tests_mtrx,2),std(tests_mtrx,2,2))
ylabel('Acceleration'); xlabel('Time (s)');
legend('min','max','mean,\sigma','location,','east');
ax = axis();
axis([ax(1),ax(2),ax(3),abs(ax(3))])
title('{*Accel\_Test\_3*}');

subplot(212)
f = (1:N/2-1)*f_s/N;
avg_fft = mean(p2,2);
semilogy(f,avg_fft)
ylabel('Power Spectrum for the Average'); xlabel('Frequency (Hz)');
                  
                  
                  //for i=1:size(xyz_avg)(2)
                  //    r=i/size(xyz_avg)(2);
                  //    g=1-i/10;
                  //    b=i/size(xyz_avg)(2);
                  //    plot(xyz_avg(1:tst_samp(i),i), 'Color', [r g b]);
                  //    hold("on")
                  //endfor
