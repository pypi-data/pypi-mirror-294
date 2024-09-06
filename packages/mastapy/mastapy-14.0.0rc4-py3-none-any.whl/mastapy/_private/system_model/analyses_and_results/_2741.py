"""PartAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2737

_PART_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "PartAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7423,
        _7424,
        _7425,
        _7430,
        _7432,
        _7433,
        _7434,
        _7436,
        _7437,
        _7439,
        _7440,
        _7441,
        _7442,
        _7444,
        _7445,
        _7446,
        _7447,
        _7449,
        _7451,
        _7452,
        _7454,
        _7455,
        _7457,
        _7458,
        _7460,
        _7462,
        _7464,
        _7466,
        _7467,
        _7469,
        _7470,
        _7471,
        _7474,
        _7476,
        _7478,
        _7479,
        _7480,
        _7481,
        _7483,
        _7484,
        _7485,
        _7486,
        _7488,
        _7489,
        _7490,
        _7492,
        _7494,
        _7496,
        _7497,
        _7499,
        _7500,
        _7502,
        _7504,
        _7505,
        _7506,
        _7507,
        _7508,
        _7509,
        _7510,
        _7511,
        _7513,
        _7515,
        _7516,
        _7517,
        _7518,
        _7519,
        _7520,
        _7522,
        _7523,
        _7525,
        _7526,
        _7527,
        _7529,
        _7530,
        _7532,
        _7533,
        _7535,
        _7536,
        _7538,
        _7539,
        _7541,
        _7542,
        _7543,
        _7544,
        _7545,
        _7546,
        _7547,
        _7548,
        _7550,
        _7551,
        _7553,
        _7554,
        _7555,
        _7557,
        _7558,
        _7560,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7155,
        _7156,
        _7157,
        _7163,
        _7165,
        _7166,
        _7168,
        _7170,
        _7171,
        _7173,
        _7174,
        _7175,
        _7176,
        _7178,
        _7179,
        _7180,
        _7181,
        _7183,
        _7185,
        _7186,
        _7188,
        _7189,
        _7191,
        _7192,
        _7194,
        _7196,
        _7197,
        _7199,
        _7200,
        _7202,
        _7203,
        _7204,
        _7207,
        _7209,
        _7210,
        _7211,
        _7212,
        _7213,
        _7215,
        _7216,
        _7217,
        _7218,
        _7220,
        _7221,
        _7223,
        _7225,
        _7227,
        _7229,
        _7230,
        _7232,
        _7233,
        _7235,
        _7236,
        _7237,
        _7238,
        _7239,
        _7240,
        _7241,
        _7242,
        _7243,
        _7245,
        _7247,
        _7248,
        _7249,
        _7250,
        _7251,
        _7252,
        _7254,
        _7255,
        _7257,
        _7258,
        _7259,
        _7261,
        _7262,
        _7264,
        _7265,
        _7267,
        _7268,
        _7270,
        _7271,
        _7273,
        _7274,
        _7275,
        _7276,
        _7277,
        _7278,
        _7279,
        _7280,
        _7282,
        _7283,
        _7284,
        _7285,
        _7286,
        _7288,
        _7289,
        _7291,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7716,
        _7717,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6686,
        _6687,
        _6688,
        _6690,
        _6692,
        _6693,
        _6694,
        _6696,
        _6697,
        _6699,
        _6700,
        _6701,
        _6702,
        _6704,
        _6705,
        _6706,
        _6708,
        _6709,
        _6711,
        _6713,
        _6714,
        _6715,
        _6717,
        _6718,
        _6720,
        _6722,
        _6724,
        _6725,
        _6730,
        _6731,
        _6732,
        _6734,
        _6736,
        _6738,
        _6739,
        _6740,
        _6741,
        _6742,
        _6744,
        _6745,
        _6746,
        _6747,
        _6749,
        _6750,
        _6751,
        _6753,
        _6755,
        _6757,
        _6758,
        _6760,
        _6761,
        _6763,
        _6764,
        _6765,
        _6766,
        _6767,
        _6768,
        _6769,
        _6770,
        _6772,
        _6773,
        _6775,
        _6776,
        _6777,
        _6778,
        _6779,
        _6780,
        _6782,
        _6784,
        _6785,
        _6786,
        _6787,
        _6789,
        _6790,
        _6792,
        _6794,
        _6795,
        _6796,
        _6798,
        _6799,
        _6801,
        _6802,
        _6803,
        _6804,
        _6805,
        _6806,
        _6807,
        _6809,
        _6810,
        _6811,
        _6812,
        _6813,
        _6814,
        _6816,
        _6817,
        _6819,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6416,
        _6417,
        _6418,
        _6420,
        _6422,
        _6423,
        _6424,
        _6426,
        _6427,
        _6429,
        _6430,
        _6431,
        _6432,
        _6434,
        _6435,
        _6436,
        _6438,
        _6439,
        _6441,
        _6443,
        _6444,
        _6445,
        _6447,
        _6448,
        _6450,
        _6452,
        _6454,
        _6455,
        _6457,
        _6458,
        _6459,
        _6461,
        _6463,
        _6465,
        _6466,
        _6467,
        _6470,
        _6471,
        _6473,
        _6474,
        _6475,
        _6476,
        _6478,
        _6479,
        _6480,
        _6482,
        _6484,
        _6486,
        _6487,
        _6489,
        _6490,
        _6492,
        _6493,
        _6494,
        _6495,
        _6496,
        _6497,
        _6498,
        _6499,
        _6501,
        _6502,
        _6504,
        _6505,
        _6506,
        _6507,
        _6508,
        _6509,
        _6511,
        _6513,
        _6514,
        _6515,
        _6516,
        _6518,
        _6519,
        _6521,
        _6523,
        _6524,
        _6525,
        _6527,
        _6528,
        _6530,
        _6531,
        _6532,
        _6533,
        _6534,
        _6535,
        _6536,
        _6538,
        _6539,
        _6540,
        _6541,
        _6542,
        _6543,
        _6545,
        _6546,
        _6548,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5809,
        _5811,
        _5812,
        _5814,
        _5816,
        _5817,
        _5818,
        _5820,
        _5821,
        _5823,
        _5824,
        _5825,
        _5826,
        _5828,
        _5829,
        _5830,
        _5832,
        _5833,
        _5836,
        _5838,
        _5839,
        _5840,
        _5842,
        _5843,
        _5845,
        _5847,
        _5849,
        _5850,
        _5852,
        _5853,
        _5854,
        _5856,
        _5858,
        _5860,
        _5861,
        _5862,
        _5877,
        _5878,
        _5880,
        _5881,
        _5882,
        _5884,
        _5889,
        _5891,
        _5902,
        _5904,
        _5906,
        _5908,
        _5909,
        _5911,
        _5912,
        _5914,
        _5915,
        _5916,
        _5917,
        _5918,
        _5919,
        _5920,
        _5921,
        _5923,
        _5924,
        _5927,
        _5928,
        _5929,
        _5930,
        _5931,
        _5933,
        _5935,
        _5937,
        _5938,
        _5939,
        _5940,
        _5943,
        _5945,
        _5947,
        _5949,
        _5950,
        _5952,
        _5954,
        _5955,
        _5957,
        _5958,
        _5959,
        _5960,
        _5961,
        _5962,
        _5963,
        _5965,
        _5966,
        _5967,
        _5969,
        _5970,
        _5971,
        _5973,
        _5974,
        _5976,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6143,
        _6144,
        _6145,
        _6147,
        _6149,
        _6150,
        _6151,
        _6153,
        _6154,
        _6156,
        _6157,
        _6158,
        _6159,
        _6161,
        _6162,
        _6163,
        _6165,
        _6166,
        _6168,
        _6170,
        _6171,
        _6172,
        _6174,
        _6175,
        _6177,
        _6179,
        _6181,
        _6182,
        _6184,
        _6185,
        _6186,
        _6188,
        _6190,
        _6192,
        _6193,
        _6194,
        _6195,
        _6196,
        _6198,
        _6199,
        _6200,
        _6201,
        _6203,
        _6204,
        _6206,
        _6208,
        _6210,
        _6212,
        _6213,
        _6215,
        _6216,
        _6218,
        _6219,
        _6220,
        _6221,
        _6222,
        _6224,
        _6225,
        _6226,
        _6228,
        _6229,
        _6231,
        _6232,
        _6233,
        _6234,
        _6235,
        _6236,
        _6238,
        _6240,
        _6241,
        _6242,
        _6243,
        _6245,
        _6246,
        _6248,
        _6250,
        _6251,
        _6252,
        _6254,
        _6255,
        _6257,
        _6258,
        _6259,
        _6260,
        _6261,
        _6262,
        _6263,
        _6265,
        _6266,
        _6267,
        _6268,
        _6269,
        _6270,
        _6272,
        _6273,
        _6275,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5500,
        _5501,
        _5502,
        _5505,
        _5506,
        _5508,
        _5510,
        _5513,
        _5515,
        _5516,
        _5517,
        _5518,
        _5520,
        _5521,
        _5522,
        _5523,
        _5525,
        _5526,
        _5529,
        _5531,
        _5532,
        _5534,
        _5535,
        _5537,
        _5538,
        _5540,
        _5542,
        _5543,
        _5545,
        _5546,
        _5547,
        _5549,
        _5552,
        _5553,
        _5554,
        _5555,
        _5556,
        _5558,
        _5559,
        _5560,
        _5561,
        _5564,
        _5565,
        _5566,
        _5568,
        _5569,
        _5576,
        _5577,
        _5579,
        _5580,
        _5582,
        _5583,
        _5584,
        _5588,
        _5589,
        _5590,
        _5591,
        _5593,
        _5594,
        _5596,
        _5597,
        _5599,
        _5600,
        _5601,
        _5602,
        _5603,
        _5604,
        _5606,
        _5608,
        _5609,
        _5612,
        _5613,
        _5616,
        _5618,
        _5619,
        _5622,
        _5623,
        _5625,
        _5626,
        _5628,
        _5629,
        _5630,
        _5631,
        _5632,
        _5633,
        _5634,
        _5635,
        _5638,
        _5639,
        _5641,
        _5642,
        _5643,
        _5646,
        _5647,
        _5649,
        _5650,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4684,
        _4685,
        _4686,
        _4689,
        _4690,
        _4691,
        _4692,
        _4694,
        _4696,
        _4697,
        _4698,
        _4699,
        _4701,
        _4702,
        _4703,
        _4704,
        _4706,
        _4707,
        _4709,
        _4711,
        _4712,
        _4714,
        _4715,
        _4717,
        _4718,
        _4720,
        _4723,
        _4724,
        _4726,
        _4727,
        _4728,
        _4730,
        _4733,
        _4734,
        _4735,
        _4736,
        _4740,
        _4742,
        _4743,
        _4744,
        _4745,
        _4748,
        _4749,
        _4750,
        _4752,
        _4753,
        _4756,
        _4757,
        _4759,
        _4760,
        _4762,
        _4763,
        _4764,
        _4765,
        _4766,
        _4767,
        _4772,
        _4774,
        _4776,
        _4778,
        _4779,
        _4781,
        _4782,
        _4783,
        _4784,
        _4785,
        _4786,
        _4788,
        _4790,
        _4791,
        _4792,
        _4793,
        _4796,
        _4798,
        _4799,
        _4801,
        _4802,
        _4804,
        _4805,
        _4807,
        _4808,
        _4809,
        _4810,
        _4811,
        _4812,
        _4813,
        _4814,
        _4816,
        _4817,
        _4818,
        _4819,
        _4820,
        _4825,
        _4826,
        _4828,
        _4829,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5237,
        _5238,
        _5239,
        _5242,
        _5243,
        _5244,
        _5245,
        _5247,
        _5249,
        _5250,
        _5251,
        _5252,
        _5254,
        _5255,
        _5256,
        _5257,
        _5259,
        _5260,
        _5262,
        _5264,
        _5265,
        _5267,
        _5268,
        _5270,
        _5271,
        _5273,
        _5275,
        _5276,
        _5278,
        _5279,
        _5280,
        _5282,
        _5285,
        _5286,
        _5287,
        _5288,
        _5289,
        _5291,
        _5292,
        _5293,
        _5294,
        _5296,
        _5297,
        _5298,
        _5300,
        _5301,
        _5304,
        _5305,
        _5307,
        _5308,
        _5310,
        _5311,
        _5312,
        _5313,
        _5314,
        _5315,
        _5317,
        _5318,
        _5319,
        _5321,
        _5322,
        _5324,
        _5325,
        _5326,
        _5327,
        _5328,
        _5329,
        _5331,
        _5333,
        _5334,
        _5335,
        _5336,
        _5338,
        _5340,
        _5341,
        _5343,
        _5344,
        _5346,
        _5347,
        _5349,
        _5350,
        _5351,
        _5352,
        _5353,
        _5354,
        _5355,
        _5356,
        _5358,
        _5359,
        _5360,
        _5361,
        _5362,
        _5364,
        _5365,
        _5367,
        _5368,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _4973,
        _4974,
        _4975,
        _4978,
        _4979,
        _4980,
        _4981,
        _4983,
        _4985,
        _4986,
        _4987,
        _4988,
        _4990,
        _4991,
        _4992,
        _4993,
        _4995,
        _4996,
        _4998,
        _5000,
        _5001,
        _5003,
        _5004,
        _5006,
        _5007,
        _5009,
        _5011,
        _5012,
        _5014,
        _5015,
        _5016,
        _5018,
        _5021,
        _5022,
        _5023,
        _5024,
        _5026,
        _5028,
        _5029,
        _5030,
        _5031,
        _5033,
        _5034,
        _5035,
        _5037,
        _5038,
        _5041,
        _5042,
        _5044,
        _5045,
        _5047,
        _5048,
        _5049,
        _5050,
        _5051,
        _5052,
        _5054,
        _5055,
        _5056,
        _5058,
        _5059,
        _5061,
        _5062,
        _5063,
        _5064,
        _5065,
        _5066,
        _5068,
        _5070,
        _5071,
        _5072,
        _5073,
        _5075,
        _5077,
        _5078,
        _5080,
        _5081,
        _5083,
        _5084,
        _5086,
        _5087,
        _5088,
        _5089,
        _5090,
        _5091,
        _5092,
        _5093,
        _5095,
        _5096,
        _5097,
        _5098,
        _5099,
        _5101,
        _5102,
        _5104,
        _5105,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4404,
        _4405,
        _4406,
        _4409,
        _4410,
        _4411,
        _4412,
        _4414,
        _4416,
        _4417,
        _4418,
        _4419,
        _4421,
        _4422,
        _4423,
        _4424,
        _4426,
        _4427,
        _4429,
        _4431,
        _4432,
        _4434,
        _4435,
        _4437,
        _4438,
        _4440,
        _4442,
        _4443,
        _4445,
        _4446,
        _4447,
        _4449,
        _4452,
        _4453,
        _4454,
        _4455,
        _4463,
        _4465,
        _4466,
        _4467,
        _4468,
        _4470,
        _4471,
        _4472,
        _4474,
        _4475,
        _4478,
        _4479,
        _4481,
        _4482,
        _4484,
        _4485,
        _4486,
        _4487,
        _4488,
        _4489,
        _4491,
        _4492,
        _4503,
        _4505,
        _4506,
        _4508,
        _4509,
        _4510,
        _4511,
        _4512,
        _4513,
        _4515,
        _4517,
        _4518,
        _4519,
        _4520,
        _4522,
        _4524,
        _4525,
        _4527,
        _4528,
        _4530,
        _4531,
        _4533,
        _4534,
        _4535,
        _4536,
        _4537,
        _4538,
        _4539,
        _4540,
        _4542,
        _4543,
        _4544,
        _4545,
        _4546,
        _4548,
        _4549,
        _4551,
        _4552,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4136,
        _4137,
        _4138,
        _4141,
        _4142,
        _4143,
        _4144,
        _4146,
        _4148,
        _4149,
        _4150,
        _4151,
        _4153,
        _4154,
        _4155,
        _4156,
        _4158,
        _4159,
        _4161,
        _4163,
        _4164,
        _4166,
        _4167,
        _4169,
        _4170,
        _4172,
        _4174,
        _4175,
        _4177,
        _4178,
        _4179,
        _4182,
        _4185,
        _4186,
        _4187,
        _4188,
        _4189,
        _4191,
        _4192,
        _4195,
        _4196,
        _4198,
        _4199,
        _4200,
        _4202,
        _4203,
        _4206,
        _4207,
        _4209,
        _4210,
        _4212,
        _4213,
        _4214,
        _4215,
        _4216,
        _4217,
        _4218,
        _4219,
        _4220,
        _4222,
        _4223,
        _4225,
        _4226,
        _4227,
        _4230,
        _4231,
        _4232,
        _4234,
        _4236,
        _4237,
        _4238,
        _4239,
        _4241,
        _4243,
        _4244,
        _4246,
        _4247,
        _4249,
        _4250,
        _4252,
        _4253,
        _4254,
        _4255,
        _4256,
        _4257,
        _4258,
        _4259,
        _4262,
        _4263,
        _4264,
        _4265,
        _4266,
        _4268,
        _4269,
        _4271,
        _4272,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3863,
        _3864,
        _3865,
        _3868,
        _3869,
        _3870,
        _3871,
        _3873,
        _3875,
        _3876,
        _3877,
        _3878,
        _3880,
        _3881,
        _3882,
        _3883,
        _3885,
        _3886,
        _3888,
        _3890,
        _3891,
        _3893,
        _3894,
        _3896,
        _3897,
        _3899,
        _3901,
        _3902,
        _3905,
        _3906,
        _3907,
        _3910,
        _3912,
        _3913,
        _3914,
        _3915,
        _3917,
        _3919,
        _3920,
        _3921,
        _3922,
        _3924,
        _3925,
        _3926,
        _3928,
        _3929,
        _3932,
        _3933,
        _3935,
        _3936,
        _3938,
        _3939,
        _3940,
        _3941,
        _3942,
        _3943,
        _3944,
        _3945,
        _3946,
        _3948,
        _3949,
        _3951,
        _3952,
        _3953,
        _3954,
        _3955,
        _3956,
        _3958,
        _3960,
        _3961,
        _3962,
        _3963,
        _3965,
        _3967,
        _3968,
        _3970,
        _3971,
        _3976,
        _3977,
        _3979,
        _3980,
        _3981,
        _3982,
        _3983,
        _3984,
        _3985,
        _3986,
        _3988,
        _3989,
        _3990,
        _3991,
        _3992,
        _3994,
        _3995,
        _3997,
        _3998,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6954,
        _6955,
        _6956,
        _6961,
        _6963,
        _6966,
        _6967,
        _6969,
        _6970,
        _6972,
        _6973,
        _6974,
        _6975,
        _6977,
        _6978,
        _6979,
        _6981,
        _6982,
        _6985,
        _6987,
        _6988,
        _6989,
        _6991,
        _6992,
        _6996,
        _6998,
        _7000,
        _7001,
        _7003,
        _7004,
        _7005,
        _7007,
        _7009,
        _7013,
        _7014,
        _7017,
        _7031,
        _7032,
        _7034,
        _7035,
        _7036,
        _7038,
        _7043,
        _7044,
        _7053,
        _7055,
        _7060,
        _7062,
        _7063,
        _7065,
        _7066,
        _7068,
        _7069,
        _7070,
        _7072,
        _7073,
        _7074,
        _7076,
        _7078,
        _7080,
        _7081,
        _7083,
        _7085,
        _7088,
        _7089,
        _7090,
        _7093,
        _7095,
        _7097,
        _7098,
        _7099,
        _7100,
        _7102,
        _7103,
        _7105,
        _7107,
        _7108,
        _7109,
        _7111,
        _7112,
        _7114,
        _7115,
        _7116,
        _7117,
        _7118,
        _7119,
        _7120,
        _7123,
        _7124,
        _7125,
        _7130,
        _7131,
        _7132,
        _7134,
        _7135,
        _7137,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3071,
        _3072,
        _3073,
        _3076,
        _3077,
        _3078,
        _3079,
        _3081,
        _3083,
        _3084,
        _3085,
        _3086,
        _3088,
        _3089,
        _3090,
        _3091,
        _3093,
        _3094,
        _3096,
        _3098,
        _3099,
        _3101,
        _3102,
        _3104,
        _3105,
        _3107,
        _3109,
        _3110,
        _3112,
        _3113,
        _3114,
        _3117,
        _3119,
        _3120,
        _3121,
        _3122,
        _3124,
        _3126,
        _3127,
        _3128,
        _3129,
        _3131,
        _3132,
        _3133,
        _3135,
        _3136,
        _3139,
        _3140,
        _3142,
        _3143,
        _3145,
        _3146,
        _3147,
        _3148,
        _3149,
        _3150,
        _3151,
        _3152,
        _3153,
        _3155,
        _3156,
        _3158,
        _3159,
        _3160,
        _3161,
        _3162,
        _3163,
        _3165,
        _3167,
        _3168,
        _3169,
        _3170,
        _3172,
        _3174,
        _3175,
        _3177,
        _3178,
        _3183,
        _3184,
        _3186,
        _3187,
        _3188,
        _3189,
        _3190,
        _3191,
        _3192,
        _3193,
        _3195,
        _3196,
        _3197,
        _3198,
        _3199,
        _3201,
        _3202,
        _3204,
        _3205,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3600,
        _3601,
        _3602,
        _3605,
        _3606,
        _3607,
        _3608,
        _3610,
        _3612,
        _3613,
        _3614,
        _3615,
        _3617,
        _3618,
        _3619,
        _3620,
        _3622,
        _3623,
        _3625,
        _3627,
        _3628,
        _3630,
        _3631,
        _3633,
        _3634,
        _3636,
        _3638,
        _3639,
        _3641,
        _3642,
        _3643,
        _3646,
        _3648,
        _3649,
        _3650,
        _3651,
        _3652,
        _3654,
        _3655,
        _3656,
        _3657,
        _3659,
        _3660,
        _3661,
        _3663,
        _3664,
        _3667,
        _3668,
        _3670,
        _3671,
        _3673,
        _3674,
        _3675,
        _3676,
        _3677,
        _3678,
        _3679,
        _3680,
        _3681,
        _3683,
        _3684,
        _3686,
        _3687,
        _3688,
        _3689,
        _3690,
        _3691,
        _3693,
        _3695,
        _3696,
        _3697,
        _3698,
        _3700,
        _3702,
        _3703,
        _3705,
        _3706,
        _3709,
        _3710,
        _3712,
        _3713,
        _3714,
        _3715,
        _3716,
        _3717,
        _3718,
        _3719,
        _3721,
        _3722,
        _3723,
        _3724,
        _3725,
        _3727,
        _3728,
        _3730,
        _3731,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3337,
        _3338,
        _3339,
        _3342,
        _3343,
        _3344,
        _3345,
        _3347,
        _3349,
        _3350,
        _3351,
        _3352,
        _3354,
        _3355,
        _3356,
        _3357,
        _3359,
        _3360,
        _3362,
        _3364,
        _3365,
        _3367,
        _3368,
        _3370,
        _3371,
        _3373,
        _3375,
        _3376,
        _3378,
        _3379,
        _3380,
        _3383,
        _3385,
        _3386,
        _3387,
        _3388,
        _3389,
        _3391,
        _3392,
        _3393,
        _3394,
        _3396,
        _3397,
        _3398,
        _3400,
        _3401,
        _3404,
        _3405,
        _3407,
        _3408,
        _3410,
        _3411,
        _3412,
        _3413,
        _3414,
        _3415,
        _3416,
        _3417,
        _3418,
        _3420,
        _3421,
        _3423,
        _3424,
        _3425,
        _3426,
        _3427,
        _3428,
        _3430,
        _3432,
        _3433,
        _3434,
        _3435,
        _3437,
        _3439,
        _3440,
        _3442,
        _3443,
        _3446,
        _3447,
        _3449,
        _3450,
        _3451,
        _3452,
        _3453,
        _3454,
        _3455,
        _3456,
        _3458,
        _3459,
        _3460,
        _3461,
        _3462,
        _3464,
        _3465,
        _3467,
        _3468,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2769,
        _2770,
        _2771,
        _2774,
        _2775,
        _2776,
        _2782,
        _2784,
        _2786,
        _2787,
        _2788,
        _2789,
        _2791,
        _2792,
        _2793,
        _2794,
        _2796,
        _2797,
        _2799,
        _2802,
        _2803,
        _2805,
        _2806,
        _2809,
        _2810,
        _2812,
        _2814,
        _2815,
        _2817,
        _2818,
        _2819,
        _2822,
        _2826,
        _2827,
        _2828,
        _2829,
        _2830,
        _2831,
        _2834,
        _2835,
        _2836,
        _2839,
        _2840,
        _2841,
        _2842,
        _2844,
        _2845,
        _2846,
        _2848,
        _2849,
        _2853,
        _2854,
        _2856,
        _2857,
        _2859,
        _2860,
        _2863,
        _2864,
        _2866,
        _2867,
        _2868,
        _2870,
        _2871,
        _2873,
        _2874,
        _2876,
        _2877,
        _2878,
        _2879,
        _2880,
        _2883,
        _2885,
        _2886,
        _2887,
        _2890,
        _2892,
        _2894,
        _2895,
        _2897,
        _2898,
        _2900,
        _2901,
        _2903,
        _2904,
        _2905,
        _2906,
        _2907,
        _2908,
        _2909,
        _2910,
        _2915,
        _2916,
        _2917,
        _2920,
        _2921,
        _2923,
        _2924,
        _2926,
        _2927,
    )

    Self = TypeVar("Self", bound="PartAnalysis")
    CastSelf = TypeVar("CastSelf", bound="PartAnalysis._Cast_PartAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("PartAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartAnalysis:
    """Special nested class for casting PartAnalysis to subclasses."""

    __parent__: "PartAnalysis"

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2737.DesignEntitySingleContextAnalysis":
        return self.__parent__._cast(_2737.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2769.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2769,
        )

        return self.__parent__._cast(_2769.AbstractAssemblySystemDeflection)

    @property
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2770.AbstractShaftOrHousingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2770,
        )

        return self.__parent__._cast(_2770.AbstractShaftOrHousingSystemDeflection)

    @property
    def abstract_shaft_system_deflection(
        self: "CastSelf",
    ) -> "_2771.AbstractShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2771,
        )

        return self.__parent__._cast(_2771.AbstractShaftSystemDeflection)

    @property
    def agma_gleason_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2774.AGMAGleasonConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2774,
        )

        return self.__parent__._cast(_2774.AGMAGleasonConicalGearSetSystemDeflection)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2775.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2775,
        )

        return self.__parent__._cast(_2775.AGMAGleasonConicalGearSystemDeflection)

    @property
    def assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2776.AssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2776,
        )

        return self.__parent__._cast(_2776.AssemblySystemDeflection)

    @property
    def bearing_system_deflection(self: "CastSelf") -> "_2782.BearingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2782,
        )

        return self.__parent__._cast(_2782.BearingSystemDeflection)

    @property
    def belt_drive_system_deflection(
        self: "CastSelf",
    ) -> "_2784.BeltDriveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2784,
        )

        return self.__parent__._cast(_2784.BeltDriveSystemDeflection)

    @property
    def bevel_differential_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2786.BevelDifferentialGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2786,
        )

        return self.__parent__._cast(_2786.BevelDifferentialGearSetSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2787.BevelDifferentialGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2787,
        )

        return self.__parent__._cast(_2787.BevelDifferentialGearSystemDeflection)

    @property
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2788.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2788,
        )

        return self.__parent__._cast(_2788.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2789.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2789,
        )

        return self.__parent__._cast(_2789.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2791.BevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2791,
        )

        return self.__parent__._cast(_2791.BevelGearSetSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2792.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2792,
        )

        return self.__parent__._cast(_2792.BevelGearSystemDeflection)

    @property
    def bolted_joint_system_deflection(
        self: "CastSelf",
    ) -> "_2793.BoltedJointSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2793,
        )

        return self.__parent__._cast(_2793.BoltedJointSystemDeflection)

    @property
    def bolt_system_deflection(self: "CastSelf") -> "_2794.BoltSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2794,
        )

        return self.__parent__._cast(_2794.BoltSystemDeflection)

    @property
    def clutch_half_system_deflection(
        self: "CastSelf",
    ) -> "_2796.ClutchHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2796,
        )

        return self.__parent__._cast(_2796.ClutchHalfSystemDeflection)

    @property
    def clutch_system_deflection(self: "CastSelf") -> "_2797.ClutchSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2797,
        )

        return self.__parent__._cast(_2797.ClutchSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2799.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2799,
        )

        return self.__parent__._cast(_2799.ComponentSystemDeflection)

    @property
    def concept_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2802.ConceptCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2802,
        )

        return self.__parent__._cast(_2802.ConceptCouplingHalfSystemDeflection)

    @property
    def concept_coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2803.ConceptCouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2803,
        )

        return self.__parent__._cast(_2803.ConceptCouplingSystemDeflection)

    @property
    def concept_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2805.ConceptGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2805,
        )

        return self.__parent__._cast(_2805.ConceptGearSetSystemDeflection)

    @property
    def concept_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2806.ConceptGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2806,
        )

        return self.__parent__._cast(_2806.ConceptGearSystemDeflection)

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2809.ConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2809,
        )

        return self.__parent__._cast(_2809.ConicalGearSetSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2810.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2810,
        )

        return self.__parent__._cast(_2810.ConicalGearSystemDeflection)

    @property
    def connector_system_deflection(
        self: "CastSelf",
    ) -> "_2812.ConnectorSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2812,
        )

        return self.__parent__._cast(_2812.ConnectorSystemDeflection)

    @property
    def coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2814.CouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2814,
        )

        return self.__parent__._cast(_2814.CouplingHalfSystemDeflection)

    @property
    def coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2815.CouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2815,
        )

        return self.__parent__._cast(_2815.CouplingSystemDeflection)

    @property
    def cvt_pulley_system_deflection(
        self: "CastSelf",
    ) -> "_2817.CVTPulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2817,
        )

        return self.__parent__._cast(_2817.CVTPulleySystemDeflection)

    @property
    def cvt_system_deflection(self: "CastSelf") -> "_2818.CVTSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2818,
        )

        return self.__parent__._cast(_2818.CVTSystemDeflection)

    @property
    def cycloidal_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2819.CycloidalAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2819,
        )

        return self.__parent__._cast(_2819.CycloidalAssemblySystemDeflection)

    @property
    def cycloidal_disc_system_deflection(
        self: "CastSelf",
    ) -> "_2822.CycloidalDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2822,
        )

        return self.__parent__._cast(_2822.CycloidalDiscSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2826.CylindricalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2826,
        )

        return self.__parent__._cast(_2826.CylindricalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2827.CylindricalGearSetSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2827,
        )

        return self.__parent__._cast(_2827.CylindricalGearSetSystemDeflectionTimestep)

    @property
    def cylindrical_gear_set_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2828.CylindricalGearSetSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2828,
        )

        return self.__parent__._cast(
            _2828.CylindricalGearSetSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2829.CylindricalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2829,
        )

        return self.__parent__._cast(_2829.CylindricalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2830.CylindricalGearSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2830,
        )

        return self.__parent__._cast(_2830.CylindricalGearSystemDeflectionTimestep)

    @property
    def cylindrical_gear_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2831.CylindricalGearSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2831,
        )

        return self.__parent__._cast(
            _2831.CylindricalGearSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2834.CylindricalPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2834,
        )

        return self.__parent__._cast(_2834.CylindricalPlanetGearSystemDeflection)

    @property
    def datum_system_deflection(self: "CastSelf") -> "_2835.DatumSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2835,
        )

        return self.__parent__._cast(_2835.DatumSystemDeflection)

    @property
    def external_cad_model_system_deflection(
        self: "CastSelf",
    ) -> "_2836.ExternalCADModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2836,
        )

        return self.__parent__._cast(_2836.ExternalCADModelSystemDeflection)

    @property
    def face_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2839.FaceGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2839,
        )

        return self.__parent__._cast(_2839.FaceGearSetSystemDeflection)

    @property
    def face_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2840.FaceGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2840,
        )

        return self.__parent__._cast(_2840.FaceGearSystemDeflection)

    @property
    def fe_part_system_deflection(self: "CastSelf") -> "_2841.FEPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2841,
        )

        return self.__parent__._cast(_2841.FEPartSystemDeflection)

    @property
    def flexible_pin_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2842.FlexiblePinAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2842,
        )

        return self.__parent__._cast(_2842.FlexiblePinAssemblySystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "_2844.GearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2844,
        )

        return self.__parent__._cast(_2844.GearSetSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_2845.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2845,
        )

        return self.__parent__._cast(_2845.GearSystemDeflection)

    @property
    def guide_dxf_model_system_deflection(
        self: "CastSelf",
    ) -> "_2846.GuideDxfModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2846,
        )

        return self.__parent__._cast(_2846.GuideDxfModelSystemDeflection)

    @property
    def hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2848.HypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2848,
        )

        return self.__parent__._cast(_2848.HypoidGearSetSystemDeflection)

    @property
    def hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2849.HypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2849,
        )

        return self.__parent__._cast(_2849.HypoidGearSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2853.KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2853,
        )

        return self.__parent__._cast(
            _2853.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2854.KlingelnbergCycloPalloidConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2854,
        )

        return self.__parent__._cast(
            _2854.KlingelnbergCycloPalloidConicalGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2856.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2856,
        )

        return self.__parent__._cast(
            _2856.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2857.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2857,
        )

        return self.__parent__._cast(
            _2857.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2859.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2859,
        )

        return self.__parent__._cast(
            _2859.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2860.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2860,
        )

        return self.__parent__._cast(
            _2860.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        )

    @property
    def mass_disc_system_deflection(
        self: "CastSelf",
    ) -> "_2863.MassDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2863,
        )

        return self.__parent__._cast(_2863.MassDiscSystemDeflection)

    @property
    def measurement_component_system_deflection(
        self: "CastSelf",
    ) -> "_2864.MeasurementComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2864,
        )

        return self.__parent__._cast(_2864.MeasurementComponentSystemDeflection)

    @property
    def microphone_array_system_deflection(
        self: "CastSelf",
    ) -> "_2866.MicrophoneArraySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2866,
        )

        return self.__parent__._cast(_2866.MicrophoneArraySystemDeflection)

    @property
    def microphone_system_deflection(
        self: "CastSelf",
    ) -> "_2867.MicrophoneSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2867,
        )

        return self.__parent__._cast(_2867.MicrophoneSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2868.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2868,
        )

        return self.__parent__._cast(_2868.MountableComponentSystemDeflection)

    @property
    def oil_seal_system_deflection(self: "CastSelf") -> "_2870.OilSealSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2870,
        )

        return self.__parent__._cast(_2870.OilSealSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2871.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2871,
        )

        return self.__parent__._cast(_2871.PartSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2873.PartToPartShearCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2873,
        )

        return self.__parent__._cast(_2873.PartToPartShearCouplingHalfSystemDeflection)

    @property
    def part_to_part_shear_coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2874.PartToPartShearCouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartToPartShearCouplingSystemDeflection)

    @property
    def planet_carrier_system_deflection(
        self: "CastSelf",
    ) -> "_2876.PlanetCarrierSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2876,
        )

        return self.__parent__._cast(_2876.PlanetCarrierSystemDeflection)

    @property
    def point_load_system_deflection(
        self: "CastSelf",
    ) -> "_2877.PointLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2877,
        )

        return self.__parent__._cast(_2877.PointLoadSystemDeflection)

    @property
    def power_load_system_deflection(
        self: "CastSelf",
    ) -> "_2878.PowerLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2878,
        )

        return self.__parent__._cast(_2878.PowerLoadSystemDeflection)

    @property
    def pulley_system_deflection(self: "CastSelf") -> "_2879.PulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2879,
        )

        return self.__parent__._cast(_2879.PulleySystemDeflection)

    @property
    def ring_pins_system_deflection(
        self: "CastSelf",
    ) -> "_2880.RingPinsSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2880,
        )

        return self.__parent__._cast(_2880.RingPinsSystemDeflection)

    @property
    def rolling_ring_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2883.RollingRingAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2883,
        )

        return self.__parent__._cast(_2883.RollingRingAssemblySystemDeflection)

    @property
    def rolling_ring_system_deflection(
        self: "CastSelf",
    ) -> "_2885.RollingRingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2885,
        )

        return self.__parent__._cast(_2885.RollingRingSystemDeflection)

    @property
    def root_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2886.RootAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2886,
        )

        return self.__parent__._cast(_2886.RootAssemblySystemDeflection)

    @property
    def shaft_hub_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2887.ShaftHubConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2887,
        )

        return self.__parent__._cast(_2887.ShaftHubConnectionSystemDeflection)

    @property
    def shaft_system_deflection(self: "CastSelf") -> "_2890.ShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2890,
        )

        return self.__parent__._cast(_2890.ShaftSystemDeflection)

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2892.SpecialisedAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2892,
        )

        return self.__parent__._cast(_2892.SpecialisedAssemblySystemDeflection)

    @property
    def spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2894.SpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2894,
        )

        return self.__parent__._cast(_2894.SpiralBevelGearSetSystemDeflection)

    @property
    def spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2895.SpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2895,
        )

        return self.__parent__._cast(_2895.SpiralBevelGearSystemDeflection)

    @property
    def spring_damper_half_system_deflection(
        self: "CastSelf",
    ) -> "_2897.SpringDamperHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2897,
        )

        return self.__parent__._cast(_2897.SpringDamperHalfSystemDeflection)

    @property
    def spring_damper_system_deflection(
        self: "CastSelf",
    ) -> "_2898.SpringDamperSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2898,
        )

        return self.__parent__._cast(_2898.SpringDamperSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2900.StraightBevelDiffGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2900,
        )

        return self.__parent__._cast(_2900.StraightBevelDiffGearSetSystemDeflection)

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2901.StraightBevelDiffGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2901,
        )

        return self.__parent__._cast(_2901.StraightBevelDiffGearSystemDeflection)

    @property
    def straight_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2903.StraightBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2903,
        )

        return self.__parent__._cast(_2903.StraightBevelGearSetSystemDeflection)

    @property
    def straight_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2904.StraightBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2904,
        )

        return self.__parent__._cast(_2904.StraightBevelGearSystemDeflection)

    @property
    def straight_bevel_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2905.StraightBevelPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2905,
        )

        return self.__parent__._cast(_2905.StraightBevelPlanetGearSystemDeflection)

    @property
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2906.StraightBevelSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2906,
        )

        return self.__parent__._cast(_2906.StraightBevelSunGearSystemDeflection)

    @property
    def synchroniser_half_system_deflection(
        self: "CastSelf",
    ) -> "_2907.SynchroniserHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2907,
        )

        return self.__parent__._cast(_2907.SynchroniserHalfSystemDeflection)

    @property
    def synchroniser_part_system_deflection(
        self: "CastSelf",
    ) -> "_2908.SynchroniserPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2908,
        )

        return self.__parent__._cast(_2908.SynchroniserPartSystemDeflection)

    @property
    def synchroniser_sleeve_system_deflection(
        self: "CastSelf",
    ) -> "_2909.SynchroniserSleeveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2909,
        )

        return self.__parent__._cast(_2909.SynchroniserSleeveSystemDeflection)

    @property
    def synchroniser_system_deflection(
        self: "CastSelf",
    ) -> "_2910.SynchroniserSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2910,
        )

        return self.__parent__._cast(_2910.SynchroniserSystemDeflection)

    @property
    def torque_converter_pump_system_deflection(
        self: "CastSelf",
    ) -> "_2915.TorqueConverterPumpSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2915,
        )

        return self.__parent__._cast(_2915.TorqueConverterPumpSystemDeflection)

    @property
    def torque_converter_system_deflection(
        self: "CastSelf",
    ) -> "_2916.TorqueConverterSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2916,
        )

        return self.__parent__._cast(_2916.TorqueConverterSystemDeflection)

    @property
    def torque_converter_turbine_system_deflection(
        self: "CastSelf",
    ) -> "_2917.TorqueConverterTurbineSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2917,
        )

        return self.__parent__._cast(_2917.TorqueConverterTurbineSystemDeflection)

    @property
    def unbalanced_mass_system_deflection(
        self: "CastSelf",
    ) -> "_2920.UnbalancedMassSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2920,
        )

        return self.__parent__._cast(_2920.UnbalancedMassSystemDeflection)

    @property
    def virtual_component_system_deflection(
        self: "CastSelf",
    ) -> "_2921.VirtualComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2921,
        )

        return self.__parent__._cast(_2921.VirtualComponentSystemDeflection)

    @property
    def worm_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2923.WormGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2923,
        )

        return self.__parent__._cast(_2923.WormGearSetSystemDeflection)

    @property
    def worm_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2924.WormGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2924,
        )

        return self.__parent__._cast(_2924.WormGearSystemDeflection)

    @property
    def zerol_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2926.ZerolBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2926,
        )

        return self.__parent__._cast(_2926.ZerolBevelGearSetSystemDeflection)

    @property
    def zerol_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2927.ZerolBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.ZerolBevelGearSystemDeflection)

    @property
    def abstract_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3071.AbstractAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3071,
        )

        return self.__parent__._cast(
            _3071.AbstractAssemblySteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3072.AbstractShaftOrHousingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3072,
        )

        return self.__parent__._cast(
            _3072.AbstractShaftOrHousingSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3073.AbstractShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3073,
        )

        return self.__parent__._cast(_3073.AbstractShaftSteadyStateSynchronousResponse)

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3076.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3076,
        )

        return self.__parent__._cast(
            _3076.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3077.AGMAGleasonConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3077,
        )

        return self.__parent__._cast(
            _3077.AGMAGleasonConicalGearSteadyStateSynchronousResponse
        )

    @property
    def assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3078.AssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3078,
        )

        return self.__parent__._cast(_3078.AssemblySteadyStateSynchronousResponse)

    @property
    def bearing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3079.BearingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3079,
        )

        return self.__parent__._cast(_3079.BearingSteadyStateSynchronousResponse)

    @property
    def belt_drive_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3081.BeltDriveSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3081,
        )

        return self.__parent__._cast(_3081.BeltDriveSteadyStateSynchronousResponse)

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3083.BevelDifferentialGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3083,
        )

        return self.__parent__._cast(
            _3083.BevelDifferentialGearSetSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3084.BevelDifferentialGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3084,
        )

        return self.__parent__._cast(
            _3084.BevelDifferentialGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3085.BevelDifferentialPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3085,
        )

        return self.__parent__._cast(
            _3085.BevelDifferentialPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3086.BevelDifferentialSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3086,
        )

        return self.__parent__._cast(
            _3086.BevelDifferentialSunGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3088.BevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3088,
        )

        return self.__parent__._cast(_3088.BevelGearSetSteadyStateSynchronousResponse)

    @property
    def bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3089.BevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3089,
        )

        return self.__parent__._cast(_3089.BevelGearSteadyStateSynchronousResponse)

    @property
    def bolted_joint_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3090.BoltedJointSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3090,
        )

        return self.__parent__._cast(_3090.BoltedJointSteadyStateSynchronousResponse)

    @property
    def bolt_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3091.BoltSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3091,
        )

        return self.__parent__._cast(_3091.BoltSteadyStateSynchronousResponse)

    @property
    def clutch_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3093.ClutchHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3093,
        )

        return self.__parent__._cast(_3093.ClutchHalfSteadyStateSynchronousResponse)

    @property
    def clutch_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3094.ClutchSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3094,
        )

        return self.__parent__._cast(_3094.ClutchSteadyStateSynchronousResponse)

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3096.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3096,
        )

        return self.__parent__._cast(_3096.ComponentSteadyStateSynchronousResponse)

    @property
    def concept_coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3098.ConceptCouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3098,
        )

        return self.__parent__._cast(
            _3098.ConceptCouplingHalfSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3099.ConceptCouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3099,
        )

        return self.__parent__._cast(
            _3099.ConceptCouplingSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3101.ConceptGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3101,
        )

        return self.__parent__._cast(_3101.ConceptGearSetSteadyStateSynchronousResponse)

    @property
    def concept_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3102.ConceptGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3102,
        )

        return self.__parent__._cast(_3102.ConceptGearSteadyStateSynchronousResponse)

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3104.ConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3104,
        )

        return self.__parent__._cast(_3104.ConicalGearSetSteadyStateSynchronousResponse)

    @property
    def conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3105.ConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3105,
        )

        return self.__parent__._cast(_3105.ConicalGearSteadyStateSynchronousResponse)

    @property
    def connector_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3107.ConnectorSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3107,
        )

        return self.__parent__._cast(_3107.ConnectorSteadyStateSynchronousResponse)

    @property
    def coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3109.CouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3109,
        )

        return self.__parent__._cast(_3109.CouplingHalfSteadyStateSynchronousResponse)

    @property
    def coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3110.CouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3110,
        )

        return self.__parent__._cast(_3110.CouplingSteadyStateSynchronousResponse)

    @property
    def cvt_pulley_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3112.CVTPulleySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3112,
        )

        return self.__parent__._cast(_3112.CVTPulleySteadyStateSynchronousResponse)

    @property
    def cvt_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3113.CVTSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3113,
        )

        return self.__parent__._cast(_3113.CVTSteadyStateSynchronousResponse)

    @property
    def cycloidal_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3114.CycloidalAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3114,
        )

        return self.__parent__._cast(
            _3114.CycloidalAssemblySteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3117.CycloidalDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3117,
        )

        return self.__parent__._cast(_3117.CycloidalDiscSteadyStateSynchronousResponse)

    @property
    def cylindrical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3119.CylindricalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3119,
        )

        return self.__parent__._cast(
            _3119.CylindricalGearSetSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3120.CylindricalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3120,
        )

        return self.__parent__._cast(
            _3120.CylindricalGearSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3121.CylindricalPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3121,
        )

        return self.__parent__._cast(
            _3121.CylindricalPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def datum_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3122.DatumSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3122,
        )

        return self.__parent__._cast(_3122.DatumSteadyStateSynchronousResponse)

    @property
    def external_cad_model_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3124.ExternalCADModelSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3124,
        )

        return self.__parent__._cast(
            _3124.ExternalCADModelSteadyStateSynchronousResponse
        )

    @property
    def face_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3126.FaceGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3126,
        )

        return self.__parent__._cast(_3126.FaceGearSetSteadyStateSynchronousResponse)

    @property
    def face_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3127.FaceGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3127,
        )

        return self.__parent__._cast(_3127.FaceGearSteadyStateSynchronousResponse)

    @property
    def fe_part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3128.FEPartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3128,
        )

        return self.__parent__._cast(_3128.FEPartSteadyStateSynchronousResponse)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3129.FlexiblePinAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3129,
        )

        return self.__parent__._cast(
            _3129.FlexiblePinAssemblySteadyStateSynchronousResponse
        )

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3131.GearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3131,
        )

        return self.__parent__._cast(_3131.GearSetSteadyStateSynchronousResponse)

    @property
    def gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3132.GearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3132,
        )

        return self.__parent__._cast(_3132.GearSteadyStateSynchronousResponse)

    @property
    def guide_dxf_model_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3133.GuideDxfModelSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3133,
        )

        return self.__parent__._cast(_3133.GuideDxfModelSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3135.HypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3135,
        )

        return self.__parent__._cast(_3135.HypoidGearSetSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3136.HypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3136,
        )

        return self.__parent__._cast(_3136.HypoidGearSteadyStateSynchronousResponse)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3139.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3139,
        )

        return self.__parent__._cast(
            _3139.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3140.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3140,
        )

        return self.__parent__._cast(
            _3140.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3142.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3142,
        )

        return self.__parent__._cast(
            _3142.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3143.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3143,
        )

        return self.__parent__._cast(
            _3143.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3145.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3145,
        )

        return self.__parent__._cast(
            _3145.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3146.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3146,
        )

        return self.__parent__._cast(
            _3146.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse
        )

    @property
    def mass_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3147.MassDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3147,
        )

        return self.__parent__._cast(_3147.MassDiscSteadyStateSynchronousResponse)

    @property
    def measurement_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3148.MeasurementComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3148,
        )

        return self.__parent__._cast(
            _3148.MeasurementComponentSteadyStateSynchronousResponse
        )

    @property
    def microphone_array_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3149.MicrophoneArraySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3149,
        )

        return self.__parent__._cast(
            _3149.MicrophoneArraySteadyStateSynchronousResponse
        )

    @property
    def microphone_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3150.MicrophoneSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3150,
        )

        return self.__parent__._cast(_3150.MicrophoneSteadyStateSynchronousResponse)

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3151.MountableComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3151,
        )

        return self.__parent__._cast(
            _3151.MountableComponentSteadyStateSynchronousResponse
        )

    @property
    def oil_seal_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3152.OilSealSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3152,
        )

        return self.__parent__._cast(_3152.OilSealSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3153.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3153,
        )

        return self.__parent__._cast(_3153.PartSteadyStateSynchronousResponse)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3155.PartToPartShearCouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3155,
        )

        return self.__parent__._cast(
            _3155.PartToPartShearCouplingHalfSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3156.PartToPartShearCouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3156,
        )

        return self.__parent__._cast(
            _3156.PartToPartShearCouplingSteadyStateSynchronousResponse
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3158.PlanetaryGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3158,
        )

        return self.__parent__._cast(
            _3158.PlanetaryGearSetSteadyStateSynchronousResponse
        )

    @property
    def planet_carrier_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3159.PlanetCarrierSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3159,
        )

        return self.__parent__._cast(_3159.PlanetCarrierSteadyStateSynchronousResponse)

    @property
    def point_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3160.PointLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3160,
        )

        return self.__parent__._cast(_3160.PointLoadSteadyStateSynchronousResponse)

    @property
    def power_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3161.PowerLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3161,
        )

        return self.__parent__._cast(_3161.PowerLoadSteadyStateSynchronousResponse)

    @property
    def pulley_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3162.PulleySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3162,
        )

        return self.__parent__._cast(_3162.PulleySteadyStateSynchronousResponse)

    @property
    def ring_pins_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3163.RingPinsSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3163,
        )

        return self.__parent__._cast(_3163.RingPinsSteadyStateSynchronousResponse)

    @property
    def rolling_ring_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3165.RollingRingAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3165,
        )

        return self.__parent__._cast(
            _3165.RollingRingAssemblySteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3167.RollingRingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3167,
        )

        return self.__parent__._cast(_3167.RollingRingSteadyStateSynchronousResponse)

    @property
    def root_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3168.RootAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3168,
        )

        return self.__parent__._cast(_3168.RootAssemblySteadyStateSynchronousResponse)

    @property
    def shaft_hub_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3169.ShaftHubConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3169,
        )

        return self.__parent__._cast(
            _3169.ShaftHubConnectionSteadyStateSynchronousResponse
        )

    @property
    def shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3170.ShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3170,
        )

        return self.__parent__._cast(_3170.ShaftSteadyStateSynchronousResponse)

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3172.SpecialisedAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3172,
        )

        return self.__parent__._cast(
            _3172.SpecialisedAssemblySteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3174.SpiralBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3174,
        )

        return self.__parent__._cast(
            _3174.SpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3175.SpiralBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3175,
        )

        return self.__parent__._cast(
            _3175.SpiralBevelGearSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3177.SpringDamperHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3177,
        )

        return self.__parent__._cast(
            _3177.SpringDamperHalfSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3178.SpringDamperSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3178,
        )

        return self.__parent__._cast(_3178.SpringDamperSteadyStateSynchronousResponse)

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3183.StraightBevelDiffGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3183,
        )

        return self.__parent__._cast(
            _3183.StraightBevelDiffGearSetSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3184.StraightBevelDiffGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3184,
        )

        return self.__parent__._cast(
            _3184.StraightBevelDiffGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3186.StraightBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3186,
        )

        return self.__parent__._cast(
            _3186.StraightBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3187.StraightBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3187,
        )

        return self.__parent__._cast(
            _3187.StraightBevelGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3188.StraightBevelPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3188,
        )

        return self.__parent__._cast(
            _3188.StraightBevelPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3189.StraightBevelSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3189,
        )

        return self.__parent__._cast(
            _3189.StraightBevelSunGearSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3190.SynchroniserHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3190,
        )

        return self.__parent__._cast(
            _3190.SynchroniserHalfSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3191.SynchroniserPartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3191,
        )

        return self.__parent__._cast(
            _3191.SynchroniserPartSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3192.SynchroniserSleeveSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3192,
        )

        return self.__parent__._cast(
            _3192.SynchroniserSleeveSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3193.SynchroniserSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3193,
        )

        return self.__parent__._cast(_3193.SynchroniserSteadyStateSynchronousResponse)

    @property
    def torque_converter_pump_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3195.TorqueConverterPumpSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3195,
        )

        return self.__parent__._cast(
            _3195.TorqueConverterPumpSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3196.TorqueConverterSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3196,
        )

        return self.__parent__._cast(
            _3196.TorqueConverterSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3197.TorqueConverterTurbineSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3197,
        )

        return self.__parent__._cast(
            _3197.TorqueConverterTurbineSteadyStateSynchronousResponse
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3198.UnbalancedMassSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3198,
        )

        return self.__parent__._cast(_3198.UnbalancedMassSteadyStateSynchronousResponse)

    @property
    def virtual_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3199.VirtualComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3199,
        )

        return self.__parent__._cast(
            _3199.VirtualComponentSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3201.WormGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3201,
        )

        return self.__parent__._cast(_3201.WormGearSetSteadyStateSynchronousResponse)

    @property
    def worm_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3202.WormGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3202,
        )

        return self.__parent__._cast(_3202.WormGearSteadyStateSynchronousResponse)

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3204.ZerolBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3204,
        )

        return self.__parent__._cast(
            _3204.ZerolBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3205.ZerolBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3205,
        )

        return self.__parent__._cast(_3205.ZerolBevelGearSteadyStateSynchronousResponse)

    @property
    def abstract_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3337.AbstractAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3337,
        )

        return self.__parent__._cast(
            _3337.AbstractAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3338.AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3338,
        )

        return self.__parent__._cast(
            _3338.AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3339.AbstractShaftSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3339,
        )

        return self.__parent__._cast(
            _3339.AbstractShaftSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3342.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3342,
        )

        return self.__parent__._cast(
            _3342.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3343.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3343,
        )

        return self.__parent__._cast(
            _3343.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3344.AssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3344,
        )

        return self.__parent__._cast(
            _3344.AssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bearing_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3345.BearingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3345,
        )

        return self.__parent__._cast(
            _3345.BearingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_drive_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3347.BeltDriveSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3347,
        )

        return self.__parent__._cast(
            _3347.BeltDriveSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3349.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3349,
        )

        return self.__parent__._cast(
            _3349.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3350.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3350,
        )

        return self.__parent__._cast(
            _3350.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3351.BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3351,
        )

        return self.__parent__._cast(
            _3351.BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3352.BevelDifferentialSunGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3352,
        )

        return self.__parent__._cast(
            _3352.BevelDifferentialSunGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3354.BevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3354,
        )

        return self.__parent__._cast(
            _3354.BevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3355.BevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3355,
        )

        return self.__parent__._cast(
            _3355.BevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bolted_joint_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3356.BoltedJointSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3356,
        )

        return self.__parent__._cast(
            _3356.BoltedJointSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bolt_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3357.BoltSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3357,
        )

        return self.__parent__._cast(_3357.BoltSteadyStateSynchronousResponseOnAShaft)

    @property
    def clutch_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3359.ClutchHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3359,
        )

        return self.__parent__._cast(
            _3359.ClutchHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3360.ClutchSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3360,
        )

        return self.__parent__._cast(_3360.ClutchSteadyStateSynchronousResponseOnAShaft)

    @property
    def component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3362.ComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3362,
        )

        return self.__parent__._cast(
            _3362.ComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3364.ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3364,
        )

        return self.__parent__._cast(
            _3364.ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3365.ConceptCouplingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3365,
        )

        return self.__parent__._cast(
            _3365.ConceptCouplingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3367.ConceptGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3367,
        )

        return self.__parent__._cast(
            _3367.ConceptGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3368.ConceptGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3368,
        )

        return self.__parent__._cast(
            _3368.ConceptGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3370.ConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3370,
        )

        return self.__parent__._cast(
            _3370.ConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3371.ConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3371,
        )

        return self.__parent__._cast(
            _3371.ConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connector_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3373.ConnectorSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3373,
        )

        return self.__parent__._cast(
            _3373.ConnectorSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3375.CouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3375,
        )

        return self.__parent__._cast(
            _3375.CouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3376.CouplingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3376,
        )

        return self.__parent__._cast(
            _3376.CouplingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_pulley_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3378.CVTPulleySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3378,
        )

        return self.__parent__._cast(
            _3378.CVTPulleySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3379.CVTSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3379,
        )

        return self.__parent__._cast(_3379.CVTSteadyStateSynchronousResponseOnAShaft)

    @property
    def cycloidal_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3380.CycloidalAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3380,
        )

        return self.__parent__._cast(
            _3380.CycloidalAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3383.CycloidalDiscSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3383,
        )

        return self.__parent__._cast(
            _3383.CycloidalDiscSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3385.CylindricalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3385,
        )

        return self.__parent__._cast(
            _3385.CylindricalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3386.CylindricalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3386,
        )

        return self.__parent__._cast(
            _3386.CylindricalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3387.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3387,
        )

        return self.__parent__._cast(
            _3387.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def datum_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3388.DatumSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3388,
        )

        return self.__parent__._cast(_3388.DatumSteadyStateSynchronousResponseOnAShaft)

    @property
    def external_cad_model_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3389.ExternalCADModelSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3389,
        )

        return self.__parent__._cast(
            _3389.ExternalCADModelSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3391.FaceGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3391,
        )

        return self.__parent__._cast(
            _3391.FaceGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3392.FaceGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3392,
        )

        return self.__parent__._cast(
            _3392.FaceGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def fe_part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3393.FEPartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3393,
        )

        return self.__parent__._cast(_3393.FEPartSteadyStateSynchronousResponseOnAShaft)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3394.FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3394,
        )

        return self.__parent__._cast(
            _3394.FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3396.GearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3396,
        )

        return self.__parent__._cast(
            _3396.GearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3397.GearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3397,
        )

        return self.__parent__._cast(_3397.GearSteadyStateSynchronousResponseOnAShaft)

    @property
    def guide_dxf_model_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3398.GuideDxfModelSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3398,
        )

        return self.__parent__._cast(
            _3398.GuideDxfModelSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3400.HypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3400,
        )

        return self.__parent__._cast(
            _3400.HypoidGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3401.HypoidGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3401,
        )

        return self.__parent__._cast(
            _3401.HypoidGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3404.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3404,
        )

        return self.__parent__._cast(
            _3404.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3405.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3405,
        )

        return self.__parent__._cast(
            _3405.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3407.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3407,
        )

        return self.__parent__._cast(
            _3407.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3408.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3408,
        )

        return self.__parent__._cast(
            _3408.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3410.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3410,
        )

        return self.__parent__._cast(
            _3410.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3411.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3411,
        )

        return self.__parent__._cast(
            _3411.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def mass_disc_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3412.MassDiscSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3412,
        )

        return self.__parent__._cast(
            _3412.MassDiscSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def measurement_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3413.MeasurementComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3413,
        )

        return self.__parent__._cast(
            _3413.MeasurementComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def microphone_array_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3414.MicrophoneArraySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3414,
        )

        return self.__parent__._cast(
            _3414.MicrophoneArraySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def microphone_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3415.MicrophoneSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3415,
        )

        return self.__parent__._cast(
            _3415.MicrophoneSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def mountable_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3416.MountableComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3416,
        )

        return self.__parent__._cast(
            _3416.MountableComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def oil_seal_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3417.OilSealSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3417,
        )

        return self.__parent__._cast(
            _3417.OilSealSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3418.PartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3418,
        )

        return self.__parent__._cast(_3418.PartSteadyStateSynchronousResponseOnAShaft)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3420.PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3420,
        )

        return self.__parent__._cast(
            _3420.PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3421.PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3421,
        )

        return self.__parent__._cast(
            _3421.PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3423.PlanetaryGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3423,
        )

        return self.__parent__._cast(
            _3423.PlanetaryGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planet_carrier_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3424.PlanetCarrierSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3424,
        )

        return self.__parent__._cast(
            _3424.PlanetCarrierSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def point_load_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3425.PointLoadSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3425,
        )

        return self.__parent__._cast(
            _3425.PointLoadSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def power_load_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3426.PowerLoadSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3426,
        )

        return self.__parent__._cast(
            _3426.PowerLoadSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def pulley_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3427.PulleySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3427,
        )

        return self.__parent__._cast(_3427.PulleySteadyStateSynchronousResponseOnAShaft)

    @property
    def ring_pins_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3428.RingPinsSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3428,
        )

        return self.__parent__._cast(
            _3428.RingPinsSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3430.RollingRingAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3430,
        )

        return self.__parent__._cast(
            _3430.RollingRingAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3432.RollingRingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3432,
        )

        return self.__parent__._cast(
            _3432.RollingRingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def root_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3433.RootAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3433,
        )

        return self.__parent__._cast(
            _3433.RootAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_hub_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3434.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3434,
        )

        return self.__parent__._cast(
            _3434.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3435.ShaftSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3435,
        )

        return self.__parent__._cast(_3435.ShaftSteadyStateSynchronousResponseOnAShaft)

    @property
    def specialised_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3437.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3437,
        )

        return self.__parent__._cast(
            _3437.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3439.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3439,
        )

        return self.__parent__._cast(
            _3439.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3440.SpiralBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3440,
        )

        return self.__parent__._cast(
            _3440.SpiralBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3442.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3442,
        )

        return self.__parent__._cast(
            _3442.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3443.SpringDamperSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3443,
        )

        return self.__parent__._cast(
            _3443.SpringDamperSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3446.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3446,
        )

        return self.__parent__._cast(
            _3446.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3447.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3447,
        )

        return self.__parent__._cast(
            _3447.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3449.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3449,
        )

        return self.__parent__._cast(
            _3449.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3450.StraightBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3450,
        )

        return self.__parent__._cast(
            _3450.StraightBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3451.StraightBevelPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3451,
        )

        return self.__parent__._cast(
            _3451.StraightBevelPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3452.StraightBevelSunGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3452,
        )

        return self.__parent__._cast(
            _3452.StraightBevelSunGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3453.SynchroniserHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3453,
        )

        return self.__parent__._cast(
            _3453.SynchroniserHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3454.SynchroniserPartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3454,
        )

        return self.__parent__._cast(
            _3454.SynchroniserPartSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3455.SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3455,
        )

        return self.__parent__._cast(
            _3455.SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3456.SynchroniserSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3456,
        )

        return self.__parent__._cast(
            _3456.SynchroniserSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_pump_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3458.TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3458,
        )

        return self.__parent__._cast(
            _3458.TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3459.TorqueConverterSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3459,
        )

        return self.__parent__._cast(
            _3459.TorqueConverterSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3460.TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3460,
        )

        return self.__parent__._cast(
            _3460.TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3461.UnbalancedMassSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3461,
        )

        return self.__parent__._cast(
            _3461.UnbalancedMassSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def virtual_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3462.VirtualComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3462,
        )

        return self.__parent__._cast(
            _3462.VirtualComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3464.WormGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3464,
        )

        return self.__parent__._cast(
            _3464.WormGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3465.WormGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3465,
        )

        return self.__parent__._cast(
            _3465.WormGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3467.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3467,
        )

        return self.__parent__._cast(
            _3467.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3468.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3468,
        )

        return self.__parent__._cast(
            _3468.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3600.AbstractAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3600,
        )

        return self.__parent__._cast(
            _3600.AbstractAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3601.AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3601,
        )

        return self.__parent__._cast(
            _3601.AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3602.AbstractShaftSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3602,
        )

        return self.__parent__._cast(
            _3602.AbstractShaftSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3605.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3605,
        )

        return self.__parent__._cast(
            _3605.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3606.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3606,
        )

        return self.__parent__._cast(
            _3606.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3607.AssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3607,
        )

        return self.__parent__._cast(
            _3607.AssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bearing_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3608.BearingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3608,
        )

        return self.__parent__._cast(
            _3608.BearingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_drive_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3610.BeltDriveSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3610,
        )

        return self.__parent__._cast(
            _3610.BeltDriveSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3612.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3612,
        )

        return self.__parent__._cast(
            _3612.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3613.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3613,
        )

        return self.__parent__._cast(
            _3613.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3614.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3614,
        )

        return self.__parent__._cast(
            _3614.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3615.BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3615,
        )

        return self.__parent__._cast(
            _3615.BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3617.BevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3617,
        )

        return self.__parent__._cast(
            _3617.BevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3618.BevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3618,
        )

        return self.__parent__._cast(
            _3618.BevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bolted_joint_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3619.BoltedJointSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3619,
        )

        return self.__parent__._cast(
            _3619.BoltedJointSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bolt_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3620.BoltSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3620,
        )

        return self.__parent__._cast(_3620.BoltSteadyStateSynchronousResponseAtASpeed)

    @property
    def clutch_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3622.ClutchHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3622,
        )

        return self.__parent__._cast(
            _3622.ClutchHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3623.ClutchSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3623,
        )

        return self.__parent__._cast(_3623.ClutchSteadyStateSynchronousResponseAtASpeed)

    @property
    def component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3625.ComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3625,
        )

        return self.__parent__._cast(
            _3625.ComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3627.ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3627,
        )

        return self.__parent__._cast(
            _3627.ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3628.ConceptCouplingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3628,
        )

        return self.__parent__._cast(
            _3628.ConceptCouplingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3630.ConceptGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3630,
        )

        return self.__parent__._cast(
            _3630.ConceptGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3631.ConceptGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3631,
        )

        return self.__parent__._cast(
            _3631.ConceptGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3633.ConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3633,
        )

        return self.__parent__._cast(
            _3633.ConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3634.ConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3634,
        )

        return self.__parent__._cast(
            _3634.ConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connector_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3636.ConnectorSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3636,
        )

        return self.__parent__._cast(
            _3636.ConnectorSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3638.CouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3638,
        )

        return self.__parent__._cast(
            _3638.CouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3639.CouplingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3639,
        )

        return self.__parent__._cast(
            _3639.CouplingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_pulley_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3641.CVTPulleySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3641,
        )

        return self.__parent__._cast(
            _3641.CVTPulleySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3642.CVTSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3642,
        )

        return self.__parent__._cast(_3642.CVTSteadyStateSynchronousResponseAtASpeed)

    @property
    def cycloidal_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3643.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3643,
        )

        return self.__parent__._cast(
            _3643.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3646.CycloidalDiscSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3646,
        )

        return self.__parent__._cast(
            _3646.CycloidalDiscSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3648.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3648,
        )

        return self.__parent__._cast(
            _3648.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3649.CylindricalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3649,
        )

        return self.__parent__._cast(
            _3649.CylindricalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3650.CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3650,
        )

        return self.__parent__._cast(
            _3650.CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def datum_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3651.DatumSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3651,
        )

        return self.__parent__._cast(_3651.DatumSteadyStateSynchronousResponseAtASpeed)

    @property
    def external_cad_model_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3652.ExternalCADModelSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3652,
        )

        return self.__parent__._cast(
            _3652.ExternalCADModelSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3654.FaceGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3654,
        )

        return self.__parent__._cast(
            _3654.FaceGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3655.FaceGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3655,
        )

        return self.__parent__._cast(
            _3655.FaceGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def fe_part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3656.FEPartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3656,
        )

        return self.__parent__._cast(_3656.FEPartSteadyStateSynchronousResponseAtASpeed)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3657.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3657,
        )

        return self.__parent__._cast(
            _3657.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3659.GearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3659,
        )

        return self.__parent__._cast(
            _3659.GearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3660.GearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3660,
        )

        return self.__parent__._cast(_3660.GearSteadyStateSynchronousResponseAtASpeed)

    @property
    def guide_dxf_model_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3661.GuideDxfModelSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3661,
        )

        return self.__parent__._cast(
            _3661.GuideDxfModelSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3663.HypoidGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3663,
        )

        return self.__parent__._cast(
            _3663.HypoidGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3664.HypoidGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3664,
        )

        return self.__parent__._cast(
            _3664.HypoidGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3667.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3667,
        )

        return self.__parent__._cast(
            _3667.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3668.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3668,
        )

        return self.__parent__._cast(
            _3668.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3670.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3670,
        )

        return self.__parent__._cast(
            _3670.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3671.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3671,
        )

        return self.__parent__._cast(
            _3671.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3673.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3673,
        )

        return self.__parent__._cast(
            _3673.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3674.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3674,
        )

        return self.__parent__._cast(
            _3674.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def mass_disc_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3675.MassDiscSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3675,
        )

        return self.__parent__._cast(
            _3675.MassDiscSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def measurement_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3676.MeasurementComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3676,
        )

        return self.__parent__._cast(
            _3676.MeasurementComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def microphone_array_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3677.MicrophoneArraySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3677,
        )

        return self.__parent__._cast(
            _3677.MicrophoneArraySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def microphone_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3678.MicrophoneSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3678,
        )

        return self.__parent__._cast(
            _3678.MicrophoneSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def mountable_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3679.MountableComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3679,
        )

        return self.__parent__._cast(
            _3679.MountableComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def oil_seal_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3680.OilSealSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3680,
        )

        return self.__parent__._cast(
            _3680.OilSealSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3681.PartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3681,
        )

        return self.__parent__._cast(_3681.PartSteadyStateSynchronousResponseAtASpeed)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3683.PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3683,
        )

        return self.__parent__._cast(
            _3683.PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3684.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3684,
        )

        return self.__parent__._cast(
            _3684.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3686.PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3686,
        )

        return self.__parent__._cast(
            _3686.PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planet_carrier_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3687.PlanetCarrierSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3687,
        )

        return self.__parent__._cast(
            _3687.PlanetCarrierSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def point_load_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3688.PointLoadSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3688,
        )

        return self.__parent__._cast(
            _3688.PointLoadSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def power_load_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3689.PowerLoadSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3689,
        )

        return self.__parent__._cast(
            _3689.PowerLoadSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def pulley_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3690.PulleySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3690,
        )

        return self.__parent__._cast(_3690.PulleySteadyStateSynchronousResponseAtASpeed)

    @property
    def ring_pins_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3691.RingPinsSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3691,
        )

        return self.__parent__._cast(
            _3691.RingPinsSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3693.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3693,
        )

        return self.__parent__._cast(
            _3693.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3695.RollingRingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3695,
        )

        return self.__parent__._cast(
            _3695.RollingRingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def root_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3696.RootAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3696,
        )

        return self.__parent__._cast(
            _3696.RootAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_hub_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3697.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3697,
        )

        return self.__parent__._cast(
            _3697.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3698.ShaftSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3698,
        )

        return self.__parent__._cast(_3698.ShaftSteadyStateSynchronousResponseAtASpeed)

    @property
    def specialised_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3700.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3700,
        )

        return self.__parent__._cast(
            _3700.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3702.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3702,
        )

        return self.__parent__._cast(
            _3702.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3703.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3703,
        )

        return self.__parent__._cast(
            _3703.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3705.SpringDamperHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3705,
        )

        return self.__parent__._cast(
            _3705.SpringDamperHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3706.SpringDamperSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3706,
        )

        return self.__parent__._cast(
            _3706.SpringDamperSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3709.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3709,
        )

        return self.__parent__._cast(
            _3709.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3710.StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3710,
        )

        return self.__parent__._cast(
            _3710.StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3712.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3712,
        )

        return self.__parent__._cast(
            _3712.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3713.StraightBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3713,
        )

        return self.__parent__._cast(
            _3713.StraightBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3714.StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3714,
        )

        return self.__parent__._cast(
            _3714.StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3715.StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3715,
        )

        return self.__parent__._cast(
            _3715.StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3716.SynchroniserHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3716,
        )

        return self.__parent__._cast(
            _3716.SynchroniserHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3717.SynchroniserPartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3717,
        )

        return self.__parent__._cast(
            _3717.SynchroniserPartSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3718.SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3718,
        )

        return self.__parent__._cast(
            _3718.SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3719.SynchroniserSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3719,
        )

        return self.__parent__._cast(
            _3719.SynchroniserSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_pump_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3721.TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3721,
        )

        return self.__parent__._cast(
            _3721.TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3722.TorqueConverterSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3722,
        )

        return self.__parent__._cast(
            _3722.TorqueConverterSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3723.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3723,
        )

        return self.__parent__._cast(
            _3723.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3724.UnbalancedMassSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3724,
        )

        return self.__parent__._cast(
            _3724.UnbalancedMassSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def virtual_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3725.VirtualComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3725,
        )

        return self.__parent__._cast(
            _3725.VirtualComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3727.WormGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3727,
        )

        return self.__parent__._cast(
            _3727.WormGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3728.WormGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3728,
        )

        return self.__parent__._cast(
            _3728.WormGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3730.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3730,
        )

        return self.__parent__._cast(
            _3730.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3731.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3731,
        )

        return self.__parent__._cast(
            _3731.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3863.AbstractAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3863,
        )

        return self.__parent__._cast(_3863.AbstractAssemblyStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_stability_analysis(
        self: "CastSelf",
    ) -> "_3864.AbstractShaftOrHousingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3864,
        )

        return self.__parent__._cast(_3864.AbstractShaftOrHousingStabilityAnalysis)

    @property
    def abstract_shaft_stability_analysis(
        self: "CastSelf",
    ) -> "_3865.AbstractShaftStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3865,
        )

        return self.__parent__._cast(_3865.AbstractShaftStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3868.AGMAGleasonConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3868,
        )

        return self.__parent__._cast(_3868.AGMAGleasonConicalGearSetStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3869.AGMAGleasonConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3869,
        )

        return self.__parent__._cast(_3869.AGMAGleasonConicalGearStabilityAnalysis)

    @property
    def assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3870.AssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3870,
        )

        return self.__parent__._cast(_3870.AssemblyStabilityAnalysis)

    @property
    def bearing_stability_analysis(
        self: "CastSelf",
    ) -> "_3871.BearingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3871,
        )

        return self.__parent__._cast(_3871.BearingStabilityAnalysis)

    @property
    def belt_drive_stability_analysis(
        self: "CastSelf",
    ) -> "_3873.BeltDriveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3873,
        )

        return self.__parent__._cast(_3873.BeltDriveStabilityAnalysis)

    @property
    def bevel_differential_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3875.BevelDifferentialGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3875,
        )

        return self.__parent__._cast(_3875.BevelDifferentialGearSetStabilityAnalysis)

    @property
    def bevel_differential_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3876.BevelDifferentialGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3876,
        )

        return self.__parent__._cast(_3876.BevelDifferentialGearStabilityAnalysis)

    @property
    def bevel_differential_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3877.BevelDifferentialPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3877,
        )

        return self.__parent__._cast(_3877.BevelDifferentialPlanetGearStabilityAnalysis)

    @property
    def bevel_differential_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3878.BevelDifferentialSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3878,
        )

        return self.__parent__._cast(_3878.BevelDifferentialSunGearStabilityAnalysis)

    @property
    def bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3880.BevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3880,
        )

        return self.__parent__._cast(_3880.BevelGearSetStabilityAnalysis)

    @property
    def bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3881.BevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3881,
        )

        return self.__parent__._cast(_3881.BevelGearStabilityAnalysis)

    @property
    def bolted_joint_stability_analysis(
        self: "CastSelf",
    ) -> "_3882.BoltedJointStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3882,
        )

        return self.__parent__._cast(_3882.BoltedJointStabilityAnalysis)

    @property
    def bolt_stability_analysis(self: "CastSelf") -> "_3883.BoltStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3883,
        )

        return self.__parent__._cast(_3883.BoltStabilityAnalysis)

    @property
    def clutch_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3885.ClutchHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3885,
        )

        return self.__parent__._cast(_3885.ClutchHalfStabilityAnalysis)

    @property
    def clutch_stability_analysis(self: "CastSelf") -> "_3886.ClutchStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3886,
        )

        return self.__parent__._cast(_3886.ClutchStabilityAnalysis)

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_3888.ComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3888,
        )

        return self.__parent__._cast(_3888.ComponentStabilityAnalysis)

    @property
    def concept_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3890.ConceptCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3890,
        )

        return self.__parent__._cast(_3890.ConceptCouplingHalfStabilityAnalysis)

    @property
    def concept_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3891.ConceptCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3891,
        )

        return self.__parent__._cast(_3891.ConceptCouplingStabilityAnalysis)

    @property
    def concept_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3893.ConceptGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3893,
        )

        return self.__parent__._cast(_3893.ConceptGearSetStabilityAnalysis)

    @property
    def concept_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3894.ConceptGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3894,
        )

        return self.__parent__._cast(_3894.ConceptGearStabilityAnalysis)

    @property
    def conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3896.ConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3896,
        )

        return self.__parent__._cast(_3896.ConicalGearSetStabilityAnalysis)

    @property
    def conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3897.ConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3897,
        )

        return self.__parent__._cast(_3897.ConicalGearStabilityAnalysis)

    @property
    def connector_stability_analysis(
        self: "CastSelf",
    ) -> "_3899.ConnectorStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3899,
        )

        return self.__parent__._cast(_3899.ConnectorStabilityAnalysis)

    @property
    def coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3901.CouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3901,
        )

        return self.__parent__._cast(_3901.CouplingHalfStabilityAnalysis)

    @property
    def coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3902.CouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3902,
        )

        return self.__parent__._cast(_3902.CouplingStabilityAnalysis)

    @property
    def cvt_pulley_stability_analysis(
        self: "CastSelf",
    ) -> "_3905.CVTPulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3905,
        )

        return self.__parent__._cast(_3905.CVTPulleyStabilityAnalysis)

    @property
    def cvt_stability_analysis(self: "CastSelf") -> "_3906.CVTStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3906,
        )

        return self.__parent__._cast(_3906.CVTStabilityAnalysis)

    @property
    def cycloidal_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3907.CycloidalAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3907,
        )

        return self.__parent__._cast(_3907.CycloidalAssemblyStabilityAnalysis)

    @property
    def cycloidal_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_3910.CycloidalDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3910,
        )

        return self.__parent__._cast(_3910.CycloidalDiscStabilityAnalysis)

    @property
    def cylindrical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3912.CylindricalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3912,
        )

        return self.__parent__._cast(_3912.CylindricalGearSetStabilityAnalysis)

    @property
    def cylindrical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3913.CylindricalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3913,
        )

        return self.__parent__._cast(_3913.CylindricalGearStabilityAnalysis)

    @property
    def cylindrical_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3914.CylindricalPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3914,
        )

        return self.__parent__._cast(_3914.CylindricalPlanetGearStabilityAnalysis)

    @property
    def datum_stability_analysis(self: "CastSelf") -> "_3915.DatumStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3915,
        )

        return self.__parent__._cast(_3915.DatumStabilityAnalysis)

    @property
    def external_cad_model_stability_analysis(
        self: "CastSelf",
    ) -> "_3917.ExternalCADModelStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3917,
        )

        return self.__parent__._cast(_3917.ExternalCADModelStabilityAnalysis)

    @property
    def face_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3919.FaceGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3919,
        )

        return self.__parent__._cast(_3919.FaceGearSetStabilityAnalysis)

    @property
    def face_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3920.FaceGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3920,
        )

        return self.__parent__._cast(_3920.FaceGearStabilityAnalysis)

    @property
    def fe_part_stability_analysis(self: "CastSelf") -> "_3921.FEPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3921,
        )

        return self.__parent__._cast(_3921.FEPartStabilityAnalysis)

    @property
    def flexible_pin_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3922.FlexiblePinAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3922,
        )

        return self.__parent__._cast(_3922.FlexiblePinAssemblyStabilityAnalysis)

    @property
    def gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3924.GearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3924,
        )

        return self.__parent__._cast(_3924.GearSetStabilityAnalysis)

    @property
    def gear_stability_analysis(self: "CastSelf") -> "_3925.GearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3925,
        )

        return self.__parent__._cast(_3925.GearStabilityAnalysis)

    @property
    def guide_dxf_model_stability_analysis(
        self: "CastSelf",
    ) -> "_3926.GuideDxfModelStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3926,
        )

        return self.__parent__._cast(_3926.GuideDxfModelStabilityAnalysis)

    @property
    def hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3928.HypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3928,
        )

        return self.__parent__._cast(_3928.HypoidGearSetStabilityAnalysis)

    @property
    def hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3929.HypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3929,
        )

        return self.__parent__._cast(_3929.HypoidGearStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3932.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3932,
        )

        return self.__parent__._cast(
            _3932.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3933.KlingelnbergCycloPalloidConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3933,
        )

        return self.__parent__._cast(
            _3933.KlingelnbergCycloPalloidConicalGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3935.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3935,
        )

        return self.__parent__._cast(
            _3935.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3936.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3936,
        )

        return self.__parent__._cast(
            _3936.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3938.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3938,
        )

        return self.__parent__._cast(
            _3938.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3939.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3939,
        )

        return self.__parent__._cast(
            _3939.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis
        )

    @property
    def mass_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_3940.MassDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3940,
        )

        return self.__parent__._cast(_3940.MassDiscStabilityAnalysis)

    @property
    def measurement_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3941.MeasurementComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3941,
        )

        return self.__parent__._cast(_3941.MeasurementComponentStabilityAnalysis)

    @property
    def microphone_array_stability_analysis(
        self: "CastSelf",
    ) -> "_3942.MicrophoneArrayStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3942,
        )

        return self.__parent__._cast(_3942.MicrophoneArrayStabilityAnalysis)

    @property
    def microphone_stability_analysis(
        self: "CastSelf",
    ) -> "_3943.MicrophoneStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3943,
        )

        return self.__parent__._cast(_3943.MicrophoneStabilityAnalysis)

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3944.MountableComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3944,
        )

        return self.__parent__._cast(_3944.MountableComponentStabilityAnalysis)

    @property
    def oil_seal_stability_analysis(
        self: "CastSelf",
    ) -> "_3945.OilSealStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3945,
        )

        return self.__parent__._cast(_3945.OilSealStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_3946.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3946,
        )

        return self.__parent__._cast(_3946.PartStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3948.PartToPartShearCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3948,
        )

        return self.__parent__._cast(_3948.PartToPartShearCouplingHalfStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3949.PartToPartShearCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3949,
        )

        return self.__parent__._cast(_3949.PartToPartShearCouplingStabilityAnalysis)

    @property
    def planetary_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3951.PlanetaryGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3951,
        )

        return self.__parent__._cast(_3951.PlanetaryGearSetStabilityAnalysis)

    @property
    def planet_carrier_stability_analysis(
        self: "CastSelf",
    ) -> "_3952.PlanetCarrierStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3952,
        )

        return self.__parent__._cast(_3952.PlanetCarrierStabilityAnalysis)

    @property
    def point_load_stability_analysis(
        self: "CastSelf",
    ) -> "_3953.PointLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3953,
        )

        return self.__parent__._cast(_3953.PointLoadStabilityAnalysis)

    @property
    def power_load_stability_analysis(
        self: "CastSelf",
    ) -> "_3954.PowerLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3954,
        )

        return self.__parent__._cast(_3954.PowerLoadStabilityAnalysis)

    @property
    def pulley_stability_analysis(self: "CastSelf") -> "_3955.PulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3955,
        )

        return self.__parent__._cast(_3955.PulleyStabilityAnalysis)

    @property
    def ring_pins_stability_analysis(
        self: "CastSelf",
    ) -> "_3956.RingPinsStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3956,
        )

        return self.__parent__._cast(_3956.RingPinsStabilityAnalysis)

    @property
    def rolling_ring_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3958.RollingRingAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3958,
        )

        return self.__parent__._cast(_3958.RollingRingAssemblyStabilityAnalysis)

    @property
    def rolling_ring_stability_analysis(
        self: "CastSelf",
    ) -> "_3960.RollingRingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3960,
        )

        return self.__parent__._cast(_3960.RollingRingStabilityAnalysis)

    @property
    def root_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3961.RootAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3961,
        )

        return self.__parent__._cast(_3961.RootAssemblyStabilityAnalysis)

    @property
    def shaft_hub_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3962.ShaftHubConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3962,
        )

        return self.__parent__._cast(_3962.ShaftHubConnectionStabilityAnalysis)

    @property
    def shaft_stability_analysis(self: "CastSelf") -> "_3963.ShaftStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3963,
        )

        return self.__parent__._cast(_3963.ShaftStabilityAnalysis)

    @property
    def specialised_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3965.SpecialisedAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3965,
        )

        return self.__parent__._cast(_3965.SpecialisedAssemblyStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3967.SpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3967,
        )

        return self.__parent__._cast(_3967.SpiralBevelGearSetStabilityAnalysis)

    @property
    def spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3968.SpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3968,
        )

        return self.__parent__._cast(_3968.SpiralBevelGearStabilityAnalysis)

    @property
    def spring_damper_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3970.SpringDamperHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3970,
        )

        return self.__parent__._cast(_3970.SpringDamperHalfStabilityAnalysis)

    @property
    def spring_damper_stability_analysis(
        self: "CastSelf",
    ) -> "_3971.SpringDamperStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3971,
        )

        return self.__parent__._cast(_3971.SpringDamperStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3976.StraightBevelDiffGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3976,
        )

        return self.__parent__._cast(_3976.StraightBevelDiffGearSetStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3977.StraightBevelDiffGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3977,
        )

        return self.__parent__._cast(_3977.StraightBevelDiffGearStabilityAnalysis)

    @property
    def straight_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3979.StraightBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3979,
        )

        return self.__parent__._cast(_3979.StraightBevelGearSetStabilityAnalysis)

    @property
    def straight_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3980.StraightBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3980,
        )

        return self.__parent__._cast(_3980.StraightBevelGearStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3981.StraightBevelPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3981,
        )

        return self.__parent__._cast(_3981.StraightBevelPlanetGearStabilityAnalysis)

    @property
    def straight_bevel_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3982.StraightBevelSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3982,
        )

        return self.__parent__._cast(_3982.StraightBevelSunGearStabilityAnalysis)

    @property
    def synchroniser_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3983.SynchroniserHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3983,
        )

        return self.__parent__._cast(_3983.SynchroniserHalfStabilityAnalysis)

    @property
    def synchroniser_part_stability_analysis(
        self: "CastSelf",
    ) -> "_3984.SynchroniserPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3984,
        )

        return self.__parent__._cast(_3984.SynchroniserPartStabilityAnalysis)

    @property
    def synchroniser_sleeve_stability_analysis(
        self: "CastSelf",
    ) -> "_3985.SynchroniserSleeveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3985,
        )

        return self.__parent__._cast(_3985.SynchroniserSleeveStabilityAnalysis)

    @property
    def synchroniser_stability_analysis(
        self: "CastSelf",
    ) -> "_3986.SynchroniserStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3986,
        )

        return self.__parent__._cast(_3986.SynchroniserStabilityAnalysis)

    @property
    def torque_converter_pump_stability_analysis(
        self: "CastSelf",
    ) -> "_3988.TorqueConverterPumpStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3988,
        )

        return self.__parent__._cast(_3988.TorqueConverterPumpStabilityAnalysis)

    @property
    def torque_converter_stability_analysis(
        self: "CastSelf",
    ) -> "_3989.TorqueConverterStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3989,
        )

        return self.__parent__._cast(_3989.TorqueConverterStabilityAnalysis)

    @property
    def torque_converter_turbine_stability_analysis(
        self: "CastSelf",
    ) -> "_3990.TorqueConverterTurbineStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3990,
        )

        return self.__parent__._cast(_3990.TorqueConverterTurbineStabilityAnalysis)

    @property
    def unbalanced_mass_stability_analysis(
        self: "CastSelf",
    ) -> "_3991.UnbalancedMassStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3991,
        )

        return self.__parent__._cast(_3991.UnbalancedMassStabilityAnalysis)

    @property
    def virtual_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3992.VirtualComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3992,
        )

        return self.__parent__._cast(_3992.VirtualComponentStabilityAnalysis)

    @property
    def worm_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3994.WormGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3994,
        )

        return self.__parent__._cast(_3994.WormGearSetStabilityAnalysis)

    @property
    def worm_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3995.WormGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3995,
        )

        return self.__parent__._cast(_3995.WormGearStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3997.ZerolBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3997,
        )

        return self.__parent__._cast(_3997.ZerolBevelGearSetStabilityAnalysis)

    @property
    def zerol_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3998.ZerolBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3998,
        )

        return self.__parent__._cast(_3998.ZerolBevelGearStabilityAnalysis)

    @property
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4136.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4136

        return self.__parent__._cast(_4136.AbstractAssemblyPowerFlow)

    @property
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4137.AbstractShaftOrHousingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4137

        return self.__parent__._cast(_4137.AbstractShaftOrHousingPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4138.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4138

        return self.__parent__._cast(_4138.AbstractShaftPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4141.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4141

        return self.__parent__._cast(_4141.AGMAGleasonConicalGearPowerFlow)

    @property
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4142.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4142

        return self.__parent__._cast(_4142.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4143.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4143

        return self.__parent__._cast(_4143.AssemblyPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4144.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4144

        return self.__parent__._cast(_4144.BearingPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4146.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4146

        return self.__parent__._cast(_4146.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4148.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4148

        return self.__parent__._cast(_4148.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4149.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4149

        return self.__parent__._cast(_4149.BevelDifferentialGearSetPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4150.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4150

        return self.__parent__._cast(_4150.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4151.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4153.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelGearPowerFlow)

    @property
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4154.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4155.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4155

        return self.__parent__._cast(_4155.BoltedJointPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4156.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4156

        return self.__parent__._cast(_4156.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4158.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4158

        return self.__parent__._cast(_4158.ClutchHalfPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4159.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4159

        return self.__parent__._cast(_4159.ClutchPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4161.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ComponentPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4163.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4163

        return self.__parent__._cast(_4163.ConceptCouplingHalfPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4164.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ConceptCouplingPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4166.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ConceptGearPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4167.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4167

        return self.__parent__._cast(_4167.ConceptGearSetPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4169.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConicalGearPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4170.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4170

        return self.__parent__._cast(_4170.ConicalGearSetPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4172.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4174.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4174

        return self.__parent__._cast(_4174.CouplingHalfPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4175.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4177.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.CVTPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4178.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4178

        return self.__parent__._cast(_4178.CVTPulleyPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4179.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4179

        return self.__parent__._cast(_4179.CycloidalAssemblyPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4182.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4182

        return self.__parent__._cast(_4182.CycloidalDiscPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4185.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4185

        return self.__parent__._cast(_4185.CylindricalGearPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4186.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4186

        return self.__parent__._cast(_4186.CylindricalGearSetPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4187.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4187

        return self.__parent__._cast(_4187.CylindricalPlanetGearPowerFlow)

    @property
    def datum_power_flow(self: "CastSelf") -> "_4188.DatumPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4188

        return self.__parent__._cast(_4188.DatumPowerFlow)

    @property
    def external_cad_model_power_flow(
        self: "CastSelf",
    ) -> "_4189.ExternalCADModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4189

        return self.__parent__._cast(_4189.ExternalCADModelPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4191.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4191

        return self.__parent__._cast(_4191.FaceGearPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4192.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4192

        return self.__parent__._cast(_4192.FaceGearSetPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4195.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4195

        return self.__parent__._cast(_4195.FEPartPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4196.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4196

        return self.__parent__._cast(_4196.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4198.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4198

        return self.__parent__._cast(_4198.GearPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4199.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4199

        return self.__parent__._cast(_4199.GearSetPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4200.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4200

        return self.__parent__._cast(_4200.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4202.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4202

        return self.__parent__._cast(_4202.HypoidGearPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4203.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4203

        return self.__parent__._cast(_4203.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4206.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4207.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4207

        return self.__parent__._cast(
            _4207.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4210

        return self.__parent__._cast(
            _4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(
            _4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4213.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4213

        return self.__parent__._cast(
            _4213.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4214.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4214

        return self.__parent__._cast(_4214.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4215.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4215

        return self.__parent__._cast(_4215.MeasurementComponentPowerFlow)

    @property
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4216.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4216

        return self.__parent__._cast(_4216.MicrophoneArrayPowerFlow)

    @property
    def microphone_power_flow(self: "CastSelf") -> "_4217.MicrophonePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4217

        return self.__parent__._cast(_4217.MicrophonePowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4218.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(_4218.MountableComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4219.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4219

        return self.__parent__._cast(_4219.OilSealPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4220.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4220

        return self.__parent__._cast(_4220.PartPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4222.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4222

        return self.__parent__._cast(_4222.PartToPartShearCouplingHalfPowerFlow)

    @property
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4223.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4225.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PlanetaryGearSetPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4226.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4226

        return self.__parent__._cast(_4226.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4227.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4227

        return self.__parent__._cast(_4227.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4230.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4230

        return self.__parent__._cast(_4230.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4231.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4231

        return self.__parent__._cast(_4231.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4232.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4232

        return self.__parent__._cast(_4232.RingPinsPowerFlow)

    @property
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4234.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4234

        return self.__parent__._cast(_4234.RollingRingAssemblyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4236.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4236

        return self.__parent__._cast(_4236.RollingRingPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4237.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4237

        return self.__parent__._cast(_4237.RootAssemblyPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4238.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4238

        return self.__parent__._cast(_4238.ShaftHubConnectionPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4239.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.ShaftPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4241.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4243.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4243

        return self.__parent__._cast(_4243.SpiralBevelGearPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4244.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpringDamperHalfPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4247.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4247

        return self.__parent__._cast(_4247.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4249.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4250.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4250

        return self.__parent__._cast(_4250.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4252.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4253.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4253

        return self.__parent__._cast(_4253.StraightBevelGearSetPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4254.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4254

        return self.__parent__._cast(_4254.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4256.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4256

        return self.__parent__._cast(_4256.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4257.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4257

        return self.__parent__._cast(_4257.SynchroniserPartPowerFlow)

    @property
    def synchroniser_power_flow(self: "CastSelf") -> "_4258.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.SynchroniserPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4259.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4262.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.TorqueConverterPowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4263.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4263

        return self.__parent__._cast(_4263.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4264.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4264

        return self.__parent__._cast(_4264.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4265.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4265

        return self.__parent__._cast(_4265.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4266.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4266

        return self.__parent__._cast(_4266.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4268.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4268

        return self.__parent__._cast(_4268.WormGearPowerFlow)

    @property
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4269.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4269

        return self.__parent__._cast(_4269.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4271.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.ZerolBevelGearPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4272.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4272

        return self.__parent__._cast(_4272.ZerolBevelGearSetPowerFlow)

    @property
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4404.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4404,
        )

        return self.__parent__._cast(_4404.AbstractAssemblyParametricStudyTool)

    @property
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4405.AbstractShaftOrHousingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4405,
        )

        return self.__parent__._cast(_4405.AbstractShaftOrHousingParametricStudyTool)

    @property
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4406.AbstractShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4406,
        )

        return self.__parent__._cast(_4406.AbstractShaftParametricStudyTool)

    @property
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4409.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4409,
        )

        return self.__parent__._cast(_4409.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4410.AGMAGleasonConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4410,
        )

        return self.__parent__._cast(_4410.AGMAGleasonConicalGearSetParametricStudyTool)

    @property
    def assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4411.AssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4411,
        )

        return self.__parent__._cast(_4411.AssemblyParametricStudyTool)

    @property
    def bearing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4412.BearingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4412,
        )

        return self.__parent__._cast(_4412.BearingParametricStudyTool)

    @property
    def belt_drive_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4414.BeltDriveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4414,
        )

        return self.__parent__._cast(_4414.BeltDriveParametricStudyTool)

    @property
    def bevel_differential_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4416.BevelDifferentialGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4416,
        )

        return self.__parent__._cast(_4416.BevelDifferentialGearParametricStudyTool)

    @property
    def bevel_differential_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4417.BevelDifferentialGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4417,
        )

        return self.__parent__._cast(_4417.BevelDifferentialGearSetParametricStudyTool)

    @property
    def bevel_differential_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4418.BevelDifferentialPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4418,
        )

        return self.__parent__._cast(
            _4418.BevelDifferentialPlanetGearParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4419.BevelDifferentialSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4419,
        )

        return self.__parent__._cast(_4419.BevelDifferentialSunGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4421.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4421,
        )

        return self.__parent__._cast(_4421.BevelGearParametricStudyTool)

    @property
    def bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4422.BevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4422,
        )

        return self.__parent__._cast(_4422.BevelGearSetParametricStudyTool)

    @property
    def bolted_joint_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4423.BoltedJointParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4423,
        )

        return self.__parent__._cast(_4423.BoltedJointParametricStudyTool)

    @property
    def bolt_parametric_study_tool(self: "CastSelf") -> "_4424.BoltParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4424,
        )

        return self.__parent__._cast(_4424.BoltParametricStudyTool)

    @property
    def clutch_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4426.ClutchHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4426,
        )

        return self.__parent__._cast(_4426.ClutchHalfParametricStudyTool)

    @property
    def clutch_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4427.ClutchParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4427,
        )

        return self.__parent__._cast(_4427.ClutchParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4429.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4429,
        )

        return self.__parent__._cast(_4429.ComponentParametricStudyTool)

    @property
    def concept_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4431.ConceptCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4431,
        )

        return self.__parent__._cast(_4431.ConceptCouplingHalfParametricStudyTool)

    @property
    def concept_coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4432.ConceptCouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4432,
        )

        return self.__parent__._cast(_4432.ConceptCouplingParametricStudyTool)

    @property
    def concept_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4434.ConceptGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4434,
        )

        return self.__parent__._cast(_4434.ConceptGearParametricStudyTool)

    @property
    def concept_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4435.ConceptGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4435,
        )

        return self.__parent__._cast(_4435.ConceptGearSetParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4437.ConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4437,
        )

        return self.__parent__._cast(_4437.ConicalGearParametricStudyTool)

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4438.ConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4438,
        )

        return self.__parent__._cast(_4438.ConicalGearSetParametricStudyTool)

    @property
    def connector_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4440.ConnectorParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4440,
        )

        return self.__parent__._cast(_4440.ConnectorParametricStudyTool)

    @property
    def coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4442.CouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4442,
        )

        return self.__parent__._cast(_4442.CouplingHalfParametricStudyTool)

    @property
    def coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4443.CouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4443,
        )

        return self.__parent__._cast(_4443.CouplingParametricStudyTool)

    @property
    def cvt_parametric_study_tool(self: "CastSelf") -> "_4445.CVTParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4445,
        )

        return self.__parent__._cast(_4445.CVTParametricStudyTool)

    @property
    def cvt_pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4446.CVTPulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4446,
        )

        return self.__parent__._cast(_4446.CVTPulleyParametricStudyTool)

    @property
    def cycloidal_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4447.CycloidalAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4447,
        )

        return self.__parent__._cast(_4447.CycloidalAssemblyParametricStudyTool)

    @property
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4449.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4449,
        )

        return self.__parent__._cast(_4449.CycloidalDiscParametricStudyTool)

    @property
    def cylindrical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4452.CylindricalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4452,
        )

        return self.__parent__._cast(_4452.CylindricalGearParametricStudyTool)

    @property
    def cylindrical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4453.CylindricalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4453,
        )

        return self.__parent__._cast(_4453.CylindricalGearSetParametricStudyTool)

    @property
    def cylindrical_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4454.CylindricalPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4454,
        )

        return self.__parent__._cast(_4454.CylindricalPlanetGearParametricStudyTool)

    @property
    def datum_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4455.DatumParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4455,
        )

        return self.__parent__._cast(_4455.DatumParametricStudyTool)

    @property
    def external_cad_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4463.ExternalCADModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4463,
        )

        return self.__parent__._cast(_4463.ExternalCADModelParametricStudyTool)

    @property
    def face_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4465.FaceGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4465,
        )

        return self.__parent__._cast(_4465.FaceGearParametricStudyTool)

    @property
    def face_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4466.FaceGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4466,
        )

        return self.__parent__._cast(_4466.FaceGearSetParametricStudyTool)

    @property
    def fe_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4467.FEPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4467,
        )

        return self.__parent__._cast(_4467.FEPartParametricStudyTool)

    @property
    def flexible_pin_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4468.FlexiblePinAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4468,
        )

        return self.__parent__._cast(_4468.FlexiblePinAssemblyParametricStudyTool)

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4470.GearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4470,
        )

        return self.__parent__._cast(_4470.GearParametricStudyTool)

    @property
    def gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4471.GearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4471,
        )

        return self.__parent__._cast(_4471.GearSetParametricStudyTool)

    @property
    def guide_dxf_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4472.GuideDxfModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4472,
        )

        return self.__parent__._cast(_4472.GuideDxfModelParametricStudyTool)

    @property
    def hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4474.HypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4474,
        )

        return self.__parent__._cast(_4474.HypoidGearParametricStudyTool)

    @property
    def hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4475.HypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4475,
        )

        return self.__parent__._cast(_4475.HypoidGearSetParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4478.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4478,
        )

        return self.__parent__._cast(
            _4478.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4479.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4479,
        )

        return self.__parent__._cast(
            _4479.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4481.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4481,
        )

        return self.__parent__._cast(
            _4481.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4482.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4482,
        )

        return self.__parent__._cast(
            _4482.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4484.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4484,
        )

        return self.__parent__._cast(
            _4484.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4485.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4485,
        )

        return self.__parent__._cast(
            _4485.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        )

    @property
    def mass_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4486.MassDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4486,
        )

        return self.__parent__._cast(_4486.MassDiscParametricStudyTool)

    @property
    def measurement_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4487.MeasurementComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4487,
        )

        return self.__parent__._cast(_4487.MeasurementComponentParametricStudyTool)

    @property
    def microphone_array_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4488.MicrophoneArrayParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4488,
        )

        return self.__parent__._cast(_4488.MicrophoneArrayParametricStudyTool)

    @property
    def microphone_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4489.MicrophoneParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4489,
        )

        return self.__parent__._cast(_4489.MicrophoneParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4491.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4491,
        )

        return self.__parent__._cast(_4491.MountableComponentParametricStudyTool)

    @property
    def oil_seal_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4492.OilSealParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4492,
        )

        return self.__parent__._cast(_4492.OilSealParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4503.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4503,
        )

        return self.__parent__._cast(_4503.PartParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4505.PartToPartShearCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4505,
        )

        return self.__parent__._cast(
            _4505.PartToPartShearCouplingHalfParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4506.PartToPartShearCouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4506,
        )

        return self.__parent__._cast(_4506.PartToPartShearCouplingParametricStudyTool)

    @property
    def planetary_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4508.PlanetaryGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4508,
        )

        return self.__parent__._cast(_4508.PlanetaryGearSetParametricStudyTool)

    @property
    def planet_carrier_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4509.PlanetCarrierParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4509,
        )

        return self.__parent__._cast(_4509.PlanetCarrierParametricStudyTool)

    @property
    def point_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4510.PointLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4510,
        )

        return self.__parent__._cast(_4510.PointLoadParametricStudyTool)

    @property
    def power_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4511.PowerLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4511,
        )

        return self.__parent__._cast(_4511.PowerLoadParametricStudyTool)

    @property
    def pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4512.PulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4512,
        )

        return self.__parent__._cast(_4512.PulleyParametricStudyTool)

    @property
    def ring_pins_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4513.RingPinsParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4513,
        )

        return self.__parent__._cast(_4513.RingPinsParametricStudyTool)

    @property
    def rolling_ring_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4515.RollingRingAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4515,
        )

        return self.__parent__._cast(_4515.RollingRingAssemblyParametricStudyTool)

    @property
    def rolling_ring_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4517.RollingRingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4517,
        )

        return self.__parent__._cast(_4517.RollingRingParametricStudyTool)

    @property
    def root_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4518.RootAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4518,
        )

        return self.__parent__._cast(_4518.RootAssemblyParametricStudyTool)

    @property
    def shaft_hub_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4519.ShaftHubConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4519,
        )

        return self.__parent__._cast(_4519.ShaftHubConnectionParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4520.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4520,
        )

        return self.__parent__._cast(_4520.ShaftParametricStudyTool)

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4522.SpecialisedAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4522,
        )

        return self.__parent__._cast(_4522.SpecialisedAssemblyParametricStudyTool)

    @property
    def spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4524.SpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4524,
        )

        return self.__parent__._cast(_4524.SpiralBevelGearParametricStudyTool)

    @property
    def spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4525.SpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4525,
        )

        return self.__parent__._cast(_4525.SpiralBevelGearSetParametricStudyTool)

    @property
    def spring_damper_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4527.SpringDamperHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4527,
        )

        return self.__parent__._cast(_4527.SpringDamperHalfParametricStudyTool)

    @property
    def spring_damper_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4528.SpringDamperParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4528,
        )

        return self.__parent__._cast(_4528.SpringDamperParametricStudyTool)

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4530.StraightBevelDiffGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4530,
        )

        return self.__parent__._cast(_4530.StraightBevelDiffGearParametricStudyTool)

    @property
    def straight_bevel_diff_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4531.StraightBevelDiffGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4531,
        )

        return self.__parent__._cast(_4531.StraightBevelDiffGearSetParametricStudyTool)

    @property
    def straight_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4533.StraightBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4533,
        )

        return self.__parent__._cast(_4533.StraightBevelGearParametricStudyTool)

    @property
    def straight_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4534.StraightBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4534,
        )

        return self.__parent__._cast(_4534.StraightBevelGearSetParametricStudyTool)

    @property
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4535.StraightBevelPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4535,
        )

        return self.__parent__._cast(_4535.StraightBevelPlanetGearParametricStudyTool)

    @property
    def straight_bevel_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4536.StraightBevelSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4536,
        )

        return self.__parent__._cast(_4536.StraightBevelSunGearParametricStudyTool)

    @property
    def synchroniser_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4537.SynchroniserHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4537,
        )

        return self.__parent__._cast(_4537.SynchroniserHalfParametricStudyTool)

    @property
    def synchroniser_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4538.SynchroniserParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4538,
        )

        return self.__parent__._cast(_4538.SynchroniserParametricStudyTool)

    @property
    def synchroniser_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4539.SynchroniserPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4539,
        )

        return self.__parent__._cast(_4539.SynchroniserPartParametricStudyTool)

    @property
    def synchroniser_sleeve_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4540.SynchroniserSleeveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4540,
        )

        return self.__parent__._cast(_4540.SynchroniserSleeveParametricStudyTool)

    @property
    def torque_converter_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4542.TorqueConverterParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4542,
        )

        return self.__parent__._cast(_4542.TorqueConverterParametricStudyTool)

    @property
    def torque_converter_pump_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4543.TorqueConverterPumpParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4543,
        )

        return self.__parent__._cast(_4543.TorqueConverterPumpParametricStudyTool)

    @property
    def torque_converter_turbine_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4544.TorqueConverterTurbineParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4544,
        )

        return self.__parent__._cast(_4544.TorqueConverterTurbineParametricStudyTool)

    @property
    def unbalanced_mass_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4545.UnbalancedMassParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4545,
        )

        return self.__parent__._cast(_4545.UnbalancedMassParametricStudyTool)

    @property
    def virtual_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4546.VirtualComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4546,
        )

        return self.__parent__._cast(_4546.VirtualComponentParametricStudyTool)

    @property
    def worm_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4548.WormGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4548,
        )

        return self.__parent__._cast(_4548.WormGearParametricStudyTool)

    @property
    def worm_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4549.WormGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4549,
        )

        return self.__parent__._cast(_4549.WormGearSetParametricStudyTool)

    @property
    def zerol_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4551.ZerolBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4551,
        )

        return self.__parent__._cast(_4551.ZerolBevelGearParametricStudyTool)

    @property
    def zerol_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4552.ZerolBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4552,
        )

        return self.__parent__._cast(_4552.ZerolBevelGearSetParametricStudyTool)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4684.AbstractAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4684,
        )

        return self.__parent__._cast(_4684.AbstractAssemblyModalAnalysis)

    @property
    def abstract_shaft_modal_analysis(
        self: "CastSelf",
    ) -> "_4685.AbstractShaftModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4685,
        )

        return self.__parent__._cast(_4685.AbstractShaftModalAnalysis)

    @property
    def abstract_shaft_or_housing_modal_analysis(
        self: "CastSelf",
    ) -> "_4686.AbstractShaftOrHousingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4686,
        )

        return self.__parent__._cast(_4686.AbstractShaftOrHousingModalAnalysis)

    @property
    def agma_gleason_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4689.AGMAGleasonConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4689,
        )

        return self.__parent__._cast(_4689.AGMAGleasonConicalGearModalAnalysis)

    @property
    def agma_gleason_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4690.AGMAGleasonConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4690,
        )

        return self.__parent__._cast(_4690.AGMAGleasonConicalGearSetModalAnalysis)

    @property
    def assembly_modal_analysis(self: "CastSelf") -> "_4691.AssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4691,
        )

        return self.__parent__._cast(_4691.AssemblyModalAnalysis)

    @property
    def bearing_modal_analysis(self: "CastSelf") -> "_4692.BearingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4692,
        )

        return self.__parent__._cast(_4692.BearingModalAnalysis)

    @property
    def belt_drive_modal_analysis(self: "CastSelf") -> "_4694.BeltDriveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4694,
        )

        return self.__parent__._cast(_4694.BeltDriveModalAnalysis)

    @property
    def bevel_differential_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4696.BevelDifferentialGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4696,
        )

        return self.__parent__._cast(_4696.BevelDifferentialGearModalAnalysis)

    @property
    def bevel_differential_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4697.BevelDifferentialGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4697,
        )

        return self.__parent__._cast(_4697.BevelDifferentialGearSetModalAnalysis)

    @property
    def bevel_differential_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4698.BevelDifferentialPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4698,
        )

        return self.__parent__._cast(_4698.BevelDifferentialPlanetGearModalAnalysis)

    @property
    def bevel_differential_sun_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4699.BevelDifferentialSunGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4699,
        )

        return self.__parent__._cast(_4699.BevelDifferentialSunGearModalAnalysis)

    @property
    def bevel_gear_modal_analysis(self: "CastSelf") -> "_4701.BevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4701,
        )

        return self.__parent__._cast(_4701.BevelGearModalAnalysis)

    @property
    def bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4702.BevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4702,
        )

        return self.__parent__._cast(_4702.BevelGearSetModalAnalysis)

    @property
    def bolted_joint_modal_analysis(
        self: "CastSelf",
    ) -> "_4703.BoltedJointModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4703,
        )

        return self.__parent__._cast(_4703.BoltedJointModalAnalysis)

    @property
    def bolt_modal_analysis(self: "CastSelf") -> "_4704.BoltModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4704,
        )

        return self.__parent__._cast(_4704.BoltModalAnalysis)

    @property
    def clutch_half_modal_analysis(self: "CastSelf") -> "_4706.ClutchHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4706,
        )

        return self.__parent__._cast(_4706.ClutchHalfModalAnalysis)

    @property
    def clutch_modal_analysis(self: "CastSelf") -> "_4707.ClutchModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4707,
        )

        return self.__parent__._cast(_4707.ClutchModalAnalysis)

    @property
    def component_modal_analysis(self: "CastSelf") -> "_4709.ComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4709,
        )

        return self.__parent__._cast(_4709.ComponentModalAnalysis)

    @property
    def concept_coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4711.ConceptCouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4711,
        )

        return self.__parent__._cast(_4711.ConceptCouplingHalfModalAnalysis)

    @property
    def concept_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4712.ConceptCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4712,
        )

        return self.__parent__._cast(_4712.ConceptCouplingModalAnalysis)

    @property
    def concept_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4714.ConceptGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4714,
        )

        return self.__parent__._cast(_4714.ConceptGearModalAnalysis)

    @property
    def concept_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4715.ConceptGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4715,
        )

        return self.__parent__._cast(_4715.ConceptGearSetModalAnalysis)

    @property
    def conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4717.ConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4717,
        )

        return self.__parent__._cast(_4717.ConicalGearModalAnalysis)

    @property
    def conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4718.ConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4718,
        )

        return self.__parent__._cast(_4718.ConicalGearSetModalAnalysis)

    @property
    def connector_modal_analysis(self: "CastSelf") -> "_4720.ConnectorModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4720,
        )

        return self.__parent__._cast(_4720.ConnectorModalAnalysis)

    @property
    def coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4723.CouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4723,
        )

        return self.__parent__._cast(_4723.CouplingHalfModalAnalysis)

    @property
    def coupling_modal_analysis(self: "CastSelf") -> "_4724.CouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4724,
        )

        return self.__parent__._cast(_4724.CouplingModalAnalysis)

    @property
    def cvt_modal_analysis(self: "CastSelf") -> "_4726.CVTModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4726,
        )

        return self.__parent__._cast(_4726.CVTModalAnalysis)

    @property
    def cvt_pulley_modal_analysis(self: "CastSelf") -> "_4727.CVTPulleyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4727,
        )

        return self.__parent__._cast(_4727.CVTPulleyModalAnalysis)

    @property
    def cycloidal_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4728.CycloidalAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4728,
        )

        return self.__parent__._cast(_4728.CycloidalAssemblyModalAnalysis)

    @property
    def cycloidal_disc_modal_analysis(
        self: "CastSelf",
    ) -> "_4730.CycloidalDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4730,
        )

        return self.__parent__._cast(_4730.CycloidalDiscModalAnalysis)

    @property
    def cylindrical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4733.CylindricalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4733,
        )

        return self.__parent__._cast(_4733.CylindricalGearModalAnalysis)

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4734.CylindricalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4734,
        )

        return self.__parent__._cast(_4734.CylindricalGearSetModalAnalysis)

    @property
    def cylindrical_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4735.CylindricalPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4735,
        )

        return self.__parent__._cast(_4735.CylindricalPlanetGearModalAnalysis)

    @property
    def datum_modal_analysis(self: "CastSelf") -> "_4736.DatumModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4736,
        )

        return self.__parent__._cast(_4736.DatumModalAnalysis)

    @property
    def external_cad_model_modal_analysis(
        self: "CastSelf",
    ) -> "_4740.ExternalCADModelModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4740,
        )

        return self.__parent__._cast(_4740.ExternalCADModelModalAnalysis)

    @property
    def face_gear_modal_analysis(self: "CastSelf") -> "_4742.FaceGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4742,
        )

        return self.__parent__._cast(_4742.FaceGearModalAnalysis)

    @property
    def face_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4743.FaceGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4743,
        )

        return self.__parent__._cast(_4743.FaceGearSetModalAnalysis)

    @property
    def fe_part_modal_analysis(self: "CastSelf") -> "_4744.FEPartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4744,
        )

        return self.__parent__._cast(_4744.FEPartModalAnalysis)

    @property
    def flexible_pin_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4745.FlexiblePinAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4745,
        )

        return self.__parent__._cast(_4745.FlexiblePinAssemblyModalAnalysis)

    @property
    def gear_modal_analysis(self: "CastSelf") -> "_4748.GearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4748,
        )

        return self.__parent__._cast(_4748.GearModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4749.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4749,
        )

        return self.__parent__._cast(_4749.GearSetModalAnalysis)

    @property
    def guide_dxf_model_modal_analysis(
        self: "CastSelf",
    ) -> "_4750.GuideDxfModelModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4750,
        )

        return self.__parent__._cast(_4750.GuideDxfModelModalAnalysis)

    @property
    def hypoid_gear_modal_analysis(self: "CastSelf") -> "_4752.HypoidGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4752,
        )

        return self.__parent__._cast(_4752.HypoidGearModalAnalysis)

    @property
    def hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4753.HypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4753,
        )

        return self.__parent__._cast(_4753.HypoidGearSetModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4756.KlingelnbergCycloPalloidConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4756,
        )

        return self.__parent__._cast(
            _4756.KlingelnbergCycloPalloidConicalGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4757.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4757,
        )

        return self.__parent__._cast(
            _4757.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4759.KlingelnbergCycloPalloidHypoidGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4759,
        )

        return self.__parent__._cast(
            _4759.KlingelnbergCycloPalloidHypoidGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4760.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4760,
        )

        return self.__parent__._cast(
            _4760.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4762.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4762,
        )

        return self.__parent__._cast(
            _4762.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4763.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4763,
        )

        return self.__parent__._cast(
            _4763.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        )

    @property
    def mass_disc_modal_analysis(self: "CastSelf") -> "_4764.MassDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4764,
        )

        return self.__parent__._cast(_4764.MassDiscModalAnalysis)

    @property
    def measurement_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4765.MeasurementComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4765,
        )

        return self.__parent__._cast(_4765.MeasurementComponentModalAnalysis)

    @property
    def microphone_array_modal_analysis(
        self: "CastSelf",
    ) -> "_4766.MicrophoneArrayModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4766,
        )

        return self.__parent__._cast(_4766.MicrophoneArrayModalAnalysis)

    @property
    def microphone_modal_analysis(self: "CastSelf") -> "_4767.MicrophoneModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4767,
        )

        return self.__parent__._cast(_4767.MicrophoneModalAnalysis)

    @property
    def mountable_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4772.MountableComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4772,
        )

        return self.__parent__._cast(_4772.MountableComponentModalAnalysis)

    @property
    def oil_seal_modal_analysis(self: "CastSelf") -> "_4774.OilSealModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4774,
        )

        return self.__parent__._cast(_4774.OilSealModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4776.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4776,
        )

        return self.__parent__._cast(_4776.PartModalAnalysis)

    @property
    def part_to_part_shear_coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4778.PartToPartShearCouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4778,
        )

        return self.__parent__._cast(_4778.PartToPartShearCouplingHalfModalAnalysis)

    @property
    def part_to_part_shear_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4779.PartToPartShearCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4779,
        )

        return self.__parent__._cast(_4779.PartToPartShearCouplingModalAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4781.PlanetaryGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4781,
        )

        return self.__parent__._cast(_4781.PlanetaryGearSetModalAnalysis)

    @property
    def planet_carrier_modal_analysis(
        self: "CastSelf",
    ) -> "_4782.PlanetCarrierModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4782,
        )

        return self.__parent__._cast(_4782.PlanetCarrierModalAnalysis)

    @property
    def point_load_modal_analysis(self: "CastSelf") -> "_4783.PointLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4783,
        )

        return self.__parent__._cast(_4783.PointLoadModalAnalysis)

    @property
    def power_load_modal_analysis(self: "CastSelf") -> "_4784.PowerLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4784,
        )

        return self.__parent__._cast(_4784.PowerLoadModalAnalysis)

    @property
    def pulley_modal_analysis(self: "CastSelf") -> "_4785.PulleyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4785,
        )

        return self.__parent__._cast(_4785.PulleyModalAnalysis)

    @property
    def ring_pins_modal_analysis(self: "CastSelf") -> "_4786.RingPinsModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4786,
        )

        return self.__parent__._cast(_4786.RingPinsModalAnalysis)

    @property
    def rolling_ring_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4788.RollingRingAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4788,
        )

        return self.__parent__._cast(_4788.RollingRingAssemblyModalAnalysis)

    @property
    def rolling_ring_modal_analysis(
        self: "CastSelf",
    ) -> "_4790.RollingRingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4790,
        )

        return self.__parent__._cast(_4790.RollingRingModalAnalysis)

    @property
    def root_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4791.RootAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4791,
        )

        return self.__parent__._cast(_4791.RootAssemblyModalAnalysis)

    @property
    def shaft_hub_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4792.ShaftHubConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4792,
        )

        return self.__parent__._cast(_4792.ShaftHubConnectionModalAnalysis)

    @property
    def shaft_modal_analysis(self: "CastSelf") -> "_4793.ShaftModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4793,
        )

        return self.__parent__._cast(_4793.ShaftModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4796.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4796,
        )

        return self.__parent__._cast(_4796.SpecialisedAssemblyModalAnalysis)

    @property
    def spiral_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4798.SpiralBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4798,
        )

        return self.__parent__._cast(_4798.SpiralBevelGearModalAnalysis)

    @property
    def spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4799.SpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4799,
        )

        return self.__parent__._cast(_4799.SpiralBevelGearSetModalAnalysis)

    @property
    def spring_damper_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4801.SpringDamperHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4801,
        )

        return self.__parent__._cast(_4801.SpringDamperHalfModalAnalysis)

    @property
    def spring_damper_modal_analysis(
        self: "CastSelf",
    ) -> "_4802.SpringDamperModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4802,
        )

        return self.__parent__._cast(_4802.SpringDamperModalAnalysis)

    @property
    def straight_bevel_diff_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4804.StraightBevelDiffGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4804,
        )

        return self.__parent__._cast(_4804.StraightBevelDiffGearModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4805.StraightBevelDiffGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4805,
        )

        return self.__parent__._cast(_4805.StraightBevelDiffGearSetModalAnalysis)

    @property
    def straight_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4807.StraightBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4807,
        )

        return self.__parent__._cast(_4807.StraightBevelGearModalAnalysis)

    @property
    def straight_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4808.StraightBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4808,
        )

        return self.__parent__._cast(_4808.StraightBevelGearSetModalAnalysis)

    @property
    def straight_bevel_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4809.StraightBevelPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4809,
        )

        return self.__parent__._cast(_4809.StraightBevelPlanetGearModalAnalysis)

    @property
    def straight_bevel_sun_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4810.StraightBevelSunGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4810,
        )

        return self.__parent__._cast(_4810.StraightBevelSunGearModalAnalysis)

    @property
    def synchroniser_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4811.SynchroniserHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4811,
        )

        return self.__parent__._cast(_4811.SynchroniserHalfModalAnalysis)

    @property
    def synchroniser_modal_analysis(
        self: "CastSelf",
    ) -> "_4812.SynchroniserModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4812,
        )

        return self.__parent__._cast(_4812.SynchroniserModalAnalysis)

    @property
    def synchroniser_part_modal_analysis(
        self: "CastSelf",
    ) -> "_4813.SynchroniserPartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4813,
        )

        return self.__parent__._cast(_4813.SynchroniserPartModalAnalysis)

    @property
    def synchroniser_sleeve_modal_analysis(
        self: "CastSelf",
    ) -> "_4814.SynchroniserSleeveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4814,
        )

        return self.__parent__._cast(_4814.SynchroniserSleeveModalAnalysis)

    @property
    def torque_converter_modal_analysis(
        self: "CastSelf",
    ) -> "_4816.TorqueConverterModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4816,
        )

        return self.__parent__._cast(_4816.TorqueConverterModalAnalysis)

    @property
    def torque_converter_pump_modal_analysis(
        self: "CastSelf",
    ) -> "_4817.TorqueConverterPumpModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4817,
        )

        return self.__parent__._cast(_4817.TorqueConverterPumpModalAnalysis)

    @property
    def torque_converter_turbine_modal_analysis(
        self: "CastSelf",
    ) -> "_4818.TorqueConverterTurbineModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4818,
        )

        return self.__parent__._cast(_4818.TorqueConverterTurbineModalAnalysis)

    @property
    def unbalanced_mass_modal_analysis(
        self: "CastSelf",
    ) -> "_4819.UnbalancedMassModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4819,
        )

        return self.__parent__._cast(_4819.UnbalancedMassModalAnalysis)

    @property
    def virtual_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4820.VirtualComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4820,
        )

        return self.__parent__._cast(_4820.VirtualComponentModalAnalysis)

    @property
    def worm_gear_modal_analysis(self: "CastSelf") -> "_4825.WormGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4825,
        )

        return self.__parent__._cast(_4825.WormGearModalAnalysis)

    @property
    def worm_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4826.WormGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4826,
        )

        return self.__parent__._cast(_4826.WormGearSetModalAnalysis)

    @property
    def zerol_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4828.ZerolBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4828,
        )

        return self.__parent__._cast(_4828.ZerolBevelGearModalAnalysis)

    @property
    def zerol_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4829.ZerolBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4829,
        )

        return self.__parent__._cast(_4829.ZerolBevelGearSetModalAnalysis)

    @property
    def abstract_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4973.AbstractAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4973,
        )

        return self.__parent__._cast(_4973.AbstractAssemblyModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4974.AbstractShaftModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4974,
        )

        return self.__parent__._cast(_4974.AbstractShaftModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_or_housing_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4975.AbstractShaftOrHousingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4975,
        )

        return self.__parent__._cast(
            _4975.AbstractShaftOrHousingModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4978.AGMAGleasonConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4978,
        )

        return self.__parent__._cast(
            _4978.AGMAGleasonConicalGearModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4979.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4979,
        )

        return self.__parent__._cast(
            _4979.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness
        )

    @property
    def assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4980.AssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4980,
        )

        return self.__parent__._cast(_4980.AssemblyModalAnalysisAtAStiffness)

    @property
    def bearing_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4981.BearingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4981,
        )

        return self.__parent__._cast(_4981.BearingModalAnalysisAtAStiffness)

    @property
    def belt_drive_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4983.BeltDriveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4983,
        )

        return self.__parent__._cast(_4983.BeltDriveModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4985.BevelDifferentialGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4985,
        )

        return self.__parent__._cast(
            _4985.BevelDifferentialGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4986.BevelDifferentialGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4986,
        )

        return self.__parent__._cast(
            _4986.BevelDifferentialGearSetModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4987.BevelDifferentialPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4987,
        )

        return self.__parent__._cast(
            _4987.BevelDifferentialPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4988.BevelDifferentialSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4988,
        )

        return self.__parent__._cast(
            _4988.BevelDifferentialSunGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4990.BevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4990,
        )

        return self.__parent__._cast(_4990.BevelGearModalAnalysisAtAStiffness)

    @property
    def bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4991.BevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4991,
        )

        return self.__parent__._cast(_4991.BevelGearSetModalAnalysisAtAStiffness)

    @property
    def bolted_joint_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4992.BoltedJointModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4992,
        )

        return self.__parent__._cast(_4992.BoltedJointModalAnalysisAtAStiffness)

    @property
    def bolt_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4993.BoltModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4993,
        )

        return self.__parent__._cast(_4993.BoltModalAnalysisAtAStiffness)

    @property
    def clutch_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4995.ClutchHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4995,
        )

        return self.__parent__._cast(_4995.ClutchHalfModalAnalysisAtAStiffness)

    @property
    def clutch_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4996.ClutchModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4996,
        )

        return self.__parent__._cast(_4996.ClutchModalAnalysisAtAStiffness)

    @property
    def component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4998.ComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4998,
        )

        return self.__parent__._cast(_4998.ComponentModalAnalysisAtAStiffness)

    @property
    def concept_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5000.ConceptCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5000,
        )

        return self.__parent__._cast(_5000.ConceptCouplingHalfModalAnalysisAtAStiffness)

    @property
    def concept_coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5001.ConceptCouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5001,
        )

        return self.__parent__._cast(_5001.ConceptCouplingModalAnalysisAtAStiffness)

    @property
    def concept_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5003.ConceptGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5003,
        )

        return self.__parent__._cast(_5003.ConceptGearModalAnalysisAtAStiffness)

    @property
    def concept_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5004.ConceptGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5004,
        )

        return self.__parent__._cast(_5004.ConceptGearSetModalAnalysisAtAStiffness)

    @property
    def conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5006.ConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5006,
        )

        return self.__parent__._cast(_5006.ConicalGearModalAnalysisAtAStiffness)

    @property
    def conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5007.ConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5007,
        )

        return self.__parent__._cast(_5007.ConicalGearSetModalAnalysisAtAStiffness)

    @property
    def connector_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5009.ConnectorModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5009,
        )

        return self.__parent__._cast(_5009.ConnectorModalAnalysisAtAStiffness)

    @property
    def coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5011.CouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5011,
        )

        return self.__parent__._cast(_5011.CouplingHalfModalAnalysisAtAStiffness)

    @property
    def coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5012.CouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5012,
        )

        return self.__parent__._cast(_5012.CouplingModalAnalysisAtAStiffness)

    @property
    def cvt_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5014.CVTModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5014,
        )

        return self.__parent__._cast(_5014.CVTModalAnalysisAtAStiffness)

    @property
    def cvt_pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5015.CVTPulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5015,
        )

        return self.__parent__._cast(_5015.CVTPulleyModalAnalysisAtAStiffness)

    @property
    def cycloidal_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5016.CycloidalAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5016,
        )

        return self.__parent__._cast(_5016.CycloidalAssemblyModalAnalysisAtAStiffness)

    @property
    def cycloidal_disc_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5018.CycloidalDiscModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5018,
        )

        return self.__parent__._cast(_5018.CycloidalDiscModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5021.CylindricalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5021,
        )

        return self.__parent__._cast(_5021.CylindricalGearModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5022.CylindricalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5022,
        )

        return self.__parent__._cast(_5022.CylindricalGearSetModalAnalysisAtAStiffness)

    @property
    def cylindrical_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5023.CylindricalPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5023,
        )

        return self.__parent__._cast(
            _5023.CylindricalPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def datum_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5024.DatumModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5024,
        )

        return self.__parent__._cast(_5024.DatumModalAnalysisAtAStiffness)

    @property
    def external_cad_model_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5026.ExternalCADModelModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5026,
        )

        return self.__parent__._cast(_5026.ExternalCADModelModalAnalysisAtAStiffness)

    @property
    def face_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5028.FaceGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5028,
        )

        return self.__parent__._cast(_5028.FaceGearModalAnalysisAtAStiffness)

    @property
    def face_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5029.FaceGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5029,
        )

        return self.__parent__._cast(_5029.FaceGearSetModalAnalysisAtAStiffness)

    @property
    def fe_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5030.FEPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5030,
        )

        return self.__parent__._cast(_5030.FEPartModalAnalysisAtAStiffness)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5031.FlexiblePinAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5031,
        )

        return self.__parent__._cast(_5031.FlexiblePinAssemblyModalAnalysisAtAStiffness)

    @property
    def gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5033.GearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5033,
        )

        return self.__parent__._cast(_5033.GearModalAnalysisAtAStiffness)

    @property
    def gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5034.GearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5034,
        )

        return self.__parent__._cast(_5034.GearSetModalAnalysisAtAStiffness)

    @property
    def guide_dxf_model_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5035.GuideDxfModelModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5035,
        )

        return self.__parent__._cast(_5035.GuideDxfModelModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5037.HypoidGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5037,
        )

        return self.__parent__._cast(_5037.HypoidGearModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5038.HypoidGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5038,
        )

        return self.__parent__._cast(_5038.HypoidGearSetModalAnalysisAtAStiffness)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5041.KlingelnbergCycloPalloidConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5041,
        )

        return self.__parent__._cast(
            _5041.KlingelnbergCycloPalloidConicalGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5042.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5042,
        )

        return self.__parent__._cast(
            _5042.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5044.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5044,
        )

        return self.__parent__._cast(
            _5044.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5045.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5045,
        )

        return self.__parent__._cast(
            _5045.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5047.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5047,
        )

        return self.__parent__._cast(
            _5047.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5048.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5048,
        )

        return self.__parent__._cast(
            _5048.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness
        )

    @property
    def mass_disc_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5049.MassDiscModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5049,
        )

        return self.__parent__._cast(_5049.MassDiscModalAnalysisAtAStiffness)

    @property
    def measurement_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5050.MeasurementComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5050,
        )

        return self.__parent__._cast(
            _5050.MeasurementComponentModalAnalysisAtAStiffness
        )

    @property
    def microphone_array_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5051.MicrophoneArrayModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5051,
        )

        return self.__parent__._cast(_5051.MicrophoneArrayModalAnalysisAtAStiffness)

    @property
    def microphone_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5052.MicrophoneModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5052,
        )

        return self.__parent__._cast(_5052.MicrophoneModalAnalysisAtAStiffness)

    @property
    def mountable_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5054.MountableComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5054,
        )

        return self.__parent__._cast(_5054.MountableComponentModalAnalysisAtAStiffness)

    @property
    def oil_seal_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5055.OilSealModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5055,
        )

        return self.__parent__._cast(_5055.OilSealModalAnalysisAtAStiffness)

    @property
    def part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5056.PartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5056,
        )

        return self.__parent__._cast(_5056.PartModalAnalysisAtAStiffness)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5058.PartToPartShearCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5058,
        )

        return self.__parent__._cast(
            _5058.PartToPartShearCouplingHalfModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5059.PartToPartShearCouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5059,
        )

        return self.__parent__._cast(
            _5059.PartToPartShearCouplingModalAnalysisAtAStiffness
        )

    @property
    def planetary_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5061.PlanetaryGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5061,
        )

        return self.__parent__._cast(_5061.PlanetaryGearSetModalAnalysisAtAStiffness)

    @property
    def planet_carrier_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5062.PlanetCarrierModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5062,
        )

        return self.__parent__._cast(_5062.PlanetCarrierModalAnalysisAtAStiffness)

    @property
    def point_load_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5063.PointLoadModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5063,
        )

        return self.__parent__._cast(_5063.PointLoadModalAnalysisAtAStiffness)

    @property
    def power_load_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5064.PowerLoadModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5064,
        )

        return self.__parent__._cast(_5064.PowerLoadModalAnalysisAtAStiffness)

    @property
    def pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5065.PulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5065,
        )

        return self.__parent__._cast(_5065.PulleyModalAnalysisAtAStiffness)

    @property
    def ring_pins_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5066.RingPinsModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5066,
        )

        return self.__parent__._cast(_5066.RingPinsModalAnalysisAtAStiffness)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5068.RollingRingAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5068,
        )

        return self.__parent__._cast(_5068.RollingRingAssemblyModalAnalysisAtAStiffness)

    @property
    def rolling_ring_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5070.RollingRingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5070,
        )

        return self.__parent__._cast(_5070.RollingRingModalAnalysisAtAStiffness)

    @property
    def root_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5071.RootAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5071,
        )

        return self.__parent__._cast(_5071.RootAssemblyModalAnalysisAtAStiffness)

    @property
    def shaft_hub_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5072.ShaftHubConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5072,
        )

        return self.__parent__._cast(_5072.ShaftHubConnectionModalAnalysisAtAStiffness)

    @property
    def shaft_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5073.ShaftModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5073,
        )

        return self.__parent__._cast(_5073.ShaftModalAnalysisAtAStiffness)

    @property
    def specialised_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5075.SpecialisedAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5075,
        )

        return self.__parent__._cast(_5075.SpecialisedAssemblyModalAnalysisAtAStiffness)

    @property
    def spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5077.SpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5077,
        )

        return self.__parent__._cast(_5077.SpiralBevelGearModalAnalysisAtAStiffness)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5078.SpiralBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5078,
        )

        return self.__parent__._cast(_5078.SpiralBevelGearSetModalAnalysisAtAStiffness)

    @property
    def spring_damper_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5080.SpringDamperHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5080,
        )

        return self.__parent__._cast(_5080.SpringDamperHalfModalAnalysisAtAStiffness)

    @property
    def spring_damper_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5081.SpringDamperModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5081,
        )

        return self.__parent__._cast(_5081.SpringDamperModalAnalysisAtAStiffness)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5083.StraightBevelDiffGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5083,
        )

        return self.__parent__._cast(
            _5083.StraightBevelDiffGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5084.StraightBevelDiffGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5084,
        )

        return self.__parent__._cast(
            _5084.StraightBevelDiffGearSetModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5086.StraightBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5086,
        )

        return self.__parent__._cast(_5086.StraightBevelGearModalAnalysisAtAStiffness)

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5087.StraightBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5087,
        )

        return self.__parent__._cast(
            _5087.StraightBevelGearSetModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5088.StraightBevelPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5088,
        )

        return self.__parent__._cast(
            _5088.StraightBevelPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5089.StraightBevelSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5089,
        )

        return self.__parent__._cast(
            _5089.StraightBevelSunGearModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5090.SynchroniserHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5090,
        )

        return self.__parent__._cast(_5090.SynchroniserHalfModalAnalysisAtAStiffness)

    @property
    def synchroniser_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5091.SynchroniserModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5091,
        )

        return self.__parent__._cast(_5091.SynchroniserModalAnalysisAtAStiffness)

    @property
    def synchroniser_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5092.SynchroniserPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5092,
        )

        return self.__parent__._cast(_5092.SynchroniserPartModalAnalysisAtAStiffness)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5093.SynchroniserSleeveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5093,
        )

        return self.__parent__._cast(_5093.SynchroniserSleeveModalAnalysisAtAStiffness)

    @property
    def torque_converter_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5095.TorqueConverterModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5095,
        )

        return self.__parent__._cast(_5095.TorqueConverterModalAnalysisAtAStiffness)

    @property
    def torque_converter_pump_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5096.TorqueConverterPumpModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5096,
        )

        return self.__parent__._cast(_5096.TorqueConverterPumpModalAnalysisAtAStiffness)

    @property
    def torque_converter_turbine_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5097.TorqueConverterTurbineModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5097,
        )

        return self.__parent__._cast(
            _5097.TorqueConverterTurbineModalAnalysisAtAStiffness
        )

    @property
    def unbalanced_mass_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5098.UnbalancedMassModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5098,
        )

        return self.__parent__._cast(_5098.UnbalancedMassModalAnalysisAtAStiffness)

    @property
    def virtual_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5099.VirtualComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5099,
        )

        return self.__parent__._cast(_5099.VirtualComponentModalAnalysisAtAStiffness)

    @property
    def worm_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5101.WormGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5101,
        )

        return self.__parent__._cast(_5101.WormGearModalAnalysisAtAStiffness)

    @property
    def worm_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5102.WormGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5102,
        )

        return self.__parent__._cast(_5102.WormGearSetModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5104.ZerolBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5104,
        )

        return self.__parent__._cast(_5104.ZerolBevelGearModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5105.ZerolBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5105,
        )

        return self.__parent__._cast(_5105.ZerolBevelGearSetModalAnalysisAtAStiffness)

    @property
    def abstract_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5237.AbstractAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5237,
        )

        return self.__parent__._cast(_5237.AbstractAssemblyModalAnalysisAtASpeed)

    @property
    def abstract_shaft_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5238.AbstractShaftModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5238,
        )

        return self.__parent__._cast(_5238.AbstractShaftModalAnalysisAtASpeed)

    @property
    def abstract_shaft_or_housing_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5239.AbstractShaftOrHousingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5239,
        )

        return self.__parent__._cast(_5239.AbstractShaftOrHousingModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5242.AGMAGleasonConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5242,
        )

        return self.__parent__._cast(_5242.AGMAGleasonConicalGearModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5243.AGMAGleasonConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5243,
        )

        return self.__parent__._cast(
            _5243.AGMAGleasonConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5244.AssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5244,
        )

        return self.__parent__._cast(_5244.AssemblyModalAnalysisAtASpeed)

    @property
    def bearing_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5245.BearingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5245,
        )

        return self.__parent__._cast(_5245.BearingModalAnalysisAtASpeed)

    @property
    def belt_drive_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5247.BeltDriveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5247,
        )

        return self.__parent__._cast(_5247.BeltDriveModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5249.BevelDifferentialGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5249,
        )

        return self.__parent__._cast(_5249.BevelDifferentialGearModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5250.BevelDifferentialGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5250,
        )

        return self.__parent__._cast(
            _5250.BevelDifferentialGearSetModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5251.BevelDifferentialPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5251,
        )

        return self.__parent__._cast(
            _5251.BevelDifferentialPlanetGearModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5252.BevelDifferentialSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5252,
        )

        return self.__parent__._cast(
            _5252.BevelDifferentialSunGearModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5254.BevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5254,
        )

        return self.__parent__._cast(_5254.BevelGearModalAnalysisAtASpeed)

    @property
    def bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5255.BevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5255,
        )

        return self.__parent__._cast(_5255.BevelGearSetModalAnalysisAtASpeed)

    @property
    def bolted_joint_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5256.BoltedJointModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5256,
        )

        return self.__parent__._cast(_5256.BoltedJointModalAnalysisAtASpeed)

    @property
    def bolt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5257.BoltModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5257,
        )

        return self.__parent__._cast(_5257.BoltModalAnalysisAtASpeed)

    @property
    def clutch_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5259.ClutchHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5259,
        )

        return self.__parent__._cast(_5259.ClutchHalfModalAnalysisAtASpeed)

    @property
    def clutch_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5260.ClutchModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5260,
        )

        return self.__parent__._cast(_5260.ClutchModalAnalysisAtASpeed)

    @property
    def component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5262.ComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5262,
        )

        return self.__parent__._cast(_5262.ComponentModalAnalysisAtASpeed)

    @property
    def concept_coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5264.ConceptCouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5264,
        )

        return self.__parent__._cast(_5264.ConceptCouplingHalfModalAnalysisAtASpeed)

    @property
    def concept_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5265.ConceptCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5265,
        )

        return self.__parent__._cast(_5265.ConceptCouplingModalAnalysisAtASpeed)

    @property
    def concept_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5267.ConceptGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5267,
        )

        return self.__parent__._cast(_5267.ConceptGearModalAnalysisAtASpeed)

    @property
    def concept_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5268.ConceptGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5268,
        )

        return self.__parent__._cast(_5268.ConceptGearSetModalAnalysisAtASpeed)

    @property
    def conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5270.ConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5270,
        )

        return self.__parent__._cast(_5270.ConicalGearModalAnalysisAtASpeed)

    @property
    def conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5271.ConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5271,
        )

        return self.__parent__._cast(_5271.ConicalGearSetModalAnalysisAtASpeed)

    @property
    def connector_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5273.ConnectorModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5273,
        )

        return self.__parent__._cast(_5273.ConnectorModalAnalysisAtASpeed)

    @property
    def coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5275.CouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5275,
        )

        return self.__parent__._cast(_5275.CouplingHalfModalAnalysisAtASpeed)

    @property
    def coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5276.CouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5276,
        )

        return self.__parent__._cast(_5276.CouplingModalAnalysisAtASpeed)

    @property
    def cvt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5278.CVTModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5278,
        )

        return self.__parent__._cast(_5278.CVTModalAnalysisAtASpeed)

    @property
    def cvt_pulley_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5279.CVTPulleyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5279,
        )

        return self.__parent__._cast(_5279.CVTPulleyModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5280.CycloidalAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5280,
        )

        return self.__parent__._cast(_5280.CycloidalAssemblyModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5282.CycloidalDiscModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5282,
        )

        return self.__parent__._cast(_5282.CycloidalDiscModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5285.CylindricalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5285,
        )

        return self.__parent__._cast(_5285.CylindricalGearModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5286.CylindricalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5286,
        )

        return self.__parent__._cast(_5286.CylindricalGearSetModalAnalysisAtASpeed)

    @property
    def cylindrical_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5287.CylindricalPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5287,
        )

        return self.__parent__._cast(_5287.CylindricalPlanetGearModalAnalysisAtASpeed)

    @property
    def datum_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5288.DatumModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5288,
        )

        return self.__parent__._cast(_5288.DatumModalAnalysisAtASpeed)

    @property
    def external_cad_model_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5289.ExternalCADModelModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5289,
        )

        return self.__parent__._cast(_5289.ExternalCADModelModalAnalysisAtASpeed)

    @property
    def face_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5291.FaceGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5291,
        )

        return self.__parent__._cast(_5291.FaceGearModalAnalysisAtASpeed)

    @property
    def face_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5292.FaceGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5292,
        )

        return self.__parent__._cast(_5292.FaceGearSetModalAnalysisAtASpeed)

    @property
    def fe_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5293.FEPartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5293,
        )

        return self.__parent__._cast(_5293.FEPartModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5294.FlexiblePinAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5294,
        )

        return self.__parent__._cast(_5294.FlexiblePinAssemblyModalAnalysisAtASpeed)

    @property
    def gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5296.GearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5296,
        )

        return self.__parent__._cast(_5296.GearModalAnalysisAtASpeed)

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5297.GearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5297,
        )

        return self.__parent__._cast(_5297.GearSetModalAnalysisAtASpeed)

    @property
    def guide_dxf_model_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5298.GuideDxfModelModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5298,
        )

        return self.__parent__._cast(_5298.GuideDxfModelModalAnalysisAtASpeed)

    @property
    def hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5300.HypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5300,
        )

        return self.__parent__._cast(_5300.HypoidGearModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5301.HypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5301,
        )

        return self.__parent__._cast(_5301.HypoidGearSetModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5304.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5304,
        )

        return self.__parent__._cast(
            _5304.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5305.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5305,
        )

        return self.__parent__._cast(
            _5305.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5307.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5307,
        )

        return self.__parent__._cast(
            _5307.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5308.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5308,
        )

        return self.__parent__._cast(
            _5308.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5310.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5310,
        )

        return self.__parent__._cast(
            _5310.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5311.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5311,
        )

        return self.__parent__._cast(
            _5311.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
        )

    @property
    def mass_disc_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5312.MassDiscModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5312,
        )

        return self.__parent__._cast(_5312.MassDiscModalAnalysisAtASpeed)

    @property
    def measurement_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5313.MeasurementComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5313,
        )

        return self.__parent__._cast(_5313.MeasurementComponentModalAnalysisAtASpeed)

    @property
    def microphone_array_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5314.MicrophoneArrayModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5314,
        )

        return self.__parent__._cast(_5314.MicrophoneArrayModalAnalysisAtASpeed)

    @property
    def microphone_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5315.MicrophoneModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5315,
        )

        return self.__parent__._cast(_5315.MicrophoneModalAnalysisAtASpeed)

    @property
    def mountable_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5317.MountableComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5317,
        )

        return self.__parent__._cast(_5317.MountableComponentModalAnalysisAtASpeed)

    @property
    def oil_seal_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5318.OilSealModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5318,
        )

        return self.__parent__._cast(_5318.OilSealModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5319.PartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5319,
        )

        return self.__parent__._cast(_5319.PartModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5321.PartToPartShearCouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5321,
        )

        return self.__parent__._cast(
            _5321.PartToPartShearCouplingHalfModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5322.PartToPartShearCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5322,
        )

        return self.__parent__._cast(_5322.PartToPartShearCouplingModalAnalysisAtASpeed)

    @property
    def planetary_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5324.PlanetaryGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5324,
        )

        return self.__parent__._cast(_5324.PlanetaryGearSetModalAnalysisAtASpeed)

    @property
    def planet_carrier_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5325.PlanetCarrierModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5325,
        )

        return self.__parent__._cast(_5325.PlanetCarrierModalAnalysisAtASpeed)

    @property
    def point_load_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5326.PointLoadModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5326,
        )

        return self.__parent__._cast(_5326.PointLoadModalAnalysisAtASpeed)

    @property
    def power_load_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5327.PowerLoadModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5327,
        )

        return self.__parent__._cast(_5327.PowerLoadModalAnalysisAtASpeed)

    @property
    def pulley_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5328.PulleyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5328,
        )

        return self.__parent__._cast(_5328.PulleyModalAnalysisAtASpeed)

    @property
    def ring_pins_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5329.RingPinsModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5329,
        )

        return self.__parent__._cast(_5329.RingPinsModalAnalysisAtASpeed)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5331.RollingRingAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5331,
        )

        return self.__parent__._cast(_5331.RollingRingAssemblyModalAnalysisAtASpeed)

    @property
    def rolling_ring_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5333.RollingRingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5333,
        )

        return self.__parent__._cast(_5333.RollingRingModalAnalysisAtASpeed)

    @property
    def root_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5334.RootAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5334,
        )

        return self.__parent__._cast(_5334.RootAssemblyModalAnalysisAtASpeed)

    @property
    def shaft_hub_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5335.ShaftHubConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5335,
        )

        return self.__parent__._cast(_5335.ShaftHubConnectionModalAnalysisAtASpeed)

    @property
    def shaft_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5336.ShaftModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5336,
        )

        return self.__parent__._cast(_5336.ShaftModalAnalysisAtASpeed)

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5338.SpecialisedAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5338,
        )

        return self.__parent__._cast(_5338.SpecialisedAssemblyModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5340.SpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5340,
        )

        return self.__parent__._cast(_5340.SpiralBevelGearModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5341.SpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5341,
        )

        return self.__parent__._cast(_5341.SpiralBevelGearSetModalAnalysisAtASpeed)

    @property
    def spring_damper_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5343.SpringDamperHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5343,
        )

        return self.__parent__._cast(_5343.SpringDamperHalfModalAnalysisAtASpeed)

    @property
    def spring_damper_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5344.SpringDamperModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5344,
        )

        return self.__parent__._cast(_5344.SpringDamperModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5346.StraightBevelDiffGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5346,
        )

        return self.__parent__._cast(_5346.StraightBevelDiffGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5347.StraightBevelDiffGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5347,
        )

        return self.__parent__._cast(
            _5347.StraightBevelDiffGearSetModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5349.StraightBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5349,
        )

        return self.__parent__._cast(_5349.StraightBevelGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5350.StraightBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5350,
        )

        return self.__parent__._cast(_5350.StraightBevelGearSetModalAnalysisAtASpeed)

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5351.StraightBevelPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5351,
        )

        return self.__parent__._cast(_5351.StraightBevelPlanetGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5352.StraightBevelSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5352,
        )

        return self.__parent__._cast(_5352.StraightBevelSunGearModalAnalysisAtASpeed)

    @property
    def synchroniser_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5353.SynchroniserHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5353,
        )

        return self.__parent__._cast(_5353.SynchroniserHalfModalAnalysisAtASpeed)

    @property
    def synchroniser_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5354.SynchroniserModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5354,
        )

        return self.__parent__._cast(_5354.SynchroniserModalAnalysisAtASpeed)

    @property
    def synchroniser_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5355.SynchroniserPartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5355,
        )

        return self.__parent__._cast(_5355.SynchroniserPartModalAnalysisAtASpeed)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5356.SynchroniserSleeveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5356,
        )

        return self.__parent__._cast(_5356.SynchroniserSleeveModalAnalysisAtASpeed)

    @property
    def torque_converter_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5358.TorqueConverterModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5358,
        )

        return self.__parent__._cast(_5358.TorqueConverterModalAnalysisAtASpeed)

    @property
    def torque_converter_pump_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5359.TorqueConverterPumpModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5359,
        )

        return self.__parent__._cast(_5359.TorqueConverterPumpModalAnalysisAtASpeed)

    @property
    def torque_converter_turbine_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5360.TorqueConverterTurbineModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5360,
        )

        return self.__parent__._cast(_5360.TorqueConverterTurbineModalAnalysisAtASpeed)

    @property
    def unbalanced_mass_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5361.UnbalancedMassModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5361,
        )

        return self.__parent__._cast(_5361.UnbalancedMassModalAnalysisAtASpeed)

    @property
    def virtual_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5362.VirtualComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5362,
        )

        return self.__parent__._cast(_5362.VirtualComponentModalAnalysisAtASpeed)

    @property
    def worm_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5364.WormGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5364,
        )

        return self.__parent__._cast(_5364.WormGearModalAnalysisAtASpeed)

    @property
    def worm_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5365.WormGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5365,
        )

        return self.__parent__._cast(_5365.WormGearSetModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5367.ZerolBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5367,
        )

        return self.__parent__._cast(_5367.ZerolBevelGearModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5368.ZerolBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5368,
        )

        return self.__parent__._cast(_5368.ZerolBevelGearSetModalAnalysisAtASpeed)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5500.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5500,
        )

        return self.__parent__._cast(_5500.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5501.AbstractShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5501,
        )

        return self.__parent__._cast(_5501.AbstractShaftMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_or_housing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5502.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5502,
        )

        return self.__parent__._cast(
            _5502.AbstractShaftOrHousingMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5505.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5505,
        )

        return self.__parent__._cast(
            _5505.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5506.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5506,
        )

        return self.__parent__._cast(
            _5506.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5508.AssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5508,
        )

        return self.__parent__._cast(_5508.AssemblyMultibodyDynamicsAnalysis)

    @property
    def bearing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5510.BearingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5510,
        )

        return self.__parent__._cast(_5510.BearingMultibodyDynamicsAnalysis)

    @property
    def belt_drive_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5513.BeltDriveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5513,
        )

        return self.__parent__._cast(_5513.BeltDriveMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5515.BevelDifferentialGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5515,
        )

        return self.__parent__._cast(
            _5515.BevelDifferentialGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5516.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5516,
        )

        return self.__parent__._cast(
            _5516.BevelDifferentialGearSetMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5517.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5517,
        )

        return self.__parent__._cast(
            _5517.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5518.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5518,
        )

        return self.__parent__._cast(
            _5518.BevelDifferentialSunGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5520.BevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5520,
        )

        return self.__parent__._cast(_5520.BevelGearMultibodyDynamicsAnalysis)

    @property
    def bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5521.BevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5521,
        )

        return self.__parent__._cast(_5521.BevelGearSetMultibodyDynamicsAnalysis)

    @property
    def bolted_joint_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5522.BoltedJointMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5522,
        )

        return self.__parent__._cast(_5522.BoltedJointMultibodyDynamicsAnalysis)

    @property
    def bolt_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5523.BoltMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5523,
        )

        return self.__parent__._cast(_5523.BoltMultibodyDynamicsAnalysis)

    @property
    def clutch_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5525.ClutchHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5525,
        )

        return self.__parent__._cast(_5525.ClutchHalfMultibodyDynamicsAnalysis)

    @property
    def clutch_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5526.ClutchMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5526,
        )

        return self.__parent__._cast(_5526.ClutchMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5529.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5529,
        )

        return self.__parent__._cast(_5529.ComponentMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5531.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5531,
        )

        return self.__parent__._cast(_5531.ConceptCouplingHalfMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5532.ConceptCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5532,
        )

        return self.__parent__._cast(_5532.ConceptCouplingMultibodyDynamicsAnalysis)

    @property
    def concept_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5534.ConceptGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5534,
        )

        return self.__parent__._cast(_5534.ConceptGearMultibodyDynamicsAnalysis)

    @property
    def concept_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5535.ConceptGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5535,
        )

        return self.__parent__._cast(_5535.ConceptGearSetMultibodyDynamicsAnalysis)

    @property
    def conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5537.ConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5537,
        )

        return self.__parent__._cast(_5537.ConicalGearMultibodyDynamicsAnalysis)

    @property
    def conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5538.ConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5538,
        )

        return self.__parent__._cast(_5538.ConicalGearSetMultibodyDynamicsAnalysis)

    @property
    def connector_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5540.ConnectorMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5540,
        )

        return self.__parent__._cast(_5540.ConnectorMultibodyDynamicsAnalysis)

    @property
    def coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5542.CouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5542,
        )

        return self.__parent__._cast(_5542.CouplingHalfMultibodyDynamicsAnalysis)

    @property
    def coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5543.CouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5543,
        )

        return self.__parent__._cast(_5543.CouplingMultibodyDynamicsAnalysis)

    @property
    def cvt_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5545.CVTMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5545,
        )

        return self.__parent__._cast(_5545.CVTMultibodyDynamicsAnalysis)

    @property
    def cvt_pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5546.CVTPulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5546,
        )

        return self.__parent__._cast(_5546.CVTPulleyMultibodyDynamicsAnalysis)

    @property
    def cycloidal_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5547.CycloidalAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5547,
        )

        return self.__parent__._cast(_5547.CycloidalAssemblyMultibodyDynamicsAnalysis)

    @property
    def cycloidal_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5549.CycloidalDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5549,
        )

        return self.__parent__._cast(_5549.CycloidalDiscMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5552.CylindricalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5552,
        )

        return self.__parent__._cast(_5552.CylindricalGearMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5553.CylindricalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5553,
        )

        return self.__parent__._cast(_5553.CylindricalGearSetMultibodyDynamicsAnalysis)

    @property
    def cylindrical_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5554.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5554,
        )

        return self.__parent__._cast(
            _5554.CylindricalPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def datum_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5555.DatumMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5555,
        )

        return self.__parent__._cast(_5555.DatumMultibodyDynamicsAnalysis)

    @property
    def external_cad_model_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5556.ExternalCADModelMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5556,
        )

        return self.__parent__._cast(_5556.ExternalCADModelMultibodyDynamicsAnalysis)

    @property
    def face_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5558.FaceGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5558,
        )

        return self.__parent__._cast(_5558.FaceGearMultibodyDynamicsAnalysis)

    @property
    def face_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5559.FaceGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5559,
        )

        return self.__parent__._cast(_5559.FaceGearSetMultibodyDynamicsAnalysis)

    @property
    def fe_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5560.FEPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5560,
        )

        return self.__parent__._cast(_5560.FEPartMultibodyDynamicsAnalysis)

    @property
    def flexible_pin_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5561.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5561,
        )

        return self.__parent__._cast(_5561.FlexiblePinAssemblyMultibodyDynamicsAnalysis)

    @property
    def gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5564.GearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5564,
        )

        return self.__parent__._cast(_5564.GearMultibodyDynamicsAnalysis)

    @property
    def gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5565.GearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5565,
        )

        return self.__parent__._cast(_5565.GearSetMultibodyDynamicsAnalysis)

    @property
    def guide_dxf_model_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5566.GuideDxfModelMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5566,
        )

        return self.__parent__._cast(_5566.GuideDxfModelMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5568.HypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5568,
        )

        return self.__parent__._cast(_5568.HypoidGearMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5569.HypoidGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5569,
        )

        return self.__parent__._cast(_5569.HypoidGearSetMultibodyDynamicsAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5576.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5576,
        )

        return self.__parent__._cast(
            _5576.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5577.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5577,
        )

        return self.__parent__._cast(
            _5577.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5579.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5579,
        )

        return self.__parent__._cast(
            _5579.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5580.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5580,
        )

        return self.__parent__._cast(
            _5580.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5582.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5582,
        )

        return self.__parent__._cast(
            _5582.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5583.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5583,
        )

        return self.__parent__._cast(
            _5583.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis
        )

    @property
    def mass_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5584.MassDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5584,
        )

        return self.__parent__._cast(_5584.MassDiscMultibodyDynamicsAnalysis)

    @property
    def measurement_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5588.MeasurementComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5588,
        )

        return self.__parent__._cast(
            _5588.MeasurementComponentMultibodyDynamicsAnalysis
        )

    @property
    def microphone_array_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5589.MicrophoneArrayMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5589,
        )

        return self.__parent__._cast(_5589.MicrophoneArrayMultibodyDynamicsAnalysis)

    @property
    def microphone_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5590.MicrophoneMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5590,
        )

        return self.__parent__._cast(_5590.MicrophoneMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5591.MountableComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5591,
        )

        return self.__parent__._cast(_5591.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def oil_seal_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5593.OilSealMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5593,
        )

        return self.__parent__._cast(_5593.OilSealMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5594,
        )

        return self.__parent__._cast(_5594.PartMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5596.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5596,
        )

        return self.__parent__._cast(
            _5596.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5597.PartToPartShearCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5597,
        )

        return self.__parent__._cast(
            _5597.PartToPartShearCouplingMultibodyDynamicsAnalysis
        )

    @property
    def planetary_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5599.PlanetaryGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5599,
        )

        return self.__parent__._cast(_5599.PlanetaryGearSetMultibodyDynamicsAnalysis)

    @property
    def planet_carrier_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5600.PlanetCarrierMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5600,
        )

        return self.__parent__._cast(_5600.PlanetCarrierMultibodyDynamicsAnalysis)

    @property
    def point_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5601.PointLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5601,
        )

        return self.__parent__._cast(_5601.PointLoadMultibodyDynamicsAnalysis)

    @property
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5602.PowerLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5602,
        )

        return self.__parent__._cast(_5602.PowerLoadMultibodyDynamicsAnalysis)

    @property
    def pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5603.PulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5603,
        )

        return self.__parent__._cast(_5603.PulleyMultibodyDynamicsAnalysis)

    @property
    def ring_pins_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5604.RingPinsMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5604,
        )

        return self.__parent__._cast(_5604.RingPinsMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5606.RollingRingAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5606,
        )

        return self.__parent__._cast(_5606.RollingRingAssemblyMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5608.RollingRingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5608,
        )

        return self.__parent__._cast(_5608.RollingRingMultibodyDynamicsAnalysis)

    @property
    def root_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5609.RootAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5609,
        )

        return self.__parent__._cast(_5609.RootAssemblyMultibodyDynamicsAnalysis)

    @property
    def shaft_hub_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5612.ShaftHubConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5612,
        )

        return self.__parent__._cast(_5612.ShaftHubConnectionMultibodyDynamicsAnalysis)

    @property
    def shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5613.ShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5613,
        )

        return self.__parent__._cast(_5613.ShaftMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5616.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5616,
        )

        return self.__parent__._cast(_5616.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5618.SpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5618,
        )

        return self.__parent__._cast(_5618.SpiralBevelGearMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5619.SpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5619,
        )

        return self.__parent__._cast(_5619.SpiralBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def spring_damper_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5622.SpringDamperHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5622,
        )

        return self.__parent__._cast(_5622.SpringDamperHalfMultibodyDynamicsAnalysis)

    @property
    def spring_damper_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5623.SpringDamperMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5623,
        )

        return self.__parent__._cast(_5623.SpringDamperMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5625.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5625,
        )

        return self.__parent__._cast(
            _5625.StraightBevelDiffGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5626.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5626,
        )

        return self.__parent__._cast(
            _5626.StraightBevelDiffGearSetMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5628.StraightBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5628,
        )

        return self.__parent__._cast(_5628.StraightBevelGearMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5629.StraightBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5629,
        )

        return self.__parent__._cast(
            _5629.StraightBevelGearSetMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5630.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5630,
        )

        return self.__parent__._cast(
            _5630.StraightBevelPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5631.StraightBevelSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5631,
        )

        return self.__parent__._cast(
            _5631.StraightBevelSunGearMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5632.SynchroniserHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5632,
        )

        return self.__parent__._cast(_5632.SynchroniserHalfMultibodyDynamicsAnalysis)

    @property
    def synchroniser_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5633.SynchroniserMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5633,
        )

        return self.__parent__._cast(_5633.SynchroniserMultibodyDynamicsAnalysis)

    @property
    def synchroniser_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5634.SynchroniserPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5634,
        )

        return self.__parent__._cast(_5634.SynchroniserPartMultibodyDynamicsAnalysis)

    @property
    def synchroniser_sleeve_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5635.SynchroniserSleeveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5635,
        )

        return self.__parent__._cast(_5635.SynchroniserSleeveMultibodyDynamicsAnalysis)

    @property
    def torque_converter_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5638.TorqueConverterMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5638,
        )

        return self.__parent__._cast(_5638.TorqueConverterMultibodyDynamicsAnalysis)

    @property
    def torque_converter_pump_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5639.TorqueConverterPumpMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5639,
        )

        return self.__parent__._cast(_5639.TorqueConverterPumpMultibodyDynamicsAnalysis)

    @property
    def torque_converter_turbine_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5641.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5641,
        )

        return self.__parent__._cast(
            _5641.TorqueConverterTurbineMultibodyDynamicsAnalysis
        )

    @property
    def unbalanced_mass_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5642.UnbalancedMassMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5642,
        )

        return self.__parent__._cast(_5642.UnbalancedMassMultibodyDynamicsAnalysis)

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5643.VirtualComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5643,
        )

        return self.__parent__._cast(_5643.VirtualComponentMultibodyDynamicsAnalysis)

    @property
    def worm_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5646.WormGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5646,
        )

        return self.__parent__._cast(_5646.WormGearMultibodyDynamicsAnalysis)

    @property
    def worm_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5647.WormGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5647,
        )

        return self.__parent__._cast(_5647.WormGearSetMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5649.ZerolBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5649,
        )

        return self.__parent__._cast(_5649.ZerolBevelGearMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5650.ZerolBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5650,
        )

        return self.__parent__._cast(_5650.ZerolBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5809.AbstractAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5809,
        )

        return self.__parent__._cast(_5809.AbstractAssemblyHarmonicAnalysis)

    @property
    def abstract_shaft_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5811.AbstractShaftHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5811,
        )

        return self.__parent__._cast(_5811.AbstractShaftHarmonicAnalysis)

    @property
    def abstract_shaft_or_housing_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5812.AbstractShaftOrHousingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5812,
        )

        return self.__parent__._cast(_5812.AbstractShaftOrHousingHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5814.AGMAGleasonConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5814,
        )

        return self.__parent__._cast(_5814.AGMAGleasonConicalGearHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5816.AGMAGleasonConicalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5816,
        )

        return self.__parent__._cast(_5816.AGMAGleasonConicalGearSetHarmonicAnalysis)

    @property
    def assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5817.AssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5817,
        )

        return self.__parent__._cast(_5817.AssemblyHarmonicAnalysis)

    @property
    def bearing_harmonic_analysis(self: "CastSelf") -> "_5818.BearingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5818,
        )

        return self.__parent__._cast(_5818.BearingHarmonicAnalysis)

    @property
    def belt_drive_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5820.BeltDriveHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5820,
        )

        return self.__parent__._cast(_5820.BeltDriveHarmonicAnalysis)

    @property
    def bevel_differential_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5821.BevelDifferentialGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5821,
        )

        return self.__parent__._cast(_5821.BevelDifferentialGearHarmonicAnalysis)

    @property
    def bevel_differential_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5823.BevelDifferentialGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5823,
        )

        return self.__parent__._cast(_5823.BevelDifferentialGearSetHarmonicAnalysis)

    @property
    def bevel_differential_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5824.BevelDifferentialPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5824,
        )

        return self.__parent__._cast(_5824.BevelDifferentialPlanetGearHarmonicAnalysis)

    @property
    def bevel_differential_sun_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5825.BevelDifferentialSunGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5825,
        )

        return self.__parent__._cast(_5825.BevelDifferentialSunGearHarmonicAnalysis)

    @property
    def bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5826.BevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5826,
        )

        return self.__parent__._cast(_5826.BevelGearHarmonicAnalysis)

    @property
    def bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5828.BevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5828,
        )

        return self.__parent__._cast(_5828.BevelGearSetHarmonicAnalysis)

    @property
    def bolted_joint_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5829.BoltedJointHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5829,
        )

        return self.__parent__._cast(_5829.BoltedJointHarmonicAnalysis)

    @property
    def bolt_harmonic_analysis(self: "CastSelf") -> "_5830.BoltHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5830,
        )

        return self.__parent__._cast(_5830.BoltHarmonicAnalysis)

    @property
    def clutch_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5832.ClutchHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5832,
        )

        return self.__parent__._cast(_5832.ClutchHalfHarmonicAnalysis)

    @property
    def clutch_harmonic_analysis(self: "CastSelf") -> "_5833.ClutchHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5833,
        )

        return self.__parent__._cast(_5833.ClutchHarmonicAnalysis)

    @property
    def component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5836.ComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5836,
        )

        return self.__parent__._cast(_5836.ComponentHarmonicAnalysis)

    @property
    def concept_coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5838.ConceptCouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5838,
        )

        return self.__parent__._cast(_5838.ConceptCouplingHalfHarmonicAnalysis)

    @property
    def concept_coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5839.ConceptCouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5839,
        )

        return self.__parent__._cast(_5839.ConceptCouplingHarmonicAnalysis)

    @property
    def concept_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5840.ConceptGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5840,
        )

        return self.__parent__._cast(_5840.ConceptGearHarmonicAnalysis)

    @property
    def concept_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5842.ConceptGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5842,
        )

        return self.__parent__._cast(_5842.ConceptGearSetHarmonicAnalysis)

    @property
    def conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5843.ConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5843,
        )

        return self.__parent__._cast(_5843.ConicalGearHarmonicAnalysis)

    @property
    def conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5845.ConicalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5845,
        )

        return self.__parent__._cast(_5845.ConicalGearSetHarmonicAnalysis)

    @property
    def connector_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5847.ConnectorHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5847,
        )

        return self.__parent__._cast(_5847.ConnectorHarmonicAnalysis)

    @property
    def coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5849.CouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5849,
        )

        return self.__parent__._cast(_5849.CouplingHalfHarmonicAnalysis)

    @property
    def coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5850.CouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5850,
        )

        return self.__parent__._cast(_5850.CouplingHarmonicAnalysis)

    @property
    def cvt_harmonic_analysis(self: "CastSelf") -> "_5852.CVTHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5852,
        )

        return self.__parent__._cast(_5852.CVTHarmonicAnalysis)

    @property
    def cvt_pulley_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5853.CVTPulleyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5853,
        )

        return self.__parent__._cast(_5853.CVTPulleyHarmonicAnalysis)

    @property
    def cycloidal_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5854.CycloidalAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5854,
        )

        return self.__parent__._cast(_5854.CycloidalAssemblyHarmonicAnalysis)

    @property
    def cycloidal_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5856.CycloidalDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5856,
        )

        return self.__parent__._cast(_5856.CycloidalDiscHarmonicAnalysis)

    @property
    def cylindrical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5858.CylindricalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5858,
        )

        return self.__parent__._cast(_5858.CylindricalGearHarmonicAnalysis)

    @property
    def cylindrical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5860.CylindricalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5860,
        )

        return self.__parent__._cast(_5860.CylindricalGearSetHarmonicAnalysis)

    @property
    def cylindrical_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5861.CylindricalPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5861,
        )

        return self.__parent__._cast(_5861.CylindricalPlanetGearHarmonicAnalysis)

    @property
    def datum_harmonic_analysis(self: "CastSelf") -> "_5862.DatumHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5862,
        )

        return self.__parent__._cast(_5862.DatumHarmonicAnalysis)

    @property
    def external_cad_model_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5877.ExternalCADModelHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5877,
        )

        return self.__parent__._cast(_5877.ExternalCADModelHarmonicAnalysis)

    @property
    def face_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5878.FaceGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5878,
        )

        return self.__parent__._cast(_5878.FaceGearHarmonicAnalysis)

    @property
    def face_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5880.FaceGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5880,
        )

        return self.__parent__._cast(_5880.FaceGearSetHarmonicAnalysis)

    @property
    def fe_part_harmonic_analysis(self: "CastSelf") -> "_5881.FEPartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5881,
        )

        return self.__parent__._cast(_5881.FEPartHarmonicAnalysis)

    @property
    def flexible_pin_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5882.FlexiblePinAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5882,
        )

        return self.__parent__._cast(_5882.FlexiblePinAssemblyHarmonicAnalysis)

    @property
    def gear_harmonic_analysis(self: "CastSelf") -> "_5884.GearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5884,
        )

        return self.__parent__._cast(_5884.GearHarmonicAnalysis)

    @property
    def gear_set_harmonic_analysis(self: "CastSelf") -> "_5889.GearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5889,
        )

        return self.__parent__._cast(_5889.GearSetHarmonicAnalysis)

    @property
    def guide_dxf_model_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5891.GuideDxfModelHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5891,
        )

        return self.__parent__._cast(_5891.GuideDxfModelHarmonicAnalysis)

    @property
    def hypoid_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5902.HypoidGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5902,
        )

        return self.__parent__._cast(_5902.HypoidGearHarmonicAnalysis)

    @property
    def hypoid_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5904.HypoidGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5904,
        )

        return self.__parent__._cast(_5904.HypoidGearSetHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5906.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5906,
        )

        return self.__parent__._cast(
            _5906.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5908.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5908,
        )

        return self.__parent__._cast(
            _5908.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5909.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5909,
        )

        return self.__parent__._cast(
            _5909.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5911.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5911,
        )

        return self.__parent__._cast(
            _5911.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5912.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5912,
        )

        return self.__parent__._cast(
            _5912.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5914.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5914,
        )

        return self.__parent__._cast(
            _5914.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis
        )

    @property
    def mass_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5915.MassDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5915,
        )

        return self.__parent__._cast(_5915.MassDiscHarmonicAnalysis)

    @property
    def measurement_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5916.MeasurementComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5916,
        )

        return self.__parent__._cast(_5916.MeasurementComponentHarmonicAnalysis)

    @property
    def microphone_array_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5917.MicrophoneArrayHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5917,
        )

        return self.__parent__._cast(_5917.MicrophoneArrayHarmonicAnalysis)

    @property
    def microphone_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5918.MicrophoneHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5918,
        )

        return self.__parent__._cast(_5918.MicrophoneHarmonicAnalysis)

    @property
    def mountable_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5919.MountableComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5919,
        )

        return self.__parent__._cast(_5919.MountableComponentHarmonicAnalysis)

    @property
    def oil_seal_harmonic_analysis(self: "CastSelf") -> "_5920.OilSealHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5920,
        )

        return self.__parent__._cast(_5920.OilSealHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_5921.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5921,
        )

        return self.__parent__._cast(_5921.PartHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5923.PartToPartShearCouplingHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5923,
        )

        return self.__parent__._cast(_5923.PartToPartShearCouplingHalfHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5924.PartToPartShearCouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5924,
        )

        return self.__parent__._cast(_5924.PartToPartShearCouplingHarmonicAnalysis)

    @property
    def planetary_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5927.PlanetaryGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5927,
        )

        return self.__parent__._cast(_5927.PlanetaryGearSetHarmonicAnalysis)

    @property
    def planet_carrier_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5928.PlanetCarrierHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5928,
        )

        return self.__parent__._cast(_5928.PlanetCarrierHarmonicAnalysis)

    @property
    def point_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5929.PointLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5929,
        )

        return self.__parent__._cast(_5929.PointLoadHarmonicAnalysis)

    @property
    def power_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5930.PowerLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5930,
        )

        return self.__parent__._cast(_5930.PowerLoadHarmonicAnalysis)

    @property
    def pulley_harmonic_analysis(self: "CastSelf") -> "_5931.PulleyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5931,
        )

        return self.__parent__._cast(_5931.PulleyHarmonicAnalysis)

    @property
    def ring_pins_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5933.RingPinsHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5933,
        )

        return self.__parent__._cast(_5933.RingPinsHarmonicAnalysis)

    @property
    def rolling_ring_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5935.RollingRingAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5935,
        )

        return self.__parent__._cast(_5935.RollingRingAssemblyHarmonicAnalysis)

    @property
    def rolling_ring_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5937.RollingRingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5937,
        )

        return self.__parent__._cast(_5937.RollingRingHarmonicAnalysis)

    @property
    def root_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5938.RootAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5938,
        )

        return self.__parent__._cast(_5938.RootAssemblyHarmonicAnalysis)

    @property
    def shaft_harmonic_analysis(self: "CastSelf") -> "_5939.ShaftHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5939,
        )

        return self.__parent__._cast(_5939.ShaftHarmonicAnalysis)

    @property
    def shaft_hub_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5940.ShaftHubConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5940,
        )

        return self.__parent__._cast(_5940.ShaftHubConnectionHarmonicAnalysis)

    @property
    def specialised_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5943.SpecialisedAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5943,
        )

        return self.__parent__._cast(_5943.SpecialisedAssemblyHarmonicAnalysis)

    @property
    def spiral_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5945.SpiralBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5945,
        )

        return self.__parent__._cast(_5945.SpiralBevelGearHarmonicAnalysis)

    @property
    def spiral_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5947.SpiralBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5947,
        )

        return self.__parent__._cast(_5947.SpiralBevelGearSetHarmonicAnalysis)

    @property
    def spring_damper_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5949.SpringDamperHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5949,
        )

        return self.__parent__._cast(_5949.SpringDamperHalfHarmonicAnalysis)

    @property
    def spring_damper_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5950.SpringDamperHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5950,
        )

        return self.__parent__._cast(_5950.SpringDamperHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5952.StraightBevelDiffGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5952,
        )

        return self.__parent__._cast(_5952.StraightBevelDiffGearHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5954.StraightBevelDiffGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5954,
        )

        return self.__parent__._cast(_5954.StraightBevelDiffGearSetHarmonicAnalysis)

    @property
    def straight_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5955.StraightBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5955,
        )

        return self.__parent__._cast(_5955.StraightBevelGearHarmonicAnalysis)

    @property
    def straight_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5957.StraightBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5957,
        )

        return self.__parent__._cast(_5957.StraightBevelGearSetHarmonicAnalysis)

    @property
    def straight_bevel_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5958.StraightBevelPlanetGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5958,
        )

        return self.__parent__._cast(_5958.StraightBevelPlanetGearHarmonicAnalysis)

    @property
    def straight_bevel_sun_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5959.StraightBevelSunGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5959,
        )

        return self.__parent__._cast(_5959.StraightBevelSunGearHarmonicAnalysis)

    @property
    def synchroniser_half_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5960.SynchroniserHalfHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5960,
        )

        return self.__parent__._cast(_5960.SynchroniserHalfHarmonicAnalysis)

    @property
    def synchroniser_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5961.SynchroniserHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5961,
        )

        return self.__parent__._cast(_5961.SynchroniserHarmonicAnalysis)

    @property
    def synchroniser_part_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5962.SynchroniserPartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5962,
        )

        return self.__parent__._cast(_5962.SynchroniserPartHarmonicAnalysis)

    @property
    def synchroniser_sleeve_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5963.SynchroniserSleeveHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5963,
        )

        return self.__parent__._cast(_5963.SynchroniserSleeveHarmonicAnalysis)

    @property
    def torque_converter_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5965.TorqueConverterHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5965,
        )

        return self.__parent__._cast(_5965.TorqueConverterHarmonicAnalysis)

    @property
    def torque_converter_pump_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5966.TorqueConverterPumpHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5966,
        )

        return self.__parent__._cast(_5966.TorqueConverterPumpHarmonicAnalysis)

    @property
    def torque_converter_turbine_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5967.TorqueConverterTurbineHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5967,
        )

        return self.__parent__._cast(_5967.TorqueConverterTurbineHarmonicAnalysis)

    @property
    def unbalanced_mass_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5969.UnbalancedMassHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5969,
        )

        return self.__parent__._cast(_5969.UnbalancedMassHarmonicAnalysis)

    @property
    def virtual_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5970.VirtualComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5970,
        )

        return self.__parent__._cast(_5970.VirtualComponentHarmonicAnalysis)

    @property
    def worm_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5971.WormGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5971,
        )

        return self.__parent__._cast(_5971.WormGearHarmonicAnalysis)

    @property
    def worm_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5973.WormGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5973,
        )

        return self.__parent__._cast(_5973.WormGearSetHarmonicAnalysis)

    @property
    def zerol_bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5974.ZerolBevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5974,
        )

        return self.__parent__._cast(_5974.ZerolBevelGearHarmonicAnalysis)

    @property
    def zerol_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5976.ZerolBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5976,
        )

        return self.__parent__._cast(_5976.ZerolBevelGearSetHarmonicAnalysis)

    @property
    def abstract_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6143.AbstractAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6143,
        )

        return self.__parent__._cast(
            _6143.AbstractAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6144.AbstractShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6144,
        )

        return self.__parent__._cast(
            _6144.AbstractShaftHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_or_housing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6145.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6145,
        )

        return self.__parent__._cast(
            _6145.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6147.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6147,
        )

        return self.__parent__._cast(
            _6147.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6149.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6149,
        )

        return self.__parent__._cast(
            _6149.AGMAGleasonConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6150.AssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6150,
        )

        return self.__parent__._cast(_6150.AssemblyHarmonicAnalysisOfSingleExcitation)

    @property
    def bearing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6151.BearingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6151,
        )

        return self.__parent__._cast(_6151.BearingHarmonicAnalysisOfSingleExcitation)

    @property
    def belt_drive_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6153.BeltDriveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6153,
        )

        return self.__parent__._cast(_6153.BeltDriveHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_differential_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6154.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6154,
        )

        return self.__parent__._cast(
            _6154.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6156.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6156,
        )

        return self.__parent__._cast(
            _6156.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6157.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6157,
        )

        return self.__parent__._cast(
            _6157.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6158.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6158,
        )

        return self.__parent__._cast(
            _6158.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6159.BevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6159,
        )

        return self.__parent__._cast(_6159.BevelGearHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6161.BevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6161,
        )

        return self.__parent__._cast(
            _6161.BevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolted_joint_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6162.BoltedJointHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6162,
        )

        return self.__parent__._cast(
            _6162.BoltedJointHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6163.BoltHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6163,
        )

        return self.__parent__._cast(_6163.BoltHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6165.ClutchHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6165,
        )

        return self.__parent__._cast(_6165.ClutchHalfHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6166.ClutchHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6166,
        )

        return self.__parent__._cast(_6166.ClutchHarmonicAnalysisOfSingleExcitation)

    @property
    def component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6168.ComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6168,
        )

        return self.__parent__._cast(_6168.ComponentHarmonicAnalysisOfSingleExcitation)

    @property
    def concept_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6170.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6170,
        )

        return self.__parent__._cast(
            _6170.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6171.ConceptCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6171,
        )

        return self.__parent__._cast(
            _6171.ConceptCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6172.ConceptGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6172,
        )

        return self.__parent__._cast(
            _6172.ConceptGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6174.ConceptGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6174,
        )

        return self.__parent__._cast(
            _6174.ConceptGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6175.ConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6175,
        )

        return self.__parent__._cast(
            _6175.ConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6177.ConicalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6177,
        )

        return self.__parent__._cast(
            _6177.ConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connector_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6179.ConnectorHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6179,
        )

        return self.__parent__._cast(_6179.ConnectorHarmonicAnalysisOfSingleExcitation)

    @property
    def coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6181.CouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6181,
        )

        return self.__parent__._cast(
            _6181.CouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6182.CouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6182,
        )

        return self.__parent__._cast(_6182.CouplingHarmonicAnalysisOfSingleExcitation)

    @property
    def cvt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6184.CVTHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6184,
        )

        return self.__parent__._cast(_6184.CVTHarmonicAnalysisOfSingleExcitation)

    @property
    def cvt_pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6185.CVTPulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6185,
        )

        return self.__parent__._cast(_6185.CVTPulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def cycloidal_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6186.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6186,
        )

        return self.__parent__._cast(
            _6186.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6188.CycloidalDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6188,
        )

        return self.__parent__._cast(
            _6188.CycloidalDiscHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6190.CylindricalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6190,
        )

        return self.__parent__._cast(
            _6190.CylindricalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6192.CylindricalGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6192,
        )

        return self.__parent__._cast(
            _6192.CylindricalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6193.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6193,
        )

        return self.__parent__._cast(
            _6193.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def datum_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6194.DatumHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6194,
        )

        return self.__parent__._cast(_6194.DatumHarmonicAnalysisOfSingleExcitation)

    @property
    def external_cad_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6195.ExternalCADModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6195,
        )

        return self.__parent__._cast(
            _6195.ExternalCADModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6196.FaceGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6196,
        )

        return self.__parent__._cast(_6196.FaceGearHarmonicAnalysisOfSingleExcitation)

    @property
    def face_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6198.FaceGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6198,
        )

        return self.__parent__._cast(
            _6198.FaceGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def fe_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6199.FEPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6199,
        )

        return self.__parent__._cast(_6199.FEPartHarmonicAnalysisOfSingleExcitation)

    @property
    def flexible_pin_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6200.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6200,
        )

        return self.__parent__._cast(
            _6200.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6201.GearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6201,
        )

        return self.__parent__._cast(_6201.GearHarmonicAnalysisOfSingleExcitation)

    @property
    def gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6203.GearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6203,
        )

        return self.__parent__._cast(_6203.GearSetHarmonicAnalysisOfSingleExcitation)

    @property
    def guide_dxf_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6204.GuideDxfModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6204,
        )

        return self.__parent__._cast(
            _6204.GuideDxfModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6206.HypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6206,
        )

        return self.__parent__._cast(_6206.HypoidGearHarmonicAnalysisOfSingleExcitation)

    @property
    def hypoid_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6208.HypoidGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6208,
        )

        return self.__parent__._cast(
            _6208.HypoidGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6210.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6210,
        )

        return self.__parent__._cast(
            _6210.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6212.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6212,
        )

        return self.__parent__._cast(
            _6212.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6213.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6213,
        )

        return self.__parent__._cast(
            _6213.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6215.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6215,
        )

        return self.__parent__._cast(
            _6215.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6216.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6216,
        )

        return self.__parent__._cast(
            _6216.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6218.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6218,
        )

        return self.__parent__._cast(
            _6218.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mass_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6219.MassDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6219,
        )

        return self.__parent__._cast(_6219.MassDiscHarmonicAnalysisOfSingleExcitation)

    @property
    def measurement_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6220.MeasurementComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6220,
        )

        return self.__parent__._cast(
            _6220.MeasurementComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_array_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6221.MicrophoneArrayHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6221,
        )

        return self.__parent__._cast(
            _6221.MicrophoneArrayHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6222.MicrophoneHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6222,
        )

        return self.__parent__._cast(_6222.MicrophoneHarmonicAnalysisOfSingleExcitation)

    @property
    def mountable_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6224.MountableComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6224,
        )

        return self.__parent__._cast(
            _6224.MountableComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def oil_seal_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6225.OilSealHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6225,
        )

        return self.__parent__._cast(_6225.OilSealHarmonicAnalysisOfSingleExcitation)

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6226.PartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6226,
        )

        return self.__parent__._cast(_6226.PartHarmonicAnalysisOfSingleExcitation)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6228.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6228,
        )

        return self.__parent__._cast(
            _6228.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6229.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6229,
        )

        return self.__parent__._cast(
            _6229.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6231.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6231,
        )

        return self.__parent__._cast(
            _6231.PlanetaryGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planet_carrier_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6232.PlanetCarrierHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6232,
        )

        return self.__parent__._cast(
            _6232.PlanetCarrierHarmonicAnalysisOfSingleExcitation
        )

    @property
    def point_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6233.PointLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6233,
        )

        return self.__parent__._cast(_6233.PointLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def power_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6234.PowerLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6234,
        )

        return self.__parent__._cast(_6234.PowerLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6235.PulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6235,
        )

        return self.__parent__._cast(_6235.PulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def ring_pins_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6236.RingPinsHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6236,
        )

        return self.__parent__._cast(_6236.RingPinsHarmonicAnalysisOfSingleExcitation)

    @property
    def rolling_ring_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6238.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6238,
        )

        return self.__parent__._cast(
            _6238.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6240.RollingRingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6240,
        )

        return self.__parent__._cast(
            _6240.RollingRingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def root_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6241.RootAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6241,
        )

        return self.__parent__._cast(
            _6241.RootAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6242.ShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6242,
        )

        return self.__parent__._cast(_6242.ShaftHarmonicAnalysisOfSingleExcitation)

    @property
    def shaft_hub_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6243.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6243,
        )

        return self.__parent__._cast(
            _6243.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def specialised_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6245.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6245,
        )

        return self.__parent__._cast(
            _6245.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6246.SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6246,
        )

        return self.__parent__._cast(
            _6246.SpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6248.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6248,
        )

        return self.__parent__._cast(
            _6248.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6250.SpringDamperHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6250,
        )

        return self.__parent__._cast(
            _6250.SpringDamperHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6251.SpringDamperHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6251,
        )

        return self.__parent__._cast(
            _6251.SpringDamperHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6252.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6252,
        )

        return self.__parent__._cast(
            _6252.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6254.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6254,
        )

        return self.__parent__._cast(
            _6254.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6255.StraightBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6255,
        )

        return self.__parent__._cast(
            _6255.StraightBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6257.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6257,
        )

        return self.__parent__._cast(
            _6257.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6258.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6258,
        )

        return self.__parent__._cast(
            _6258.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6259.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6259,
        )

        return self.__parent__._cast(
            _6259.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6260.SynchroniserHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6260,
        )

        return self.__parent__._cast(
            _6260.SynchroniserHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6261.SynchroniserHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6261,
        )

        return self.__parent__._cast(
            _6261.SynchroniserHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6262.SynchroniserPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6262,
        )

        return self.__parent__._cast(
            _6262.SynchroniserPartHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_sleeve_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6263.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6263,
        )

        return self.__parent__._cast(
            _6263.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6265.TorqueConverterHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6265,
        )

        return self.__parent__._cast(
            _6265.TorqueConverterHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_pump_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6266.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6266,
        )

        return self.__parent__._cast(
            _6266.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_turbine_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6267.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6267,
        )

        return self.__parent__._cast(
            _6267.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation
        )

    @property
    def unbalanced_mass_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6268.UnbalancedMassHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6268,
        )

        return self.__parent__._cast(
            _6268.UnbalancedMassHarmonicAnalysisOfSingleExcitation
        )

    @property
    def virtual_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6269.VirtualComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6269,
        )

        return self.__parent__._cast(
            _6269.VirtualComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6270.WormGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6270,
        )

        return self.__parent__._cast(_6270.WormGearHarmonicAnalysisOfSingleExcitation)

    @property
    def worm_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6272.WormGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6272,
        )

        return self.__parent__._cast(
            _6272.WormGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6273.ZerolBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6273,
        )

        return self.__parent__._cast(
            _6273.ZerolBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_set_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6275.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6275,
        )

        return self.__parent__._cast(
            _6275.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6416.AbstractAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6416,
        )

        return self.__parent__._cast(_6416.AbstractAssemblyDynamicAnalysis)

    @property
    def abstract_shaft_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6417.AbstractShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6417,
        )

        return self.__parent__._cast(_6417.AbstractShaftDynamicAnalysis)

    @property
    def abstract_shaft_or_housing_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6418.AbstractShaftOrHousingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6418,
        )

        return self.__parent__._cast(_6418.AbstractShaftOrHousingDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6420.AGMAGleasonConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6420,
        )

        return self.__parent__._cast(_6420.AGMAGleasonConicalGearDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6422.AGMAGleasonConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6422,
        )

        return self.__parent__._cast(_6422.AGMAGleasonConicalGearSetDynamicAnalysis)

    @property
    def assembly_dynamic_analysis(self: "CastSelf") -> "_6423.AssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6423,
        )

        return self.__parent__._cast(_6423.AssemblyDynamicAnalysis)

    @property
    def bearing_dynamic_analysis(self: "CastSelf") -> "_6424.BearingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6424,
        )

        return self.__parent__._cast(_6424.BearingDynamicAnalysis)

    @property
    def belt_drive_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6426.BeltDriveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6426,
        )

        return self.__parent__._cast(_6426.BeltDriveDynamicAnalysis)

    @property
    def bevel_differential_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6427.BevelDifferentialGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6427,
        )

        return self.__parent__._cast(_6427.BevelDifferentialGearDynamicAnalysis)

    @property
    def bevel_differential_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6429.BevelDifferentialGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6429,
        )

        return self.__parent__._cast(_6429.BevelDifferentialGearSetDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6430.BevelDifferentialPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6430,
        )

        return self.__parent__._cast(_6430.BevelDifferentialPlanetGearDynamicAnalysis)

    @property
    def bevel_differential_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6431.BevelDifferentialSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6431,
        )

        return self.__parent__._cast(_6431.BevelDifferentialSunGearDynamicAnalysis)

    @property
    def bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6432.BevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6432,
        )

        return self.__parent__._cast(_6432.BevelGearDynamicAnalysis)

    @property
    def bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6434.BevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6434,
        )

        return self.__parent__._cast(_6434.BevelGearSetDynamicAnalysis)

    @property
    def bolt_dynamic_analysis(self: "CastSelf") -> "_6435.BoltDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6435,
        )

        return self.__parent__._cast(_6435.BoltDynamicAnalysis)

    @property
    def bolted_joint_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6436.BoltedJointDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6436,
        )

        return self.__parent__._cast(_6436.BoltedJointDynamicAnalysis)

    @property
    def clutch_dynamic_analysis(self: "CastSelf") -> "_6438.ClutchDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6438,
        )

        return self.__parent__._cast(_6438.ClutchDynamicAnalysis)

    @property
    def clutch_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6439.ClutchHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6439,
        )

        return self.__parent__._cast(_6439.ClutchHalfDynamicAnalysis)

    @property
    def component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6441.ComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6441,
        )

        return self.__parent__._cast(_6441.ComponentDynamicAnalysis)

    @property
    def concept_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6443.ConceptCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6443,
        )

        return self.__parent__._cast(_6443.ConceptCouplingDynamicAnalysis)

    @property
    def concept_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6444.ConceptCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6444,
        )

        return self.__parent__._cast(_6444.ConceptCouplingHalfDynamicAnalysis)

    @property
    def concept_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6445.ConceptGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6445,
        )

        return self.__parent__._cast(_6445.ConceptGearDynamicAnalysis)

    @property
    def concept_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6447.ConceptGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6447,
        )

        return self.__parent__._cast(_6447.ConceptGearSetDynamicAnalysis)

    @property
    def conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6448.ConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6448,
        )

        return self.__parent__._cast(_6448.ConicalGearDynamicAnalysis)

    @property
    def conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6450.ConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6450,
        )

        return self.__parent__._cast(_6450.ConicalGearSetDynamicAnalysis)

    @property
    def connector_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6452.ConnectorDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6452,
        )

        return self.__parent__._cast(_6452.ConnectorDynamicAnalysis)

    @property
    def coupling_dynamic_analysis(self: "CastSelf") -> "_6454.CouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6454,
        )

        return self.__parent__._cast(_6454.CouplingDynamicAnalysis)

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6455.CouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6455,
        )

        return self.__parent__._cast(_6455.CouplingHalfDynamicAnalysis)

    @property
    def cvt_dynamic_analysis(self: "CastSelf") -> "_6457.CVTDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6457,
        )

        return self.__parent__._cast(_6457.CVTDynamicAnalysis)

    @property
    def cvt_pulley_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6458.CVTPulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6458,
        )

        return self.__parent__._cast(_6458.CVTPulleyDynamicAnalysis)

    @property
    def cycloidal_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6459.CycloidalAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6459,
        )

        return self.__parent__._cast(_6459.CycloidalAssemblyDynamicAnalysis)

    @property
    def cycloidal_disc_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6461.CycloidalDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6461,
        )

        return self.__parent__._cast(_6461.CycloidalDiscDynamicAnalysis)

    @property
    def cylindrical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6463.CylindricalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6463,
        )

        return self.__parent__._cast(_6463.CylindricalGearDynamicAnalysis)

    @property
    def cylindrical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6465.CylindricalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6465,
        )

        return self.__parent__._cast(_6465.CylindricalGearSetDynamicAnalysis)

    @property
    def cylindrical_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6466.CylindricalPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6466,
        )

        return self.__parent__._cast(_6466.CylindricalPlanetGearDynamicAnalysis)

    @property
    def datum_dynamic_analysis(self: "CastSelf") -> "_6467.DatumDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6467,
        )

        return self.__parent__._cast(_6467.DatumDynamicAnalysis)

    @property
    def external_cad_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6470.ExternalCADModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6470,
        )

        return self.__parent__._cast(_6470.ExternalCADModelDynamicAnalysis)

    @property
    def face_gear_dynamic_analysis(self: "CastSelf") -> "_6471.FaceGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6471,
        )

        return self.__parent__._cast(_6471.FaceGearDynamicAnalysis)

    @property
    def face_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6473.FaceGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6473,
        )

        return self.__parent__._cast(_6473.FaceGearSetDynamicAnalysis)

    @property
    def fe_part_dynamic_analysis(self: "CastSelf") -> "_6474.FEPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6474,
        )

        return self.__parent__._cast(_6474.FEPartDynamicAnalysis)

    @property
    def flexible_pin_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6475.FlexiblePinAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6475,
        )

        return self.__parent__._cast(_6475.FlexiblePinAssemblyDynamicAnalysis)

    @property
    def gear_dynamic_analysis(self: "CastSelf") -> "_6476.GearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6476,
        )

        return self.__parent__._cast(_6476.GearDynamicAnalysis)

    @property
    def gear_set_dynamic_analysis(self: "CastSelf") -> "_6478.GearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6478,
        )

        return self.__parent__._cast(_6478.GearSetDynamicAnalysis)

    @property
    def guide_dxf_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6479.GuideDxfModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6479,
        )

        return self.__parent__._cast(_6479.GuideDxfModelDynamicAnalysis)

    @property
    def hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6480.HypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6480,
        )

        return self.__parent__._cast(_6480.HypoidGearDynamicAnalysis)

    @property
    def hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6482.HypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6482,
        )

        return self.__parent__._cast(_6482.HypoidGearSetDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6484.KlingelnbergCycloPalloidConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6484,
        )

        return self.__parent__._cast(
            _6484.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6486.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6486,
        )

        return self.__parent__._cast(
            _6486.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6487.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6487,
        )

        return self.__parent__._cast(
            _6487.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6489.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6489,
        )

        return self.__parent__._cast(
            _6489.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6490.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6490,
        )

        return self.__parent__._cast(
            _6490.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6492.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6492,
        )

        return self.__parent__._cast(
            _6492.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        )

    @property
    def mass_disc_dynamic_analysis(self: "CastSelf") -> "_6493.MassDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6493,
        )

        return self.__parent__._cast(_6493.MassDiscDynamicAnalysis)

    @property
    def measurement_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6494.MeasurementComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6494,
        )

        return self.__parent__._cast(_6494.MeasurementComponentDynamicAnalysis)

    @property
    def microphone_array_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6495.MicrophoneArrayDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6495,
        )

        return self.__parent__._cast(_6495.MicrophoneArrayDynamicAnalysis)

    @property
    def microphone_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6496.MicrophoneDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6496,
        )

        return self.__parent__._cast(_6496.MicrophoneDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6497.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6497,
        )

        return self.__parent__._cast(_6497.MountableComponentDynamicAnalysis)

    @property
    def oil_seal_dynamic_analysis(self: "CastSelf") -> "_6498.OilSealDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6498,
        )

        return self.__parent__._cast(_6498.OilSealDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6499.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6499,
        )

        return self.__parent__._cast(_6499.PartDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6501.PartToPartShearCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6501,
        )

        return self.__parent__._cast(_6501.PartToPartShearCouplingDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6502.PartToPartShearCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6502,
        )

        return self.__parent__._cast(_6502.PartToPartShearCouplingHalfDynamicAnalysis)

    @property
    def planetary_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6504.PlanetaryGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6504,
        )

        return self.__parent__._cast(_6504.PlanetaryGearSetDynamicAnalysis)

    @property
    def planet_carrier_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6505.PlanetCarrierDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6505,
        )

        return self.__parent__._cast(_6505.PlanetCarrierDynamicAnalysis)

    @property
    def point_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6506.PointLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6506,
        )

        return self.__parent__._cast(_6506.PointLoadDynamicAnalysis)

    @property
    def power_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6507.PowerLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6507,
        )

        return self.__parent__._cast(_6507.PowerLoadDynamicAnalysis)

    @property
    def pulley_dynamic_analysis(self: "CastSelf") -> "_6508.PulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6508,
        )

        return self.__parent__._cast(_6508.PulleyDynamicAnalysis)

    @property
    def ring_pins_dynamic_analysis(self: "CastSelf") -> "_6509.RingPinsDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6509,
        )

        return self.__parent__._cast(_6509.RingPinsDynamicAnalysis)

    @property
    def rolling_ring_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6511.RollingRingAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6511,
        )

        return self.__parent__._cast(_6511.RollingRingAssemblyDynamicAnalysis)

    @property
    def rolling_ring_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6513.RollingRingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6513,
        )

        return self.__parent__._cast(_6513.RollingRingDynamicAnalysis)

    @property
    def root_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6514.RootAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6514,
        )

        return self.__parent__._cast(_6514.RootAssemblyDynamicAnalysis)

    @property
    def shaft_dynamic_analysis(self: "CastSelf") -> "_6515.ShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6515,
        )

        return self.__parent__._cast(_6515.ShaftDynamicAnalysis)

    @property
    def shaft_hub_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6516.ShaftHubConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6516,
        )

        return self.__parent__._cast(_6516.ShaftHubConnectionDynamicAnalysis)

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6518.SpecialisedAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6518,
        )

        return self.__parent__._cast(_6518.SpecialisedAssemblyDynamicAnalysis)

    @property
    def spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6519.SpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6519,
        )

        return self.__parent__._cast(_6519.SpiralBevelGearDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6521.SpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6521,
        )

        return self.__parent__._cast(_6521.SpiralBevelGearSetDynamicAnalysis)

    @property
    def spring_damper_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6523.SpringDamperDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6523,
        )

        return self.__parent__._cast(_6523.SpringDamperDynamicAnalysis)

    @property
    def spring_damper_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6524.SpringDamperHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6524,
        )

        return self.__parent__._cast(_6524.SpringDamperHalfDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6525.StraightBevelDiffGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6525,
        )

        return self.__parent__._cast(_6525.StraightBevelDiffGearDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6527.StraightBevelDiffGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6527,
        )

        return self.__parent__._cast(_6527.StraightBevelDiffGearSetDynamicAnalysis)

    @property
    def straight_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6528.StraightBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6528,
        )

        return self.__parent__._cast(_6528.StraightBevelGearDynamicAnalysis)

    @property
    def straight_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6530.StraightBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6530,
        )

        return self.__parent__._cast(_6530.StraightBevelGearSetDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6531.StraightBevelPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6531,
        )

        return self.__parent__._cast(_6531.StraightBevelPlanetGearDynamicAnalysis)

    @property
    def straight_bevel_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6532.StraightBevelSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6532,
        )

        return self.__parent__._cast(_6532.StraightBevelSunGearDynamicAnalysis)

    @property
    def synchroniser_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6533.SynchroniserDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6533,
        )

        return self.__parent__._cast(_6533.SynchroniserDynamicAnalysis)

    @property
    def synchroniser_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6534.SynchroniserHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6534,
        )

        return self.__parent__._cast(_6534.SynchroniserHalfDynamicAnalysis)

    @property
    def synchroniser_part_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6535.SynchroniserPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6535,
        )

        return self.__parent__._cast(_6535.SynchroniserPartDynamicAnalysis)

    @property
    def synchroniser_sleeve_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6536.SynchroniserSleeveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6536,
        )

        return self.__parent__._cast(_6536.SynchroniserSleeveDynamicAnalysis)

    @property
    def torque_converter_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6538.TorqueConverterDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6538,
        )

        return self.__parent__._cast(_6538.TorqueConverterDynamicAnalysis)

    @property
    def torque_converter_pump_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6539.TorqueConverterPumpDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6539,
        )

        return self.__parent__._cast(_6539.TorqueConverterPumpDynamicAnalysis)

    @property
    def torque_converter_turbine_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6540.TorqueConverterTurbineDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6540,
        )

        return self.__parent__._cast(_6540.TorqueConverterTurbineDynamicAnalysis)

    @property
    def unbalanced_mass_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6541.UnbalancedMassDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6541,
        )

        return self.__parent__._cast(_6541.UnbalancedMassDynamicAnalysis)

    @property
    def virtual_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6542.VirtualComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6542,
        )

        return self.__parent__._cast(_6542.VirtualComponentDynamicAnalysis)

    @property
    def worm_gear_dynamic_analysis(self: "CastSelf") -> "_6543.WormGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6543,
        )

        return self.__parent__._cast(_6543.WormGearDynamicAnalysis)

    @property
    def worm_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6545.WormGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6545,
        )

        return self.__parent__._cast(_6545.WormGearSetDynamicAnalysis)

    @property
    def zerol_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6546.ZerolBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6546,
        )

        return self.__parent__._cast(_6546.ZerolBevelGearDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6548.ZerolBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6548,
        )

        return self.__parent__._cast(_6548.ZerolBevelGearSetDynamicAnalysis)

    @property
    def abstract_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6686.AbstractAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6686,
        )

        return self.__parent__._cast(_6686.AbstractAssemblyCriticalSpeedAnalysis)

    @property
    def abstract_shaft_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6687.AbstractShaftCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6687,
        )

        return self.__parent__._cast(_6687.AbstractShaftCriticalSpeedAnalysis)

    @property
    def abstract_shaft_or_housing_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6688.AbstractShaftOrHousingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6688,
        )

        return self.__parent__._cast(_6688.AbstractShaftOrHousingCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6690.AGMAGleasonConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6690,
        )

        return self.__parent__._cast(_6690.AGMAGleasonConicalGearCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6692.AGMAGleasonConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6692,
        )

        return self.__parent__._cast(
            _6692.AGMAGleasonConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6693.AssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6693,
        )

        return self.__parent__._cast(_6693.AssemblyCriticalSpeedAnalysis)

    @property
    def bearing_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6694.BearingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6694,
        )

        return self.__parent__._cast(_6694.BearingCriticalSpeedAnalysis)

    @property
    def belt_drive_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6696.BeltDriveCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6696,
        )

        return self.__parent__._cast(_6696.BeltDriveCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6697.BevelDifferentialGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6697,
        )

        return self.__parent__._cast(_6697.BevelDifferentialGearCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6699.BevelDifferentialGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6699,
        )

        return self.__parent__._cast(
            _6699.BevelDifferentialGearSetCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_planet_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6700.BevelDifferentialPlanetGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6700,
        )

        return self.__parent__._cast(
            _6700.BevelDifferentialPlanetGearCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_sun_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6701.BevelDifferentialSunGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6701,
        )

        return self.__parent__._cast(
            _6701.BevelDifferentialSunGearCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6702.BevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6702,
        )

        return self.__parent__._cast(_6702.BevelGearCriticalSpeedAnalysis)

    @property
    def bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6704.BevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6704,
        )

        return self.__parent__._cast(_6704.BevelGearSetCriticalSpeedAnalysis)

    @property
    def bolt_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6705.BoltCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6705,
        )

        return self.__parent__._cast(_6705.BoltCriticalSpeedAnalysis)

    @property
    def bolted_joint_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6706.BoltedJointCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6706,
        )

        return self.__parent__._cast(_6706.BoltedJointCriticalSpeedAnalysis)

    @property
    def clutch_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6708.ClutchCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6708,
        )

        return self.__parent__._cast(_6708.ClutchCriticalSpeedAnalysis)

    @property
    def clutch_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6709.ClutchHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6709,
        )

        return self.__parent__._cast(_6709.ClutchHalfCriticalSpeedAnalysis)

    @property
    def component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6711.ComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6711,
        )

        return self.__parent__._cast(_6711.ComponentCriticalSpeedAnalysis)

    @property
    def concept_coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6713.ConceptCouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6713,
        )

        return self.__parent__._cast(_6713.ConceptCouplingCriticalSpeedAnalysis)

    @property
    def concept_coupling_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6714.ConceptCouplingHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6714,
        )

        return self.__parent__._cast(_6714.ConceptCouplingHalfCriticalSpeedAnalysis)

    @property
    def concept_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6715.ConceptGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6715,
        )

        return self.__parent__._cast(_6715.ConceptGearCriticalSpeedAnalysis)

    @property
    def concept_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6717.ConceptGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6717,
        )

        return self.__parent__._cast(_6717.ConceptGearSetCriticalSpeedAnalysis)

    @property
    def conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6718.ConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6718,
        )

        return self.__parent__._cast(_6718.ConicalGearCriticalSpeedAnalysis)

    @property
    def conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6720.ConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6720,
        )

        return self.__parent__._cast(_6720.ConicalGearSetCriticalSpeedAnalysis)

    @property
    def connector_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6722.ConnectorCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6722,
        )

        return self.__parent__._cast(_6722.ConnectorCriticalSpeedAnalysis)

    @property
    def coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6724.CouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6724,
        )

        return self.__parent__._cast(_6724.CouplingCriticalSpeedAnalysis)

    @property
    def coupling_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6725.CouplingHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6725,
        )

        return self.__parent__._cast(_6725.CouplingHalfCriticalSpeedAnalysis)

    @property
    def cvt_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6730.CVTCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6730,
        )

        return self.__parent__._cast(_6730.CVTCriticalSpeedAnalysis)

    @property
    def cvt_pulley_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6731.CVTPulleyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6731,
        )

        return self.__parent__._cast(_6731.CVTPulleyCriticalSpeedAnalysis)

    @property
    def cycloidal_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6732.CycloidalAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6732,
        )

        return self.__parent__._cast(_6732.CycloidalAssemblyCriticalSpeedAnalysis)

    @property
    def cycloidal_disc_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6734.CycloidalDiscCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6734,
        )

        return self.__parent__._cast(_6734.CycloidalDiscCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6736.CylindricalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6736,
        )

        return self.__parent__._cast(_6736.CylindricalGearCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6738.CylindricalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6738,
        )

        return self.__parent__._cast(_6738.CylindricalGearSetCriticalSpeedAnalysis)

    @property
    def cylindrical_planet_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6739.CylindricalPlanetGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6739,
        )

        return self.__parent__._cast(_6739.CylindricalPlanetGearCriticalSpeedAnalysis)

    @property
    def datum_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6740.DatumCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6740,
        )

        return self.__parent__._cast(_6740.DatumCriticalSpeedAnalysis)

    @property
    def external_cad_model_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6741.ExternalCADModelCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6741,
        )

        return self.__parent__._cast(_6741.ExternalCADModelCriticalSpeedAnalysis)

    @property
    def face_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6742.FaceGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6742,
        )

        return self.__parent__._cast(_6742.FaceGearCriticalSpeedAnalysis)

    @property
    def face_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6744.FaceGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6744,
        )

        return self.__parent__._cast(_6744.FaceGearSetCriticalSpeedAnalysis)

    @property
    def fe_part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6745.FEPartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6745,
        )

        return self.__parent__._cast(_6745.FEPartCriticalSpeedAnalysis)

    @property
    def flexible_pin_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6746.FlexiblePinAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6746,
        )

        return self.__parent__._cast(_6746.FlexiblePinAssemblyCriticalSpeedAnalysis)

    @property
    def gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6747.GearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6747,
        )

        return self.__parent__._cast(_6747.GearCriticalSpeedAnalysis)

    @property
    def gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6749.GearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6749,
        )

        return self.__parent__._cast(_6749.GearSetCriticalSpeedAnalysis)

    @property
    def guide_dxf_model_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6750.GuideDxfModelCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6750,
        )

        return self.__parent__._cast(_6750.GuideDxfModelCriticalSpeedAnalysis)

    @property
    def hypoid_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6751.HypoidGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6751,
        )

        return self.__parent__._cast(_6751.HypoidGearCriticalSpeedAnalysis)

    @property
    def hypoid_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6753.HypoidGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6753,
        )

        return self.__parent__._cast(_6753.HypoidGearSetCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6755.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6755,
        )

        return self.__parent__._cast(
            _6755.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6757.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6757,
        )

        return self.__parent__._cast(
            _6757.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6758.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6758,
        )

        return self.__parent__._cast(
            _6758.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6760.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6760,
        )

        return self.__parent__._cast(
            _6760.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6761.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6761,
        )

        return self.__parent__._cast(
            _6761.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6763.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6763,
        )

        return self.__parent__._cast(
            _6763.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis
        )

    @property
    def mass_disc_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6764.MassDiscCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6764,
        )

        return self.__parent__._cast(_6764.MassDiscCriticalSpeedAnalysis)

    @property
    def measurement_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6765.MeasurementComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6765,
        )

        return self.__parent__._cast(_6765.MeasurementComponentCriticalSpeedAnalysis)

    @property
    def microphone_array_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6766.MicrophoneArrayCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6766,
        )

        return self.__parent__._cast(_6766.MicrophoneArrayCriticalSpeedAnalysis)

    @property
    def microphone_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6767.MicrophoneCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6767,
        )

        return self.__parent__._cast(_6767.MicrophoneCriticalSpeedAnalysis)

    @property
    def mountable_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6768.MountableComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6768,
        )

        return self.__parent__._cast(_6768.MountableComponentCriticalSpeedAnalysis)

    @property
    def oil_seal_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6769.OilSealCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6769,
        )

        return self.__parent__._cast(_6769.OilSealCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6770.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6770,
        )

        return self.__parent__._cast(_6770.PartCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6772.PartToPartShearCouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6772,
        )

        return self.__parent__._cast(_6772.PartToPartShearCouplingCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6773.PartToPartShearCouplingHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6773,
        )

        return self.__parent__._cast(
            _6773.PartToPartShearCouplingHalfCriticalSpeedAnalysis
        )

    @property
    def planetary_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6775.PlanetaryGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6775,
        )

        return self.__parent__._cast(_6775.PlanetaryGearSetCriticalSpeedAnalysis)

    @property
    def planet_carrier_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6776.PlanetCarrierCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6776,
        )

        return self.__parent__._cast(_6776.PlanetCarrierCriticalSpeedAnalysis)

    @property
    def point_load_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6777.PointLoadCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6777,
        )

        return self.__parent__._cast(_6777.PointLoadCriticalSpeedAnalysis)

    @property
    def power_load_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6778.PowerLoadCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6778,
        )

        return self.__parent__._cast(_6778.PowerLoadCriticalSpeedAnalysis)

    @property
    def pulley_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6779.PulleyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6779,
        )

        return self.__parent__._cast(_6779.PulleyCriticalSpeedAnalysis)

    @property
    def ring_pins_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6780.RingPinsCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6780,
        )

        return self.__parent__._cast(_6780.RingPinsCriticalSpeedAnalysis)

    @property
    def rolling_ring_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6782.RollingRingAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6782,
        )

        return self.__parent__._cast(_6782.RollingRingAssemblyCriticalSpeedAnalysis)

    @property
    def rolling_ring_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6784.RollingRingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6784,
        )

        return self.__parent__._cast(_6784.RollingRingCriticalSpeedAnalysis)

    @property
    def root_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6785.RootAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6785,
        )

        return self.__parent__._cast(_6785.RootAssemblyCriticalSpeedAnalysis)

    @property
    def shaft_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6786.ShaftCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6786,
        )

        return self.__parent__._cast(_6786.ShaftCriticalSpeedAnalysis)

    @property
    def shaft_hub_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6787.ShaftHubConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6787,
        )

        return self.__parent__._cast(_6787.ShaftHubConnectionCriticalSpeedAnalysis)

    @property
    def specialised_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6789.SpecialisedAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6789,
        )

        return self.__parent__._cast(_6789.SpecialisedAssemblyCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6790.SpiralBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6790,
        )

        return self.__parent__._cast(_6790.SpiralBevelGearCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6792.SpiralBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6792,
        )

        return self.__parent__._cast(_6792.SpiralBevelGearSetCriticalSpeedAnalysis)

    @property
    def spring_damper_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6794.SpringDamperCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6794,
        )

        return self.__parent__._cast(_6794.SpringDamperCriticalSpeedAnalysis)

    @property
    def spring_damper_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6795.SpringDamperHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6795,
        )

        return self.__parent__._cast(_6795.SpringDamperHalfCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6796.StraightBevelDiffGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6796,
        )

        return self.__parent__._cast(_6796.StraightBevelDiffGearCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6798.StraightBevelDiffGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6798,
        )

        return self.__parent__._cast(
            _6798.StraightBevelDiffGearSetCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6799.StraightBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6799,
        )

        return self.__parent__._cast(_6799.StraightBevelGearCriticalSpeedAnalysis)

    @property
    def straight_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6801.StraightBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6801,
        )

        return self.__parent__._cast(_6801.StraightBevelGearSetCriticalSpeedAnalysis)

    @property
    def straight_bevel_planet_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6802.StraightBevelPlanetGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6802,
        )

        return self.__parent__._cast(_6802.StraightBevelPlanetGearCriticalSpeedAnalysis)

    @property
    def straight_bevel_sun_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6803.StraightBevelSunGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6803,
        )

        return self.__parent__._cast(_6803.StraightBevelSunGearCriticalSpeedAnalysis)

    @property
    def synchroniser_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6804.SynchroniserCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6804,
        )

        return self.__parent__._cast(_6804.SynchroniserCriticalSpeedAnalysis)

    @property
    def synchroniser_half_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6805.SynchroniserHalfCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6805,
        )

        return self.__parent__._cast(_6805.SynchroniserHalfCriticalSpeedAnalysis)

    @property
    def synchroniser_part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6806.SynchroniserPartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6806,
        )

        return self.__parent__._cast(_6806.SynchroniserPartCriticalSpeedAnalysis)

    @property
    def synchroniser_sleeve_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6807.SynchroniserSleeveCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6807,
        )

        return self.__parent__._cast(_6807.SynchroniserSleeveCriticalSpeedAnalysis)

    @property
    def torque_converter_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6809.TorqueConverterCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6809,
        )

        return self.__parent__._cast(_6809.TorqueConverterCriticalSpeedAnalysis)

    @property
    def torque_converter_pump_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6810.TorqueConverterPumpCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6810,
        )

        return self.__parent__._cast(_6810.TorqueConverterPumpCriticalSpeedAnalysis)

    @property
    def torque_converter_turbine_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6811.TorqueConverterTurbineCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6811,
        )

        return self.__parent__._cast(_6811.TorqueConverterTurbineCriticalSpeedAnalysis)

    @property
    def unbalanced_mass_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6812.UnbalancedMassCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6812,
        )

        return self.__parent__._cast(_6812.UnbalancedMassCriticalSpeedAnalysis)

    @property
    def virtual_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6813.VirtualComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6813,
        )

        return self.__parent__._cast(_6813.VirtualComponentCriticalSpeedAnalysis)

    @property
    def worm_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6814.WormGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6814,
        )

        return self.__parent__._cast(_6814.WormGearCriticalSpeedAnalysis)

    @property
    def worm_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6816.WormGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6816,
        )

        return self.__parent__._cast(_6816.WormGearSetCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6817.ZerolBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6817,
        )

        return self.__parent__._cast(_6817.ZerolBevelGearCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6819.ZerolBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6819,
        )

        return self.__parent__._cast(_6819.ZerolBevelGearSetCriticalSpeedAnalysis)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6954.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6954,
        )

        return self.__parent__._cast(_6954.AbstractAssemblyLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_6955.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6955,
        )

        return self.__parent__._cast(_6955.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_6956.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6956,
        )

        return self.__parent__._cast(_6956.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6961.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6961,
        )

        return self.__parent__._cast(_6961.AGMAGleasonConicalGearLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6963.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6963,
        )

        return self.__parent__._cast(_6963.AGMAGleasonConicalGearSetLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "_6966.AssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6966,
        )

        return self.__parent__._cast(_6966.AssemblyLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_6967.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6967,
        )

        return self.__parent__._cast(_6967.BearingLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_6969.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6969,
        )

        return self.__parent__._cast(_6969.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6970.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6970,
        )

        return self.__parent__._cast(_6970.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6972.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6972,
        )

        return self.__parent__._cast(_6972.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_6973.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_6974.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6974,
        )

        return self.__parent__._cast(_6974.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_6975.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6975,
        )

        return self.__parent__._cast(_6975.BevelGearLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_6977.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6977,
        )

        return self.__parent__._cast(_6977.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_6978.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6978,
        )

        return self.__parent__._cast(_6978.BoltedJointLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_6979.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6979,
        )

        return self.__parent__._cast(_6979.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_6981.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6981,
        )

        return self.__parent__._cast(_6981.ClutchHalfLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_6982.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6982,
        )

        return self.__parent__._cast(_6982.ClutchLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6985.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6985,
        )

        return self.__parent__._cast(_6985.ComponentLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6987.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.ConceptCouplingHalfLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6988.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6988,
        )

        return self.__parent__._cast(_6988.ConceptCouplingLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6989.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6989,
        )

        return self.__parent__._cast(_6989.ConceptGearLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_6991.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6991,
        )

        return self.__parent__._cast(_6991.ConceptGearSetLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6992.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConicalGearLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_6996.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6996,
        )

        return self.__parent__._cast(_6996.ConicalGearSetLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_6998.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6998,
        )

        return self.__parent__._cast(_6998.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7000.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7000,
        )

        return self.__parent__._cast(_7000.CouplingHalfLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7001.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7001,
        )

        return self.__parent__._cast(_7001.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7003.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7003,
        )

        return self.__parent__._cast(_7003.CVTLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7004.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7004,
        )

        return self.__parent__._cast(_7004.CVTPulleyLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7005.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7005,
        )

        return self.__parent__._cast(_7005.CycloidalAssemblyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7007.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7009.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7009,
        )

        return self.__parent__._cast(_7009.CylindricalGearLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7013.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7013,
        )

        return self.__parent__._cast(_7013.CylindricalGearSetLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7014.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7014,
        )

        return self.__parent__._cast(_7014.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7017.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7017,
        )

        return self.__parent__._cast(_7017.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7031.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7031,
        )

        return self.__parent__._cast(_7031.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7032.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7032,
        )

        return self.__parent__._cast(_7032.FaceGearLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7034.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7034,
        )

        return self.__parent__._cast(_7034.FaceGearSetLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7035.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7035,
        )

        return self.__parent__._cast(_7035.FEPartLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7036.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7036,
        )

        return self.__parent__._cast(_7036.FlexiblePinAssemblyLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7038.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.GearLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7043.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearSetLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7044.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7044,
        )

        return self.__parent__._cast(_7044.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7053.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7053,
        )

        return self.__parent__._cast(_7053.HypoidGearLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7055.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7055,
        )

        return self.__parent__._cast(_7055.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7060.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7060,
        )

        return self.__parent__._cast(_7060.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7062.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7062,
        )

        return self.__parent__._cast(
            _7062.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7063.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7063,
        )

        return self.__parent__._cast(_7063.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7065.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7065,
        )

        return self.__parent__._cast(
            _7065.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(
            _7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7068.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7068,
        )

        return self.__parent__._cast(
            _7068.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7069.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7069,
        )

        return self.__parent__._cast(_7069.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7070.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7070,
        )

        return self.__parent__._cast(_7070.MeasurementComponentLoadCase)

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7072.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7072,
        )

        return self.__parent__._cast(_7072.MicrophoneArrayLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7073.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7073,
        )

        return self.__parent__._cast(_7073.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7074.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7074,
        )

        return self.__parent__._cast(_7074.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7076.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7076,
        )

        return self.__parent__._cast(_7076.OilSealLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7078.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7078,
        )

        return self.__parent__._cast(_7078.PartLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7080.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7080,
        )

        return self.__parent__._cast(_7080.PartToPartShearCouplingHalfLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7081.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7081,
        )

        return self.__parent__._cast(_7081.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7083.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PlanetaryGearSetLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7085.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7085,
        )

        return self.__parent__._cast(_7085.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7088.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7088,
        )

        return self.__parent__._cast(_7088.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7089.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7089,
        )

        return self.__parent__._cast(_7089.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7090.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7090,
        )

        return self.__parent__._cast(_7090.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7093.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7093,
        )

        return self.__parent__._cast(_7093.RingPinsLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7095.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7095,
        )

        return self.__parent__._cast(_7095.RollingRingAssemblyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7097.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7097,
        )

        return self.__parent__._cast(_7097.RollingRingLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7098.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7098,
        )

        return self.__parent__._cast(_7098.RootAssemblyLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7099.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7099,
        )

        return self.__parent__._cast(_7099.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7100.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.ShaftLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7102.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7102,
        )

        return self.__parent__._cast(_7102.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7103.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7103,
        )

        return self.__parent__._cast(_7103.SpiralBevelGearLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7105.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7107.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpringDamperHalfLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7108.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7108,
        )

        return self.__parent__._cast(_7108.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7109.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7109,
        )

        return self.__parent__._cast(_7109.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7111.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7111,
        )

        return self.__parent__._cast(_7111.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7112.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.StraightBevelGearLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7114.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7114,
        )

        return self.__parent__._cast(_7114.StraightBevelGearSetLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7116.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7116,
        )

        return self.__parent__._cast(_7116.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7117.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.SynchroniserHalfLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7118.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7118,
        )

        return self.__parent__._cast(_7118.SynchroniserLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7119.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7123.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7123,
        )

        return self.__parent__._cast(_7123.TorqueConverterLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7124.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7124,
        )

        return self.__parent__._cast(_7124.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7125.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7125,
        )

        return self.__parent__._cast(_7125.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7130.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7130,
        )

        return self.__parent__._cast(_7130.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7131.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7131,
        )

        return self.__parent__._cast(_7131.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7132.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7132,
        )

        return self.__parent__._cast(_7132.WormGearLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7134.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7134,
        )

        return self.__parent__._cast(_7134.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7135.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7135,
        )

        return self.__parent__._cast(_7135.ZerolBevelGearLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7137.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7137,
        )

        return self.__parent__._cast(_7137.ZerolBevelGearSetLoadCase)

    @property
    def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7155.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7155,
        )

        return self.__parent__._cast(
            _7155.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7156.AbstractShaftAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7156,
        )

        return self.__parent__._cast(
            _7156.AbstractShaftAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_or_housing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7157.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7157,
        )

        return self.__parent__._cast(
            _7157.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7163.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7163,
        )

        return self.__parent__._cast(
            _7163.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7165.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7165,
        )

        return self.__parent__._cast(
            _7165.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7166.AssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7166,
        )

        return self.__parent__._cast(
            _7166.AssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bearing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7168.BearingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7168,
        )

        return self.__parent__._cast(
            _7168.BearingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_drive_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7170.BeltDriveAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7170,
        )

        return self.__parent__._cast(
            _7170.BeltDriveAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7171.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7171,
        )

        return self.__parent__._cast(
            _7171.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7173.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7173,
        )

        return self.__parent__._cast(
            _7173.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7174.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7174,
        )

        return self.__parent__._cast(
            _7174.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7175.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7175,
        )

        return self.__parent__._cast(
            _7175.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7176.BevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7176,
        )

        return self.__parent__._cast(
            _7176.BevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7178.BevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7178,
        )

        return self.__parent__._cast(
            _7178.BevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolt_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7179.BoltAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7179,
        )

        return self.__parent__._cast(
            _7179.BoltAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolted_joint_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7180.BoltedJointAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7180,
        )

        return self.__parent__._cast(
            _7180.BoltedJointAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7181.ClutchAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7181,
        )

        return self.__parent__._cast(
            _7181.ClutchAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7183.ClutchHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7183,
        )

        return self.__parent__._cast(
            _7183.ClutchHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7185.ComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7185,
        )

        return self.__parent__._cast(
            _7185.ComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7186.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7186,
        )

        return self.__parent__._cast(
            _7186.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7188.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7188,
        )

        return self.__parent__._cast(
            _7188.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7189.ConceptGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7189,
        )

        return self.__parent__._cast(
            _7189.ConceptGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7191.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7191,
        )

        return self.__parent__._cast(
            _7191.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7192.ConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7192,
        )

        return self.__parent__._cast(
            _7192.ConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7194.ConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7194,
        )

        return self.__parent__._cast(
            _7194.ConicalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connector_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7196.ConnectorAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7196,
        )

        return self.__parent__._cast(
            _7196.ConnectorAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7197.CouplingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7197,
        )

        return self.__parent__._cast(
            _7197.CouplingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7199.CouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7199,
        )

        return self.__parent__._cast(
            _7199.CouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7200.CVTAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7200,
        )

        return self.__parent__._cast(_7200.CVTAdvancedTimeSteppingAnalysisForModulation)

    @property
    def cvt_pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7202.CVTPulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7202,
        )

        return self.__parent__._cast(
            _7202.CVTPulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7203.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7203,
        )

        return self.__parent__._cast(
            _7203.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7204.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7204,
        )

        return self.__parent__._cast(
            _7204.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7207.CylindricalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7207,
        )

        return self.__parent__._cast(
            _7207.CylindricalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7209.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7209,
        )

        return self.__parent__._cast(
            _7209.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7210.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7210,
        )

        return self.__parent__._cast(
            _7210.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def datum_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.DatumAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.DatumAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def external_cad_model_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7212.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7212,
        )

        return self.__parent__._cast(
            _7212.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7213.FaceGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7213,
        )

        return self.__parent__._cast(
            _7213.FaceGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7215.FaceGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7215,
        )

        return self.__parent__._cast(
            _7215.FaceGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def fe_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7216.FEPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7216,
        )

        return self.__parent__._cast(
            _7216.FEPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def flexible_pin_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7217.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7217,
        )

        return self.__parent__._cast(
            _7217.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7218.GearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7218,
        )

        return self.__parent__._cast(
            _7218.GearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7220.GearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7220,
        )

        return self.__parent__._cast(
            _7220.GearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def guide_dxf_model_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7221.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7221,
        )

        return self.__parent__._cast(
            _7221.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7223.HypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7223,
        )

        return self.__parent__._cast(
            _7223.HypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7225.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7225,
        )

        return self.__parent__._cast(
            _7225.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7227.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7227,
        )

        return self.__parent__._cast(
            _7227.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7229.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7229,
        )

        return self.__parent__._cast(
            _7229.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7230.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7230,
        )

        return self.__parent__._cast(
            _7230.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7232.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7232,
        )

        return self.__parent__._cast(
            _7232.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7233.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7233,
        )

        return self.__parent__._cast(
            _7233.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7235.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7235,
        )

        return self.__parent__._cast(
            _7235.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mass_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7236.MassDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7236,
        )

        return self.__parent__._cast(
            _7236.MassDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def measurement_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7237.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7237,
        )

        return self.__parent__._cast(
            _7237.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7238.MicrophoneAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7238,
        )

        return self.__parent__._cast(
            _7238.MicrophoneAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_array_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7239.MicrophoneArrayAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7239,
        )

        return self.__parent__._cast(
            _7239.MicrophoneArrayAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7240,
        )

        return self.__parent__._cast(
            _7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def oil_seal_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7241.OilSealAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7241,
        )

        return self.__parent__._cast(
            _7241.OilSealAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7242.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7242,
        )

        return self.__parent__._cast(
            _7242.PartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7243.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7243,
        )

        return self.__parent__._cast(
            _7243.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7245.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7245,
        )

        return self.__parent__._cast(
            _7245.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7247.PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7247,
        )

        return self.__parent__._cast(
            _7247.PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planet_carrier_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7248.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7248,
        )

        return self.__parent__._cast(
            _7248.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def point_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7249.PointLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7249,
        )

        return self.__parent__._cast(
            _7249.PointLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def power_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7250.PowerLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7250,
        )

        return self.__parent__._cast(
            _7250.PowerLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7251.PulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7251,
        )

        return self.__parent__._cast(
            _7251.PulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7252.RingPinsAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7252,
        )

        return self.__parent__._cast(
            _7252.RingPinsAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7254.RollingRingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7254,
        )

        return self.__parent__._cast(
            _7254.RollingRingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7255.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7255,
        )

        return self.__parent__._cast(
            _7255.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def root_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7257.RootAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7257,
        )

        return self.__parent__._cast(
            _7257.RootAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7258.ShaftAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7258,
        )

        return self.__parent__._cast(
            _7258.ShaftAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_hub_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7259.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7259,
        )

        return self.__parent__._cast(
            _7259.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7261.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7261,
        )

        return self.__parent__._cast(
            _7261.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7262.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7262,
        )

        return self.__parent__._cast(
            _7262.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7264.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7264,
        )

        return self.__parent__._cast(
            _7264.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7265.SpringDamperAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7265,
        )

        return self.__parent__._cast(
            _7265.SpringDamperAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7267.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7267,
        )

        return self.__parent__._cast(
            _7267.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7268.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7268,
        )

        return self.__parent__._cast(
            _7268.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7270.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7270,
        )

        return self.__parent__._cast(
            _7270.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7271.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7271,
        )

        return self.__parent__._cast(
            _7271.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7273.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7273,
        )

        return self.__parent__._cast(
            _7273.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7274.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7274,
        )

        return self.__parent__._cast(
            _7274.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7275.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7275,
        )

        return self.__parent__._cast(
            _7275.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7276.SynchroniserAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7276,
        )

        return self.__parent__._cast(
            _7276.SynchroniserAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7277.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7277,
        )

        return self.__parent__._cast(
            _7277.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7278.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7278,
        )

        return self.__parent__._cast(
            _7278.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_sleeve_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7279.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7279,
        )

        return self.__parent__._cast(
            _7279.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7280.TorqueConverterAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7280,
        )

        return self.__parent__._cast(
            _7280.TorqueConverterAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_pump_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7282.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7282,
        )

        return self.__parent__._cast(
            _7282.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_turbine_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7283.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7283,
        )

        return self.__parent__._cast(
            _7283.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def unbalanced_mass_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7284.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7284,
        )

        return self.__parent__._cast(
            _7284.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def virtual_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7285.VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7285,
        )

        return self.__parent__._cast(
            _7285.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7286.WormGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7286,
        )

        return self.__parent__._cast(
            _7286.WormGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7288.WormGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7288,
        )

        return self.__parent__._cast(
            _7288.WormGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7289,
        )

        return self.__parent__._cast(
            _7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7291.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7291,
        )

        return self.__parent__._cast(
            _7291.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7423.AbstractAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7423,
        )

        return self.__parent__._cast(_7423.AbstractAssemblyAdvancedSystemDeflection)

    @property
    def abstract_shaft_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7424.AbstractShaftAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7424,
        )

        return self.__parent__._cast(_7424.AbstractShaftAdvancedSystemDeflection)

    @property
    def abstract_shaft_or_housing_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7425.AbstractShaftOrHousingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7425,
        )

        return self.__parent__._cast(
            _7425.AbstractShaftOrHousingAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7430.AGMAGleasonConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7430,
        )

        return self.__parent__._cast(
            _7430.AGMAGleasonConicalGearAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7432.AGMAGleasonConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7432,
        )

        return self.__parent__._cast(
            _7432.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        )

    @property
    def assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7433.AssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7433,
        )

        return self.__parent__._cast(_7433.AssemblyAdvancedSystemDeflection)

    @property
    def bearing_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7434.BearingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7434,
        )

        return self.__parent__._cast(_7434.BearingAdvancedSystemDeflection)

    @property
    def belt_drive_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7436.BeltDriveAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7436,
        )

        return self.__parent__._cast(_7436.BeltDriveAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7437.BevelDifferentialGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7437,
        )

        return self.__parent__._cast(
            _7437.BevelDifferentialGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7439.BevelDifferentialGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7439,
        )

        return self.__parent__._cast(
            _7439.BevelDifferentialGearSetAdvancedSystemDeflection
        )

    @property
    def bevel_differential_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7440.BevelDifferentialPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7440,
        )

        return self.__parent__._cast(
            _7440.BevelDifferentialPlanetGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7441.BevelDifferentialSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7441,
        )

        return self.__parent__._cast(
            _7441.BevelDifferentialSunGearAdvancedSystemDeflection
        )

    @property
    def bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7442.BevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7442,
        )

        return self.__parent__._cast(_7442.BevelGearAdvancedSystemDeflection)

    @property
    def bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7444.BevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7444,
        )

        return self.__parent__._cast(_7444.BevelGearSetAdvancedSystemDeflection)

    @property
    def bolt_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7445.BoltAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7445,
        )

        return self.__parent__._cast(_7445.BoltAdvancedSystemDeflection)

    @property
    def bolted_joint_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7446.BoltedJointAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7446,
        )

        return self.__parent__._cast(_7446.BoltedJointAdvancedSystemDeflection)

    @property
    def clutch_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7447.ClutchAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7447,
        )

        return self.__parent__._cast(_7447.ClutchAdvancedSystemDeflection)

    @property
    def clutch_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7449.ClutchHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7449,
        )

        return self.__parent__._cast(_7449.ClutchHalfAdvancedSystemDeflection)

    @property
    def component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7451.ComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7451,
        )

        return self.__parent__._cast(_7451.ComponentAdvancedSystemDeflection)

    @property
    def concept_coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7452.ConceptCouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7452,
        )

        return self.__parent__._cast(_7452.ConceptCouplingAdvancedSystemDeflection)

    @property
    def concept_coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7454.ConceptCouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7454,
        )

        return self.__parent__._cast(_7454.ConceptCouplingHalfAdvancedSystemDeflection)

    @property
    def concept_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7455.ConceptGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7455,
        )

        return self.__parent__._cast(_7455.ConceptGearAdvancedSystemDeflection)

    @property
    def concept_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7457.ConceptGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7457,
        )

        return self.__parent__._cast(_7457.ConceptGearSetAdvancedSystemDeflection)

    @property
    def conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7458.ConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7458,
        )

        return self.__parent__._cast(_7458.ConicalGearAdvancedSystemDeflection)

    @property
    def conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7460.ConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7460,
        )

        return self.__parent__._cast(_7460.ConicalGearSetAdvancedSystemDeflection)

    @property
    def connector_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7462.ConnectorAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7462,
        )

        return self.__parent__._cast(_7462.ConnectorAdvancedSystemDeflection)

    @property
    def coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7464.CouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7464,
        )

        return self.__parent__._cast(_7464.CouplingAdvancedSystemDeflection)

    @property
    def coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7466.CouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7466,
        )

        return self.__parent__._cast(_7466.CouplingHalfAdvancedSystemDeflection)

    @property
    def cvt_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7467.CVTAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7467,
        )

        return self.__parent__._cast(_7467.CVTAdvancedSystemDeflection)

    @property
    def cvt_pulley_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7469.CVTPulleyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7469,
        )

        return self.__parent__._cast(_7469.CVTPulleyAdvancedSystemDeflection)

    @property
    def cycloidal_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7470.CycloidalAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7470,
        )

        return self.__parent__._cast(_7470.CycloidalAssemblyAdvancedSystemDeflection)

    @property
    def cycloidal_disc_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7471.CycloidalDiscAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7471,
        )

        return self.__parent__._cast(_7471.CycloidalDiscAdvancedSystemDeflection)

    @property
    def cylindrical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7474.CylindricalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7474,
        )

        return self.__parent__._cast(_7474.CylindricalGearAdvancedSystemDeflection)

    @property
    def cylindrical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7476.CylindricalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7476,
        )

        return self.__parent__._cast(_7476.CylindricalGearSetAdvancedSystemDeflection)

    @property
    def cylindrical_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7478.CylindricalPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7478,
        )

        return self.__parent__._cast(
            _7478.CylindricalPlanetGearAdvancedSystemDeflection
        )

    @property
    def datum_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7479.DatumAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7479,
        )

        return self.__parent__._cast(_7479.DatumAdvancedSystemDeflection)

    @property
    def external_cad_model_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7480.ExternalCADModelAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7480,
        )

        return self.__parent__._cast(_7480.ExternalCADModelAdvancedSystemDeflection)

    @property
    def face_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7481.FaceGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7481,
        )

        return self.__parent__._cast(_7481.FaceGearAdvancedSystemDeflection)

    @property
    def face_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7483.FaceGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7483,
        )

        return self.__parent__._cast(_7483.FaceGearSetAdvancedSystemDeflection)

    @property
    def fe_part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7484.FEPartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7484,
        )

        return self.__parent__._cast(_7484.FEPartAdvancedSystemDeflection)

    @property
    def flexible_pin_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7485.FlexiblePinAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7485,
        )

        return self.__parent__._cast(_7485.FlexiblePinAssemblyAdvancedSystemDeflection)

    @property
    def gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7486.GearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7486,
        )

        return self.__parent__._cast(_7486.GearAdvancedSystemDeflection)

    @property
    def gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7488.GearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7488,
        )

        return self.__parent__._cast(_7488.GearSetAdvancedSystemDeflection)

    @property
    def guide_dxf_model_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7489.GuideDxfModelAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7489,
        )

        return self.__parent__._cast(_7489.GuideDxfModelAdvancedSystemDeflection)

    @property
    def hypoid_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7490.HypoidGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7490,
        )

        return self.__parent__._cast(_7490.HypoidGearAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7492.HypoidGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7492,
        )

        return self.__parent__._cast(_7492.HypoidGearSetAdvancedSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7494.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7494,
        )

        return self.__parent__._cast(
            _7494.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7496.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7496,
        )

        return self.__parent__._cast(
            _7496.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7497.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7497,
        )

        return self.__parent__._cast(
            _7497.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7499.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7499,
        )

        return self.__parent__._cast(
            _7499.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7500.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7500,
        )

        return self.__parent__._cast(
            _7500.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7502.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7502,
        )

        return self.__parent__._cast(
            _7502.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        )

    @property
    def mass_disc_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7504.MassDiscAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7504,
        )

        return self.__parent__._cast(_7504.MassDiscAdvancedSystemDeflection)

    @property
    def measurement_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7505.MeasurementComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7505,
        )

        return self.__parent__._cast(_7505.MeasurementComponentAdvancedSystemDeflection)

    @property
    def microphone_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7506.MicrophoneAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7506,
        )

        return self.__parent__._cast(_7506.MicrophoneAdvancedSystemDeflection)

    @property
    def microphone_array_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7507.MicrophoneArrayAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7507,
        )

        return self.__parent__._cast(_7507.MicrophoneArrayAdvancedSystemDeflection)

    @property
    def mountable_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7508.MountableComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7508,
        )

        return self.__parent__._cast(_7508.MountableComponentAdvancedSystemDeflection)

    @property
    def oil_seal_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7509.OilSealAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7509,
        )

        return self.__parent__._cast(_7509.OilSealAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7510.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7510,
        )

        return self.__parent__._cast(_7510.PartAdvancedSystemDeflection)

    @property
    def part_to_part_shear_coupling_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7511.PartToPartShearCouplingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7511,
        )

        return self.__parent__._cast(
            _7511.PartToPartShearCouplingAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7513.PartToPartShearCouplingHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7513,
        )

        return self.__parent__._cast(
            _7513.PartToPartShearCouplingHalfAdvancedSystemDeflection
        )

    @property
    def planetary_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7515.PlanetaryGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7515,
        )

        return self.__parent__._cast(_7515.PlanetaryGearSetAdvancedSystemDeflection)

    @property
    def planet_carrier_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7516.PlanetCarrierAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7516,
        )

        return self.__parent__._cast(_7516.PlanetCarrierAdvancedSystemDeflection)

    @property
    def point_load_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7517.PointLoadAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7517,
        )

        return self.__parent__._cast(_7517.PointLoadAdvancedSystemDeflection)

    @property
    def power_load_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7518.PowerLoadAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7518,
        )

        return self.__parent__._cast(_7518.PowerLoadAdvancedSystemDeflection)

    @property
    def pulley_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7519.PulleyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7519,
        )

        return self.__parent__._cast(_7519.PulleyAdvancedSystemDeflection)

    @property
    def ring_pins_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7520.RingPinsAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7520,
        )

        return self.__parent__._cast(_7520.RingPinsAdvancedSystemDeflection)

    @property
    def rolling_ring_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7522.RollingRingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7522,
        )

        return self.__parent__._cast(_7522.RollingRingAdvancedSystemDeflection)

    @property
    def rolling_ring_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7523.RollingRingAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7523,
        )

        return self.__parent__._cast(_7523.RollingRingAssemblyAdvancedSystemDeflection)

    @property
    def root_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7525.RootAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7525,
        )

        return self.__parent__._cast(_7525.RootAssemblyAdvancedSystemDeflection)

    @property
    def shaft_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7526.ShaftAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7526,
        )

        return self.__parent__._cast(_7526.ShaftAdvancedSystemDeflection)

    @property
    def shaft_hub_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7527.ShaftHubConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7527,
        )

        return self.__parent__._cast(_7527.ShaftHubConnectionAdvancedSystemDeflection)

    @property
    def specialised_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7529.SpecialisedAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7529,
        )

        return self.__parent__._cast(_7529.SpecialisedAssemblyAdvancedSystemDeflection)

    @property
    def spiral_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7530.SpiralBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7530,
        )

        return self.__parent__._cast(_7530.SpiralBevelGearAdvancedSystemDeflection)

    @property
    def spiral_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7532.SpiralBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7532,
        )

        return self.__parent__._cast(_7532.SpiralBevelGearSetAdvancedSystemDeflection)

    @property
    def spring_damper_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7533.SpringDamperAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7533,
        )

        return self.__parent__._cast(_7533.SpringDamperAdvancedSystemDeflection)

    @property
    def spring_damper_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7535.SpringDamperHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7535,
        )

        return self.__parent__._cast(_7535.SpringDamperHalfAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7536.StraightBevelDiffGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7536,
        )

        return self.__parent__._cast(
            _7536.StraightBevelDiffGearAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7538.StraightBevelDiffGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7538,
        )

        return self.__parent__._cast(
            _7538.StraightBevelDiffGearSetAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7539.StraightBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7539,
        )

        return self.__parent__._cast(_7539.StraightBevelGearAdvancedSystemDeflection)

    @property
    def straight_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7541.StraightBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7541,
        )

        return self.__parent__._cast(_7541.StraightBevelGearSetAdvancedSystemDeflection)

    @property
    def straight_bevel_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7542.StraightBevelPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7542,
        )

        return self.__parent__._cast(
            _7542.StraightBevelPlanetGearAdvancedSystemDeflection
        )

    @property
    def straight_bevel_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7543.StraightBevelSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7543,
        )

        return self.__parent__._cast(_7543.StraightBevelSunGearAdvancedSystemDeflection)

    @property
    def synchroniser_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7544.SynchroniserAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7544,
        )

        return self.__parent__._cast(_7544.SynchroniserAdvancedSystemDeflection)

    @property
    def synchroniser_half_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7545.SynchroniserHalfAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7545,
        )

        return self.__parent__._cast(_7545.SynchroniserHalfAdvancedSystemDeflection)

    @property
    def synchroniser_part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7546.SynchroniserPartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7546,
        )

        return self.__parent__._cast(_7546.SynchroniserPartAdvancedSystemDeflection)

    @property
    def synchroniser_sleeve_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7547.SynchroniserSleeveAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7547,
        )

        return self.__parent__._cast(_7547.SynchroniserSleeveAdvancedSystemDeflection)

    @property
    def torque_converter_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7548.TorqueConverterAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7548,
        )

        return self.__parent__._cast(_7548.TorqueConverterAdvancedSystemDeflection)

    @property
    def torque_converter_pump_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7550.TorqueConverterPumpAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7550,
        )

        return self.__parent__._cast(_7550.TorqueConverterPumpAdvancedSystemDeflection)

    @property
    def torque_converter_turbine_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7551.TorqueConverterTurbineAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7551,
        )

        return self.__parent__._cast(
            _7551.TorqueConverterTurbineAdvancedSystemDeflection
        )

    @property
    def unbalanced_mass_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7553.UnbalancedMassAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7553,
        )

        return self.__parent__._cast(_7553.UnbalancedMassAdvancedSystemDeflection)

    @property
    def virtual_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7554.VirtualComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7554,
        )

        return self.__parent__._cast(_7554.VirtualComponentAdvancedSystemDeflection)

    @property
    def worm_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7555.WormGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7555,
        )

        return self.__parent__._cast(_7555.WormGearAdvancedSystemDeflection)

    @property
    def worm_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7557.WormGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7557,
        )

        return self.__parent__._cast(_7557.WormGearSetAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7558.ZerolBevelGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7558,
        )

        return self.__parent__._cast(_7558.ZerolBevelGearAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7560.ZerolBevelGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7560,
        )

        return self.__parent__._cast(_7560.ZerolBevelGearSetAdvancedSystemDeflection)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7716.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7718.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartTimeSeriesLoadAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "PartAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class PartAnalysis(_2737.DesignEntitySingleContextAnalysis):
    """PartAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetary_original(self: "Self") -> "PartAnalysis":
        """mastapy.system_model.analyses_and_results.PartAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryOriginal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartAnalysis
        """
        return _Cast_PartAnalysis(self)
