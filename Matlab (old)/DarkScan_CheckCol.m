function [ newR,newG,newB ] = DarkScan_CheckCol( R,G,B )
    if R>150 & G>150 & B>150
        R=255;
        G=255;
        B=255;
    elseif R<150 & G<150 & B<150
        %R=R-70;
        %G=G-70;
        %B=B-70;
        R=DarkScan_Reset(R);
        G=DarkScan_Reset(G);
        B=DarkScan_Reset(B);
    else
        R=255;
        G=255;
        B=255;
    end
    newR=R;newG=G;newB=B;
end

