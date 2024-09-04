from shyft.time_series import ByteVector
from ._r_pm_st_k import *
# Fix up types that we need attached to the model
RPMSTKStateVector.size = lambda self: len(self)


RPMSTKModel.cell_t = RPMSTKCellAll
RPMSTKParameter.map_t = RPMSTKParameterMap
RPMSTKModel.parameter_t = RPMSTKParameter
RPMSTKModel.state_t = RPMSTKState
RPMSTKModel.state_with_id_t = RPMSTKStateWithId
RPMSTKModel.state = property(lambda self:RPMSTKCellAllStateHandler(self.get_cells()))
RPMSTKModel.statistics = property(lambda self: RPMSTKCellAllStatistics(self.get_cells()))


RPMSTKModel.snow_tiles_state = property(lambda self: RPMSTKCellSnowTilesStateStatistics(self.get_cells()))
RPMSTKModel.snow_tiles_response = property(lambda self: RPMSTKCellSnowTilesResponseStatistics(self.get_cells()))
RPMSTKModel.penman_monteith_response = property(lambda self: RPMSTKCellPenmanMonteithResponseStatistics(self.get_cells()))
RPMSTKModel.actual_evaptranspiration_response=property(lambda self: RPMSTKCellActualEvapotranspirationResponseStatistics(self.get_cells()))
RPMSTKModel.kirchner_state = property(lambda self: RPMSTKCellKirchnerStateStatistics(self.get_cells()))

RPMSTKOptModel.cell_t = RPMSTKCellOpt
RPMSTKOptModel.parameter_t = RPMSTKParameter
RPMSTKOptModel.state_t = RPMSTKState
RPMSTKOptModel.state_with_id_t = RPMSTKStateWithId
RPMSTKOptModel.state = property(lambda self:RPMSTKCellOptStateHandler(self.get_cells()))
RPMSTKOptModel.statistics = property(lambda self:RPMSTKCellOptStatistics(self.get_cells()))

RPMSTKOptModel.optimizer_t = RPMSTKOptimizer
RPMSTKOptModel.full_model_t =RPMSTKModel
RPMSTKModel.opt_model_t =RPMSTKOptModel
RPMSTKModel.create_opt_model_clone = lambda self: create_opt_model_clone(self)
RPMSTKOptModel.create_full_model_clone = lambda self: create_full_model_clone(self)


RPMSTKCellAll.vector_t = RPMSTKCellAllVector
RPMSTKCellOpt.vector_t = RPMSTKCellOptVector
RPMSTKState.vector_t = RPMSTKStateVector

#decorate StateWithId for serialization support
def serialize_to_bytes(state_with_id_vector:RPMSTKStateWithIdVector)->ByteVector:
    if not isinstance(state_with_id_vector,RPMSTKStateWithIdVector):
        raise RuntimeError("supplied argument must be of type RPMSTKStateWithIdVector")
    return serialize(state_with_id_vector)

def __serialize_to_str(state_with_id_vector:RPMSTKStateWithIdVector)->str:
    return str(serialize_to_bytes(state_with_id_vector))  # returns hex-string formatted vector

def __deserialize_from_str(s:str)->RPMSTKStateWithIdVector:
    return deserialize_from_bytes(ByteVector.from_str(s))

RPMSTKStateWithIdVector.serialize_to_bytes = lambda self: serialize_to_bytes(self)
RPMSTKStateWithIdVector.serialize_to_str = lambda self: __serialize_to_str(self)
RPMSTKStateWithIdVector.state_vector = property(lambda self: extract_state_vector(self),doc="extract_state_vector.__doc__")
RPMSTKStateWithIdVector.deserialize_from_str = __deserialize_from_str
RPMSTKStateWithId.vector_t = RPMSTKStateWithIdVector
def deserialize_from_bytes(bytes: ByteVector)->RPMSTKStateWithIdVector:
    if not isinstance(bytes,ByteVector):
        raise RuntimeError("Supplied type must be a ByteVector, as created from serialize_to_bytes")
    states=RPMSTKStateWithIdVector()
    deserialize(bytes,states)
    return states

__all__=[
    'RPMSTKStateVector',
    'RPMSTKStateWithId',
    'RPMSTKStateWithIdVector',
    'RPMSTKCellAll',
    'RPMSTKCellOpt',
    'RPMSTKState',
    'RPMSTKModel',
    'RPMSTKOptModel',
    'RPMSTKParameter'
]
