import itertools
import subprocess
import sys
import tempfile
from pathlib import Path


executable = Path(sys.argv[1]).resolve()
repository = Path(__file__).resolve().parents[1]
checks = 0


def run(path, expected=0, input_text="", timeout=10):
    global checks
    result = subprocess.run([str(executable), str(path)], input=input_text,
                            capture_output=True, text=True, timeout=timeout)
    assert result.returncode == expected, (path, result.returncode, result.stdout, result.stderr)
    checks += 1
    return result.stdout + result.stderr


with tempfile.TemporaryDirectory(prefix="badd regression.") as directory:
    scratch = Path(directory)
    for name, marker, expected in [
        ("standart-example.ba", "Sum:15", 0),
        ("loop-example.ba", "sum=36", 0),
        ("loop-example-2.ba", "^^", 0),
        ("error-example.ba", "line 7 column 12", 1),
    ]:
        assert marker in run(repository / "Only Source Code" / name, expected)

    values = [-999, -100, -42, -2, -1, 0, 1, 2, 42, 100, 999]
    pairs = list(itertools.product(values, repeat=2))
    pairs += [(10**99, 1), (1, 10**99), (-10**99, 1), (-10**99, -1),
              (10**99, -10**99), (-10**99, 10**99)]
    for offset in range(0, len(pairs), 20):
        batch = pairs[offset:offset + 20]
        source = "int x.\n"
        expected = ""
        for a, b in batch:
            source += f'move {a} to x. add {b} to x. out x,"|". '
            source += f'move {a} to x. sub {b} from x. out x,";".\n'
            expected += f"{a+b}|{a-b};"
        path = scratch / "arithmetic.ba"
        path.write_text(source)
        assert run(path).startswith(expected)

    cases = [
        ('out "%s%n 100%",newline.', 0, "%s%n 100%"),
        ('int x.move 0002 to x.add -0001 to x.out x.', 0, "1"),
        ('int x. move 1-2 to x.', 1, "not valid integer"),
        ('int x. move - to x.', 1, "not valid integer"),
        ('int _x.', 1, "alphabetic"),
        ('move 1 to', 1, "Expected"),
        ('out', 1, "Expected an output value"),
        ('out "value",', 1, "Expected string"),
        ('loop unknown times out "x".', 1, "not declared"),
        ('out "unterminated', 1, "Unterminated string"),
        ('{unterminated', 1, "Unterminated comment"),
        ('out "' + 'x' * 104 + '".', 0, "x" * 104),
        ('out "' + 'x' * 105 + '".', 1, "String length limit"),
        ('a' * 105, 1, "Lexeme length limit"),
        ('out "x".' * 332, 0, "x" * 332),
        ('out "x".' * 333, 1, "Token limit"),
        (' '.join(f'int x{i}.' for i in range(101)), 1, "Symbol limit"),
        ('int x. move ' + '9' * 100 + ' to x. add 1 to x.', 1, "Maximum value"),
        ('loop 1 times [' * 100 + 'out "x".' + ']' * 100, 0, "x"),
        ('loop 1 times [' * 101 + 'out "x".' + ']' * 101, 1, "Loop nesting limit"),
        ('out "x".\0', 1, "NUL byte"),
        ('out "x".\xff', 1, "Unexpected character"),
    ]
    for source, expected, marker in cases:
        path = scratch / "case.ba"
        path.write_bytes(source.encode("latin1"))
        assert marker in run(path, expected)

    for keyword in ("to", "from", "times", "newline"):
        path = scratch / "standalone-keyword.ba"
        path.write_text(keyword + ".")
        assert "Unexpected keyword at statement start" in run(path, 1, timeout=3)

    path = scratch / "bare.ba"
    path.write_text('out "bare filename".')
    assert "bare filename" in run(path.with_suffix(""))
    assert "extension" in run(scratch / "wrong.txt", 1)
    assert "too long" in run("x" * 2000, 1)
    run(scratch / "missing.ba", 1)
    result = subprocess.run([str(executable)], input="x" * 2000 + "\n",
                            text=True, capture_output=True, timeout=10)
    assert result.returncode == 1 and "too long" in result.stderr
    checks += 1

assert (repository / "Only Source Code/main.c").read_bytes() == (
    repository / "Source Code and Executable/main.c").read_bytes()
print(f"Passed {checks} interpreter regression runs and duplicate-source check.")
