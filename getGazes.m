clc;
edf = Edf2Mat(strcat(path,'/',filePrefixName,'.edf'));
timelineBaseline = edf.Samples.time(1);
gazes = [edf.Samples.posX,edf.Samples.posY, edf.Samples.pupilSize];
csvwrite(strcat(path,'/',filePrefixName,'_gazes.csv') , gazes )
