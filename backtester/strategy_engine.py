import ast,operator,numpy as np
ALLOWED={'open','high','low','close','previous_open','previous_high','previous_low','previous_close'}
FUN={'abs':abs,'min':min,'max':max,'round':round}
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.USub:operator.neg}
def safe_formula(expr,ctx):
 def ev(n):
  if isinstance(n,ast.Expression): return ev(n.body)
  if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
  if isinstance(n,ast.Name) and n.id in ALLOWED: return float(ctx[n.id])
  if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left),ev(n.right))
  if isinstance(n,ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.operand))
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in FUN: return FUN[n.func.id](*[ev(a) for a in n.args])
  raise ValueError('Formula contains unsupported syntax')
 tree=ast.parse(expr,mode='eval'); return float(ev(tree))
def levels(df,formula):
 out=[]
 for i in range(len(df)):
  if i==0: out.append(np.nan); continue
  r=df.iloc[i]; p=df.iloc[i-1]
  c={'open':r.Open,'high':r.High,'low':r.Low,'close':r.Close,'previous_open':p.Open,'previous_high':p.High,'previous_low':p.Low,'previous_close':p.Close}
  out.append(safe_formula(formula,c))
 return np.array(out,float)
