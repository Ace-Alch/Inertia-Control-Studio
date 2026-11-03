import casadi as ca
import numpy as np
import sys
n=int(sys.argv[1]); T=float(sys.argv[2]) if len(sys.argv)>2 else 6.; N=int(T/.025); h=T/N; d=n+1; ns=2*d+1
ls=.55-.035*np.arange(n); ms=np.full(n,.16); hs=np.zeros(n); H=np.zeros((n,n))
for k in range(n):
 a=np.array([ls[i] if i<k else ls[i]/2 if i==k else 0 for i in range(n)])
 hs+=ms[k]*a; H+=ms[k]*np.outer(a,a); H[k,k]+=ms[k]*ls[k]**2/12
x=ca.SX.sym('x',ns); u=ca.SX.sym('u'); q=x[:d]; v=x[d:2*d]; M=ca.SX.zeros(d,d); b=ca.SX.zeros(d); M[0,0]=1+sum(ms); b[0]=.12*v[0]+.03*ca.tanh(v[0]/.02)
for i in range(n):
 M[0,i+1]=M[i+1,0]=hs[i]*ca.cos(q[i+1]); b[0]-=hs[i]*ca.sin(q[i+1])*v[i+1]**2; b[i+1]-=9.81*hs[i]*ca.sin(q[i+1])
 for j in range(n):
  M[i+1,j+1]=H[i,j]*ca.cos(q[i+1]-q[j+1]); b[i+1]+=H[i,j]*ca.sin(q[i+1]-q[j+1])*v[j+1]**2
 rel=v[i+1]-(v[i] if i else 0); loss=.006*rel+.0006*ca.tanh(rel/.05); b[i+1]+=loss
 if i:b[i]-=loss
# Use actual force derivative as optimized input. The command is F + lag*dF.
f=ca.Function('f',[x,u],[ca.vertcat(v,ca.solve(M,ca.vertcat(x[-1],ca.SX.zeros(n))-b),u)])
xx=x
for _ in range(5):
 dt=h/5; a=f(xx,u); bb=f(xx+dt*a/2,u); c=f(xx+dt*bb/2,u); e=f(xx+dt*c,u); xx=xx+dt*(a+2*bb+2*c+e)/6
F=ca.Function('F',[x,u],[xx]); op=ca.Opti(); X=op.variable(ns,N+1); U=op.variable(1,N)
start=np.zeros(ns);start[1:d]=np.pi
op.subject_to(X[:,0]==start)
for k in range(N):op.subject_to(X[:,k+1]==F(X[:,k],U[k]))
op.subject_to(op.bounded(-1.3,X[0,:],1.3));op.subject_to(op.bounded(-22,X[-1,:],22));op.subject_to(op.bounded(-400,U,400));op.subject_to(op.bounded(-24,X[-1,:-1]+.02*U,24));op.subject_to(op.bounded(-20,X[d:2*d,:],20))
op.subject_to(X[:,-1]==np.zeros(ns))
op.minimize(h*(.02*ca.sumsqr(X[-1,:])+.00002*ca.sumsqr(U)+ca.sumsqr(X[0,:])+.005*ca.sumsqr(X[d:2*d,:])))
op.solver('ipopt',{'expand':False},{'max_iter':2500,'tol':1e-7,'print_level':5,'linear_solver':'mumps'})
guess=np.zeros((ns,N+1)); tt=np.linspace(0,T,N+1)
for i in range(n):guess[i+1]=np.pi*(1-tt/T)+.5*np.sin(2*np.pi*tt/T+i*.4)*np.sin(np.pi*tt/T)
guess[0]=.7*np.sin(4*np.pi*tt/T)*np.sin(np.pi*tt/T);guess[d:2*d]=np.gradient(guess[:d],h,axis=1)
if len(sys.argv)>3:
 old=np.load(sys.argv[3]);guess=np.array([np.interp(tt,np.linspace(0,T,old['X'].shape[1]),r) for r in old['X']]);op.set_initial(U,np.interp(tt[:-1],np.linspace(0,T,old['U'].size),old['U'].flatten()))
op.set_initial(X,guess)
try:
 sol=op.solve();outX=sol.value(X);outU=sol.value(U);status='success'
except Exception:
 outX=op.debug.value(X);outU=op.debug.value(U);status='failed'
np.savez(f'inertia/tools/swing{n}.npz',X=outX,U=outU,T=T,status=status)
print(status,flush=True)

if status != "success": sys.exit(1)
