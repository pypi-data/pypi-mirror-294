"""
    ProxylessNAS for ImageNet-1K, implemented in PyTorch.
    Original paper: 'ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware,'
    https://arxiv.org/abs/1812.00332.
"""

__all__ = ['ProxylessNAS', 'proxylessnas_cpu', 'proxylessnas_gpu', 'proxylessnas_mobile', 'proxylessnas_mobile14',
           'ProxylessUnit', 'get_proxylessnas']

import os
import torch.nn as nn
from typing import Callable
from .common.activ import lambda_relu6
from .common.norm import lambda_batchnorm2d
from .common.conv import ConvBlock, conv1x1_block, conv3x3_block


class ProxylessBlock(nn.Module):
    """
    ProxylessNAS block for residual path in ProxylessNAS unit.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    kernel_size : int
        Convolution window size.
    stride : int
        Strides of the convolution.
    normalization : function
        Lambda-function generator for normalization layer.
    activation : function
        Lambda-function generator for activation layer.
    expansion : int
        Expansion ratio.
    """
    def __init__(self,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: int,
                 stride: int,
                 normalization: Callable[..., nn.Module],
                 activation: Callable[..., nn.Module],
                 expansion: int):
        super(ProxylessBlock, self).__init__()
        self.use_bc = (expansion > 1)
        mid_channels = in_channels * expansion

        if self.use_bc:
            self.bc_conv = conv1x1_block(
                in_channels=in_channels,
                out_channels=mid_channels,
                normalization=normalization,
                activation=activation)

        padding = (kernel_size - 1) // 2
        self.dw_conv = ConvBlock(
            in_channels=mid_channels,
            out_channels=mid_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            groups=mid_channels,
            normalization=normalization,
            activation=activation)
        self.pw_conv = conv1x1_block(
            in_channels=mid_channels,
            out_channels=out_channels,
            normalization=normalization,
            activation=None)

    def forward(self, x):
        if self.use_bc:
            x = self.bc_conv(x)
        x = self.dw_conv(x)
        x = self.pw_conv(x)
        return x


class ProxylessUnit(nn.Module):
    """
    ProxylessNAS unit.

    Parameters
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    kernel_size : int
        Convolution window size for body block.
    stride : int
        Strides of the convolution.
    normalization : function
        Lambda-function generator for normalization layer.
    activation : function
        Lambda-function generator for activation layer.
    expansion : int
        Expansion ratio for body block.
    residual : bool
        Whether to use residual branch.
    shortcut : bool
        Whether to use identity branch.
    """
    def __init__(self,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: int,
                 stride: int,
                 normalization: Callable[..., nn.Module],
                 activation: Callable[..., nn.Module],
                 expansion: int,
                 residual: bool,
                 shortcut: bool):
        super(ProxylessUnit, self).__init__()
        assert (residual or shortcut)
        self.residual = residual
        self.shortcut = shortcut

        if self.residual:
            self.body = ProxylessBlock(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=kernel_size,
                stride=stride,
                normalization=normalization,
                activation=activation,
                expansion=expansion)

    def forward(self, x):
        if not self.residual:
            return x
        if not self.shortcut:
            return self.body(x)
        identity = x
        x = self.body(x)
        x = identity + x
        return x


