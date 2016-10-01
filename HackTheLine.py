from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

# name and event object pair
all_event = {}


class Event(object):
    def __init__(self):
        self.data = None


@app.route('/host/create_event', methods=['POST'])
def create_event():
    """
    expected data format
    data = {
        host_email: 'Juliang075@tamu.edu',
        event_name: 'TamuHack',
        event_address: '1237 TAMU College Station, Texas 77843-1237',
        lat: 30.619378,
        lng: -96.3380669,
        allow_radius: 100,
        files: [
            {"code-of-conduct.md": 'content'},
            {"community-values.md":'another content'}
        ],
        registrants: ['juliang075@tamu.edu','ellenstanfill@tamu.edu']
    }
    """
    data = request.get_json(force=True)
    if not data:
        return jsonify(**{'succeed': False, 'data': []})
    new_event = Event()
    new_event.data = data
    new_event.data['registrants'] = {email: False for email in new_event.data['registrants']}
    all_event[data['event_name']] = new_event
    return jsonify(**{'succeed': True, 'data': new_event.data})


@app.route('/host/add_registrants', methods=['POST'])
def add_registrants():
    """
    expected data format
    data = {
        event_name: 'TamuHack',
        registrants: ['jakeLeland@tamu.edu','abcde@tamu.edu']
    }
    """
    data = request.get_json(force=True)
    if data['event_name'] in all_event:
        event = all_event[data['event_name']]
        for email in data['registrants']:
            if email not in event.data['registrants']:
                event.data['registrants'][email] = False
        return jsonify(**{'succeed': True, 'data': event.data})
    else:
        return jsonify(**{'succeed': False, 'message': "Event name not found"})


@app.route('/host/view_registrants', methods=['GET'])
def view_registrants():
    """
    data = {
        event_name: "TamuHack"
    }
    """
    data = request.get_json(force=True)
    if data['event_name'] in all_event:
        event = all_event[data['event_name']]
        return jsonify(**{'succeed': True, 'data': event.data['registrants']})
    else:
        return jsonify(**{'succeed': False, 'message': "Event name not found"})

if __name__ == '__main__':
    app.run()
