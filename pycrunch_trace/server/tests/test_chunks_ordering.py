import pytest

from pycrunch_trace.server.chunks_ordering import ChunksOrdering, PyCrunchTraceServerException


def test_add_chunk_works():
    sut = ChunksOrdering()
    sut.session_will_start(session_id='s1')
    sut.did_receive_chunk(session_id='s1', chunk_number=1)

    assert 1 in sut.order_by_session['s1'].received_chunks

def test_duplicate_chunk_raises():
    with pytest.raises(PyCrunchTraceServerException):
        sut = ChunksOrdering()
        sut.session_will_start(session_id='s1')
        sut.did_receive_chunk(session_id='s1', chunk_number=1)
        sut.did_receive_chunk(session_id='s1', chunk_number=2)
        sut.did_receive_chunk(session_id='s1', chunk_number=2)

def test_lost_chunk_raises():
    with pytest.raises(PyCrunchTraceServerException):
        sut = ChunksOrdering()
        sut.session_will_start(session_id='s1')
        sut.did_receive_chunk(session_id='s1', chunk_number=1)
        sut.did_receive_chunk(session_id='s1', chunk_number=2)
        # lost 6 frames
        sut.did_receive_chunk(session_id='s1', chunk_number=8)

def test_first_chunk_lost():
    with pytest.raises(PyCrunchTraceServerException):
        sut = ChunksOrdering()
        sut.session_will_start(session_id='s1')
        sut.did_receive_chunk(session_id='s1', chunk_number=2)

def test_happy_case_no_errors():
    sut = ChunksOrdering()
    sut.session_will_start(session_id='s1')
    sut.did_receive_chunk(session_id='s1', chunk_number=1)
    sut.did_receive_chunk(session_id='s1', chunk_number=2)
    sut.did_receive_chunk(session_id='s1', chunk_number=3)


def test_multiple_sessions():
    sut = ChunksOrdering()
    sut.session_will_start(session_id='s1')
    sut.did_receive_chunk(session_id='s1', chunk_number=1)
    sut.session_will_start(session_id='s2')
    sut.did_receive_chunk(session_id='s2', chunk_number=1)
    sut.did_receive_chunk(session_id='s2', chunk_number=2)
    sut.session_will_start(session_id='s3')
    sut.did_receive_chunk(session_id='s3', chunk_number=1)
    sut.did_receive_chunk(session_id='s3', chunk_number=2)


def test_chunk_after_session_finished():
    with pytest.raises(PyCrunchTraceServerException):
        sut = ChunksOrdering()
        sut.session_will_start('s1')
        sut.did_receive_chunk('s1', 1)
        sut.session_will_finish('s1')
        sut.did_receive_chunk('s1', 1)
