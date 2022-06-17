function [] = DarkScan_SingleRun(FullPath)
    FullPath = char(FullPath);
    finput = imread(FullPath);
    dark = finput - 70;
    red = dark(:,:,1);green = dark(:,:,2);blue = dark(:,:,3);
    [row,col,d]=size(red);
    for i=1:1:row
        for j=1:1:col
            [red(i,j),green(i,j),blue(i,j)] = DarkScan_CheckCol(red(i,j),green(i,j),blue(i,j));
        end
    end
    combin_color = cat(3,red,green,blue);
    %{
    rot = input('Would you like to rotate this image? (Y/N) \n','s');
    if (rot == 'Y')
        rotdeg = input('By how many degrees? Positive for counterclockwise, negative for clockwise. \n');
        rot_im = imrotate(combin_color,rotdeg);
        combin_color = rot_im;
    end
    %}
    imwrite(combin_color,FullPath);
end

