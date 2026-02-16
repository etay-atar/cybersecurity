from flask import Flask, render_template, request, Response, stream_with_context
import json
import time
from simple_port_scanner import scan_ports_generator, get_host_ip

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    target = request.args.get('target')
    start_port = int(request.args.get('start_port', 1))
    end_port = int(request.args.get('end_port', 1024))
    threads = int(request.args.get('threads', 100))

    target_ip = get_host_ip(target)
    if not target_ip:
        def generate_error():
            yield f"data: {json.dumps({'type': 'error', 'message': f'Could not resolve host {target}'})}\n\n"
        return Response(generate_error(), mimetype='text/event-stream')

    def generate():
        yield f"data: {json.dumps({'type': 'info', 'message': f'Scanning {target} ({target_ip})...'})}\n\n"
        for event in scan_ports_generator(target_ip, start_port, end_port, threads):
            yield f"data: {json.dumps(event)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
