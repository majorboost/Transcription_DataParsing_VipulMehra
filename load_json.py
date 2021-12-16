import json

f = open('transcription-example.json')
data = json.load(f)
f.close()

for s in data['results']['segments']:

    alt1 = s['alternatives'][0]

    transcript = alt1['transcript']

    start = float(s['start_time'])
    end = float(s['end_time'])
    duration = end - start

    num_items = 0
    confidence_sum = 0.0
    items = alt1['items']
    for i, item in enumerate(items):
        num_items = i+1
        confidence_sum += float(item['confidence'])

    avg_conf = confidence_sum / float(num_items)

    print(transcript, start, end, avg_conf)