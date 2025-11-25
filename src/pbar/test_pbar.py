
from time import sleep
from pbar import progress_bar


def test_generator():
    def my_generator():
        try:
            for i in range(3):
                yield i
            print(
                "This code runs before the generator fully exits, but after the last yield."
            )
        finally:
            print(
                "This code in the finally block will always run when the generator is exhausted or closed."
            )

    gen = my_generator()
    for item in gen:
        print(f"Yielded: {item}")


def test_generator_with_progress_bar():
    # example without total (with a generator)
    def generator():
        for i in range(10):
            yield i

    print("test generator")
    for i in progress_bar(generator(), desc="test generator", transient=False):
        sleep(0.1)


def test_list():
    a = [0, 1, 2]
    for i in progress_bar(a, desc="test", transient=False):
        for j in progress_bar(range(10), desc=f"subtest {i}", transient=bool(i % 2)):
            sleep(0.1)
