clc;
edf = Edf2Mat(strcat(path,'/',filePrefixName,'.edf'));
timelineBaseline = edf.Samples.time(1);
ms = edfExtractMicrosaccades(edf);
microsaccades = [ms.StartTime' - edf.timeline(1), ms.EndTime' - edf.timeline(1), ms.vPeak', ms.Amplitude'];
csvwrite(strcat(path,'/',filePrefixName,'_microsaccades.csv') , microsaccades )
