# Dualization Code Only Workflow

## Goals

Generate an executable from compiling the Dualization code. This procedure does not use Python nor the Sibl environment. In this example, we use MATLAB and text file interop to run the C++ engine and post-process results. Matlab is not required and is only used to generate the boundary file and plot the results.

## Obtain Source Files

If you're choosing not to clone the whole repo, all you will need is the \*.h and \*.cpp files from:
sibl/geo/src/dual/

## Compile Dualization Code

Compile the C++ code to generate an executable. 

On a Mac or Linux machine, compile at the command line and renaming the a.out executable.
```bash 
>g++ -O3 -std=c++11 *.cpp
>mv a.out dual.out
```  

On a Windows machine you'll need to install a C++ compiler. Use your favorite IDE and have g++ follow the C++11 ISO standard. 

One possible route is to use Code::Blocks with MinGW. With this software, create a new project that is a console application. Add all the .cpp and .h files to the project. Under Project->Build Options you'll need to select "... follow the C++11 ISO ...". Under Build-> Select Target, pick "Release", and then Build->Build. This will generate an executable in a "bin" subfolder which you can freely move about.

## Steps

Generate an input YML file which will specify to the engine what procedures to do. For this example, use [`circle.yml`](circle.yml). Running the executable without any arguments will automatically generate a template YML file that you can modify.

```yml
boundary:circle.txt
boundary_refine:true
bounding_box:0,0,0,0
developer_output:true
output_file:circle
resolution:0.5
version:1.1
```

We are using Matlab as a wrapper to generate the boundary file and then run the dualization. However, you can simply use the YML file and the executable to generate the output mesh file.

Open [`plotCircleEx.m`](plotCircleEx.m)In Matlab editor to see the steps. Run from the editor or command line.

```Matlab
clear all
close all

%Set path to executable if not working in the same directory
binpath = 'C:\Users\acsokol\sibl\geo\src\dual\bin\';

%Create circle geometry for this example
th = [0:5:355];
pts = [5*cosd(th)' 5*sind(th)']';
%Write circle geometry to file
fid = fopen(['circle.txt'],'w');
fprintf(fid,'%12.16f  %12.16f\n',pts);
fclose(fid);

%Run executable through Matlab dos command / Can also just drag YML file onto executable or run from command prompt
dos([binpath,'dual.exe circle.yml']); %%%<<<< windows executable extension .exe , modify as needed

n = load('dualnodes');
q = load('dualquads');

figure;
plot(pts(1,:),pts(2,:),'k-','LineWidth',2);hold on;
for qq=1:size(q,1)
   seq = [q(qq,:) q(qq,1)]; %close the loops
   plot(n(seq,2),n(seq,3),'k-')
end
axis equal;
axis off
print(gcf,'-dpng',['circle.png']);
```

Running the Matlab script will generate this figure:

![circle_boundary](fig/circle.png)

[Index](README.md)
