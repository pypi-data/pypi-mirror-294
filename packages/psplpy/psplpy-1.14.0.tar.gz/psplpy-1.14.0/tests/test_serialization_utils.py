import random
from tests.__init__ import *
from psplpy.serialization_utils import *
from psplpy.other_utils import PerfCounter


bench_data = {}
rand_round = 10000
for i in range(rand_round):
    bench_data[str(random.randint(0, rand_round))] = random.uniform(0, rand_round)
python_data = {1: '100', 2: 200, 3: ['你好', [3.14, None, False]]}
json_str = '{"1":"100","2":200,"3":["你好",[3.14,null,false]]}'
pickle_bytes = (b'\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01\x8c\x03100\x94K\x02K\xc8K\x03]\x94('
                b'\x8c\x06\xe4\xbd\xa0\xe5\xa5\xbd\x94]\x94(G@\t\x1e\xb8Q\xeb\x85\x1fN\x89eeu.')
yaml_str = "1: '100'\n2: 200\n3:\n- 你好\n- - 3.14\n  - null\n  - false\n"


def test_compress_serializer():
    zlib_serializer = CompressSerializer(threshold=1)
    lzma_serializer = CompressSerializer(threshold=1, compress_lib=Compressor.LZMA)

    p = PerfCounter()
    serialized_data = zlib_serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t zlib_pickle')
    serialized_data = lzma_serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t lzma_pickle')

    for dump, load, load_kwargs in [('dump_pickle', 'load_pickle', {}), ('dump_yaml', 'load_yaml', {}),
                                    ('dump_json', 'load_json', {'trans_key_to_num': True})]:
        dumps_data = getattr(zlib_serializer, dump)(python_data)
        assert isinstance(dumps_data, bytes), dump
        loads_data = getattr(zlib_serializer, load)(dumps_data, **load_kwargs)
        assert loads_data == python_data, f'{load}, {loads_data}'


    compress_serializer = CompressSerializer(path=tmp_file, data_type=dict, compress=True)
    uncompress_serializer = CompressSerializer(path=tmp_file, data_type=dict, compress=False)

    for serializer in [compress_serializer, uncompress_serializer]:
        try:
            print(f'compress: {serializer.compress}')
            loads_data = serializer.load_json()
            assert loads_data == dict(), loads_data
            loads_data = serializer.load_json()
            assert loads_data == dict(), loads_data

            dumps_data = serializer.dump_json(python_data)
            assert isinstance(dumps_data, bytes)
            loads_data = serializer.load_json(trans_key_to_num=True)
            assert loads_data == python_data, loads_data

            dumps_data = serializer.dump_yaml(python_data)
            assert isinstance(dumps_data, bytes)
            loads_data = serializer.load_yaml()
            assert loads_data == python_data, loads_data

            dumps_data = serializer.dump_pickle(python_data)
            assert isinstance(dumps_data, bytes)
            loads_data = serializer.load_pickle()
            assert loads_data == python_data, loads_data
        finally:
            tmp_file.unlink(missing_ok=True)


def test_serializer():
    serializer = Serializer()
    p = PerfCounter()
    serialized_data = serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_pickle')
    serialized_data = serializer.dump_json(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_json')
    serialized_data = serializer.dump_yaml(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_yaml')

    dumps_data = serializer.dump_json(python_data, ensure_ascii=False)
    loads_data = serializer.load_json(dumps_data, trans_key_to_num=True)
    assert dumps_data == json_str, dumps_data
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_pickle(loads_data)
    loads_data = serializer.load_pickle(dumps_data)
    assert dumps_data == pickle_bytes, loads_data
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml(dumps_data)
    assert dumps_data == yaml_str, dumps_data
    assert loads_data == python_data

    try:
        serializer = Serializer(path=tmp_file, data_type=dict)
        loads_data = serializer.load_json()
        assert loads_data == dict(), loads_data

        dumps_data = serializer.dump_json(python_data)
        assert dumps_data == json_str, dumps_data
        loads_data = serializer.load_json(trans_key_to_num=True)
        assert loads_data == python_data, loads_data

        dumps_data = serializer.dump_yaml(python_data)
        assert dumps_data == yaml_str, dumps_data
        loads_data = serializer.load_yaml()
        assert loads_data == python_data, loads_data

        dumps_data = serializer.dump_pickle(python_data)
        assert dumps_data == pickle_bytes, dumps_data
        loads_data = serializer.load_pickle()
        assert loads_data == python_data, loads_data
    finally:
        tmp_file.unlink(missing_ok=True)


def tests():
    test_serializer()
    test_compress_serializer()


if __name__ == '__main__':
    tests()
