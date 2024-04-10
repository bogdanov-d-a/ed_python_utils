from __future__ import annotations
from abc import ABC, abstractmethod


class Remotes:
    def __init__(self: Remotes, native: list[str], storage: dict[str, str]) -> None:
        self.native = native
        self.storage = storage


class Data:
    def __init__(self: Data, host_to_path: dict[str, str], remotes: Remotes, branches: list[str], bundles: list[str]) -> None:
        self.host_to_path = host_to_path
        self.remotes = remotes
        self.branches = branches
        self.bundles = bundles


class DataProvider(ABC):
    @abstractmethod
    def get_repos(self: DataProvider) -> dict[str, Data]:
        pass

    @abstractmethod
    def get_bootstrap_repos(self: DataProvider) -> set[str]:
        pass

    @abstractmethod
    def get_autopush_repos(self: DataProvider) -> set[str]:
        pass

    @abstractmethod
    def get_bundle_path(self: DataProvider) -> str:
        pass

    @abstractmethod
    def get_bundle_hash_path(self: DataProvider, target_alias: str, repo_alias: str) -> str:
        pass

    @abstractmethod
    def get_storage_block_reasons(self: DataProvider) -> dict[str, str]:
        pass

    @abstractmethod
    def get_bundle_block_reasons(self: DataProvider) -> dict[str, str]:
        pass

    @abstractmethod
    def get_user_bundle_info_path(self: DataProvider) -> str:
        pass

    @abstractmethod
    def get_user_bundle_info_new_path(self: DataProvider) -> str:
        pass

    @abstractmethod
    def get_filename(self: DataProvider) -> str:
        pass

    @abstractmethod
    def is_debug(self: DataProvider) -> bool:
        pass
