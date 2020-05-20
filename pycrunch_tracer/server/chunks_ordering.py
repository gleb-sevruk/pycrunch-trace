from queue import Queue
from typing import Dict, Any


class PyCrunchTraceException(Exception):
    pass


class PyCrunchTraceServerException(PyCrunchTraceException):
    pass


class ReceivedChunks:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.received_chunks = set()

    def did_receive_chunk(self, chunk_number):
        self.throw_if_chunk_out_of_order(chunk_number)
        self.received_chunks.add(chunk_number)

    def throw_if_chunk_out_of_order(self, chunk_number):
        self.throw_if_chunk_already_received(chunk_number)
        if len(self.received_chunks) == 0:
            self.throw_if_first_chunk_lost(chunk_number)
        else:
            self.throw_if_previous_chunk_lost(chunk_number)

    def throw_if_previous_chunk_lost(self, chunk_number):
        current_max = max(self.received_chunks)
        if chunk_number - 1 > current_max:
            raise PyCrunchTraceServerException(f'{self.session_id}: received {chunk_number} but {current_max} is expected for')

    def throw_if_first_chunk_lost(self, chunk_number):
            if chunk_number != 1:
                raise PyCrunchTraceServerException(f'{self.session_id}: received {chunk_number} but expected chunk #1')

    def throw_if_chunk_already_received(self, chunk_number):
        if chunk_number in self.received_chunks:
            raise PyCrunchTraceServerException(f'already received {chunk_number} for {self.session_id}')


class ChunksOrdering:
    order_by_session: Dict[str, ReceivedChunks]

    def __init__(self):
        self.order_by_session = dict()
        self.history = Queue(maxsize=200)

    def session_will_start(self, session_id):
        self.order_by_session[session_id] = ReceivedChunks(session_id)

    def did_receive_chunk(self, session_id, chunk_number):
        if session_id not in self.order_by_session:
            raise PyCrunchTraceServerException(f'{session_id}: not found')

        self.order_by_session[session_id].did_receive_chunk(chunk_number)

    def session_will_finish(self, session_id):
        self.history.put_nowait(self.order_by_session[session_id])
        del self.order_by_session[session_id]


chunks_ordering: ChunksOrdering = ChunksOrdering()
