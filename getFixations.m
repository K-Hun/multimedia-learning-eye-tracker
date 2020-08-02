clc;
edf = Edf2Mat(strcat(path,'/',filePrefixName,'.edf'));
timelineBaseline = edf.Samples.time(1);
fixations = [edf.Events.Efix.start' - edf.timeline(1), edf.Events.Efix.end' - edf.timeline(1), edf.Events.Efix.posX', edf.Events.Efix.posY', edf.Events.Efix.pupilSize'];
csvwrite(strcat(path,'/',filePrefixName,'_fixations.csv') , fixations );
