from pycrunch_trace.server.perf import PerformanceInsights


def test_average_package_size_one_chunk():
    sut = PerformanceInsights()

    sut.sample(session_id='session_id', number_of_events=10, buffer_size=2000)

    actual = sut.average_event_size(session_id='session_id')
    assert actual == 200

def test_average_package_size_three_chunks():
    sut = PerformanceInsights()

    sut.sample(session_id='session_id', number_of_events=1, buffer_size=200)
    sut.sample(session_id='session_id', number_of_events=1, buffer_size=250)
    sut.sample(session_id='session_id', number_of_events=1, buffer_size=300)

    actual = sut.average_event_size(session_id='session_id')
    assert actual == 250

def test_average_package_size_three_sessions():
    sut = PerformanceInsights()

    sut.sample(session_id='1', number_of_events=1, buffer_size=200)
    sut.sample(session_id='2', number_of_events=1, buffer_size=250)
    sut.sample(session_id='3', number_of_events=2, buffer_size=700)

    assert 200 == sut.average_event_size(session_id='1')
    assert 250 == sut.average_event_size(session_id='2')
    assert 350 == sut.average_event_size(session_id='3')
