%print quads
clear all
close all

binpath = 'C:\Users\acsokol\sibl\geo\src\dual\bin\';
resFolder = datestr(date,'yyyy-mm-dd');
mkdir(resFolder);

delete *nodes
delete *polys
delete *quads
delete *tmp

%delete *.inp

%testCase = 4
resolutions = [0.5 0.25 .125/2];
 angles = [0:.125:1];
 
for testCase = 1:2
   
for aa = 1:length(angles)
for res=3:3
    
    rot = angles(aa)*90;
    rad = angles(aa);

resolution = resolutions(res);


fignum = testCase*4*2+aa*2+res;
  switch testCase
       case 1  %Legacy Line Case 
          baseName = 'Line';
          xp = [ -1:resolution:1 ];
          yp = [  -1:resolution:1 ];
          th = atan2d(yp,xp)+rot;
            rp = sqrt(xp.^2+yp.^2);
            xp = rp.*cosd(th);
            yp = rp.*sind(th);
          
       case 2  %Legacy Line Case 
          baseName = 'Circle';
          th = [0:0.01:360];
          rp = rad;
          xp = rp*cosd(th);
          yp = rp*sind(th);
          
      otherwise
          
            disp('Unknown method.')
  end
  
  
%  baseName = [baseName,num2str(resolution),'m',num2str(quadOrCube)];



pts = [(xp)' (yp)']';
baseName=[baseName ,'+', num2str(rot)];

fid = fopen([baseName,'.tmp'],'w');
fprintf(fid,'%12.16f  %12.16f\n',pts);
fclose(fid);


tic
dos([binpath,'dual.exe  ',num2str(resolution),' ',baseName,'.tmp',' 1']);
toc

ddd = dir('*quads');    
figure;
fscl = .5;
set(gcf,'Units','inches','Position',[0.5 0.5 9*fscl 9*fscl],'PaperUnits','inches')
set(gcf,'PaperSize',[9*fscl 9*fscl],'PaperPositionMode','manual')
set(gcf,'PaperPosition',[0.05 0.05 9*fscl 9*fscl]);

for ff = 1:length(ddd)

fileName = ddd(ff).name(1:end-5);
    
n = load([fileName,'nodes']);
q = load([fileName,'quads']);
l = load('line');

if strcmp(fileName , 'dual') | strcmp(fileName , 'primal')

    if strcmp(fileName , 'primal')
    linestyle = ':';
    else
        linestyle = '-';
    end
    
plot(l(:,1),l(:,2),'ko-','LineWidth',2);hold on;

for qq=1:size(q,1)

    NE = q(qq,1);
    SE = q(qq,2);
    SW = q(qq,3);
    NW = q(qq,4);
    
    seq = q(qq,:);
    seq = seq(seq~=-1);
 
     if strcmp(fileName , 'primal')
   plot(wrap(n([seq],2)),wrap(n([seq],3)),['k',linestyle])
     else
         fill(wrap(n([seq],2)),wrap(n([seq],3)),['k',linestyle],'FaceAlpha',0.2)
     end

end
axis equal;
axis off



end %dual

end %file loop


print(gcf,'-dpng',[resFolder,'\\',baseName,'DP','date',datestr(date,'yyyy-mm-dd'),'.png']);
end %%res
end %%angles
end %%test cases
delete *nodes
delete *polys
delete *quads
delete *tmp

% 
% figure;
% n=load('sph');
% plot3(n(:,1),n(:,2),n(:,3),'o');
% axis equal