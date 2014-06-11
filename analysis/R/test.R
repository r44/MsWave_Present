
MaxNumMachine = 5000; MaxNumForEach = 200;
ExpPath = '/nfs/master/01/r01922165/zzzzz/Results/'
ExpDir = 'Exp0605/'
ExpData = 'ANN_SIFT/'
#ExpSize = str(MaxNumForEach)+'_'+str(MaxNumMachine)+'/'
MethodChoice = 0;
if( MethodChoice == 0){
    Method = 'New/'
}else if( MethodChoice ==1)
{
    Method = 'MsWave/'
}else{
}
File = '0605.csv'
#AnalyzeFile(ExpPath+ExpDir+ExpData+ExpSize+Method+File);
print(paste(ExpPath,ExpDir,ExpData,'200_5000/',Method,File,sep=""));
filename = paste(ExpPath,ExpDir,ExpData,'200_5000/',Method,File,sep="");
data <- read.csv(filename, header=T)
print( data)
dim(data)
