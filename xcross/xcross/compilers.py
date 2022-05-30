from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xcross.architectures import Architecture


class CompilerBase:
    def get_rule_contents(self, architecture: Architecture):
        raise NotImplementedError


class CompilerCpp(CompilerBase):
    @classmethod
    def get_rule_contents(cls, architecture: Architecture):
        return "\n".join(
            [
                f"  command = clang++ --target={architecture.triplet} -fuse-ld=lld $ARGS -o $out -c $in",
                "  description = Compiling C++ object $out",
            ]
        )


class CompilerC(CompilerBase):
    @classmethod
    def get_rule_contents(cls, architecture: Architecture):
        return "\n".join(
            [
                f"  command = clang --target={architecture.triplet} -fuse-ld=lld $ARGS -o $out -c $in",
                "  description = Compiling C object $out",
            ]
        )
