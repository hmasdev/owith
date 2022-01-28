# OWith: one liner `with`

Do you want to reduce the number of characters in your python codes?

Regarding `with` statement, OWith helps you.

## Introduction

Python `with` statement is useful.
A little bit long python script like

```python
import json
f = open("sample.json")
try:
    dic = json.load(f)
finally:
    f.close()
```

becomes the following short script like

```python
import json
with open("sample.json") as f:
    dic = json.load(f)
```

with `with`.
Also, using `with`, `__enter__` and `__exit__` methods of a context manager are called automatically.
For example, you can use your custom context manager

```python
class CustomCM:
    def __enter__(self):
        print("Start")
    def __exit__(self):
        print("End")
```

with `with` like the followings.

```python
>>> with CustomCM():
...     print("Excecution")
...
start
Execution
end
```

As above, needless to say, `with` is quite helpful for you to write python codes.

However, OWith provides you an alternative tool which enables you to write fewer characters when you use `with` to execute one-line suite.
OWith also enables you to use `close` or `__exit__` required objects like `open("sample.json")` in list comprehensions and so on with the confidence that it is safe.

## Installation

### Requirements

- Python >= 3.7

### User Installation

```bash
pip install git+https://github.com/hmasdev/owith.git@master
```

## How to Use

OWith provides three functions:

1. `owith`: a functional like `functools.partial` which help you to use `with`;
2. `owith_all`: a decorator which help you to create a function in which the arguments will be used in `with` statement;
3. `dcwith`: a function to create a decorator which enable you to use `with` outside of a decorated function.

### 1st function: `owith(func: typing.Callable, *args, **kwargs) -> typing.Callable`

When writing

```python
with some_context_manager as scm:
    ret = some_function(scm)
```

, you can alternatively write

```python
ret = owith(some_function, scm)
```

with `owith`.
When some_function is able to received `scm` as a keyword argument `kwarg` in the above example, you can also write

```python
ret = owith(some_function, kwarg=scm)
```

with `owith`.
Of course, `owith` can receive context managers at once like

```python
ret = owith(some_function, cm1, cm2, cm3=cm3)
```

which behaves as the same as

```python
with cm1 as cm1_, cm2 as cm2_, cm3 as cm3_:
    ret = some_function(cm1_, cm2_, cm3=cm3_)
```

By the way, if you are concerned when writing

```python
from glob import glob
jsons = [
    json.load(open(fname))
    for fname in glob("./*.json")
]
```

, you can also write the following

```python
from glob import glob
jsons = [
    owith(json.load, open(fname))
    for fname in glob("./*.json")
]
```

### 2nd function: `owith_all(func: typing.Callable) -> typing.Callable`

When writing

```python
def func(cm):
    with cm as cm_:
        return True
```

, you can alternatively write

```python
@owith_all
def func(cm):
    return True
```

with `owith_all` decorator.

### 3rd function: `dcwith(*args) -> Callable[[typing.Callable, ], typing.Callable]`

When writing

```python
def func():
    return True

with cm1, cm2, ..., cmN:
    func()
```

, you can alternatively write

```python
def func():
    return True

dcwith(cm1, cm2, ..., cmN)(func)()
```

or

```python
@dcwith(cm1, cm2, ..., cmN)
def func():
    return True

func()
```

with `dcwith`.

## Effectiveness and Efficiency

Let us see the impact of OWith on your python codes using three example.

Assume that `import json` have been already executed in the following examples.

### First Example

The following python scripts are funcionally equivalent:

```python
with open("sample.json") as f:
    dic = json.load(f)
```

and

```python
ret = owith(json.load, open("sample.json"))
```

But the number of characters in the former is 52 while that in the latter is 43.
That is, `owith` reduce the number of characters by 9.

### Second Example

The following python scripts are functionally equivalent:

```python
def jload(file_obj):
    with file_obj as f:
        return json.load(f)
```

and

```python
@owith_all
def jload(file_obj):
    return json_load(file_obj)
```

But the number of characters in the former is 70 while that in the latter is 60.
That is, `owith_all` reduce the number of characters by 10.

### Thrid Example

The following python scripts are functionally equivalent:

```python
def func():
    return True

with stopwatch_cm:
    func()
```

and

```python
@dcwith(stopwatch_cm)
def func():
    return True

func()
```

But the number of characters in the former is 54 while that in the latter is 53.
That is, `dcwith` reduce the number of characters by 1.

## Contribution Guide

### Requirement

- python >= 3.7
- pipenv

### Setup

```bash
$ git clone https://github.com/hmasdev/owith.git
$ cd owith
$ pipenv install --dev
```

### Issues

- For any bugs, use [BUG REPORT](https://github.com/hmasdev/owith/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D) to create an issue.

- For any enhancement, use [FEATURE REQUEST](https://github.com/hmasdev/owith/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=) to create an issue.

- For other topics, create an issue with a clear and concise description.

### Pull Request

1. Fork (https://github.com/hmasdev/owith/fork);
2. Create your feature branch (git checkout -b feautre/xxxx);
3. Test codes according to Test Subsection;
4. Commit your changes (git commit -am 'Add xxxx feature);
5. Push to the branch (git push origin feature/xxxx);
6. Create new Pull Request

### Test

```bash
$ pipenv run flake8
$ pipenv run mypy .
$ pipenv run pytest
```

## LICENSE

MIT

## Authors

[hmasdev](https://github.com/hmasdev)
