% This is a matlab script for 3d visualization of VASPKIT generated datagrid.
% Copyright 2020 Vei WANG <wangvei@icloud.com>

clc
clear
file = input(" Input the file name with quotation marks (e.g. 'EMC_hole.dat'): ");
%disp(file)
data=dlmread(file,'',1,0);
phi=data(:,1)*pi/180;
theta=data(:,2)*pi/180;
R=data(:,3);  
nphi=500;
ntheta=500;
phinew=linspace(0,pi,nphi);
thetanew=linspace(0,2*pi,ntheta);
[yy,xx]=meshgrid(thetanew,phinew);
y=zeros(nphi,ntheta);
z=zeros(nphi,ntheta);
x=zeros(nphi,ntheta);
Rnew=griddata(phi,theta,R,xx,yy,'cubic');
for j=1:nphi
    for i=1:ntheta
        iphi=xx(j,i);
        itheta=yy(j,i);
        iR=Rnew(j,i);
        x(j,i)=iR*cos(itheta)*sin(iphi);      
        y(j,i)=iR*sin(itheta)*sin(iphi);      
        z(j,i)=iR*cos(iphi);       
    end
end
colormap jet
surf(x,y,z,abs(Rnew),'FaceColor','interp','EdgeColor','none','FaceLighting','gouraud')
%surf(x,y,z,abs(Rnew),'FaceLighting','gouraud')
%surf(x,y,z,Rnew,'FaceColor','interp','EdgeColor','none')
shading interp;
camlight left
light;
lighting flat;
h=colorbar('position',[0.85,0.342,0.03,0.25]);   %[left, bottom, width, height] 
t=get(h,'Limits');
T=linspace(t(1),t(2),4);
set(h,'Ticks',T);
TL=arrayfun(@(x) sprintf('%.3f',x),T,'un',0);
set(h,'TickLabels',TL);
%title('Bulk modulus')
view(90,39)
axis equal 
axis off
hold on
set(gca,'Fontsize',30)
set(gcf,'position',[200,300,800,600])
flex_factor=1.5;
mArrow3([0 0 0],[flex_factor*max(R) 0 0],'color','red','stemWidth',max(R)/100,'facealpha',0.5);
mArrow3([0 0 0],[0 flex_factor*max(R) 0],'color','green','stemWidth',max(R)/100);
mArrow3([0 0 0],[0 0 flex_factor*max(R)],'color','blue','stemWidth',max(R)/100);
text(flex_factor*max(R),0,0,'x','FontSize',35)
text(0,flex_factor*max(R),0,'y','FontSize',35)
text(0,0,flex_factor*max(R),'z','FontSize',35)
hold off





function h = mArrow3(p1,p2,varargin)
%mArrow3 - plot a 3D arrow as patch object (cylinder+cone)
%
% syntax:   h = mArrow3(p1,p2)
%           h = mArrow3(p1,p2,'propertyName',propertyValue,...)
%
% with:     p1:         starting point
%           p2:         end point
%           properties: 'color':      color according to MATLAB specification
%                                     (see MATLAB help item 'ColorSpec')
%                       'stemWidth':  width of the line
%                       'tipWidth':   width of the cone                       
%
%           Additionally, you can specify any patch object properties. (For
%           example, you can make the arrow semitransparent by using
%           'facealpha'.)
%                       
% example1: h = mArrow3([0 0 0],[1 1 1])
%           (Draws an arrow from [0 0 0] to [1 1 1] with default properties.)
%
% example2: h = mArrow3([0 0 0],[1 1 1],'color','red','stemWidth',0.02,'facealpha',0.5)
%           (Draws a red semitransparent arrow with a stem width of 0.02 units.)
%
% hint:     use light to achieve 3D impression
%

propertyNames = {'edgeColor'};
propertyValues = {'none'};    

