import oscope.base
import oscope.scope.fake
import oscope.encoding
import oscope.trace_publish
import oscope.network.util as helpers


def test_publishing():
    fakescope = oscope.scope.fake.FakeOscilloscope()

    with helpers.LinkedPubSubPair() as (pub, sub):
        publisher = oscope.trace_publish.TracePublisher(pub, fakescope)

        for x in range(10):
            publisher.publish_data()

            oscope.base.assert_pollin(sub)
            packaged = sub.recv_multipart()

            meta, _ = oscope.encoding.unpackage_trace_data(packaged)

            assert meta["sequence"] == x


def test_publishing_threaded():
    fakescope = oscope.scope.fake.FakeOscilloscope()

    with helpers.LinkedPubSubPair() as (pub, sub):
        publisher = oscope.trace_publish.TracePublisher(pub, fakescope)
        publisher.start_sender()

        oscope.base.assert_pollin(sub)
        packaged = sub.recv_multipart()
        oscope.encoding.unpackage_trace_data(packaged)

        publisher.stop_sender()
