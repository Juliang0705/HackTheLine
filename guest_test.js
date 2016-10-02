/**
 * Created by Juliang on 10/1/16.
 */
var request = require('request');
var guest_sign_in = {
    method: 'POST',
    url: 'http://localhost:5000/guest/sign_in',
    headers: {
        'Content-Type': 'application/json'
    },
    json: {
        event_name: "TamuHack",
        registrant: "jliang075@tamu.edu"
    }
};
var guest_get_event = {
    method: 'GET',
    url: 'http://localhost:5000/guest/get_events',
    headers: {
        'Content-Type': 'application/json'
    },
    json: {
        lat: 30.612305199999998,
        lng: -96.3413112
    }
}
request(guest_sign_in, function (error, response, body){
    var info = JSON.parse(JSON.stringify(body));
    console.log(info);
});

request(guest_get_event, function(error, response, body){
    var info = JSON.parse(JSON.stringify(body));
    console.log(info);
});