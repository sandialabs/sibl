%print quads
clear all
close all

resFolder = datestr(date,'yyyy-mm-dd');
mkdir(resFolder);
binpath = 'C:\Users\acsokol\sibl\geo\src\dual\bin\';
delete *nodes
delete *polys
delete *quads
delete *tmp


testCase = 8
resolution = 1;

  switch testCase
        case -4  %Matryoshka
          step = (360/2);        
           
          baseName = 'CentRef';
          xp=[5 -5 0.1];
          yp =[5 -5 0.1];
          
          resolution = 1;
        case -3  %Matryoshka
          step = (360/2);        
           
          baseName = 'Matryoshka';
          rvals = [  4 6];
          th = [-180:0];
          xp=[];
          yp =[];
          for rr=1:length(rvals)
            tx = cosd(th)*rvals(rr);
            ty = -sind(th)*rvals(rr);
            xp = [xp tx+2*sum(rvals(1:rr))];
            yp =[yp ty];
          end
          xp = xp-mean(xp);
          resolution = 1;
       case -2  %Legacy Line Case 
          step = (360/2);        
           
          baseName = 'Tripole';
          xp =[ -10 -10 -10 0 10 0 ]+.1;
          yp = [ 10 0 -10 0 10 10]+.1;
          resolution = 10*sqrt(2);
      case -1  %Legacy Line Case 
          step = (360/2);        
          th = [3] ;%[0:step:360];
          
          baseName = 'Monopole';
          xp = th;
          yp = th;
          resolution = 1;
      case 0  %Legacy Line Case 
          step = (360/2);        
          th = [-1 1]*10 ;%[0:step:360];
          
          baseName = 'Dipole';
          xp = th;
          yp = th;
          resolution = 10*sqrt(2);
      case 1  %Legacy Line Case 
          step = (360/2);        
          th = [0:step:360];
          
          baseName = 'Line3Pt';
          xp = th/360*10-5;
          yp = th/360*40-20;
          resolution = 4;
        
      case 2
          step = (360/5);        
          th = [0:step:360];
          baseName = 'Line5Pt';
          xp = th/360*10-5;
          yp = th/360*40-20;
          resolution = 2;
        
      case 3
          step = (360/8);        
          th = [0:step:360];
          baseName = 'Line5Pt';
          xp = th/360*10-5;
          yp = th/360*40-20;
          resolution = 2;
         
       case 4
          step = (.1);        
          th = [0:step:360-step];
          baseName = 'PerfectCircle';
         xp = 10*cosd(th);
         yp = 10*sind(th);
          resolution = 10*sqrt(2)*0.1%;
          resolution =.2
           case 5
          step = (.1);        
          th = [0:step:360-step];
          baseName = 'HigherResolutionPerfectCircle';
         xp = 10*cosd(th);
         yp = 10*sind(th);
          resolution = .2;
         
           case 6
          step = (1);        
          th = [0:step:360-step];
          baseName = 'ShiftedOval';
         xp = 8*cosd(th)-2;
         yp = 10*sind(th);
          resolution = 1;
         
          case 7
          step = (1);        
          th = [0:step:360-step];
          baseName = 'Squiggle';
        xp = 5.86*cosd(th+30)+0.4*cosd(2*th);
            yp = 2.86*sind(th+30)+.5*sind(3*th+30);
            xp =xp*4
         yp = yp*4
          resolution = .5;
          
        
            case 8
          step = (.1);        
          th = [0:step:360-step];
          baseName = 'NestedCircle';
        xp = 10*cosd(th);
         yp = 10*sind(th);
         xp2 = 4*cosd(th);
         yp2 = 4*sind(th);
         xp =[xp NaN reverse(xp2)];
         yp =[yp NaN reverse(yp2)];
          resolution = 1;
         
         
        case 9
          step = (.1);        
          th = [0:step:360-step];
          baseName = 'Square';
            
          edge1 = [-10:.1:10];
          edge2 = edge1*0+1;
          
          xp = [edge1 edge2*10 reverse(edge1) -edge2*10];
          yp = [-edge2*10 edge1 edge2*10 reverse(edge1)];
          
        
          resolution = 1;
          
      
      case 10
          skipPlot = 0;
          step = (.01);        
          th = [0:step:45/2-step]/180*pi;
          baseName = 'Flower';
       
            inch = 10;
            SkullRad = 4*inch;SkullLoft = 0.125*inch;

            SkullX = cos(th)*SkullRad;
            SkullY = sin(th)*SkullRad;
            CSFX = cos(th)*(SkullRad-SkullLoft);
            CSFY = sin(th)*(SkullRad-SkullLoft);
            BrainRad = 3*inch;

            BrainLoft = 0.5*inch;


            SulciN = 16;
            SulciA = 0.75*inch;


            BrainR = BrainRad +(1- cos(th*SulciN).^6)*SulciA;
            BrainIn = BrainR-BrainLoft


            BrainX = cos(th).*BrainR;
            BrainY = sin(th).*BrainR;

            BrainXIn = cos(th).*BrainIn;
            BrainYIn = sin(th).*BrainIn;
          
         
            minx = min(BrainX);
         xp =[BrainX  reverse(BrainXIn)];
         yp =[BrainY  reverse(BrainYIn)];
         
         inds = find(xp>minx);
         xp=xp(inds);
         yp=yp(inds);
  
         xp=wrap(xp);
         yp = wrap(yp);
         
          resolution = .1;
  
          arclen = [0 cumsum(sqrt(diff((xp)).^2+diff((yp)).^2))];
         
          
          xp = interp1(arclen,xp,[0:resolution/10:max(arclen)]);
          yp = interp1(arclen,yp,[0:resolution/10:max(arclen)]);
          
         
          showLabel=0;
           case 11
          step = (.1);        
          th = [0:step:360-step];
          baseName = 'Squiggle';
        xp = 5.86*cosd(th+30)+0.4*cosd(2*th);
            yp = 2.86*sind(th+30)+1.5*sind(4*th+30);
            xp =xp*4
         yp = yp*4
          resolution = 1;
          
       case 12
          step = (1);        
          th = [0:step:360-step];
          baseName = 'L-Corner';
            
          edge1 = [-10:.1:10];
          edge3 = [0:.1:10];
          edge2 = edge1*0+1;
          edge4 = edge3*0+1;
          
          xp = [edge1 edge4*10 reverse(edge3) edge4*0 reverse(edge3)-10 -edge2*10];
          yp = [-edge2*10 edge3-10 0*edge4 edge3 10*edge4 reverse(edge1)];
     
          resolution = 2;
         
          case 13
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
          
          xp = [arcx edge1 edge2a reverse(edge2) edge10 ];
          yp = [arcy edge10 edge2 edge2a reverse(edge1) ];
          
