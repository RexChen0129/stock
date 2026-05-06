import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import yfinance as yf
import pandas as pd

app = FastAPI()

@app.get("/api/stock/{code}")
def get_stock_data(code: str):
    # 對應台灣股市代號格式 (例如 2330 -> 2330.TW)
    ticker = f"{code}.TW"
    data = yf.download(ticker, period="1mo", interval="1d")
    
    if data.empty:
        return {"error": "找不到股票資料"}
    
    # 格式化數據供前端使用
    result = []
    for index, row in data.iterrows():
        result.append({
            "d": index.strftime('%m/%d'),
            "o": float(row['Open']),
            "h": float(row['High']),
            "l": float(row['Low']),
            "c": float(row['Close']),
            "v": float(row['Volume'])
        })
    return result

@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>股票查詢系統 - 真實數據版</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background: #0a0e27; color: #00ff88; font-family: sans-serif; padding: 20px; }
        .container { max-width: 1000px; margin: auto; }
        .chart-container { height: 400px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; }
        input { padding: 10px; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #00ff88; border: none; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>台灣股票查詢系統 (Real-time)</h1>
        <input type="text" id="stockInput" value="2330" placeholder="輸入代碼 (如 2330)">
        <button onclick="fetchStockData()">查詢</button>
        <p id="info"></p>
        <div class="chart-container">
            <canvas id="klineChart"></canvas>
        </div>
    </div>

    <script>
        let klineChart = null;

        async function fetchStockData() {
            const code = document.getElementById('stockInput').value;
            const response = await fetch(`/api/stock/${code}`);
            const data = await response.json();
            
            if(data.error) {
                alert(data.error);
                return;
            }

            const lastPrice = data[data.length - 1].c;
            document.getElementById('info').innerText = `目前股票: ${code} | 最新價: ${lastPrice}`;

            renderChart(data);
        }

        function renderChart(data) {
            const ctx = document.getElementById('klineChart').getContext('2d');
            const labels = data.map(d => d.d);
            const floatingData = data.map(d => [d.o, d.c]);
            const colors = data.map(d => d.c >= d.o ? '#ff4d4d' : '#26a69a');

            if (klineChart) klineChart.destroy();

            klineChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'K線棒 (收盤價)',
                        data: floatingData,
                        backgroundColor: colors,
                        borderColor: colors,
                        barPercentage: 0.8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: false, // 關鍵：根據 2250 這種高價自動縮放
                            ticks: { color: '#00ccff' }
                        },
                        x: { ticks: { color: '#00ccff' } }
                    },
                    plugins: {
                        legend: { labels: { color: '#00ff88' } }
                    }
                }
            });
        }

        // 初始載入
        fetchStockData();
    </script>
</body>
</html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)