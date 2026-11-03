# Import solver dynamics without running its optimization setup.
import sys, numpy as np, casadi as ca, json
from scipy.linalg import solve_discrete_are
n=int(sys.argv[1]); src=open('inertia/tools/solve_swing.py').read();exec(src[:src.index('xx=x')])
data=np.load(f'inertia/tools/swing{n}.npz');assert str(data['status'])=='success', 'Refuse an unconverged reference';T=float(data['T']);h=T/data['U'].size;U=data['U'].flatten(); X=data['X']; step=.01; steps=round(T/step)
# Integrate the reference using its physical force ramp, at 0.5 ms.
fnum=lambda y,u:np.asarray(f(y,u)).ravel()
def advance(y,u,dt):
 a=fnum(y,u);b=fnum(y+dt*a/2,u);c=fnum(y+dt*b/2,u);e=fnum(y+dt*c,u);return y+dt*(a+2*b+2*c+e)/6
refs=[]
for k in range(steps+1):
 t=k*step; node=min(len(U)-1,int((t+1e-8)/h));y=X[:,node].copy();remain=t-node*h
 for j in range(round(remain/.0005)):y=advance(y,U[node],.0005)
 refs.append(y.copy())
refs=np.array(refs)
print('Reference terminal drift',np.max(np.abs(refs[-1])),flush=True)
# The actual controller commands force through the first-order motor.
g=ca.Function('g',[x,u],[f(x,(u-x[-1])/.02)])
yy=x
for j in range(10):
 dt=.001;a=g(yy,u);b=g(yy+dt*a/2,u);c=g(yy+dt*b/2,u);e=g(yy+dt*c,u);yy+=dt*(a+2*b+2*c+e)/6
jac=ca.Function('linearize',[x,u],[ca.jacobian(yy,x),ca.jacobian(yy,u)])
# Match the next force sample under a zero-order-held command.
commands=(refs[1:,-1]-refs[:-1,-1]*np.exp(-step/.02))/(1-np.exp(-step/.02))
Q=np.diag([14]+[90]*n+[5]+[4]*n+[.001])*.01;R=np.array([[.2*.01]])
A,B=map(np.array,jac(np.zeros(ns),0));P=solve_discrete_are(A,B,Q,R);Ks=[]
for k in reversed(range(steps)):
 A,B=map(np.array,jac(refs[k],commands[k]));K=np.linalg.solve(R+B.T@P@B,B.T@P@A);P=Q+A.T@P@A-A.T@P@B@K;P=(P+P.T)/2;Ks.append(K.ravel())
Ks=Ks[::-1];rows=[np.r_[refs[k],commands[k],Ks[k]].round(9).tolist() for k in range(steps)]
json.dump({'dt':.01,'duration':T,'n':n,'rows':rows},open(f'inertia/tools/reference{n}.json','w'),separators=(',',':'))
print('exported',n,'command max',np.max(np.abs(commands)),flush=True)
