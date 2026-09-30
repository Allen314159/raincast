from collections import OrderedDict

import torch
import torch.nn.functional as F
from torch import nn


def make_layers(block):
    layers = []
    for layer_name, v in block.items():
        if "pool" in layer_name:
            layer = nn.MaxPool2d(kernel_size=v[0], stride=v[1], padding=v[2])
            layers.append((layer_name, layer))
        elif "deconv" in layer_name:
            output_padding = v[5] if len(v) > 5 else 0
            transposeConv2d = nn.ConvTranspose2d(
                in_channels=v[0],
                out_channels=v[1],
                kernel_size=v[2],
                stride=v[3],
                padding=v[4],
                output_padding=output_padding,
            )
            layers.append((layer_name, transposeConv2d))
            if "relu" in layer_name:
                layers.append(("relu_" + layer_name, nn.ReLU(inplace=True)))
            elif "leaky" in layer_name:
                layers.append(
                    (
                        "leaky_" + layer_name,
                        nn.LeakyReLU(negative_slope=0.2, inplace=True),
                    )
                )
        elif "conv" in layer_name:
            conv2d = nn.Conv2d(
                in_channels=v[0],
                out_channels=v[1],
                kernel_size=v[2],
                stride=v[3],
                padding=v[4],
            )
            layers.append((layer_name, conv2d))
            if "relu" in layer_name:
                layers.append(("relu_" + layer_name, nn.ReLU(inplace=True)))
            elif "leaky" in layer_name:
                layers.append(
                    (
                        "leaky_" + layer_name,
                        nn.LeakyReLU(negative_slope=0.2, inplace=True),
                    )
                )
        else:
            raise NotImplementedError

    return nn.Sequential(OrderedDict(layers))


class activation:
    def __init__(self, act_type, negative_slope=0.2, inplace=True):
        super().__init__()
        self._act_type = act_type
        self.negative_slope = negative_slope
        self.inplace = inplace

    def __call__(self, input):
        if self._act_type == "leaky":
            return F.leaky_relu(
                input, negative_slope=self.negative_slope, inplace=self.inplace
            )
        elif self._act_type == "relu":
            return F.relu(input, inplace=self.inplace)
        elif self._act_type == "sigmoid":
            return torch.sigmoid(input)
        else:
            raise NotImplementedError


class EF(nn.Module):
    def __init__(self, encoder, forecaster):
        super().__init__()
        self.encoder = encoder
        self.forecaster = forecaster

    def forward(self, input):
        state = self.encoder(input)
        output = self.forecaster(state)
        return output


