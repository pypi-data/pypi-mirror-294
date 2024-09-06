"""ComponentCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4634,
)

_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ComponentCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4429,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4554,
        _4555,
        _4557,
        _4561,
        _4564,
        _4567,
        _4568,
        _4569,
        _4572,
        _4576,
        _4581,
        _4582,
        _4585,
        _4589,
        _4592,
        _4595,
        _4598,
        _4600,
        _4603,
        _4604,
        _4605,
        _4606,
        _4609,
        _4611,
        _4614,
        _4615,
        _4619,
        _4622,
        _4625,
        _4628,
        _4629,
        _4631,
        _4632,
        _4633,
        _4637,
        _4640,
        _4641,
        _4642,
        _4643,
        _4644,
        _4647,
        _4650,
        _4651,
        _4654,
        _4659,
        _4660,
        _4663,
        _4666,
        _4667,
        _4669,
        _4670,
        _4671,
        _4674,
        _4675,
        _4676,
        _4677,
        _4678,
        _4681,
    )

    Self = TypeVar("Self", bound="ComponentCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundParametricStudyTool._Cast_ComponentCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundParametricStudyTool:
    """Special nested class for casting ComponentCompoundParametricStudyTool to subclasses."""

    __parent__: "ComponentCompoundParametricStudyTool"

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4634.PartCompoundParametricStudyTool":
        return self.__parent__._cast(_4634.PartCompoundParametricStudyTool)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7712.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def abstract_shaft_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4554.AbstractShaftCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4554,
        )

        return self.__parent__._cast(_4554.AbstractShaftCompoundParametricStudyTool)

    @property
    def abstract_shaft_or_housing_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4555.AbstractShaftOrHousingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4555,
        )

        return self.__parent__._cast(
            _4555.AbstractShaftOrHousingCompoundParametricStudyTool
        )

    @property
    def agma_gleason_conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4557.AGMAGleasonConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4557,
        )

        return self.__parent__._cast(
            _4557.AGMAGleasonConicalGearCompoundParametricStudyTool
        )

    @property
    def bearing_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4561.BearingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4561,
        )

        return self.__parent__._cast(_4561.BearingCompoundParametricStudyTool)

    @property
    def bevel_differential_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4564.BevelDifferentialGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4564,
        )

        return self.__parent__._cast(
            _4564.BevelDifferentialGearCompoundParametricStudyTool
        )

    @property
    def bevel_differential_planet_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4567.BevelDifferentialPlanetGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4567,
        )

        return self.__parent__._cast(
            _4567.BevelDifferentialPlanetGearCompoundParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4568.BevelDifferentialSunGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4568,
        )

        return self.__parent__._cast(
            _4568.BevelDifferentialSunGearCompoundParametricStudyTool
        )

    @property
    def bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4569.BevelGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4569,
        )

        return self.__parent__._cast(_4569.BevelGearCompoundParametricStudyTool)

    @property
    def bolt_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4572.BoltCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4572,
        )

        return self.__parent__._cast(_4572.BoltCompoundParametricStudyTool)

    @property
    def clutch_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4576.ClutchHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4576,
        )

        return self.__parent__._cast(_4576.ClutchHalfCompoundParametricStudyTool)

    @property
    def concept_coupling_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4581.ConceptCouplingHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4581,
        )

        return self.__parent__._cast(
            _4581.ConceptCouplingHalfCompoundParametricStudyTool
        )

    @property
    def concept_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4582.ConceptGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4582,
        )

        return self.__parent__._cast(_4582.ConceptGearCompoundParametricStudyTool)

    @property
    def conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4585.ConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4585,
        )

        return self.__parent__._cast(_4585.ConicalGearCompoundParametricStudyTool)

    @property
    def connector_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4589.ConnectorCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4589,
        )

        return self.__parent__._cast(_4589.ConnectorCompoundParametricStudyTool)

    @property
    def coupling_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4592.CouplingHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4592,
        )

        return self.__parent__._cast(_4592.CouplingHalfCompoundParametricStudyTool)

    @property
    def cvt_pulley_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4595.CVTPulleyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4595,
        )

        return self.__parent__._cast(_4595.CVTPulleyCompoundParametricStudyTool)

    @property
    def cycloidal_disc_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4598.CycloidalDiscCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4598,
        )

        return self.__parent__._cast(_4598.CycloidalDiscCompoundParametricStudyTool)

    @property
    def cylindrical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4600.CylindricalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4600,
        )

        return self.__parent__._cast(_4600.CylindricalGearCompoundParametricStudyTool)

    @property
    def cylindrical_planet_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4603.CylindricalPlanetGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4603,
        )

        return self.__parent__._cast(
            _4603.CylindricalPlanetGearCompoundParametricStudyTool
        )

    @property
    def datum_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4604.DatumCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4604,
        )

        return self.__parent__._cast(_4604.DatumCompoundParametricStudyTool)

    @property
    def external_cad_model_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4605.ExternalCADModelCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4605,
        )

        return self.__parent__._cast(_4605.ExternalCADModelCompoundParametricStudyTool)

    @property
    def face_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4606.FaceGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4606,
        )

        return self.__parent__._cast(_4606.FaceGearCompoundParametricStudyTool)

    @property
    def fe_part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4609.FEPartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4609,
        )

        return self.__parent__._cast(_4609.FEPartCompoundParametricStudyTool)

    @property
    def gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4611.GearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4611,
        )

        return self.__parent__._cast(_4611.GearCompoundParametricStudyTool)

    @property
    def guide_dxf_model_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4614.GuideDxfModelCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4614,
        )

        return self.__parent__._cast(_4614.GuideDxfModelCompoundParametricStudyTool)

    @property
    def hypoid_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4615.HypoidGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4615,
        )

        return self.__parent__._cast(_4615.HypoidGearCompoundParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4619.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4619,
        )

        return self.__parent__._cast(
            _4619.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4622.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4622,
        )

        return self.__parent__._cast(
            _4622.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4625.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4625,
        )

        return self.__parent__._cast(
            _4625.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
        )

    @property
    def mass_disc_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4628.MassDiscCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4628,
        )

        return self.__parent__._cast(_4628.MassDiscCompoundParametricStudyTool)

    @property
    def measurement_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4629.MeasurementComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4629,
        )

        return self.__parent__._cast(
            _4629.MeasurementComponentCompoundParametricStudyTool
        )

    @property
    def microphone_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4631.MicrophoneCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4631,
        )

        return self.__parent__._cast(_4631.MicrophoneCompoundParametricStudyTool)

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4632.MountableComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4632,
        )

        return self.__parent__._cast(
            _4632.MountableComponentCompoundParametricStudyTool
        )

    @property
    def oil_seal_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4633.OilSealCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4633,
        )

        return self.__parent__._cast(_4633.OilSealCompoundParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.PartToPartShearCouplingHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4637,
        )

        return self.__parent__._cast(
            _4637.PartToPartShearCouplingHalfCompoundParametricStudyTool
        )

    @property
    def planet_carrier_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4640.PlanetCarrierCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4640,
        )

        return self.__parent__._cast(_4640.PlanetCarrierCompoundParametricStudyTool)

    @property
    def point_load_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4641.PointLoadCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4641,
        )

        return self.__parent__._cast(_4641.PointLoadCompoundParametricStudyTool)

    @property
    def power_load_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4642.PowerLoadCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4642,
        )

        return self.__parent__._cast(_4642.PowerLoadCompoundParametricStudyTool)

    @property
    def pulley_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4643.PulleyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4643,
        )

        return self.__parent__._cast(_4643.PulleyCompoundParametricStudyTool)

    @property
    def ring_pins_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4644.RingPinsCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4644,
        )

        return self.__parent__._cast(_4644.RingPinsCompoundParametricStudyTool)

    @property
    def rolling_ring_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4647.RollingRingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4647,
        )

        return self.__parent__._cast(_4647.RollingRingCompoundParametricStudyTool)

    @property
    def shaft_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4650.ShaftCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4650,
        )

        return self.__parent__._cast(_4650.ShaftCompoundParametricStudyTool)

    @property
    def shaft_hub_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4651.ShaftHubConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4651,
        )

        return self.__parent__._cast(
            _4651.ShaftHubConnectionCompoundParametricStudyTool
        )

    @property
    def spiral_bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4654.SpiralBevelGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4654,
        )

        return self.__parent__._cast(_4654.SpiralBevelGearCompoundParametricStudyTool)

    @property
    def spring_damper_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4659.SpringDamperHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4659,
        )

        return self.__parent__._cast(_4659.SpringDamperHalfCompoundParametricStudyTool)

    @property
    def straight_bevel_diff_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4660.StraightBevelDiffGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4660,
        )

        return self.__parent__._cast(
            _4660.StraightBevelDiffGearCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4663.StraightBevelGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4663,
        )

        return self.__parent__._cast(_4663.StraightBevelGearCompoundParametricStudyTool)

    @property
    def straight_bevel_planet_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4666.StraightBevelPlanetGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4666,
        )

        return self.__parent__._cast(
            _4666.StraightBevelPlanetGearCompoundParametricStudyTool
        )

    @property
    def straight_bevel_sun_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4667.StraightBevelSunGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4667,
        )

        return self.__parent__._cast(
            _4667.StraightBevelSunGearCompoundParametricStudyTool
        )

    @property
    def synchroniser_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4669.SynchroniserHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4669,
        )

        return self.__parent__._cast(_4669.SynchroniserHalfCompoundParametricStudyTool)

    @property
    def synchroniser_part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4670.SynchroniserPartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4670,
        )

        return self.__parent__._cast(_4670.SynchroniserPartCompoundParametricStudyTool)

    @property
    def synchroniser_sleeve_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4671.SynchroniserSleeveCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4671,
        )

        return self.__parent__._cast(
            _4671.SynchroniserSleeveCompoundParametricStudyTool
        )

    @property
    def torque_converter_pump_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4674.TorqueConverterPumpCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4674,
        )

        return self.__parent__._cast(
            _4674.TorqueConverterPumpCompoundParametricStudyTool
        )

    @property
    def torque_converter_turbine_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4675.TorqueConverterTurbineCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4675,
        )

        return self.__parent__._cast(
            _4675.TorqueConverterTurbineCompoundParametricStudyTool
        )

    @property
    def unbalanced_mass_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4676.UnbalancedMassCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4676,
        )

        return self.__parent__._cast(_4676.UnbalancedMassCompoundParametricStudyTool)

    @property
    def virtual_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4677.VirtualComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4677,
        )

        return self.__parent__._cast(_4677.VirtualComponentCompoundParametricStudyTool)

    @property
    def worm_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4678.WormGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4678,
        )

        return self.__parent__._cast(_4678.WormGearCompoundParametricStudyTool)

    @property
    def zerol_bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4681.ZerolBevelGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4681,
        )

        return self.__parent__._cast(_4681.ZerolBevelGearCompoundParametricStudyTool)

    @property
    def component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ComponentCompoundParametricStudyTool":
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
class ComponentCompoundParametricStudyTool(_4634.PartCompoundParametricStudyTool):
    """ComponentCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4429.ComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4429.ComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundParametricStudyTool
        """
        return _Cast_ComponentCompoundParametricStudyTool(self)
