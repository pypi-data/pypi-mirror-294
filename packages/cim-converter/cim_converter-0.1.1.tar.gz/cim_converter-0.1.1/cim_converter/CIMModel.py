from cim_converter.CIM_EG.Wires.BusbarSection import BusbarSection
from cim_converter.CIM_EG.Wires.PowerTransformer import PowerTransformer
from cim_converter.CIM_EG.Wires.ACLineSegment import ACLineSegment
from cim_converter.CIM_EG.Wires.EnergyConsumer import EnergyConsumer
from cim_converter.CIM_EG.Core.ConnectivityNode import ConnectivityNode

from cim_converter.rdf_converter import cimread

class CIMModel:
    """Class for the CIM model.

    Attributes:
    ----------
    cim_dict : dict
        Dictionary of the CIM model.
    """

    def __init__(self):
        """Constructor method.
        
        Parameters:
        ----------
        cim_dict : dict
            Dictionary of the CIM model.
        """
        self.cim_dict = None

    @property
    def get_cim_dict(self):
        return self.cim_dict

    @property
    def set_cim_dict(self, cim_dict):
        self.cim_dict = cim_dict

    def convert_rdf_to_cim(self, rdf_file: str) -> None:
        """Converts RDF file to CIM model.

        Parameters:
        ----------
        rdf_file : str
            Path to the RDF file.
        """
        self.cim_dict = cimread(rdf_file)

    def get_class(self, class_name: str) -> dict:
        """Returns a dictionary of objects of a given class name from the CIM model.

        Parameters:
        ----------
        class_name : str
            Name of the class.

        Returns:
        -------
        dict:
            Dictionary of objects of the given class name.
        """
        result = dict()
        for key, value in self.cim_dict.items():
            if value.__class__.__name__ == class_name:
                result[key] = value
        return result

    def is_junction(self, connectivity_node: ConnectivityNode) -> bool:
        """Checks if a connectivity node is a junction.
        
        Parameters:
        ----------
        connectivity_node : ConnectivityNode
            Connectivity node to be checked.
        
        Returns:
        -------
        bool:
            True if the connectivity node is a junction, False otherwise.
        """
        if connectivity_node.__class__.__name__ == 'ConnectivityNode':
            equipments = [
                terminal.ConductingEquipment.__class__.__name__
                for terminal in connectivity_node.Terminals
            ]
            if len(set(equipments).difference({'ACLineSegment'})) == 0:
                if equipments != ['ACLineSegment'
                                  ] and 'EnergyConsumer' not in equipments:
                    return True
            else:
                return False
        else:
            return False

    def is_fuse_junction(self, connectivity_node: ConnectivityNode) -> bool:
        """Checks if a connectivity node is a fuse junction.

        Parameters:
        ----------
        connectivity_node : ConnectivityNode
            Connectivity node to be checked.

        Returns:
        -------
        bool:
            True if the connectivity node is a fuse junction, False otherwise.
        """
        if connectivity_node.__class__.__name__ == 'ConnectivityNode':
            equipments = [
                terminal.ConductingEquipment.__class__.__name__
                for terminal in connectivity_node.Terminals
            ]
            if len(set({'ACLineSegment', 'Fuse'}).difference(set(equipments))) == 0:
                if set(equipments) != {'Fuse'} and 'BusbarSection' not in equipments:
                    return True
            else:
                return False
        else:
            return False

    def get_power_transformer(self) -> PowerTransformer:
        """Returns the power transformer object from the CIM model.
        
        Returns:
        -------
        PowerTransformer:
            Power transformer object.    
        """
        trafo = self.get_class('PowerTransformer')
        return list(trafo.values())[0]

    def get_acline_junction_point(self, acline1: ACLineSegment, acline2: ACLineSegment) -> tuple:
        """Returns the junction point of two AC line segments.

        Parameters:
        ----------
        acline1 : ACLineSegment
            First AC line segment.
        acline2 : ACLineSegment
            Second AC line segment.

        Returns:
        -------
        tuple:
            Junction point of the two AC line segments.
        """
        ends1 = set({(acline1.Location.PositionPoints[0].xPosition,
                      acline1.Location.PositionPoints[0].yPosition),
                     (acline1.Location.PositionPoints[-1].xPosition,
                      acline1.Location.PositionPoints[-1].yPosition)})
        ends2 = set({(acline2.Location.PositionPoints[0].xPosition,
                      acline2.Location.PositionPoints[0].yPosition),
                     (acline2.Location.PositionPoints[-1].xPosition,
                      acline2.Location.PositionPoints[-1].yPosition)})

        if list(ends1.intersection(ends2)):
            return list(ends1.intersection(ends2))[0]
        else:
            return None

    def get_energy_consumer_by_alias_name(self, alias_name: str) -> EnergyConsumer:
        """Returns the energy consumer object by its alias name.

        Parameters:
        ----------
        alias_name : str
            Alias name of the energy consumer.

        Returns:
        -------
        EnergyConsumer:
            Energy consumer object.
        """
        consumers = self.get_class('EnergyConsumer')
        for key, value in consumers.items():
            if value.aliasName == alias_name:
                return value
        return None

    def get_trafo_nnr(self, trafo: PowerTransformer) -> BusbarSection:
        """Returns the busbar section object connected to the power transformer.
        
        Parameters:
        ----------
        trafo : PowerTransformer
            Power transformer object.
        
        Returns:
        -------
        BusbarSection:
            Busbar section object.
        """
        hv = 0
        for trafo_end in trafo.PowerTransformerEnd:
            if trafo_end.BaseVoltage.nominalVoltage > hv:
                hv = trafo_end.BaseVoltage.nominalVoltage
        def find_busbar_in_terminals(terminals):
            for terminal in terminals:
                if terminal.ConductingEquipment.__class__.__name__ == 'BusbarSection':
                    if terminal.ConductingEquipment.BaseVoltage.nominalVoltage == hv:
                        continue
                    else:
                        return terminal.ConductingEquipment
            return None

        def find_busbar_through_equipment(terminals, exclude_class):
            for terminal in terminals:
                if terminal.ConductingEquipment.__class__.__name__ != exclude_class:
                    busbar = find_busbar_in_terminals(terminal.ConductingEquipment.Terminals)
                    if busbar:
                        return busbar
            return None

        for trafo_end in trafo.PowerTransformerEnd:
            terminals = trafo_end.Terminal.ConnectivityNode.Terminals
            
            # First level check: Directly connected terminals
            busbar = find_busbar_in_terminals(terminals)
            if busbar:
                return busbar
            
            # Second level check: Terminals connected through other equipment
            busbar = find_busbar_through_equipment(terminals, 'PowerTransformer')
            if busbar:
                return busbar
            
            # Third level check: One more level deeper
            for terminal1 in terminals:
                if terminal1.ConductingEquipment.__class__.__name__ != 'PowerTransformer':
                    for terminal2 in terminal1.ConductingEquipment.Terminals:
                        if terminal2.ConductingEquipment.__class__.__name__ != 'PowerTransformer':
                            busbar = find_busbar_in_terminals(terminal2.ConnectivityNode.Terminals)
                            if busbar:
                                return busbar
        
        # Fallback: Return any busbar section found in the system
        for busbar in self.get_class('BusbarSection').values():
            return busbar
