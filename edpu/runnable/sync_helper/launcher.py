if __name__ == '__main__':
    from edpu.run_as_admin import run_as_admin
    from edpu_user.python_launcher import get_python3
    from edpu_user.sync_helper import sync_helper_dir_path
    from os.path import abspath, dirname, join

    run_as_admin(
        get_python3(),
        join(dirname(abspath(__file__)), 'core.py'),
        sync_helper_dir_path()
    )
