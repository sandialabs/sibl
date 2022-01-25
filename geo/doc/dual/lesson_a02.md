# Dualization Code-Only Workflow

## Goals

Generate an executable from compiling the Dualization code. This procedure does not use Python nor the Sibl environment. In this example, we compile the code and then present two approaches for running the C++ engine with a yaml file.

## Obtain Source Files

If you're choosing not to clone the whole repo, all you will need is the \*.h and \*.cpp files from:
sibl/geo/src/dual/

## Compile Dualization Code

Compile the C++ code to generate an executable. 

On a Windows machine you'll need to install a C++ compiler. The minimilist approach is to get MinGW (https://osdn.net/projects/mingw/). Once this is installed and you've added the bin folder to your path, you can compile by opening a command prompt in the folder that contains the source and header files.

On a Windows machine, compile at the command prompt.
```bash 
>g++ -O3 -std=c++11 *.cpp -o dual.exe
```  

On a Mac or Linux machine, compile at the command line.
```bash 
>g++ -O3 -std=c++11 *.cpp -o dual.out
```  

Verify it compiled properly by running the executable with no inputs. On a Windows machine, double click the executable file or run at the command prompt by typing "dual.exe". It should generate an example yml file with the inputs you'll need to specify to mesh a surface.

## Steps without Matlab

Generate an input YML file which will specify to the engine what procedures to do. For this example, use [`circle.yml`](circle.yml). Running the executable without any arguments will automatically generate a template YML file that you can modify.

```yml
boundary:circle.txt
boundary_refine:true
bounding_box:0,0,0,0
developer_output:true #false if you just want an .inp file.
output_file:circle
resolution:0.5
version:1.1
```

On a Windows machine, drag the YML file on top of the executable - make sure your boundary file has the path specified or exits in the same folder as the executable. This will generate an INP file which can be imported into many meshing and FEA software.

## Steps with Matlab

We are using Matlab as a wrapper to generate the boundary file and then run the dualization. However, you can simply use the YML file and the executable to generate the output mesh file. We are also assuming a Windows machine in the following example. If you're on a Mac or Linux, update the paths and executable call.

Open [`plotCircleEx.m`](plotCircleEx.m)In Matlab editor to see the steps. Run from the editor or command line.

```Matlab
clear all
close all

%Set path to executable if not working in the same directory
binpath = 'C:\Users\acsokol\sibl\geo\src\dual\bin\';%%%<<<< windows path, modify as needed

%Create circle geometry for this example
th = [0:5:355];
pts = [5*cosd(th)' 5*sind(th)']';
%Write circle geometry to file
fid = fopen(['circle.txt'],'w');
fprintf(fid,'%12.16f  %12.16f\n',pts);
fclose(fid);

%Run executable through Matlab dos command / Can also just drag YML file onto executable or run from command prompt
dos([binpath,'dual.exe circle.yml']); %%%<<<< windows executable extension .exe, modify as needed

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
