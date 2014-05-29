
clear all; clc;

ResultDir = '~/zzzzz/Results/PremFor0604/SIFT/';


ResultFiles = {'test.csv', 'test2.csv'};


for filename = ResultFiles
    data = csvread( [ResultDir,filename{1}], 1) % 1 means skip the header.
    time = unique(data(:,1));
    M = unique(data(:,2));
    ntime = max(time);
    nM = size(M,1);
    value = zeros( ntime , nM );
    for i = 1:nM
        value(:,i) = data( find(data(:,2)==M(i)) ,3);
    end

    figure
%    hold all
    h = errorbar(M,mean(value),std(value));
%    set(h,'linestyle','none')
    print('haha','-dpng')
end

