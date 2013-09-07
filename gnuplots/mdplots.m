clear all;
clf;
data = [
1,2700.27,0.717,0;
4,3110.36,0.556,0 ;
8,2951,0.585,0 ;
8,2456.525,0.704,816.582;
10,2792.52,0.619,0];
proinsulin = [
1,5.584,310,nan;
1,5.562,310.857,311.609e+6
4,21.087,81.95,nan;
8,40.017,43.186,nan;
10,47.017,36.756,nan;
12,23.092,74.84,1.267e+9;
24,24.293,71.138,2.442e+9;
24,24.839,69.576,2.446e+9;
64,14.702,117.547,6.698e+9];

%subplot(311e
%bar(data(:,1), data(:,4), 2,  "facecolor", "r", "edgecolor", "b", "linewidth",4); hold
%subplot(312)
%plot(data(:,1),data(:,2),'s:'); 
%subplot(313)
stem(data(:,1),  data(:,4), "linewidth",4 ); hold
    
stem(proinsulin(:,1),proinsulin(:,4),"linewidth",4 );

