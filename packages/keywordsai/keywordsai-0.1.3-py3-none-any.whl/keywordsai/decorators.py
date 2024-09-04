import time
from functools import wraps
from asyncio import iscoroutinefunction, get_event_loop
from packaging.version import Version
import openai
import types
from .core import KeywordsAI

def _is_openai_v1():
    return Version(openai.__version__) >= Version("1.0.0")

def _is_streaming_response(response):
    return (
        isinstance(response, types.GeneratorType)
        or isinstance(response, types.AsyncGeneratorType)
        or (_is_openai_v1() and isinstance(response, openai.Stream))
        or (_is_openai_v1() and isinstance(response, openai.AsyncStream))
    )

def keywordsai_generator(generator):
    start_time = time.time()
    for response in generator:
        yield response
    end_time = time.time()


def openai_wrapper(func, *args, **kwargs):
    if iscoroutinefunction(func):
        @wraps(func)
        async def wrapped_openai(*args, **kwargs):
            loop = get_event_loop()
            start_time = loop.time()
            result =  await func(*args, **kwargs)
            end_time = loop.time()
            print(f"Function {func.__name__} took {end_time - start_time} seconds")
            return result
    else:    
        @wraps(func)
        def wrapped_openai(*args, **kwargs):
            start_time = time.time()
            result =  func(*args, **kwargs)
            end_time = time.time()
            is_stream = _is_streaming_response(func)
            ttft = None
            if is_stream:
                print(f"Function {func.__name__} is a streaming response")
                ttft = end_time - start_time
            else:
                latency = end_time - start_time 
            print(f"Function {func.__name__} took {end_time - start_time} seconds")
            return result
    
    return wrapped_openai

