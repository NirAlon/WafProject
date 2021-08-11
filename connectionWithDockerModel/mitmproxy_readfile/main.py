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

#Sapir you need to paste here the path of requests.mitm. I think c:/requests.mitm
#If you can't find the path, run a search.
#The file requests.mitm is created after you run the command mitmproxy -w +requests.mitm
filename = '/Users/niralon/requests.mitm'

with open(filename, 'rb') as fp:
    reader = FlowReader(fp)
    list=[]
    for flow in reader.stream():
        encoding = 'utf-8'
        list.append(export.httpie_command(flow))

    #for l in list:
        #print(l)
    url_list=[]
    for l in list:
        i = l.find('?')
        if(i != -1 ):
            url_list.append(l[i+1:])
    print(url_list)

    a = url_list[0].split('%')
    print(a)

    #final=""
    #for url in url_list:
     #   print(final)
      #  final=""
       # for c in url.split('%'):
            #for c in a:
                #print(c[0:2])
        #        try:
                    #print(chr(int(c[0:2], 16)))
                    #print(c[2:])
         #           final += chr(int(c[0:2], 16))
          #          final += c[2:]
           #     except:
            #        print('')

    #l=[]
    #i = list.find('?')
    #if(list[i+1]!='h'):
    #    l = list[i+1:].split("\n")

