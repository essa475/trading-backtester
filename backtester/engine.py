from .strategy_engine import levels
from .metrics import calc
def run(df,cfg):
 formula=cfg.get('formula','(previous_high + previous_low) / 2'); lv=levels(df,formula); bal=float(cfg.get('initial_balance',10000)); riskpct=float(cfg.get('risk_percent',1))/100; rr=float(cfg.get('rr',2)); point=float(cfg.get('point_value',1)); trades=[]; pos=None
 for i in range(1,len(df)):
  r=df.iloc[i]; prev=df.iloc[i-1]
  # manage existing position; conservative when both touched
  if pos:
   slhit=r.Low<=pos['sl']; tphit=r.High>=pos['tp']
   if slhit or tphit:
    exitp=pos['sl'] if slhit else pos['tp']; reason='STOP LOSS' if slhit else 'TAKE PROFIT'
    pnl=(exitp-pos['entry'])*pos['size']*point; bal+=pnl
    trades.append(dict(number=len(trades)+1,direction='BUY',entry_date=str(pos['date']),exit_date=str(r.Date),entry=pos['entry'],exit=exitp,stop_loss=pos['sl'],take_profit=pos['tp'],position_size=pos['size'],risk_amount=pos['risk'],pnl=pnl,result='WIN' if pnl>0 else 'LOSS' if pnl<0 else 'BREAKEVEN',balance_after=bal,entry_reason='Level touch',exit_reason=reason,duration=i-pos['idx']))
    pos=None
   continue
  level=lv[i]
  if level==level and r.Low<=level<=r.High:
   entry=level; sl=float(prev.Low); riskper=entry-sl
   if riskper>0:
    risk=bal*riskpct; size=risk/(riskper*point); tp=entry+riskper*rr
    pos={'entry':entry,'sl':sl,'tp':tp,'size':size,'risk':risk,'date':r.Date,'idx':i}
 if pos:
  r=df.iloc[-1]; pnl=(r.Close-pos['entry'])*pos['size']*point; bal+=pnl; trades.append(dict(number=len(trades)+1,direction='BUY',entry_date=str(pos['date']),exit_date=str(r.Date),entry=pos['entry'],exit=r.Close,stop_loss=pos['sl'],take_profit=pos['tp'],position_size=pos['size'],risk_amount=pos['risk'],pnl=pnl,result='OPEN',balance_after=bal,entry_reason='Level touch',exit_reason='End of data',duration=len(df)-1-pos['idx']))
 return trades,calc(trades,float(cfg.get('initial_balance',10000))),lv
