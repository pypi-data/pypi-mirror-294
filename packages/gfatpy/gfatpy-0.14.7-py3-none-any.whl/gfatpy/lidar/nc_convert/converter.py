from datetime import datetime
import re
import sys
from pathlib import Path
import atexit

from linc.config import get_config
from loguru import logger

from gfatpy.utils.io import find_nearest_filepath
from .types import Measurement

from .utils import (
    cleanup_tmp_folders,
    filter_by_type,
    launch_write_nc,
    to_measurements,
)
from gfatpy.lidar.utils.types import LidarName, MeasurementType, Telescope


CONFIGS_DIR = Path(__file__).parent / "configs"

logger.add(sys.stdout, level="INFO")

# Register cleanup function to be executed when the interpreter exits
atexit.register(cleanup_tmp_folders)


def measurements_to_nc(
    measurements: list[Measurement],
    lidar_name: LidarName,
    telescope: Telescope = Telescope.xf,
    raw_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
    config_file: Path | str | None = None,
    number_of_previous_days: int = 5,
) -> None:
    """Converts raw data to netcdf files.

    Args:

        - measurements (list[Measurement]): Measurements to convert.
        - lidar_name (LidarName): Name of the lidar.
        - telescope (Telescope, optional): Telescope used. Defaults to Telescope.xf.
        - raw_dir (Path | str | None, optional): Raw data directory where previous data will be searched. Defaults to None means no previous data are searched.
        - output_dir (Path | str | None, optional): Output directory. Defaults to None.
        - config_file (Path | str | None, optional): Configuration file. Defaults to None.
        - number_of_previous_days (int, optional): Number of previous days to search. Defaults to 5.
        - convert_dc (bool, optional): Force conversion of ALL DC measurements. Defaults to False means only DC linked to other files will be converted.

    Raises:

        - ValueError: Value of output_dir is not a directory.
        - ValueError: Value of raw_dir is not a directory.
        - Exception: Linked DC measurement to RS|HF not found.
        - Exception: Linked DC measurement to DP|TC|OT not found.
    """

    rs_measurements = filter_by_type(measurements, MeasurementType.RS)
    hf_measurements = filter_by_type(measurements, MeasurementType.HF)
    dc_measurements = filter_by_type(measurements, MeasurementType.DC)
    dp_measurements = filter_by_type(measurements, MeasurementType.DP)
    tc_measurements = filter_by_type(measurements, MeasurementType.TC)
    ot_measurements = filter_by_type(measurements, MeasurementType.OT)

    if len(rs_measurements) != 0:
        rs_hf_measurements_to_nc(
            rs_measurements,
            lidar_name,
            telescope,
            raw_dir,
            output_dir,
            config_file,
            number_of_previous_days,
            measurement_type=MeasurementType.RS,
        )
    if len(hf_measurements) != 0:
        rs_hf_measurements_to_nc(
            hf_measurements,
            lidar_name,
            telescope,
            raw_dir,
            output_dir,
            config_file,
            number_of_previous_days,
            measurement_type=MeasurementType.HF,
        )
    if len(dc_measurements) != 0:
        dc_measurements_to_nc(
            dc_measurements,
            lidar_name,
            telescope,
            raw_dir,
            output_dir,
            config_file,
        )
    if len(dp_measurements) != 0:
        dp_tc_ot_measurements_to_nc(
            dp_measurements,
            lidar_name,
            telescope,
            raw_dir,
            output_dir,
            config_file,
            measurement_type=MeasurementType.DP,
        )
    if len(tc_measurements) != 0:
        dp_tc_ot_measurements_to_nc(
            tc_measurements,
            lidar_name,
            telescope,
            raw_dir,
            output_dir,
            config_file,
            measurement_type=MeasurementType.TC,
        )
    if len(ot_measurements) != 0:
        dp_tc_ot_measurements_to_nc(
            ot_measurements,
            lidar_name,
            telescope,
            raw_dir,
            output_dir,
            config_file,
            measurement_type=MeasurementType.OT,
        )


