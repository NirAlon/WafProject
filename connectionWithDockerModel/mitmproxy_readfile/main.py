import shlex

from mitmproxy import flow
from mitmproxy.addons.export import cleanup_request, pop_headers, request_content_for_console
from mitmproxy.io import FlowReader
from mitmproxy.addons import export


def httpie(f: flow.Flow) -> str:
    request = cleanup_request(f)
    request = pop_headers(request)
    args = [request.url]
    cmd = ' '.join(shlex.quote(arg) for arg in args)
    if request.content:
        cmd += " <<< " + shlex.quote(request_content_for_console(request))
    return cmd

#you need to paste here the path of requests.mitm. I think c:/requests.mitm
#If you can't find the path, run a search.
#The file requests.mitm is created after you run the command mitmproxy -w +requests.mitm
filename = '/Users/niralon/requests.mitm'

with open(filename, 'rb') as fp:
    reader = FlowReader(fp)
    list=[]
    for flow in reader.stream():
        encoding = 'utf-8'
        list.append(export.httpie_command(flow))

    url_list=[]
    for l in list:
        i = l.find('?')
        if(i != -1 ):
            url_list.append(l[i+1:])

    a = url_list[0].split('%')
