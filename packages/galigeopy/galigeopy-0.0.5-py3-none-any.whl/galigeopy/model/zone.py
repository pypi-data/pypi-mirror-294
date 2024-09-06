import pandas as pd
from sqlalchemy import text

from galigeopy.model.poi import Poi
from galigeopy.model.zone_geounit import ZoneGeounit

class Zone:
    # Constructor
    def __init__(
        self,
        zone_id:int,
        properties:dict,
        geolevel_id:int,
        zone_type_id:int,
        poi_id:int,
        parent_zone_id:int,
        org:'Org' # type: ignore
    ):
        # Infos
        self._zone_id = zone_id
        self._properties = properties
        self._geolevel_id = geolevel_id
        self._zone_type_id = zone_type_id
        self._poi_id = poi_id
        self._parent_zone_id = parent_zone_id
        # Org
        self._org = org

    # Getters and setters
    @property
    def zone_id(self): return self._zone_id
    @property
    def properties(self): return self._properties
    @property
    def geolevel_id(self): return self._geolevel_id
    @property
    def zone_type_id(self): return self._zone_type_id
    @property
    def poi_id(self): return self._poi_id
    @property
    def parent_zone_id(self): return self._parent_zone_id
    @property
    def org(self): return self._org

    # Public Methods
    def getPoi(self)->Poi:
        query = f"SELECT * FROM ggo_poi WHERE poi_id = {self.poi_id}"
        df = pd.read_sql(query, self._org.engine)
        if len(df) > 0:
            data = df.iloc[0].to_dict()
            data.update({"org": self._org})
            return Poi(**data)
        else:
            raise Warning(f"Poi {self.poi_id} not found in Zone {self.zone_id}")
        
    def getParentZone(self) -> 'Zone':
        query = f"SELECT * FROM ggo_zone WHERE zone_id = {self.parent_zone_id}"
        df = pd.read_sql(query, self._org.engine)
        if len(df) > 0:
            data = df.iloc[0].to_dict()
            data.update({"org": self._org})
            return Zone(**data)
        else:
            raise Warning(f"Parent Zone {self.parent_zone_id} not found in Zone {self.zone_id}")
        
    def getChildrenZones(self)->list:
        query = f"SELECT * FROM ggo_zone WHERE parent_zone_id = {self.zone_id}"
        df = pd.read_sql(query, self._org.engine)
        zones = []
        for i in range(len(df)):
            data = df.iloc[i].to_dict()
            data.update({"org": self._org})
            zones.append(Zone(**data))
        return zones
    
    def getZoneGeounitsList(self) -> pd.DataFrame:
        query = f"SELECT * FROM ggo_zone_geounit WHERE zone_id = {self.zone_id}"
        return pd.read_sql(query, self._org.engine)
    
    def getZoneGeounitById(self, geounit_id:int) -> pd.DataFrame:
        query = f"SELECT * FROM ggo_zone_geounit WHERE zone_id = {self.zone_id} AND zone_geounit_id = {geounit_id}"
        df = pd.read_sql(query, self._org.engine)
        if len(df) > 0:
            data = df.iloc[0].to_dict()
            data.update({"org": self._org})
            return ZoneGeounit(**data)
        else:
            raise Warning(f"Geounit {geounit_id} not found in Zone {self.zone_id}")
