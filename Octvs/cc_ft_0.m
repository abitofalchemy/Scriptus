clear all;

csv_files = dir('*.csv');
%for i=1:length(csv_files)
	%printf ('%s\n',csv_files(i).name) 
%	data = csvread(csv_files(i).name);
%endfor

printf ('%s\n',csv_files(10).name) 
data = csvread('bjulia.csv');
size(data)
%data(1,:)
subplot(2,1,1)
plot(data(:,8), data(:,5));
xyz = [data(:,5), data(:,6), data(:,7)];
timeVec = data(:,8)-data(1,8);
plot(data(:,8)-data(1,8), mean(xyz,2) );
N=256
nsamp = length(timeVec);
f_s=(nsamp/max(timeVec))
y_dat = mean(xyz,2);
K = length(y_dat);
for (i=0:floor(K./N)-1)
    c = fft(y_dat(i*N+1:N))/N;            % compute fft of sound data
    p[:,i+1] = 2*abs( c(2:N/2));         % compute power at each frequency

endfor

f = (1:N/2-1)*f_s/N;
semilogy(f,p)

%
%y = abs(fft(mean(xyz,2), N));
%%y = fftshift(y);
%y_fft = y(1:nsamp/2);
%f = f_s*(-N/2:N/2-1)/N;
%f = f_s*(0:nsamp/2-1)/nsamp;
%subplot(2,1,2)
%size (f) 
%size (y_fft)
%y_fft = 20*log10(y_fft);
%%y_fft -= max(y_fft);
%%plot(f, y_fft);
%
%c = fft(y_dat(1:N))/N;            % compute fft of sound data
%p = 2*abs( c(2:N/2));         % compute power at each frequency
           % frequency corresponding to p
%length(f)
%length(p)

%axis([0 4000 10^-4 1])
%title(['Power Spectrum of ' file])


%%%%

%file = 'ex3-E.wav'; 
%[y,Fs,bits] = wavread(file); 
%
%Nsamps = length(y); 
%t = (1/Fs)*(1:Nsamps);          %Prepare time data for plot 
%
%%Do Fourier Transform 
%y_fft = abs(fft(y));            %Retain Magnitude 
%y_fft = y_fft(1:Nsamps/2);      %Discard Half of Points 
%f = Fs*(0:Nsamps/2-1)/Nsamps;   %Prepare freq data for plot 
%
%%Plot Sound File in Time Domain 
%figure 
%subplot(211)
%plot(t, y); 
%xlabel('Time (s)') 
%ylabel('Amplitude') 
%title('fft action') 
%
%%Plot Sound File in Frequency Domain 
%figure 
%plot(f, y_fft); 
%xlim([0 1000]) 
%xlabel('Frequency (Hz)') 
%ylabel('Amplitude') 
%title('Frequency Response of Tuning Fork A4') 
%
