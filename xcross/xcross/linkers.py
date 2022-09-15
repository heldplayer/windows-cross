from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xcross.architectures import Architecture


class LinkerBase:
    def get_rule_contents(self, architecture: Architecture):
        raise NotImplementedError


class LinkerCpp(LinkerBase):
    @classmethod
    def get_rule_contents(cls, architecture: Architecture):
        return "\n".join(
            [
                f"  command = clang++-15 --target={architecture.triplet} -fuse-ld=lld $LINK_ARGS -o $out $in",
                "  description = Linking $out",
            ]
        )


class LinkerC(LinkerBase):
    @classmethod
    def get_rule_contents(cls, architecture: Architecture):
        return "\n".join(
            [
                f"  command = clang-15 --target={architecture.triplet} -fuse-ld=lld $LINK_ARGS -o $out $in",
                "  description = Linking $out",
            ]
        )