class ProxylessNAS(nn.Module):
    """
    ProxylessNAS model from 'ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware,'
    https://arxiv.org/abs/1812.00332.

    Parameters
    ----------
    channels : list(list(int))
        Number of output channels for each unit.
    init_block_channels : int
        Number of output channels for the initial unit.
    final_block_channels : int
        Number of output channels for the final unit.
    residuals : list(list(int))
        Whether to use residual branch in units.
    shortcuts : list(list(int))
        Whether to use identity branch in units.
    kernel_sizes : list(list(int))
        Convolution window size for each unit.
    expansions : list(list(int))
        Expansion ratio for each unit.
    bn_eps : float, default 1e-3
        Small float added to variance in Batch norm.
    in_channels : int, default 3
        Number of input channels.
    in_size : tuple(int, int), default (224, 224)
        Spatial size of the expected input image.
    num_classes : int, default 1000
        Number of classification classes.
    """
    def __init__(self,
                 channels: list[list[int]],
                 init_block_channels: int,
                 final_block_channels: int,
                 residuals: list[list[int]],
                 shortcuts: list[list[int]],
                 kernel_sizes: list[list[int]],
                 expansions: list[list[int]],
                 bn_eps: float = 1e-3,
                 in_channels: int = 3,
                 in_size: tuple[int, int] = (224, 224),
                 num_classes: int = 1000):
        super(ProxylessNAS, self).__init__()
        self.in_size = in_size
        self.num_classes = num_classes
        normalization = lambda_batchnorm2d(eps=bn_eps)
        activation = lambda_relu6()

        self.features = nn.Sequential()
        self.features.add_module("init_block", conv3x3_block(
            in_channels=in_channels,
            out_channels=init_block_channels,
            stride=2,
            normalization=normalization,
            activation=activation))
        in_channels = init_block_channels
        for i, channels_per_stage in enumerate(channels):
            stage = nn.Sequential()
            residuals_per_stage = residuals[i]
            shortcuts_per_stage = shortcuts[i]
            kernel_sizes_per_stage = kernel_sizes[i]
            expansions_per_stage = expansions[i]
            for j, out_channels in enumerate(channels_per_stage):
                residual = (residuals_per_stage[j] == 1)
                shortcut = (shortcuts_per_stage[j] == 1)
                kernel_size = kernel_sizes_per_stage[j]
                expansion = expansions_per_stage[j]
                stride = 2 if (j == 0) and (i != 0) else 1
                stage.add_module("unit{}".format(j + 1), ProxylessUnit(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=kernel_size,
                    stride=stride,
                    normalization=normalization,
                    activation=activation,
                    expansion=expansion,
                    residual=residual,
                    shortcut=shortcut))
                in_channels = out_channels
            self.features.add_module("stage{}".format(i + 1), stage)
        self.features.add_module("final_block", conv1x1_block(
            in_channels=in_channels,
            out_channels=final_block_channels,
            normalization=normalization,
            activation=activation))
        in_channels = final_block_channels
        self.features.add_module("final_pool", nn.AvgPool2d(
            kernel_size=7,
            stride=1))

        self.output = nn.Linear(
            in_features=in_channels,
            out_features=num_classes)

        self._init_params()

    def _init_params(self):
        for name, module in self.named_modules():
            if isinstance(module, nn.Conv2d):
                nn.init.kaiming_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.output(x)
        return x


