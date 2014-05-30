%% Main function for generating each type of figures.
clear all; clc;

SafeMode = true;

%ResultDir = '~/zzzzz/Results/PremFor0604/SIFT/';
ResultDir = './';
ResultFiles = {'test.csv', 'test2.csv'};
OutputDir = './output/';
OutputFiles = {'test.png', 'test2.png'};

if ~ isequal(exist(OutputDir,'dir'),7)
	'No output directory, create a new one.'
	mkdir(OutputDir);
end

Titles = {'haha','haha2'};
xlab = {'Num of machines', 'Num of repeated exp'};
ylab = {'Saving ratio', 'Num of repeat time'};

FigTypes = [0,1]; % Type of graph to be generated.
%for idx = 1:size(ResultFiles,1)
for idx = 1:1
	figpara.title = Titles{idx};
	figpara.xlab = xlab{idx}; figpara.ylab = ylab{idx};
	switch FigTypes(idx)
		case 0
			figpara.resultfile = [ResultDir,ResultFiles{idx}]; figpara.outputPath = [OutputDir,OutputFiles{idx}];
			if SafeMode && isequal(exist(figpara.outputPath,'file'),2) 
				error('Fig %d already exists, please check or rename.',idx);
			end
			CostOneParam(figpara);
		otherwise
			error('Undefined FigTypes: Fig %d type %d , please check or rename.',idx,FigTypes(idx));
	end
	clearvars figpara;
end

