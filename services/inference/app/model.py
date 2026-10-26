from collections import OrderedDict

import torch
from torch import nn

MODEL_INPUT_SHAPE = (6, 1, 1, 512, 512)
OUTPUT_LENGTH = 6


class ConvLSTMCell(nn.Module):
    def __init__(
        self,
        input_channel: int,
        num_filter: int,
        kernel_size: int = 3,
        stride: int = 1,
        padding: int = 1,
    ) -> None:
        super().__init__()
        self._conv = nn.Conv2d(
            input_channel + num_filter,
            num_filter * 4,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
        )
        self._input_channel = input_channel
        self._num_filter = num_filter

    def forward(
        self,
        inputs: torch.Tensor | None,
        states: tuple[torch.Tensor, torch.Tensor] | None = None,
        seq_len: int = 6,
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        if states is None:
            if inputs is None:
                raise ValueError("inputs are required when states are not provided")
            batch_size, _, height, width = inputs.shape[1:]
            hidden = inputs.new_zeros(batch_size, self._num_filter, height, width)
            cell = hidden.clone()
        else:
            hidden, cell = states

        outputs = []
        for index in range(seq_len):
            if inputs is None:
                input_frame = hidden.new_zeros(
                    hidden.size(0),
                    self._input_channel,
                    hidden.size(2),
                    hidden.size(3),
                )
            else:
                input_frame = inputs[index]
            input_gate, forget_gate, candidate, output_gate = self._conv(
                torch.cat((input_frame, hidden), dim=1)
            ).chunk(4, dim=1)
            input_gate = torch.sigmoid(input_gate)
            forget_gate = torch.sigmoid(forget_gate)
            candidate = torch.tanh(candidate)
            cell = forget_gate * cell + input_gate * candidate
            output_gate = torch.sigmoid(output_gate)
            hidden = output_gate * torch.tanh(cell)
            outputs.append(hidden)
        return torch.stack(outputs), (hidden, cell)


class Encoder(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.blocks = 3
        self.stage1 = nn.Sequential(
            OrderedDict(
                [("conv1_leaky_1", nn.Conv2d(1, 8, 7, stride=5, padding=1))]
                + [("leaky_conv1_leaky_1", nn.LeakyReLU(0.2, inplace=True))]
            )
        )
        self.rnn1 = ConvLSTMCell(8, 64)
        self.stage2 = nn.Sequential(
            OrderedDict(
                [("conv2_leaky_1", nn.Conv2d(64, 192, 5, stride=3, padding=1))]
                + [("leaky_conv2_leaky_1", nn.LeakyReLU(0.2, inplace=True))]
            )
        )
        self.rnn2 = ConvLSTMCell(192, 192)
        self.stage3 = nn.Sequential(
            OrderedDict(
                [("conv3_leaky_1", nn.Conv2d(192, 192, 3, stride=2, padding=1))]
                + [("leaky_conv3_leaky_1", nn.LeakyReLU(0.2, inplace=True))]
            )
        )
        self.rnn3 = ConvLSTMCell(192, 192)

    @staticmethod
    def _forward_stage(
        inputs: torch.Tensor, subnet: nn.Module, rnn: ConvLSTMCell
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        sequence_length, batch_size, channels, height, width = inputs.shape
        transformed = subnet(inputs.reshape(-1, channels, height, width))
        transformed = transformed.reshape(
            sequence_length, batch_size, *transformed.shape[1:]
        )
        return rnn(transformed, None, sequence_length)

    def forward(
        self, inputs: torch.Tensor
    ) -> tuple[
        tuple[torch.Tensor, torch.Tensor],
        tuple[torch.Tensor, torch.Tensor],
        tuple[torch.Tensor, torch.Tensor],
    ]:
        states = []
        for stage, rnn in (
            (self.stage1, self.rnn1),
            (self.stage2, self.rnn2),
            (self.stage3, self.rnn3),
        ):
            inputs, state = self._forward_stage(inputs, stage, rnn)
            states.append(state)
        return states[0], states[1], states[2]


class Forecaster(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.blocks = 3
        self.rnn3 = ConvLSTMCell(192, 192)
        self.stage3 = nn.Sequential(
            OrderedDict(
                [
                    (
                        "deconv1_leaky_1",
                        nn.ConvTranspose2d(192, 192, 4, stride=2, padding=1),
                    ),
                    ("leaky_deconv1_leaky_1", nn.LeakyReLU(0.2, inplace=True)),
                ]
            )
        )
        self.rnn2 = ConvLSTMCell(192, 192)
        self.stage2 = nn.Sequential(
            OrderedDict(
                [
                    (
                        "deconv2_leaky_1",
                        nn.ConvTranspose2d(
                            192, 64, 5, stride=3, padding=1
                        ),
                    ),
                    ("leaky_deconv2_leaky_1", nn.LeakyReLU(0.2, inplace=True)),
                ]
            )
        )
        self.rnn1 = ConvLSTMCell(64, 64)
        self.stage1 = nn.Sequential(
            OrderedDict(
                [
                    (
                        "deconv3_leaky_1",
                        nn.ConvTranspose2d(
                            64, 8, 7, stride=5, padding=1, output_padding=2
                        ),
                    ),
                    ("leaky_deconv3_leaky_1", nn.LeakyReLU(0.2, inplace=True)),
                    ("conv3_leaky_2", nn.Conv2d(8, 8, 3, padding=1)),
                    ("leaky_conv3_leaky_2", nn.LeakyReLU(0.2, inplace=True)),
                    ("conv3_3", nn.Conv2d(8, 1, 1)),
                ]
            )
        )

    @staticmethod
    def _forward_stage(
        inputs: torch.Tensor | None,
        state: tuple[torch.Tensor, torch.Tensor],
        subnet: nn.Module,
        rnn: ConvLSTMCell,
    ) -> torch.Tensor:
        recurrent, _ = rnn(inputs, state, OUTPUT_LENGTH)
        sequence_length, batch_size, channels, height, width = recurrent.shape
        transformed = subnet(recurrent.reshape(-1, channels, height, width))
        return transformed.reshape(
            sequence_length, batch_size, *transformed.shape[1:]
        )

    def forward(
        self,
        hidden_states: tuple[
            tuple[torch.Tensor, torch.Tensor],
            tuple[torch.Tensor, torch.Tensor],
            tuple[torch.Tensor, torch.Tensor],
        ],
    ) -> torch.Tensor:
        inputs = self._forward_stage(
            None, hidden_states[-1], self.stage3, self.rnn3
        )
        inputs = self._forward_stage(
            inputs, hidden_states[1], self.stage2, self.rnn2
        )
        inputs = self._forward_stage(
            inputs, hidden_states[0], self.stage1, self.rnn1
        )
        return inputs


class EF(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.encoder = Encoder()
        self.forecaster = Forecaster()

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim != 5 or tuple(inputs.shape[1:]) != MODEL_INPUT_SHAPE[1:]:
            raise ValueError(
                "model input must have shape [6, B, 1, 512, 512]; "
                f"received {tuple(inputs.shape)}"
            )
        if inputs.shape[0] != MODEL_INPUT_SHAPE[0]:
            raise ValueError(
                "model input must have shape [6, B, 1, 512, 512]; "
                f"received {tuple(inputs.shape)}"
            )
        return self.forecaster(self.encoder(inputs))


def build_model() -> nn.Module:
    return EF()
