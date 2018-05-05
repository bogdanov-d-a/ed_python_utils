import traceback

def run(f, wait_on_success=None):
    try:
        f()
    except:
        wait_on_success = None
        traceback.print_exc()
        input()
    finally:
        if wait_on_success is not None:
            print(wait_on_success)
            input()