def rs_hf_measurements_to_nc(
    measurements,
    lidar_name: LidarName,
    telescope: Telescope = Telescope.xf,
    raw_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
    config_file: Path | str | None = None,
    number_of_previous_days: int = 5,
    measurement_type: MeasurementType = MeasurementType.RS,
) -> None:
    """Converts raw data to netcdf files.

    Args:

        - measurements (list[Measurement]): Measurements to convert.
        - lidar_name (LidarName): Name of the lidar.
        - telescope (Telescope, optional): Telescope used. Defaults to Telescope.xf.
        - raw_dir (Path | str | None, optional): Raw data directory where previous data will be searched. Defaults to None means no previous data are searched.
        - output_dir (Path | str | None, optional): Output directory. Defaults to None.
        - config_file (Path | str | None, optional): Configuration file. Defaults to None.
        - number_of_previous_days (int, optional): Number of previous days to search. Defaults to 5.
        - convert_dc (bool, optional): Force conversion of ALL DC measurements. Defaults to False means only DC linked to other files will be converted.

    Raises:

        - ValueError: Value of output_dir is not a directory.
        - ValueError: Value of raw_dir is not a directory.
        - Exception: Linked DC measurement to RS|HF not found.
        - Exception: Linked DC measurement to DP|TC|OT not found.
    """

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    elif output_dir is None:
        output_dir = Path.cwd()

    if not output_dir.exists() or not output_dir.is_dir():
        raise ValueError(f"{output_dir} not found.")

    # Get lidar configuration file
    target_datetime = measurements[0].datetime
    config_filepath = search_config_file(lidar_name, target_datetime, config_file)
    config = get_config(config_filepath)

    search_previous_days = True

    # Check directory where data of previous days should be stored
    if isinstance(raw_dir, str):
        raw_dir = Path(raw_dir)
        if not raw_dir.exists() or not raw_dir.is_dir():
            raise ValueError(f"{raw_dir} not found.")
    elif raw_dir is None:
        search_previous_days = False

    measurements = filter_by_type(measurements, measurement_type)

    if len(measurements) == 0:
        return None
    # get the first measurement:
    measurement = measurements[0]

    # Add measurements of the same type and date to the measurement object
    measurement.linked_measurements = [
        m
        for m in measurements
        if m.path != measurement.path
        and m.type == measurement_type
        and m.datetime.date() == measurement.datetime.date()
    ]

    # Add previous days to the search
    if search_previous_days:
        prev_paths = measurement.find_prev_paths(
            number_of_previous_days, lidar_name, raw_dir  # type: ignore
        )
        for prev_path in prev_paths:
            prev_measurements = to_measurements(prev_path.glob("[RH][SF]*"))
            if len(prev_measurements) != 0:
                linked_ = [
                    prev_
                    for prev_ in prev_measurements
                    if prev_.has_target_date(measurement.datetime)
                ]
                measurement.add_linked_measurements(linked_)

    signal_type = measurement_type
    try:
        files2convert = measurement.get_filepaths()
    except Exception as e:
        raise RuntimeError(f"Error in {measurement.path}: {e}")
    if len(files2convert) != 0:
        launch_write_nc(
            measurement,
            files2convert,
            output_dir,
            lidar_name,
            telescope,
            signal_type,
            config,
        )
    return None


def dc_measurements_to_nc(
    measurements,
    lidar_name: LidarName,
    telescope: Telescope = Telescope.xf,
    raw_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
    config_file: Path | str | None = None,
) -> None:
    """Converts raw data to netcdf files.

    Args:

        - measurements (list[Measurement]): Measurements to convert.
        - lidar_name (LidarName): Name of the lidar.
        - telescope (Telescope, optional): Telescope used. Defaults to Telescope.xf.
        - raw_dir (Path | str | None, optional): Raw data directory where previous data will be searched. Defaults to None means no previous data are searched.
        - output_dir (Path | str | None, optional): Output directory. Defaults to None.
        - config_file (Path | str | None, optional): Configuration file. Defaults to None.

    Raises:

        - ValueError: Value of output_dir is not a directory.
        - ValueError: Value of raw_dir is not a directory.
        - Exception: Linked DC measurement to RS|HF not found.
        - Exception: Linked DC measurement to DP|TC|OT not found.
    """

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    elif output_dir is None:
        output_dir = Path.cwd()

    if not output_dir.exists() or not output_dir.is_dir():
        raise ValueError(f"{output_dir} not found.")

    # Get lidar configuration file
    target_datetime = measurements[0].datetime
    config_filepath = search_config_file(lidar_name, target_datetime, config_file)
    config = get_config(config_filepath)

    # Check directory where data of previous days should be stored
    if isinstance(raw_dir, str):
        raw_dir = Path(raw_dir)
        if not raw_dir.exists() or not raw_dir.is_dir():
            raise ValueError(f"{raw_dir} not found.")

    measurements = filter_by_type(measurements, MeasurementType.DC)

    if len(measurements) == 0:
        return None
    for measurement in measurements:
        # Gather files to convert
        files2convert = measurement.get_filepaths()
        if len(files2convert) != 0:
            launch_write_nc(
                measurement,
                files2convert,
                output_dir,
                lidar_name,
                telescope,
                signal_type=MeasurementType.RS,
                config=config,
            )
    return None


