%%  Baraka Bounds Individual Analysis
function bb_ind_an( fn_suffix )
close all;

show_files(fn_suffix);

figure(1);
subplot(211);
plot_timedomain(fn_suffix)
%
title(fn_suffix)
subplot(212);
plot_frequency_spectrum(fn_suffix)

return

%%
function plot_frequency_spectrum ( csv_filenames )
csv_files = dir( csv_filenames );
tests_mtrx = [];
xyz_avg = [];

for j=1:length(csv_files)
    %printf ('%s\n',csv_files(j).name)
    data = csvread(csv_files(j).name);
    [leg_parts] = strsplit(csv_files(j).name,'_');
    legend_list(j) = strcat(leg_parts(1),'.',leg_parts(4));
    columns = size(data);
    if (columns(2)< 8)
        continue;
    else
        xyz= [data(:,5), data(:,6), data(:,7)];
        timeVec = data(:,8)-data(1,8);
    endif
%    timeVec = 0:1/10:42;
%    xyz = [control_fft()',control_fft()', control_fft()'];
    xyzMean = mean(xyz,2);
    
    nsamp = length(timeVec);
    f_s=10;%(nsamp/max(timeVec))
%    fft_y = fft(xyzMean,256);
%    size(fft_y)
    N = 256;
    K = length(xyzMean);
    for (i=0:ceil(K./N)-1)
        if (i == ceil(K./N)-1)
            y_slice = xyzMean(i*N+1:length(xyzMean));
        else
            y_slice = xyzMean(i*N+1:N*(1+i));
        endif
        %printf('i:%d, slice:%d\n',i,length(y_slice));
        Y = fft(y_slice,N);            % compute fft of sound data
        %p = 2*abs( c(2:N/2));         % compute power at each frequency
        pyy = Y.*conj(Y); % power spectrum
        p2(:,i+1) = zeros(1,length(Y));
        p2(:,i+1) = pyy;
        f = f_s*(0:N/2)/N;
    endfor
            Pyy(:,j) = mean(abs(p2),2);

endfor
%size(Pyy)
%size(f)
figure(1);  hold ('on')
plotColors = colormap;

for ix=1:size(Pyy)(2)
    plotColorsI = round( size( plotColors, 1)* ix / size(Pyy)(2) );
    plot(f, 20*log10(Pyy(1:N/2+1,ix)),'Color', plotColors( plotColorsI,:));
endfor
%legend_list = {'test1','test2','test3','test4'};
%legend(legend_list);
xlabel('Frequency (Hz)'); ylabel('Power Spectrum (dB)')
return
%-%-%-%

%%
function show_files(fnsuffix)
csv_files = dir( fnsuffix );
tests_mtrx = [];
for j=1:length(csv_files)
    printf ('%s\n',csv_files(j).name)
end
return
%%

function plot_timedomain(filenames)

csv_files = dir( filenames );
time_mtrx = [];
xyz_avg = [];
for k=1:length(csv_files)
    [leg_parts] = strsplit(csv_files(k).name, '_' );
    legend_list(k) = strcat(leg_parts(1),'.',leg_parts(4));
endfor
for j=1:length(csv_files)
    %printf ('%s\n',csv_files(j).name)
    data = csvread(csv_files(j).name);
    columns = size(data);
    if (columns(2)< 8)
        continue;
    else
        xyz= [data(:,5), data(:,6), data(:,7)];
        timeVec = data(:,8)-data(1,8);
    endif

    
    %plot( mean(xyz,2)) %, label=csv_files(j).name )
    
    tmpMean = mean(xyz,2);
    
    tst_samp(j) = length(tmpMean);
    if (size(xyz_avg)(1))
        %length(tmpMean)
        if (length(mean(xyz,2)) > length(xyz_avg))
            xyz_avg = resize( xyz_avg, length(mean(xyz,2)), j-1);
            time_mtrx = resize( time_mtrx, length(mean(xyz,2)), j-1);
            %printf ('size of xyz_avg: %d, %d\n', size(xyz_avg)(1),size(xyz_avg)(2));
        elseif (length(tmpMean) < length(xyz_avg))
            tmpMean = resize(tmpMean, length(xyz_avg),1);
            timeVec = resize(timeVec, length(xyz_avg),1);
            %size(tmpMean)
        endif
    %else
    %    printf('something wrong with xyz_avg\n');
    endif
    time_mtrx(:,j) = timeVec;
    xyz_avg(:,j) = tmpMean;
    printf ('size of xyz_avg: %d, %d\n', size(xyz_avg)(1),size(xyz_avg)(2));
    
    
    
