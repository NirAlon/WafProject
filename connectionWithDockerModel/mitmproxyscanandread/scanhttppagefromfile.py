from mitmproxy.io import FlowReader
from mitmproxy.addons import export



filename = '/Path/to/requests.mitm'

with open(filename, 'rb') as fp:
    reader = FlowReader(fp)

    for flow in reader.stream():
        print(export.cleanup_request(flow))