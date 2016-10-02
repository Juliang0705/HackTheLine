from flask import Flask, render_template, jsonify, request
import os
from geopy.distance import vincenty
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
def host_create_event():
    """
    expected data format
    data = {
        host_email: 'Juliang075@tamu.edu',
        event_name: 'TamuHack',
        event_address: '1237 TAMU College Station, Texas 77843-1237',
        lat: 30.619378,
        lng: -96.3380669,
        allow_radius: 100,
        files: {
        "code-of-conduct.md": "content",
        "community-values.md":"another content"
        },
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
    # create folder for this event
    folder_name = data['event_name'].replace(' ', '')
    absolute_folder_name = os.path.dirname(os.path.abspath(__file__)) + '/static/files/' + folder_name
    print absolute_folder_name
    if not os.path.exists(absolute_folder_name):
        os.makedirs(absolute_folder_name)
    for key,val in data['files'].iteritems():
        file_address = absolute_folder_name + '/' + key
        with open(file_address, "w") as text_file:
            text_file.write(val)
            data['files'][key] = '/static/files/' + folder_name + '/' + key
    return jsonify(**{'succeed': True, 'data': new_event.data})


@app.route('/host/add_registrants', methods=['POST'])
def host_add_registrants():
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
def host_view_registrants():
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


# for registrants
@app.route('/guest/sign_in', methods=['POST'])
def guest_sign_in():
    """
    data = {
        event_name: "TamuHack",
        registrant: "Juliang075@tamu.edu"
    }
    """
    data = request.get_json(force=True)
    registrant = data['registrant']
    if data['event_name'] in all_event:
        event = all_event[data['event_name']]
        if registrant in event.data['registrants']:
            event.data['registrants'][registrant] = True
            return jsonify(**{'succeed': True, 'data': {registrant: event.data['registrants'][registrant]}})
        else:
            return jsonify(**{'succeed': False, 'message': "You are not one of the registrants"})
    else:
        return jsonify(**{'succeed': False, 'message': "Event name not found"})


@app.route('/guest/get_events', methods=['GET'])
def guest_get_events():
    """
    data = {
        lat: 30.619378,
        lng: -96.3380669
    }
    """
    data = request.get_json(force=True)
    current_location = (data['lat'], data['lng'])
    result = []
    for event in all_event.values():
        event_location = (event.data['lat'], event.data['lng'])
        distance = vincenty(current_location, event_location).meters
        print distance
        if distance <= event.data['allow_radius']:
            result.append(event.data['event_name'])
    return jsonify(**{'result': result})

if __name__ == '__main__':
    app.run()
