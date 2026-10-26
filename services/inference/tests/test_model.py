import pytest
import torch

from app.model import MODEL_INPUT_SHAPE, ConvLSTMCell, build_model

EXPECTED_STATE_KEYS = [
    "encoder.stage1.conv1_leaky_1.weight",
    "encoder.stage1.conv1_leaky_1.bias",
    "encoder.rnn1._conv.weight",
    "encoder.rnn1._conv.bias",
    "encoder.stage2.conv2_leaky_1.weight",
    "encoder.stage2.conv2_leaky_1.bias",
    "encoder.rnn2._conv.weight",
    "encoder.rnn2._conv.bias",
    "encoder.stage3.conv3_leaky_1.weight",
    "encoder.stage3.conv3_leaky_1.bias",
    "encoder.rnn3._conv.weight",
    "encoder.rnn3._conv.bias",
    "forecaster.rnn3._conv.weight",
    "forecaster.rnn3._conv.bias",
    "forecaster.stage3.deconv1_leaky_1.weight",
    "forecaster.stage3.deconv1_leaky_1.bias",
    "forecaster.rnn2._conv.weight",
    "forecaster.rnn2._conv.bias",
    "forecaster.stage2.deconv2_leaky_1.weight",
    "forecaster.stage2.deconv2_leaky_1.bias",
    "forecaster.rnn1._conv.weight",
    "forecaster.rnn1._conv.bias",
    "forecaster.stage1.deconv3_leaky_1.weight",
    "forecaster.stage1.deconv3_leaky_1.bias",
    "forecaster.stage1.conv3_leaky_2.weight",
    "forecaster.stage1.conv3_leaky_2.bias",
    "forecaster.stage1.conv3_3.weight",
    "forecaster.stage1.conv3_3.bias",
]
EXPECTED_STATE_SHAPES = [
    (8, 1, 7, 7),
    (8,),
    (256, 72, 3, 3),
    (256,),
    (192, 64, 5, 5),
    (192,),
    (768, 384, 3, 3),
    (768,),
    (192, 192, 3, 3),
    (192,),
    (768, 384, 3, 3),
    (768,),
    (768, 384, 3, 3),
    (768,),
    (192, 192, 4, 4),
    (192,),
    (768, 384, 3, 3),
    (768,),
    (192, 64, 5, 5),
    (64,),
    (256, 128, 3, 3),
    (256,),
    (64, 8, 7, 7),
    (8,),
    (8, 8, 3, 3),
    (8,),
    (1, 8, 1, 1),
    (1,),
]


def test_conv_lstm_uses_i_f_g_o_gate_order() -> None:
    cell = ConvLSTMCell(1, 1)
    with torch.no_grad():
        cell._conv.weight.zero_()
        cell._conv.bias.copy_(
            torch.tensor([0.0, 0.0, torch.atanh(torch.tensor(0.5)), 0.0])
        )

    output, (_, state_cell) = cell(torch.ones(1, 1, 1, 1, 1), seq_len=1)

    expected_cell = torch.sigmoid(torch.tensor(0.0)) * 0.5
    expected_hidden = torch.sigmoid(torch.tensor(0.0)) * torch.tanh(expected_cell)
    assert state_cell.item() == pytest.approx(expected_cell.item())
    assert output.item() == pytest.approx(expected_hidden.item())


def test_model_state_dict_matches_checkpoint_contract() -> None:
    model = build_model()
    assert list(model.state_dict()) == EXPECTED_STATE_KEYS
    assert [tuple(value.shape) for value in model.state_dict().values()] == EXPECTED_STATE_SHAPES


def test_model_returns_six_512_frames() -> None:
    model = build_model().eval()
    inputs = torch.rand(MODEL_INPUT_SHAPE)

    with torch.no_grad():
        outputs = model(inputs)

    assert outputs.shape == (6, 1, 1, 512, 512)
    assert torch.isfinite(outputs).all()


def test_model_rejects_wrong_spatial_size() -> None:
    model = build_model()

    with pytest.raises(ValueError, match=r"\[6, B, 1, 512, 512\]"):
        model(torch.rand(6, 1, 1, 360, 360))
