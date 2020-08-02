clc;
edf = Edf2Mat(strcat(path,'/',filePrefixName,'.edf'));
timelineBaseline = edf.Samples.time(1);
saccades = [edf.Events.Esacc.start' - edf.timeline(1), edf.Events.Esacc.end' - edf.timeline(1), edf.Events.Esacc.posX', edf.Events.Esacc.posY', edf.Events.Esacc.posXend', edf.Events.Esacc.posYend', edf.Events.Esacc.hypot', edf.Events.Esacc.pvel'];
csvwrite(strcat(path,'/',filePrefixName,'_saccades.csv') , saccades );
