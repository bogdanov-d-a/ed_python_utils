def encrypt(file_name: str) -> None:
    from .file_encryptor import encrypt as impl
    from .pack_7z import S_7Z_EXT
    from edpu_user import password_provider

    impl(file_name, password_provider.get(), file_name + S_7Z_EXT)