class ConvLSTMCell(nn.Module):
    def __init__(self, input_channels: int, hidden_channels: int) -> None:
        super().__init__()
        self.hidden_channels = hidden_channels
        self._conv = nn.Conv2d(
            input_channels + hidden_channels, 4 * hidden_channels, 3, padding=1
        )

    def forward(
        self,
        input_frame: torch.Tensor,
        state: tuple[torch.Tensor, torch.Tensor] | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if state is None:
            batch, _, height, width = input_frame.shape
            zeros = input_frame.new_zeros(batch, self.hidden_channels, height, width)
            state = (zeros, zeros)
        hidden, cell = state
        input_gate, forget_gate, output_gate, candidate = self._conv(
            torch.cat((input_frame, hidden), dim=1)
        ).chunk(4, dim=1)
        input_gate = torch.sigmoid(input_gate)
        forget_gate = torch.sigmoid(forget_gate)
        output_gate = torch.sigmoid(output_gate)
        candidate = torch.tanh(candidate)
        cell = forget_gate * cell + input_gate * candidate
        hidden = output_gate * torch.tanh(cell)
        return hidden, cell


class Encoder(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.stage1 = nn.Sequential(
            OrderedDict([("conv1_leaky_1", nn.Conv2d(1, 8, 7, stride=2, padding=3))])
        )
        self.stage2 = nn.Sequential(
            OrderedDict([("conv2_leaky_1", nn.Conv2d(64, 192, 5, stride=2, padding=2))])
        )
        self.stage3 = nn.Sequential(
            OrderedDict([("conv3_leaky_1", nn.Conv2d(192, 192, 3, padding=1))])
        )
        self.rnn1 = ConvLSTMCell(8, 64)
        self.rnn2 = ConvLSTMCell(192, 192)
        self.rnn3 = ConvLSTMCell(192, 192)

    def forward(
        self, input_sequence: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        state1 = state2 = state3 = None
        for input_frame in input_sequence:
            stage1 = F.leaky_relu(self.stage1(input_frame), negative_slope=0.2)
            hidden1, cell1 = self.rnn1(stage1, state1)
            state1 = (hidden1, cell1)
            stage2 = F.leaky_relu(self.stage2(hidden1), negative_slope=0.2)
            hidden2, cell2 = self.rnn2(stage2, state2)
            state2 = (hidden2, cell2)
            stage3 = F.leaky_relu(self.stage3(hidden2), negative_slope=0.2)
            hidden3, cell3 = self.rnn3(stage3, state3)
            state3 = (hidden3, cell3)
        if state1 is None or state2 is None or state3 is None:
            raise ValueError("The input sequence cannot be empty")
        return state1[0], state2[0], state3[0]


class Forecaster(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.rnn3 = ConvLSTMCell(192, 192)
        self.rnn2 = ConvLSTMCell(192, 192)
        self.rnn1 = ConvLSTMCell(64, 64)
        self.stage3 = nn.Sequential(
            OrderedDict(
                [
                    (
                        "deconv1_leaky_1",
                        nn.ConvTranspose2d(192, 192, 4, stride=2, padding=1),
                    )
                ]
            )
        )
        self.stage2 = nn.Sequential(
            OrderedDict(
                [
                    (
                        "deconv2_leaky_1",
                        nn.ConvTranspose2d(
                            192, 64, 5, stride=2, padding=2, output_padding=1
                        ),
                    )
                ]
            )
        )
        self.stage1 = nn.Sequential(
            OrderedDict(
                [
                    (
                        "deconv3_leaky_1",
                        nn.ConvTranspose2d(64, 8, 7, padding=3),
                    ),
                    ("conv3_leaky_2", nn.Conv2d(8, 8, 3, padding=1)),
                    ("conv3_3", nn.Conv2d(8, 1, 1)),
                ]
            )
        )

    def forward(
        self, encoder_state: tuple[torch.Tensor, torch.Tensor, torch.Tensor]
    ) -> torch.Tensor:
        hidden1, hidden2, hidden3 = encoder_state
        state1 = state2 = state3 = None
        outputs = []
        for _ in range(6):
            hidden3, cell3 = self.rnn3(hidden3, state3)
            state3 = (hidden3, cell3)
            stage3 = F.leaky_relu(self.stage3(hidden3), negative_slope=0.2)
            hidden2, cell2 = self.rnn2(stage3, state2)
            state2 = (hidden2, cell2)
            stage2 = F.leaky_relu(self.stage2(hidden2), negative_slope=0.2)
            hidden1, cell1 = self.rnn1(stage2, state1)
            state1 = (hidden1, cell1)
            output = F.leaky_relu(self.stage1[0](hidden1), negative_slope=0.2)
            output = F.leaky_relu(self.stage1[1](output), negative_slope=0.2)
            outputs.append(self.stage1[2](output))
        return torch.stack(outputs)


def build_model() -> nn.Module:
    return EF(Encoder(), Forecaster())


class Predictor(nn.Module):
    def __init__(self, params):
        super().__init__()
        self.model = make_layers(params)

    def forward(self, input):
        """
        input: S*B*1*H*W
        :param input:
        :return:
        """
        input = input.squeeze(2).permute((1, 0, 2, 3))
        output = self.model(input)
        return output.unsqueeze(2).permute((1, 0, 2, 3, 4))