%           xp =[ edge2 edge2a reverse(edge2) edge20];
%           yp = [edge20 edge2 edge2a reverse(edge2)];
%           
%           xp = [xp NaN arcx 0];
%           yp = [yp NaN arcy 0];
%           
          
            rp = sqrt(xp.^2+yp.^2);
            thp = atan2d(yp,xp)+90;
            xp = cosd(thp).*rp;
            yp = sind(thp).*rp;
            
          
          resolution = .125;
         baseName = 'Hughes' ;%['Hughes',num2str(resolution)];
           case -9
          step = (.01);        
          th = [0:step:360-step];
          baseName = 'SwissCheese';
            
          edge1 = [-10:.01:10];
          edge2 = edge1*0+1;
          
          xp = [edge1 edge2*10 reverse(edge1) -edge2*10];
          yp = [-edge2*10 edge1 edge2*10 reverse(edge1)];
          
            th = [0:step:360-step];
            
     
         xp2 = 4*cosd(th)-2;
         yp2 = 4*sind(th);
         xp =[xp NaN reverse(xp2)];
         yp =[yp NaN reverse(yp2)];
          
         
          xp2 = 2*cosd(th)+5;
         yp2 = 2*sind(th)+3;
         xp =[xp NaN reverse(xp2)];
         yp =[yp NaN reverse(yp2)];
          
            xp2 = 3*cosd(th)+1;
         yp2 = 3*sind(th)-6;
         xp =[xp NaN reverse(xp2)];
         yp =[yp NaN reverse(yp2)];
          
          resolution = .25;
      otherwise
          
            disp('Unknown method.')
  end
  
  
%  baseName = [baseName,num2str(resolution),'m',num2str(quadOrCube)];

pts = [(xp)' (yp)']';
baseName = [baseName];
fid = fopen([baseName,'.tmp'],'w');
fprintf(fid,'%12.16f  %12.16f\n',pts);
fclose(fid);


tic
dos([binpath,'dual.exe  ',num2str(resolution),' ',baseName,'.tmp', ' 0']);
toc



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
delete *nodes
delete *polys
delete *quads
delete *tmp

figure(100);
print(gcf,'-dpng',[resFolder,'\\',baseName,'DP','date',datestr(date,'yyyy-mm-dd'),'.png']);
% 
% figure;
% n=load('sph');
% plot3(n(:,1),n(:,2),n(:,3),'o');
% axis equal