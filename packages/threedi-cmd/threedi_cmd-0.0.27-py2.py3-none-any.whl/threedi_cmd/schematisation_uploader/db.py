from pathlib import Path
from sqlalchemy.orm import Query
from threedi_schema import models
from threedi_schema import ThreediDatabase
from typing import Dict
from typing import Optional


RASTERS = [
    "dem_file",
    "frict_coef_file",
    "interception_file",
    "porosity_file",
    "hydraulic_conductivity_file",
    "infiltration_rate_file",
    "max_infiltration_capacity_file",
    "groundwater_impervious_layer_level_file",
    "phreatic_storage_capacity_file",
    "initial_infiltration_rate_file",
    "equilibrium_infiltration_rate_file",
    "infiltration_decay_period_file",
    "groundwater_hydro_connectivity_file",
    "initial_waterlevel_file",
    "initial_groundwater_level_file",
]


__all__ = ["ModelDB"]


MIN_SQLITE_VERSION = 219


class ModelDB:
    """Interface to sqlite of a model."""

    def __init__(
        self,
        sqlite_path: Path,
        global_settings_id: Optional[int] = None,
        upgrade: bool = False,
    ):
        if not sqlite_path.exists():
            raise ValueError(f"Sqlite path {sqlite_path} does not exist.")

        self.sqlite_path = sqlite_path
        self.database = ThreediDatabase(self.sqlite_path.as_posix())

        version = self.get_version()
        if version < MIN_SQLITE_VERSION:
            if upgrade:
                self.upgrade()
            else:
                raise ValueError(f"Too old sqlite version {version}.")

        if global_settings_id:
            self.global_settings_id = global_settings_id
        else:
            try:
                session = self.database.get_session()
                self.global_settings_id, self.global_settings_name = Query(
                    [models.GlobalSetting.id, models.GlobalSetting.name]
                ).with_session(session)[0]
            finally:
                session.close()

    def get_version(self) -> int:
        # check version
        return self.database.schema.get_version()

    def upgrade(self):
        self.database.schema.upgrade()

    def get_raster_filepaths(self, base_path: Path) -> Dict:
        """Get all raster paths from sqlite based on global_settings id."""

        raster_filepaths = {}
        settings_map = {
            "interflow_settings_id": models.Interflow,
            "simple_infiltration_settings_id": models.SimpleInfiltration,
            "groundwater_settings_id": models.GroundWater,
        }

        try:
            session = self.database.get_session()
            glob_settings = (
                Query(models.GlobalSetting)
                .with_session(session)
                .get(self.global_settings_id)
            )
            settings = [glob_settings]
            for k, v in settings_map.items():
                settings_id = getattr(glob_settings, k)
                if settings_id:
                    settings.append(Query(v).with_session(session).get(settings_id))

            for setting in settings:
                for raster in RASTERS:
                    try:
                        raster_path = getattr(setting, raster)
                        if raster_path:
                            raster_filepaths[raster] = base_path / Path(
                                raster_path.replace("\\", "/")
                            )
                    except AttributeError:
                        pass

            if glob_settings.initial_waterlevel_file:
                raster_filepaths["initial_waterlevel_file"] = base_path / Path(
                    glob_settings.initial_waterlevel_file.replace("\\", "/")
                )
            if glob_settings.initial_groundwater_level_file:
                raster_filepaths["initial_groundwater_level_file"] = base_path / Path(
                    glob_settings.initial_groundwater_level_file.replace("\\", "/")
                )

        finally:
            session.close()


        return raster_filepaths