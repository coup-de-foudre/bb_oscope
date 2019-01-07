import datetime

import zmq

import oscope.scope.abstract as abs_scope
import oscope.schema as schema
import oscope.trace

class TracePublisher:
    def __init__(self,
            pub: zmq.Socket,
            scope: abs_scope.AbstractOscilloscope):
        self.pub = pub
        self.scope = scope
        self.timeout = datetime.timedelta(seconds=1)
        self.sequence = 0

    def _seq_get_inc(self):
        s = self.sequence
        self.sequence += 1
        return s

    def push(self):
        self.scope.block_on_ready(timeout=self.timeout)
        trace_data = self.scope.read()

        meta = dict(
            sender = schema.get_sender_meta(self.scope.get_name(), str(id(self.scope))),
            trace = self.scope.get_trace_meta(),
            sequence = self._seq_get_inc())

        packaged = oscope.trace.package_trace_data(meta, trace_data)
        self.pub.send_multipart(packaged)
