import sys, os
protos_path = os.path.join(os.path.dirname(__file__), 'protobuf')
if protos_path not in sys.path:
    sys.path.append(protos_path)
