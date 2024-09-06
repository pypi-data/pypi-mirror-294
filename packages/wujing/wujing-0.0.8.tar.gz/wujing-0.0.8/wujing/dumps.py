import json

import jsonpickle
from datasets import Dataset, DatasetDict

jsonpickle.set_encoder_options("json", ensure_ascii=False)


def dumps2json(obj: any):
    if isinstance(obj, (Dataset, DatasetDict)):
        return repr(obj)
    try:
        return json.dumps(obj, indent=4, ensure_ascii=False)
    except:
        return jsonpickle.encode(obj, indent=4, unpicklable=True, max_depth=1)


if __name__ == '__main__':
    print(dumps2json({"a": 1, "b": 2}))
