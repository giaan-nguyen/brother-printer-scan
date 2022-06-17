ans_in = 'Y';
while((ans_in == 'Y') || (ans_in == 'y'))
    clc, clear all;
    [FileName,PathName]=uigetfile('*.bmp','Select One or More Files','MultiSelect','on');
    if(~iscellstr(FileName)) 
        if(FileName == 0)   % check if cancel was pressed
            break
        else  % if only one file selected
            FullPath = strcat(PathName,FileName);
            DarkScan_SingleRun(FullPath);
        end
    else  % if multiple files selected 
        for i=1:length(FileName)
            FullPath(i) = strcat(PathName,FileName(i));
            DarkScan_SingleRun(FullPath(i));
        end
    end
    ans_in = input('Would you like to edit another image? (Y/N) \n','s');
    while((ans_in ~= 'Y') && (ans_in ~= 'y') && (ans_in ~= 'N') && (ans_in ~= 'n'))
        ans_in = input('Input error. Would you like to edit another image? (Y/N) \n','s');
    end
end