try:
    from .cog import *
except Exception as e:
    print(e)

__all__ = (
    "setup"
)