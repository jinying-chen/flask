#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask 天氣搜尋應用程式
支持搜尋全球任何城市的天氣資訊
"""

from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 支持中文顯示

# 天氣 API 配置（使用免費的 wttr.in API）
WEATHER_API_URL = "https://wttr.in"

def get_weather(city):
    """
    獲取城市天氣信息
    使用 wttr.in API（無需 API KEY）
    """
    try:
        # 請求天氣數據（JSON 格式）
        url = f"{WEATHER_API_URL}/{city}?format=j1"
        response = requests.get(url, timeout=5)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            
            # 提取當前天氣信息
            current = data['current_condition'][0]
            
            weather_info = {
                'success': True,
                'city': city,
                'temperature': current['temp_C'],
                'condition': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'feels_like': current['FeelsLikeC'],
                'visibility': current['visibility'],
                'pressure': current['pressure'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return weather_info
        else:
            return {
                'success': False,
                'message': f"找不到城市: {city}"
            }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f"網絡錯誤: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"錯誤: {str(e)}"
        }

@app.route('/')
def index():
    """主頁路由"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_weather():
    """天氣搜尋 API 端點"""
    data = request.get_json()
    city = data.get('city', '').strip()
    
    if not city:
        return jsonify({
            'success': False,
            'message': '請輸入城市名稱'
        })
    
    weather_data = get_weather(city)
    return jsonify(weather_data)

@app.route('/weather/<city>')
def get_city_weather(city):
    """直接訪問城市天氣"""
    weather_data = get_weather(city)
    return jsonify(weather_data)

@app.route('/api/status')
def status():
    """應用狀態檢查"""
    return jsonify({
        'status': 'running',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 50)
    print("    Flask 天氣搜尋應用")
    print("=" * 50)
    print("🌐 訪問地址: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
