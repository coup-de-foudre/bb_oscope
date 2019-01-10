import datetime

import threading

import zmq

import oscope.base
import oscope.scope.abstract as abs_scope
import oscope.schema as schema
import oscope.encoding

DEFAULT_STOP_TIME = datetime.timedelta(seconds=1)


class TracePublisher:
    def __init__(
            self,
            pub: zmq.Socket,
            scope: abs_scope.AbstractOscilloscope):
        self.pub = pub
        self.scope = scope
        self.timeout = datetime.timedelta(seconds=1)
        self.sequence = 0

        self._sender = None
        self._stop_event = threading.Event()

    def _seq_get_inc(self):
        s = self.sequence
        self.sequence += 1
        return s

    def publish_data(self):
        self.scope.block_on_ready(timeout=self.timeout)
        trace_data = self.scope.read()

        sender = schema.get_sender_meta(self.scope.get_name(), str(id(self.scope)))
        meta = dict(
            sender=sender,
            trace=self.scope.get_trace_meta(),
            sequence=self._seq_get_inc())

        packaged = oscope.encoding.package_trace_data(meta, trace_data)
        self.pub.send_multipart(packaged)

    def _sender_thread_run(self):
        while not self._stop_event.is_set():
            try:
                self.scope.block_on_ready(datetime.timedelta(seconds=0.1))
            except TimeoutError:
                continue
            self.publish_data()

    def start_sender(self):
        oscope.base.assert_is_none(self._sender)

        self._stop_event.clear()
        self._sender = threading.Thread(target=self._sender_thread_run)
        self._sender.start()

    def stop_sender(self, timeout: datetime.timedelta = DEFAULT_STOP_TIME):
        self._stop_event.set()
        self._sender.join(timeout=timeout.total_seconds())
        oscope.base.assert_false(self._sender.is_alive(), "Sender did not shutdown")
        self._sender = None
