clc;
edf = Edf2Mat(strcat(path,'/',filePrefixName,'.edf'));
timelineBaseline = edf.Samples.time(1);
saccades = [edf.Events.Eblink.start' - edf.timeline(1), edf.Events.Eblink.end' - edf.timeline(1)];
csvwrite(strcat(path,'/',filePrefixName,'_blinks.csv') , saccades );