def get_proxylessnas(version: str,
                     model_name: str | None = None,
                     pretrained: bool = False,
                     root: str = os.path.join("~", ".torch", "models"),
                     **kwargs) -> nn.Module:
    """
    Create ProxylessNAS model with specific parameters.

    Parameters
    ----------
    version : str
        Version of ProxylessNAS ('cpu', 'gpu', 'mobile' or 'mobile14').
    model_name : str or None, default None
        Model name for loading pretrained model.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.

    Returns
    -------
    nn.Module
        Desired module.
    """
    if version == "cpu":
        residuals = [[1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
        channels = [[24], [32, 32, 32, 32], [48, 48, 48, 48], [88, 88, 88, 88, 104, 104, 104, 104],
                    [216, 216, 216, 216, 360]]
        kernel_sizes = [[3], [3, 3, 3, 3], [3, 3, 3, 5], [3, 3, 3, 3, 5, 3, 3, 3], [5, 5, 5, 3, 5]]
        expansions = [[1], [6, 3, 3, 3], [6, 3, 3, 3], [6, 3, 3, 3, 6, 3, 3, 3], [6, 3, 3, 3, 6]]
        init_block_channels = 40
        final_block_channels = 1432
    elif version == "gpu":
        residuals = [[1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1]]
        channels = [[24], [32, 32, 32, 32], [56, 56, 56, 56], [112, 112, 112, 112, 128, 128, 128, 128],
                    [256, 256, 256, 256, 432]]
        kernel_sizes = [[3], [5, 3, 3, 3], [7, 3, 3, 3], [7, 5, 5, 5, 5, 3, 3, 5], [7, 7, 7, 5, 7]]
        expansions = [[1], [3, 3, 3, 3], [3, 3, 3, 3], [6, 3, 3, 3, 6, 3, 3, 3], [6, 6, 6, 6, 6]]
        init_block_channels = 40
        final_block_channels = 1728
    elif version == "mobile":
        residuals = [[1], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
        channels = [[16], [32, 32, 32, 32], [40, 40, 40, 40], [80, 80, 80, 80, 96, 96, 96, 96],
                    [192, 192, 192, 192, 320]]
        kernel_sizes = [[3], [5, 3, 3, 3], [7, 3, 5, 5], [7, 5, 5, 5, 5, 5, 5, 5], [7, 7, 7, 7, 7]]
        expansions = [[1], [3, 3, 3, 3], [3, 3, 3, 3], [6, 3, 3, 3, 6, 3, 3, 3], [6, 6, 3, 3, 6]]
        init_block_channels = 32
        final_block_channels = 1280
    elif version == "mobile14":
        residuals = [[1], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
        channels = [[24], [40, 40, 40, 40], [56, 56, 56, 56], [112, 112, 112, 112, 136, 136, 136, 136],
                    [256, 256, 256, 256, 448]]
        kernel_sizes = [[3], [5, 3, 3, 3], [7, 3, 5, 5], [7, 5, 5, 5, 5, 5, 5, 5], [7, 7, 7, 7, 7]]
        expansions = [[1], [3, 3, 3, 3], [3, 3, 3, 3], [6, 3, 3, 3, 6, 3, 3, 3], [6, 6, 3, 3, 6]]
        init_block_channels = 48
        final_block_channels = 1792
    else:
        raise ValueError("Unsupported ProxylessNAS version: {}".format(version))

    shortcuts = [[0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1, 0, 1, 1, 1], [0, 1, 1, 1, 0]]

    net = ProxylessNAS(
        channels=channels,
        init_block_channels=init_block_channels,
        final_block_channels=final_block_channels,
        residuals=residuals,
        shortcuts=shortcuts,
        kernel_sizes=kernel_sizes,
        expansions=expansions,
        **kwargs)

    if pretrained:
        if (model_name is None) or (not model_name):
            raise ValueError("Parameter `model_name` should be properly initialized for loading pretrained model.")
        from .common.model_store import download_model
        download_model(
            net=net,
            model_name=model_name,
            local_model_store_dir_path=root)

    return net


def proxylessnas_cpu(**kwargs) -> nn.Module:
    """
    ProxylessNAS (CPU) model from 'ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware,'
    https://arxiv.org/abs/1812.00332.

    Parameters
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.

    Returns
    -------
    nn.Module
        Desired module.
    """
    return get_proxylessnas(
        version="cpu",
        model_name="proxylessnas_cpu",
        **kwargs)


def proxylessnas_gpu(**kwargs) -> nn.Module:
    """
    ProxylessNAS (GPU) model from 'ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware,'
    https://arxiv.org/abs/1812.00332.

    Parameters
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.

    Returns
    -------
    nn.Module
        Desired module.
    """
    return get_proxylessnas(
        version="gpu",
        model_name="proxylessnas_gpu",
        **kwargs)


def proxylessnas_mobile(**kwargs) -> nn.Module:
    """
    ProxylessNAS (Mobile) model from 'ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware,'
    https://arxiv.org/abs/1812.00332.

    Parameters
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.

    Returns
    -------
    nn.Module
        Desired module.
    """
    return get_proxylessnas(
        version="mobile",
        model_name="proxylessnas_mobile",
        **kwargs)


def proxylessnas_mobile14(**kwargs) -> nn.Module:
    """
    ProxylessNAS (Mobile-14) model from 'ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware,'
    https://arxiv.org/abs/1812.00332.

    Parameters
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.

    Returns
    -------
    nn.Module
        Desired module.
    """
    return get_proxylessnas(
        version="mobile14",
        model_name="proxylessnas_mobile14",
        **kwargs)


def _test():
    import torch
    from .common.model_store import calc_net_weight_count

    pretrained = False

    models = [
        proxylessnas_cpu,
        proxylessnas_gpu,
        proxylessnas_mobile,
        proxylessnas_mobile14,
    ]

    for model in models:

        net = model(pretrained=pretrained)

        # net.train()
        net.eval()
        weight_count = calc_net_weight_count(net)
        print("m={}, {}".format(model.__name__, weight_count))
        assert (model != proxylessnas_cpu or weight_count == 4361648)
        assert (model != proxylessnas_gpu or weight_count == 7119848)
        assert (model != proxylessnas_mobile or weight_count == 4080512)
        assert (model != proxylessnas_mobile14 or weight_count == 6857568)

        x = torch.randn(14, 3, 224, 224)
        y = net(x)
        y.sum().backward()
        assert (tuple(y.size()) == (14, 1000))


if __name__ == "__main__":
    _test()
