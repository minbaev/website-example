'''
Created on Dec 21, 2016

@author: minbaev
'''
import httplib, urllib, base64
import json
import sys
import os

def run_query(search_terms):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bing_api_key = '' 
    try:
        with open(BASE_DIR+'/bing.secret', 'r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.secret file not found')
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': bing_api_key,
        'Content-Type': 'application/json'
    }

    params= urllib.urlencode({
        'q': search_terms,
        'count': '10',
        'offset': '0',
        'safesearch': 'moderate',
        'mkt': 'en-us'
        })

    results = []
    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response  = conn.getresponse()
        data = response.read()
        json_response = json.loads(data)
        pages = json_response["webPages"]["value"]
        for page in pages:
            print(page["name"])
            results.append({'name': page['name'],
                            'link': page['url'],
                            'snippet': page['snippet']})

        conn.close()
    except Exception as e:
        print e

    return results

if __name__ == "__main__": 
    query = ' '.join(sys.argv[1:])

    print(query)
    run_query(query)



