

#Nodes 
[{"id":"1","type":"customNode","data":{"assigned":{"label":"asd","customName":"asd","customType":"AGENT","customConfig":{"system_prompt":"asd"}},"functions":{},"llm":{"selected":"OLLAMA"}},"position":{"x":319,"y":122},"measured":{"width":200,"height":50},"selected":false,"dragging":false},
{"id":"2","type":"customNode","data":{"assigned":{"label":"asd2","customName":"asd2","customType":"AGENT","customConfig":{"system_prompt":"asd2"}},"functions":{},"llm":{"selected":"OLLAMA"}},"position":{"x":599,"y":52},"measured":{"width":200,"height":50},"selected":false,"dragging":false},
{"id":"3","type":"customNode","data":{"assigned":{"label":"asd3","customName":"asd3","customType":"RAG","customConfig":{"system_prompt":"asd3","sources":[{"source":"asd","type":"TXT"},{"source":"asd","type":"PDF"},{"source":"asd","type":"URL"},{"source":"","type":"TXT"}]}},"functions":{},"llm":{"selected":"GPT"}},"position":{"x":891,"y":119},"measured":{"width":200,"height":50},"selected":false,"dragging":false},
{"id":"4","type":"customNode","data":{"assigned":{"label":"asd2.5","customName":"asd2.5","customType":"AGENT","customConfig":{"system_prompt":"asd2.5"}},"functions":{},"llm":{"selected":"GPT"}},"position":{"x":600,"y":178},"measured":{"width":200,"height":50},"selected":true,"dragging":false}]

#Edges 
[{"source":"1","target":"2","id":"xy-edge__1-2"},
{"source":"2","target":"3","id":"xy-edge__2-3"},
{"source":"1","target":"4","id":"xy-edge__1-4"},
{"source":"4","target":"3","id":"xy-edge__4-3"}]

{
  "name": "Test",
  "nodes": [
    {"id": "1", "assigned": {"label": "asd", "customName": "asd", "customType": "AGENT", "customConfig": {"system_prompt": "asd"}}, "llm": {"selected": "OLLAMA"}},
    {"id": "2", "assigned": {"label": "asd2", "customName": "asd2", "customType": "AGENT", "customConfig": {"system_prompt": "asd2"}}, "llm": {"selected": "OLLAMA"}},
    {"id": "3", "assigned": {"label": "asd3", "customName": "asd3", "customType": "RAG", "customConfig": {"system_prompt": "asd3", "sources": [{"source": "asd", "type": "TXT"}, {"source": "asd", "type": "PDF"}, {"source": "asd", "type": "URL"}, {"source": "", "type": "TXT"}]}}, "llm": {"selected": "GPT"}},
    {"id": "4", "assigned": {"label": "asd2.5", "customName": "asd2.5", "customType": "AGENT", "customConfig": {"system_prompt": "asd2.5"}}, "llm": {"selected": "GPT"}}
  ],
  "edges": [
    {"source": "1", "target": "2", "id": "xy-edge__1-2"},
    {"source": "2", "target": "3", "id": "xy-edge__2-3"},
    {"source": "1", "target": "4", "id": "xy-edge__1-4"},
    {"source": "4", "target": "3", "id": "xy-edge__4-3"}
  ]
}

if __name__ == "__main__":
    print("Hello, world!")
    # Add more code here if desired