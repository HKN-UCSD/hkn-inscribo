import jinja2
from datetime import datetime

class Event:
    def __init__(self, name, time, description, urls = {}):
        self.name = name
        self.time = time
        self.description = description
        self.urls = urls


urls = {
    'fb': 'https://www.facebook.com/events/1341938379320787/',
    'rsvp': 'https://docs.google.com/forms/d/e/1FAIpQLSe1Ll9av8bskzPI6YqtfBr4rZ0is_RmNdW6L0rj_3iGA8qWAw/viewform',
    'banner': 'https://ci5.googleusercontent.com/proxy/jI2oTBRbwOmqpU9tjcAlUHy-1mc-5I_tcdleWOAN-g-sMVuyzC3GkmQr6XO_C3B4_HMC3Wiwx8NNv5D0cDGylz_VZjSk29XczD4zwA43iCyDpY9rugEpJ7cOYrcuveFi9MlOFCVBqxYzDkobQV9vLn_fZcFasBoB79Q=s0-d-e1-ft#https://gallery.mailchimp.com/59959b42eb5a47c6b4d207730/images/a7fb73da-4d8b-4ecb-a00d-8571ace12424.png'
}

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('.'),
)

context = {
    'intro': 'yo wassup everybodyyy',
    'events_by_week':{
        'Week 9':[
            Event(**{'name': 'HKN TALKS', 'time': 'last year', 'description': 'this is hkn talks.', 'urls': urls}),
            Event(**{'name': 'event2', 'time': 'event_time2', 'description': 'description2'}),
        ],
        'Week 10':[
            Event(**{'name': 'event3', 'time': 'event_time3', 'description': 'description3'}),
            Event(**{'name': 'event4', 'time': 'event_time4', 'description': 'description4'}),
        ]
    }
}

template = env.get_template('newsletter.html')
with open('works.html', 'w+') as html:
    html.write(template.render(**context))
