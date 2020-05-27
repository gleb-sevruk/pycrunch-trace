protoc --proto_path=pycrunch_tracer/proto --js_out=import_style=commonjs,binary:pycrunch_tracer/proto pycrunch_tracer/proto/message.proto


protoc --proto_path=pycrunch_tracer/proto --python_out=pycrunch_tracer/proto pycrunch_tracer/proto/message.proto
