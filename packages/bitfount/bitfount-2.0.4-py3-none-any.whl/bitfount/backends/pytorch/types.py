"""Type Variable for our PyTorch Models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Optional, Union

import torch

from bitfount.types import _TensorLike


class _AdaptorForPyTorchTensor(_TensorLike):
    """Adapter protocol for pytorch Tensor.

    This is a thin wrapper around a pytorch tensor. It is required to provide definitive
    type annotations for different tensor operations.
    """

    def __init__(self, tensor: torch.Tensor):
        self.torchtensor = tensor

    def __mul__(self, other: Any) -> _AdaptorForPyTorchTensor:
        return _AdaptorForPyTorchTensor(self.torchtensor * other)

    def __sub__(self, other: Any) -> _AdaptorForPyTorchTensor:
        return _AdaptorForPyTorchTensor(self.torchtensor - other)

    def squeeze(self, axis: Optional[Any] = None) -> _AdaptorForPyTorchTensor:
        """Returns a tensor with all the dimensions of input of size 1 removed."""
        if axis is not None:
            return _AdaptorForPyTorchTensor(torch.squeeze(self.torchtensor, dim=axis))
        else:
            return _AdaptorForPyTorchTensor(torch.squeeze(self.torchtensor))


# Pytorch Types

# Pytorch Weight dict

PytorchWeightDict = dict[str, type[_AdaptorForPyTorchTensor]]
PytorchWeightMapping = Mapping[str, type[_AdaptorForPyTorchTensor]]

# Pytorch Batch types:
ImgAndTabBatch = tuple[torch.Tensor, torch.Tensor, torch.Tensor]
ImgXorTabBatch = tuple[torch.Tensor, torch.Tensor]

# SplitDataloaderTypes:
ImgAndTabDataSplit = tuple[torch.Tensor, torch.Tensor, torch.Tensor]
ImgXorTabDataSplit = tuple[torch.Tensor, torch.Tensor]

TabDataReturnType = tuple[
    tuple[torch.Tensor, torch.Tensor], torch.Tensor, Optional[torch.Tensor]
]
ImgDataReturnType = tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]

# Pytorch forward input types
ImgFwdTypes = Union[list[torch.Tensor], torch.Tensor]
TabFwdTypes = tuple[torch.Tensor, torch.Tensor]
