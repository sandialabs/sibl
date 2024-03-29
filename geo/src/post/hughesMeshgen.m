%print quads
clear all
close all

resFolder = datestr(date,'yyyy-mm-dd');
mkdir(resFolder);
binpath = 'C:\Users\acsokol\sibl\geo\src\dual\bin\';

res = 2.^(-[8:8]);

for rr=1:length(res)
resolution = res(rr);


delete *nodes
delete *polys
delete *quads
delete *tmp

plotall =0;




step = (.1);        
rad = 1;
aside = 4.0;
th = [90:-step:0];
arcx = cosd(th)*rad;
arcy = sind(th)*rad;

edge1 = [rad:0.01:aside];
edge10 = [rad:0.01:aside]*0;

edge2 = [0:0.01:aside];
edge20 = [0:0.01:aside]*0;
edge2a = [0:0.01:aside]*0+aside;

xp = [arcx edge1(2:end-1) edge2a reverse(edge2(2:end-1)) edge10(2:end-1) ];
yp = [arcy edge10(2:end-1) edge2 edge2a(2:end-1) reverse(edge1(2:end-1)) ];

xp =wrap(xp);
yp = wrap(yp);

rp = sqrt(xp.^2+yp.^2);
thp = atan2d(yp,xp)+90;
xp = cosd(thp).*rp;
yp = sind(thp).*rp;
step =0.00001;
arclen =cumsum([0 sqrt( diff((xp)).^2+diff((yp)).^2)]);
xp = interp1(arclen,xp,[0:step:max(arclen)]);
yp = interp1(arclen,yp,[0:step:max(arclen)]);

featureFlag = 1;






baseName = ['Hughes',num2str(resolution)];
       
  
%  baseName = [baseName,num2str(resolution),'m',num2str(quadOrCube)];

pts = [(xp)' (yp)']';
baseName = [baseName];
fid = fopen([baseName,'.tmp'],'w');
fprintf(fid,'%12.16f  %12.16f\n',pts);
fclose(fid);


tic
dos([binpath,'dual.exe  ',num2str(resolution),' ',baseName,'.tmp', ' 0 ',num2str(featureFlag)]);
toc

if plotall == 1

ddd = dir('*quads');    
for ff = 1:length(ddd)

fileName = ddd(ff).name(1:end-5);
    
n = load([fileName,'nodes']);
q = load([fileName,'quads']);
l = load('line');

figure;
fscl = .5;
set(gcf,'Units','inches','Position',[0.5 0.5 9*fscl 9*fscl],'PaperUnits','inches')
set(gcf,'PaperSize',[9*fscl 9*fscl],'PaperPositionMode','manual')
set(gcf,'PaperPosition',[0.05 0.05 9*fscl 9*fscl]);
plot(l(:,1),l(:,2),'k-','LineWidth',2);hold on;

for qq=1:size(q,1)

    NE = q(qq,1);
    SE = q(qq,2);
    SW = q(qq,3);
    NW = q(qq,4);
    
    seq = q(qq,:);
    seq = seq(seq~=-1);
  if strcmp(fileName , 'dual') %| strcmp(fileName , 'subdivideddual')
    fill(wrap(n([seq],2)),wrap(n([seq],3)),'k-','facealpha',0.2)
  else
   plot(wrap(n([seq],2)),wrap(n([seq],3)),'k-')
 end

end
axis equal;
axis off
title(fileName);
%print(gcf,'-dtiff',[resFolder,'\\',baseName,char(titleNames{ff}),'date',date,'.tif']);
print(gcf,'-dpng',[resFolder,'\\',baseName,num2str(ff),'date',datestr(date,'yyyy-mm-dd'),'.png']);


if strcmp(fileName , 'dual') | strcmp(fileName , 'primal')

    if strcmp(fileName , 'primal')
    linestyle = ':';
    else
        linestyle = '-';
    end
    
figure(100);
fscl = .5;
set(gcf,'Units','inches','Position',[0.5 0.5 9*fscl 9*fscl],'PaperUnits','inches')
set(gcf,'PaperSize',[9*fscl 9*fscl],'PaperPositionMode','manual')
set(gcf,'PaperPosition',[0.05 0.05 9*fscl 9*fscl]);
plot(l(:,1),l(:,2),'k-','LineWidth',2);hold on;

for qq=1:size(q,1)

    NE = q(qq,1);
    SE = q(qq,2);
    SW = q(qq,3);
    NW = q(qq,4);
    
    seq = q(qq,:);
    seq = seq(seq~=-1);
 
   plot(wrap(n([seq],2)),wrap(n([seq],3)),['k',linestyle])
   

end
axis equal;
axis off



end %dual

end %file loop


figure(100);
print(gcf,'-dpng',[resFolder,'\\',baseName,'DP','date',datestr(date,'yyyy-mm-dd'),'.png']);


end %%plot all

delete *nodes
delete *polys
delete *quads
delete *tmp
delete line*

dos(['copy ',baseName,'.inp ',resFolder]);

end