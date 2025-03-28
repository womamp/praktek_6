from flask import Flask, jsonify, request

app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    items.append(data)
    return jsonify({"message": "Item added successfully"}), 201

@app.route('/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    if 0 <= index < len(items):
        deleted = items.pop(index)
        return jsonify({"message": "Item deleted", "item": deleted})
    return jsonify({"error": "Index out of range"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

tracer = Tracer(exporter=AzureExporter(connection_string="InstrumentationKey=YOUR_INSTRUMENTATION_KEY"),
                sampler=ProbabilitySampler(1.0))

@app.before_request
def trace_request():
    tracer.span(name=request.path)
