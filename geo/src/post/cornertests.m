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


%testCase = 4
resolutions = [.5 ];
 angles = [ 120 180 270];
 
for testCase = 1:1
   
for aa = 1:1
for res=1:1
    
    rot = angles(aa);


resolution = resolutions(res);


fignum = testCase*4*2+aa*2+res;
  switch testCase
       case 1  %Legacy Line Case 
          baseName = 'Corner';
          step = 0.001;
          lnd = [0:step:1.5]
          xp = [ reverse(lnd) lnd(2:end)*cosd(rot) ];
          yp = [ 0*lnd  lnd(2:end)*sind(rot) ];
          
          inds = find(xp <= 1);
          xp=xp(inds);
          yp =yp(inds);
          inds = find(yp <= 1);
          xp=xp(inds);
          yp =yp(inds);
          
          
          bxx = [1 0 -1 -1 -1  0  1 1];
          bxy = [1 1  1  0 -1 -1 -1 -.0000000001]
          
          bxa = mod(atan2d(bxy,bxx),360);
          inds = find(bxa> rot);
          xp =[xp bxx(inds)];
          yp = [yp bxy(inds)];
          
          
          
             arclen =cumsum([0 sqrt( diff((xp)).^2+diff((yp)).^2)]);
            xp = interp1(arclen,xp,[0:step:max(arclen)]);
            yp = interp1(arclen,yp,[0:step:max(arclen)]);
                
          
          
      otherwise
          
            disp('Unknown method.')
  end
  
  
%  baseName = [baseName,num2str(resolution),'m',num2str(quadOrCube)];

%th = atan2d(yp,xp)+rot;
%rp = sqrt(xp.^2+yp.^2);
%xp = rp.*cosd(th);
%yp = rp.*sind(th);

pts = [(xp)' (yp)']';
baseName=[baseName , num2str(rot),'at',num2str(resolution)];

fid = fopen([baseName,'.tmp'],'w');
fprintf(fid,'%12.16f  %12.16f\n',pts);
fclose(fid);


tic
dos([binpath,'dual.exe  ',num2str(resolution),' ',baseName,'.tmp',' 0']);
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
corners = load('linecorners');
da = load('delangles');

if strcmp(fileName , 'subdivideddual') | strcmp(fileName , 'primal')

    if strcmp(fileName , 'primal')
    linestyle = ':';
    else
        linestyle = '-';
    end
    
plot(l(:,1),l(:,2),'k.-','LineWidth',2);hold on;
plot(corners(:,1),corners(:,2),'ro','LineWidth',2);hold on;

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

ff
print(gcf,'-dpng',[resFolder,'\\',baseName,'DP','date',datestr(date,'yyyy-mm-dd'),'.png']);
end %%res
end %%angles
end %%test cases

figure;
plot(da);

delete *nodes
delete *polys
delete *quads
delete *tmp

% 
% figure;
% n=load('sph');
% plot3(n(:,1),n(:,2),n(:,3),'o');
% axis equal