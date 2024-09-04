from pysll.decoders import decode


def parse_bytes(value: str):
    decompressed = decode(value)
    return parse(decompressed)


def parse(expr: str):
    if expr.startswith("QuantityArray[") and expr.endswith("]"):
        return parse(expr[len("QuantityArray[") : -len("]")])
    ...
