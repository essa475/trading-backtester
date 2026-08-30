import numpy as np,pandas as pd
def calc(trades,initial):
 t=pd.DataFrame(trades); equity=[initial]+(t.balance_after.tolist() if len(t) else [])
 e=np.array(equity,float); peaks=np.maximum.accumulate(e); dd=e-peaks; ddp=np.divide(dd,peaks,out=np.zeros_like(dd),where=peaks!=0)*100
 if len(t)==0:return {'total_trades':0,'initial_balance':initial,'final_balance':initial,'net_profit':0,'net_profit_pct':0,'win_rate':0,'profit_factor':0,'max_drawdown':0,'max_drawdown_pct':0,'equity':equity,'drawdown':ddp.tolist()}
 p=t.pnl; wins=p[p>0]; losses=p[p<0]; gp=wins.sum(); gl=losses.sum(); pf=float(gp/abs(gl)) if gl else None
 return {'total_trades':len(t),'initial_balance':initial,'final_balance':float(e[-1]),'net_profit':float(p.sum()),'net_profit_pct':float(p.sum()/initial*100),'winning_trades':int((p>0).sum()),'losing_trades':int((p<0).sum()),'breakeven_trades':int((p==0).sum()),'win_rate':float((p>0).mean()*100),'gross_profit':float(gp),'gross_loss':float(gl),'profit_factor':pf,'average_trade':float(p.mean()),'largest_win':float(p.max()),'largest_loss':float(p.min()),'max_drawdown':float(dd.min()),'max_drawdown_pct':float(ddp.min()),'equity':equity,'drawdown':ddp.tolist()}
