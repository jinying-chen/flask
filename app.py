#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask 天氣搜尋應用程式
支援搜尋全球城市的天氣資訊（使用 wttr.in API，無需 API Key）
"""

import os
from datetime import datetime
from urllib.parse import quote

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

WEATHER_API_URL = "https://wttr.in"
REQUEST_HEADERS = {"User-Agent": "curl/8.0"}


def get_weather(city):
    """
    取得指定城市的天氣資訊。

    參數:
        city: 城市名稱（支援中文，例如：台北、東京）

    回傳:
        dict: 含 success 與天氣欄位，或錯誤訊息
    """
    try:
        encoded_city = quote(city.strip())
        url = f"{WEATHER_API_URL}/{encoded_city}?format=j1"
        response = requests.get(
            url, headers=REQUEST_HEADERS, timeout=10
        )
        response.encoding = "utf-8"

        if response.status_code != 200:
            return {
                "success": False,
                "message": f"找不到城市：{city}",
            }

        data = response.json()
        current = data["current_condition"][0]

        return {
            "success": True,
            "city": city,
            "temperature": current["temp_C"],
            "condition": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "wind_speed": current["windspeedKmph"],
            "feels_like": current["FeelsLikeC"],
            "visibility": current["visibility"],
            "pressure": current["pressure"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"網路錯誤：{str(e)}",
        }
    except (KeyError, IndexError, ValueError) as e:
        return {
            "success": False,
            "message": f"無法解析天氣資料：{str(e)}",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"錯誤：{str(e)}",
        }


@app.route("/")
def index():
    """首頁：天氣搜尋介面"""
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search_weather():
    """天氣搜尋 API（前端以 JSON POST 呼叫）"""
    data = request.get_json(silent=True) or {}
    city = (data.get("city") or "").strip()

    if not city:
        return jsonify({"success": False, "message": "請輸入城市名稱"})

    return jsonify(get_weather(city))


@app.route("/weather/<city>")
def get_city_weather(city):
    """直接以 URL 查詢城市天氣（JSON）"""
    return jsonify(get_weather(city))


@app.route("/api/status")
def status():
    """應用狀態檢查"""
    return jsonify(
        {
            "status": "running",
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    print("=" * 50)
    print("    Flask 天氣搜尋應用")
    print("=" * 50)
    print(f"訪問地址: http://localhost:{port}")
    print("=" * 50)
    app.run(debug=debug, host="0.0.0.0", port=port)
