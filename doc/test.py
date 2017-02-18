import subprocess
import bottle

import json
import thread
import requests

import os

 
from subprocess import call
from bottle import route, run, template, request, response


_address = '10.32.19.237'
_port = '5000'

_cpp_command = '../build/test {0} {1}'
_result_path = '../result/'
_json_path = '../jsondata/'



@bottle.route('/test', method='POST')
def process():
    print("in")
    data = json.dumps(request.json,ensure_ascii=True)
    loaded_json = json.loads(data)
    _id = loaded_json['_id']
    returnURL = loaded_json['returnURL']

    jsondata_path = _json_path + _id + '.json'
    result_path = _result_path + _id + '.json'

    with open(jsondata_path,'w') as outfile:
        json.dump(request.json,outfile)

# check any error.
# no error => result success
# else     => result fail
    

    thread.start_new_thread(callSubProcess,(jsondata_path,result_path,returnURL))
 
    return 'success'


def callSubProcess(jsondata_path,result_path,returnURL):
    subname = _cpp_command.format(jsondata_path,result_path)

    proc = subprocess.Popen(subname,shell=True)
    return_code = proc.wait()

#    if return_code == 0 :
#        with open(result_path) as readfile:
#            jsonData = json.load(readfile)
        
#        os.remove(result_path)

#	data = json.dumps(jsonData,ensure_ascii=True)	

#        res = requests.post(returnURL,data = data)



#        if res.status_code == requests.codes.ok:
#            resultData = json.loads(res.text)
#            print(resultData['dataFromU'])
#        else:
#            print('post error')

    
run(host=_address, port=_port)
