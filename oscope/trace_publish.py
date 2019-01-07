import datetime

import zmq

import oscope.abstract_scope as abs_scope
import oscope.schema as schema
import oscope.trace

class TracePublisher:
    def __init__(self,
            pub: zmq.Socket,
            scope: abs_scope.AbstractOscilloscope,
            channel: int):
        self.pub = pub
        self.scope = scope
        self.timeout = datetime.timedelta=datetime.timedelta(seconds=1)
        self.sequence = 0

    def push(self):
        self.scope.block_on_ready(timeout=self.timeout)
        trace_data = self.scope.read()

        meta = dict(
            device = self.scope.get_trace_meta(),
            trace = schema.get_device_meta(self.scope.get_sample_rate(), self.scope.get_sample_count()),
            sequence=self.sequence)
        self.sequence += 1

        packaged = oscope.trace.package_trace_data(meta, trace_data)
        self.pub.send_multipart(packaged)
