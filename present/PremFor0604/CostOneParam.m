function [ output_args ] = CostOneParam( input_args )
%COSTMNEPARAM Generate the figure comparing the cost in a range of one paramater.
%   Comparing the cost in a range of one parameter with an error bar figure. x for methods and y for cost.
%		input_args.vaule:
%			Each column is the results of the parameter for one value.  
%			The num of rows means the num of repeated experiments.
%		input_args.outputPath:
%			Destination of the generated figure.
	SkipHeader = true;
	if SkipHeader
		data = csvread( input_args.resultfile, 1); % 1 means skip the header.
	else
		data = csvread(input_args,resultfile);
	end

	time = unique(data(:,1));
	xAxis = unique(data(:,2));

	ntime = max(time);
	xLen = size(xAxis,1);
	SegLen = (max(xAxis) - min(xAxis)) / (xLen-1);
	value = zeros( ntime , xLen );
	for i = 1:xLen
	    value(:,i) = data( find(data(:,2)==xAxis(i)) ,3);
	end

    hold on
    h1 = errorbar(xAxis,mean(value),std(value),'-.or');
    %set(gca,'ytick',ha);
    %set(gca,'yticklabel','mean without matrix cost')
    %h2 = plot(xAxis,mean(mean(value)));

	title(input_args.title);
    xlabel(input_args.xlab);
    ylabel(input_args.ylab);
    % No need lengend.
    %grid on
    
	axis([min(xAxis) - SegLen , max(xAxis) + SegLen ,0, max([1,mean(value)]')]);

	print(input_args.outputPath,'-dpng');
end

