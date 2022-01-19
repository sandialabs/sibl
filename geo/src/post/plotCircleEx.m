clear all
close all

resFolder = datestr(date,'yyyy-mm-dd');
mkdir(resFolder);
binpath = 'C:\Users\acsokol\sibl\geo\src\dual\bin\';
delete *nodes
delete *polys
delete *quads
delete *tmp
delete line*

plotall = 1;
resolution = 1;
featureFlag = 0;
step = (5);        
th = [0:step:360-step];
baseName = 'PerfectCircle';
xp = 5*cosd(th);
yp = 5*sind(th);

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