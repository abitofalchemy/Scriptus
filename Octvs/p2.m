data = [
290.000000,128 ,1000 ;
289.000000,256 ,1000 ;
293.000000,512 ,1000 ;
291.000000,1024 ,1000 ;
297.000000,2048 ,1000 ;
303.000000,4096 ,1000 ;
296.000000,8192 ,1000 ;
296.000000,16384 ,1000 ;
309.000000,32768 ,1000 ;
7348.000000,65536 ,1000 ;
7828.000000,131072 ,1000 ;
9148.000000,262144 ,1000 ;
13325.000000,524288 ,1000 ;
14581.000000,1048576 ,1000 ;
13438.000000,2097152 ,1000 ;
13725.000000,4194304 ,1000 ;
14033.000000,8388608 ,1000 ;
14266.000000,16777216 ,1000 ];

for i=1:length(data(:,1))
	printf('Average time to allocate and free %d bytes is: %.4f microsecs.\n',data(i,2), data(i,1)/data(i,3));
	
end
	
void_fc = load('output1.txt');
avg_run_time = mean(void_fc)/1E9;
ratio_2to1 = ( data(:,1)./data(:,3) )./avg_run_time;

%% plot
h = figure(1)
semilogx(data(:,2),ratio_2to1,'r','LineWidth',3)
grid('on')
FN = findall(h,'-property','FontName');
set(FN,'FontName','/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf');
FS = findall(h,'-property','FontSize');
set(FS,'FontSize',10);
title('Ratio of the avg time to malloc vs calling an empty function')
xlabel('bytes');ylabel('avg malloc run-time/avg empty func call run-time')

H = 3; W = 4;
set(h,'PaperUnits','inches')
set(h,'PaperOrientation','portrait');
set(h,'PaperSize',[H,W])
set(h,'PaperPosition',[0,0,W,H])
print(h,'-dpng','-color','vib_plt4.png');
