from shyft.time_series import ByteVector
from shyft.hydrology.r_pmv_st_k._r_pmv_st_k import *
# Fix up types that we need attached to the model
RPMVSTKStateVector.size = lambda self: len(self)


RPMVSTKModel.cell_t = RPMVSTKCellAll
RPMVSTKParameter.map_t = RPMVSTKParameterMap
RPMVSTKModel.parameter_t = RPMVSTKParameter
RPMVSTKModel.state_t = RPMVSTKState
RPMVSTKModel.state_with_id_t = RPMVSTKStateWithId
RPMVSTKModel.state = property(lambda self:RPMVSTKCellAllStateHandler(self.get_cells()))
RPMVSTKModel.statistics = property(lambda self: RPMVSTKCellAllStatistics(self.get_cells()))


RPMVSTKModel.snow_tiles_state = property(lambda self: RPMVSTKCellSnowTilesStateStatistics(self.get_cells()))
RPMVSTKModel.snow_tiles_response = property(lambda self: RPMVSTKCellSnowTilesResponseStatistics(self.get_cells()))
RPMVSTKModel.penman_monteith_vegetation_response = property(lambda self: RPMVSTKCellPenmanMonteithResponseStatistics(self.get_cells()))
RPMVSTKModel.actual_evaptranspiration_response=property(lambda self: RPMVSTKCellActualEvapotranspirationResponseStatistics(self.get_cells()))
RPMVSTKModel.kirchner_state = property(lambda self: RPMVSTKCellKirchnerStateStatistics(self.get_cells()))

RPMVSTKOptModel.cell_t = RPMVSTKCellOpt
RPMVSTKOptModel.parameter_t = RPMVSTKParameter
RPMVSTKOptModel.state_t = RPMVSTKState
RPMVSTKOptModel.state_with_id_t = RPMVSTKStateWithId
RPMVSTKOptModel.state = property(lambda self:RPMVSTKCellOptStateHandler(self.get_cells()))
RPMVSTKOptModel.statistics = property(lambda self:RPMVSTKCellOptStatistics(self.get_cells()))

RPMVSTKOptModel.optimizer_t = RPMVSTKOptimizer
RPMVSTKOptModel.full_model_t =RPMVSTKModel
RPMVSTKModel.opt_model_t =RPMVSTKOptModel
RPMVSTKModel.create_opt_model_clone = lambda self: create_opt_model_clone(self)
RPMVSTKOptModel.create_full_model_clone = lambda self: create_full_model_clone(self)


RPMVSTKCellAll.vector_t = RPMVSTKCellAllVector
RPMVSTKCellOpt.vector_t = RPMVSTKCellOptVector
RPMVSTKState.vector_t = RPMVSTKStateVector

#decorate StateWithId for serialization support
def serialize_to_bytes(state_with_id_vector:RPMVSTKStateWithIdVector)->ByteVector:
    if not isinstance(state_with_id_vector,RPMVSTKStateWithIdVector):
        raise RuntimeError("supplied argument must be of type RPMVSTKStateWithIdVector")
    return serialize(state_with_id_vector)

def __serialize_to_str(state_with_id_vector:RPMVSTKStateWithIdVector)->str:
    return str(serialize_to_bytes(state_with_id_vector))  # returns hex-string formatted vector

def __deserialize_from_str(s:str)->RPMVSTKStateWithIdVector:
    return deserialize_from_bytes(ByteVector.from_str(s))

RPMVSTKStateWithIdVector.serialize_to_bytes = lambda self: serialize_to_bytes(self)
RPMVSTKStateWithIdVector.serialize_to_str = lambda self: __serialize_to_str(self)
RPMVSTKStateWithIdVector.state_vector = property(lambda self: extract_state_vector(self),doc="extract_state_vector.__doc__")
RPMVSTKStateWithIdVector.deserialize_from_str = __deserialize_from_str
RPMVSTKStateWithId.vector_t = RPMVSTKStateWithIdVector
def deserialize_from_bytes(bytes: ByteVector)->RPMVSTKStateWithIdVector:
    if not isinstance(bytes,ByteVector):
        raise RuntimeError("Supplied type must be a ByteVector, as created from serialize_to_bytes")
    states=RPMVSTKStateWithIdVector()
    deserialize(bytes,states)
    return states

__all__=[
    'RPMVSTKStateVector',
    'RPMVSTKStateWithId',
    'RPMVSTKStateWithIdVector',
    'RPMVSTKCellAll',
    'RPMVSTKCellOpt',
    'RPMVSTKState',
    'RPMVSTKModel',
    'RPMVSTKOptModel',
    'RPMVSTKParameter'
]