endfor
%size(xyz_avg)
%size( legend_list)
%legend( legend_list)
%legend_list = {'test1','test2','test3','test4'};

plotColors = colormap; 
for i=1:size(xyz_avg)(2)
    plotColorsI = round( size( plotColors, 1)* i / size(xyz_avg)(2) );
    plot(time_mtrx(1:tst_samp(i),i),
         xyz_avg  (1:tst_samp(i),i), 'Color', plotColors( plotColorsI,:) );
    hold("on")
endfor

%%
legend( legend_list)
ylabel('Averaged XYZ Accel')
xlabel('time (s)')

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [fx] = control_fft()

x = 0:1/10:42; % sample rate = 460800 Hz
fx = sin(2*pi*4*x); % sine wave @ 30000 Hz
%%N = 256
%%Y = fft(fx, N); % take first 4096 samples and fft
%%Py = Y.*conj(Y); % power spectrum
%%
%%f = 10*(0:N/2)/N; % create x-axis scale
%%Pyy = abs(Py(1:N/2));
%size(fx)
return

%%        N=256;
%%        nsamp = length(timeVec);
%%        f_s=(nsamp/max(timeVec));
%%        y_dat = mean(xyz,2);
%%    %size(y_dat)
%%    %size(tests_mtrx)
%%        tests_mtrx = resize(tests_mtrx,length(y_dat),j+1);
%%    %size(tests_mtrx)
%%        tests_mtrx(:,j) = y_dat;
%%    
%%
%%        K = length(y_dat);
%%        for (i=0:ceil(K./N)-1)
%%            if (i == ceil(K./N)-1)
%%                y_slice = y_dat(i*N+1:length(y_dat));
%%            else
%%                y_slice = y_dat(i*N+1:N*(1+i));
%%            endif
%%            %printf('i:%d, slice:%d\n',i,length(y_slice));
%%            c = fft(y_slice,N)./N;            % compute fft of sound data
%%        
%%            p = 2*abs( c(2:N/2));         % compute power at each frequency
%%            p2(:,i+1) = zeros(1,length(p));
%%            p2(:,i+1) = p;
%%        endfor
%%    endif
%%endfor
%%
%%printf('Processed:%d files\n',length(csv_files));
%%printf('size of: %d(timeVec), %d(min(tests_mtrx))\n',length(timeVec), length(tests_mtrx));
%%subplot(2,1,1);hold;
%%%plot(timeVec, mean(tests_mtrx,2),'r-' );
%%plot(timeVec, min(tests_mtrx'),'r:' );
%%plot(timeVec, max(tests_mtrx'),'c:' );
%%errorbar(timeVec,mean(tests_mtrx,2),std(tests_mtrx,2,2))
%%ylabel('Acceleration'); xlabel('Time (s)');
%%legend('min','max','mean,\sigma','location,','east');
%%ax = axis();
%%axis([ax(1),ax(2),ax(3),abs(ax(3))])
%%title('{*Accel\_Test\_3*}');
%%
%%subplot(212)
%%f = (1:N/2-1)*f_s/N;
%%avg_fft = mean(p2,2);
%%semilogy(f,avg_fft)
%%ylabel('Power Spectrum for the Average'); xlabel('Frequency (Hz)');