%% evaluate property specifications
for argno = 1:2:nargin-2
    switch varargin{argno}
        case 'color'
            propertyNames = {propertyNames{:},'facecolor'};
            propertyValues = {propertyValues{:},varargin{argno+1}};
        case 'stemWidth'
            if isreal(varargin{argno+1})
                stemWidth = varargin{argno+1};
            else
                warning('mArrow3:stemWidth','stemWidth must be a real number');
            end
        case 'tipWidth'
            if isreal(varargin{argno+1})
                tipWidth = varargin{argno+1};
            else
                warning('mArrow3:tipWidth','tipWidth must be a real number');
            end
        otherwise
            propertyNames = {propertyNames{:},varargin{argno}};
            propertyValues = {propertyValues{:},varargin{argno+1}};
    end
end            

%% default parameters
if ~exist('stemWidth','var')
    ax = axis;
    if numel(ax)==4
        stemWidth = norm(ax([2 4])-ax([1 3]))/300;
    elseif numel(ax)==6
        stemWidth = norm(ax([2 4 6])-ax([1 3 5]))/300;
    end
end
if ~exist('tipWidth','var')
    tipWidth = 3*stemWidth;
end
tipAngle = 22.5/180*pi;
tipLength = tipWidth/tan(tipAngle/2);
ppsc = 50;  % (points per small circle)
ppbc = 250; % (points per big circle)

%% ensure column vectors
p1 = p1(:);
p2 = p2(:);

%% basic lengths and vectors
x = (p2-p1)/norm(p2-p1); % (unit vector in arrow direction)
y = cross(x,[0;0;1]);    % (y and z are unit vectors orthogonal to arrow)
if norm(y)<0.1
    y = cross(x,[0;1;0]);
end
y = y/norm(y);
z = cross(x,y);
z = z/norm(z);

%% basic angles
theta = 0:2*pi/ppsc:2*pi; % (list of angles from 0 to 2*pi for small circle)
sintheta = sin(theta);
costheta = cos(theta);
upsilon = 0:2*pi/ppbc:2*pi; % (list of angles from 0 to 2*pi for big circle)
sinupsilon = sin(upsilon);
cosupsilon = cos(upsilon);

%% initialize face matrix
f = NaN([ppsc+ppbc+2 ppbc+1]);

%% normal arrow
if norm(p2-p1)>tipLength
    % vertices of the first stem circle
    for idx = 1:ppsc+1
        v(idx,:) = p1 + stemWidth*(sintheta(idx)*y + costheta(idx)*z);
    end
    % vertices of the second stem circle
    p3 = p2-tipLength*x;
    for idx = 1:ppsc+1
        v(ppsc+1+idx,:) = p3 + stemWidth*(sintheta(idx)*y + costheta(idx)*z);
    end
    % vertices of the tip circle
    for idx = 1:ppbc+1
        v(2*ppsc+2+idx,:) = p3 + tipWidth*(sinupsilon(idx)*y + cosupsilon(idx)*z);
    end
    % vertex of the tiptip
    v(2*ppsc+ppbc+4,:) = p2;

    % face of the stem circle
    f(1,1:ppsc+1) = 1:ppsc+1;
    % faces of the stem cylinder
    for idx = 1:ppsc
        f(1+idx,1:4) = [idx idx+1 ppsc+1+idx+1 ppsc+1+idx];
    end
    % face of the tip circle
    f(ppsc+2,:) = 2*ppsc+3:(2*ppsc+3)+ppbc;
    % faces of the tip cone
    for idx = 1:ppbc
        f(ppsc+2+idx,1:3) = [2*ppsc+2+idx 2*ppsc+2+idx+1 2*ppsc+ppbc+4];
    end

%% only cone v
else
    tipWidth = 2*sin(tipAngle/2)*norm(p2-p1);
    % vertices of the tip circle
    for idx = 1:ppbc+1
        v(idx,:) = p1 + tipWidth*(sinupsilon(idx)*y + cosupsilon(idx)*z);
    end
    % vertex of the tiptip
    v(ppbc+2,:) = p2;
    % face of the tip circle
    f(1,:) = 1:ppbc+1;
    % faces of the tip cone
    for idx = 1:ppbc
        f(1+idx,1:3) = [idx idx+1 ppbc+2];
    end
end

%% draw
fv.faces = f;
fv.vertices = v;
h = patch(fv);
for propno = 1:numel(propertyNames)
    try
        set(h,propertyNames{propno},propertyValues{propno});
    catch
        disp(lasterr)
    end
end
end

