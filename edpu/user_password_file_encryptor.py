def encrypt(file_name: str) -> None:
    from .file_encryptor import encrypt as impl
    from edpu_user import password_provider

    impl(file_name, password_provider.get(), file_name + '.7z')