def dp_tc_ot_measurements_to_nc(
    measurements,
    lidar_name: LidarName,
    telescope: Telescope = Telescope.xf,
    raw_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
    config_file: Path | str | None = None,
    measurement_type: MeasurementType = MeasurementType.DP,
) -> None:
    """Converts raw data to netcdf files.

    Args:

        - measurements (list[Measurement]): Measurements to convert.
        - lidar_name (LidarName): Name of the lidar.
        - telescope (Telescope, optional): Telescope used. Defaults to Telescope.xf.
        - raw_dir (Path | str | None, optional): Raw data directory where previous data will be searched. Defaults to None means no previous data are searched.
        - output_dir (Path | str | None, optional): Output directory. Defaults to None.
        - config_file (Path | str | None, optional): Configuration file. Defaults to None.
        - number_of_previous_days (int, optional): Number of previous days to search. Defaults to 5.
        - convert_dc (bool, optional): Force conversion of ALL DC measurements. Defaults to False means only DC linked to other files will be converted.

    Raises:

        - ValueError: Value of output_dir is not a directory.
        - ValueError: Value of raw_dir is not a directory.
        - Exception: Linked DC measurement to RS|HF not found.
        - Exception: Linked DC measurement to DP|TC|OT not found.
    """

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    elif output_dir is None:
        output_dir = Path.cwd()

    if not output_dir.exists() or not output_dir.is_dir():
        raise ValueError(f"{output_dir} not found.")

    # Get lidar configuration file
    target_datetime = measurements[0].datetime
    config_filepath = search_config_file(lidar_name, target_datetime, config_file)
    config = get_config(config_filepath)

    # Check directory where data of previous days should be stored
    if isinstance(raw_dir, str):
        raw_dir = Path(raw_dir)
        if not raw_dir.exists() or not raw_dir.is_dir():
            raise ValueError(f"{raw_dir} not found.")

    measurements = filter_by_type(measurements, measurement_type)
    if len(measurements) == 0:
        return None

    for measurement in measurements:
        # files2convert is taken for each subfolder
        for subdir in measurement.sub_dirs:
            if subdir == measurement.datetime.strftime("%Y%m%d"):
                continue
            try:
                escaped_subdir = re.escape(subdir)
                files2convert = measurement.get_filepaths(
                    pattern_or_list=rf".*{escaped_subdir}.*"
                )
            except:
                raise RuntimeError(f"Error in {measurement.path}")
            if len(files2convert) != 0:
                launch_write_nc(
                    measurement,
                    files2convert,
                    output_dir,
                    lidar_name,
                    telescope,
                    subdir,
                    config,
                )
    return None


def search_config_file(
    lidar_name: LidarName,
    target_datetime: datetime,
    opt_config: Path | str | None,
) -> Path:
    """Searches for a configuration file.

    Args:
        lidar_name (LidarName): Name of the lidar.
        opt_config (Path | str | None, optional): Path to the configuration file. Defaults to None.

    Raises:
        FileNotFoundError: No configution file found in opt_config.

    Returns:
        Config: Configuration object.
    """
    if opt_config is not None:
        if isinstance(opt_config, Path):
            config_path = opt_config
        elif isinstance(opt_config, str):
            config_path = Path(opt_config)

        if not config_path.exists():
            raise FileNotFoundError(f"Configution file {opt_config} not found.")
    else:
        config_dir = Path(__file__).parent / "configs"
        config_path = find_nearest_filepath(
            config_dir,
            f"{lidar_name.value}*.toml",
            1,
            target_datetime,
            and_previous=True,
        )
        if not config_path.exists():
            raise FileNotFoundError(f"No configution file found in {config_dir}")
    return config_path
