import os,uuid,json
import pandas as pd, numpy as np
from flask import Flask,render_template,request,redirect,url_for,flash,session,send_file
from werkzeug.utils import secure_filename
from backtester.engine import run
app=Flask(__name__); app.secret_key='change-this-secret'; app.config['MAX_CONTENT_LENGTH']=50*1024*1024
os.makedirs('uploads',exist_ok=True); os.makedirs('results',exist_ok=True)
def load_csv(path):
 df=pd.read_csv(path); df.columns=[c.strip().title() for c in df.columns]
 req=['Date','Open','High','Low','Close']; miss=[c for c in req if c not in df]
 if miss: raise ValueError('Missing required columns: '+', '.join(miss))
 df['Date']=pd.to_datetime(df.Date,errors='coerce');
 for c in req[1:]: df[c]=pd.to_numeric(df[c],errors='coerce')
 df=df.dropna(subset=req).drop_duplicates('Date').sort_values('Date')
 valid=(df.High>=df[['Open','Close','Low']].max(axis=1))&(df.Low<=df[['Open','Close','High']].min(axis=1))
 df=df[valid].reset_index(drop=True)
 if len(df)<2: raise ValueError('CSV has insufficient valid candles')
 return df
def current_df(): return load_csv(session['csv']) if session.get('csv') else None
@app.route('/')
def index():
 df=current_df() if session.get('csv') else None
 info=None
 if df is not None: info={'candles':len(df),'start':str(df.Date.iloc[0]),'end':str(df.Date.iloc[-1]),'preview':df.head(8).to_html(classes='data-table',index=False)}
 return render_template('index.html',info=info)
@app.route('/upload',methods=['POST'])
def upload():
 f=request.files.get('file')
 try:
  if not f or not f.filename.lower().endswith('.csv'): raise ValueError('Please upload a CSV file')
  path=os.path.join('uploads',uuid.uuid4().hex+'_'+secure_filename(f.filename)); f.save(path); df=load_csv(path); session['csv']=path; flash(f'Uploaded {len(df):,} valid candles','success')
 except Exception as e: flash(str(e),'error')
 return redirect(url_for('index'))
@app.route('/strategy')
def strategy(): return render_template('strategy.html')
@app.route('/backtest',methods=['POST'])
def backtest():
 try:
  df=current_df();
  if df is None: raise ValueError('Upload CSV data first')
  cfg=request.form.to_dict(); trades,m,levels=run(df,cfg); rid=uuid.uuid4().hex
  pd.DataFrame(trades).to_csv(f'results/{rid}_trades.csv',index=False); json.dump({'metrics':m,'config':cfg},open(f'results/{rid}.json','w'),default=lambda x: None); session['result']=rid
  return redirect(url_for('results'))
 except Exception as e: flash(str(e),'error'); return redirect(url_for('strategy'))
@app.route('/results')
def results():
 rid=session.get('result'); data=json.load(open(f'results/{rid}.json')) if rid else None
 return render_template('results.html',data=data)
@app.route('/trades')
def trades():
 rid=session.get('result'); rows=[]
 if rid and os.path.exists(f'results/{rid}_trades.csv'): rows=pd.read_csv(f'results/{rid}_trades.csv').to_dict('records')
 return render_template('trades.html',trades=rows)
@app.route('/export/trades')
def export_trades():
 rid=session.get('result'); return send_file(f'results/{rid}_trades.csv',as_attachment=True,download_name='trade_history.csv')
if __name__=='__main__': app.run(debug=True,host='0.0.0.0',port=5000)
