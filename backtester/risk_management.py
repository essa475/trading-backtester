def position_size(balance,risk_pct,entry,stop,point_value=1):
 risk=balance*risk_pct/100; d=abs(entry-stop)*point_value
 if d<=0: raise ValueError('Invalid stop distance')
 return risk/d,risk
