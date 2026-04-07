from flask import Flask, render_template

app = Flask(__name__)

TOOLS = [
    {
        "name": "Inventory Tracker",
        "description": "Chemical and supply inventory across all lab locations",
        "url": "https://biochoric-inventory-tracker-production.up.railway.app/",
        "icon": "clipboard",
    },
    {
        "name": "Kidney Supercooling Dashboard",
        "description": "Real-time monitoring for kidney supercooling experiments",
        "url": "https://kidney-supercooling-dashboard.up.railway.app/",
        "icon": "thermometer",
    },
]


@app.route("/")
def index():
    return render_template("index.html", tools=TOOLS)
