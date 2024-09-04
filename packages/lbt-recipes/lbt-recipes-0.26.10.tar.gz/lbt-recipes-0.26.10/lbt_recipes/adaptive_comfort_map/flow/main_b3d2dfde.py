"""
This file is auto-generated from adaptive-comfort-map:0.9.1.
It is unlikely that you should be editing this file directly.
Try to edit the original recipe itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    chris: chris@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from . import _queenbee_status_lock_
from .dependencies.comfort_mapping_entry_point import _ComfortMappingEntryPoint_b3d2dfdeOrchestrator as ComfortMappingEntryPoint_b3d2dfdeWorkerbee
from .dependencies.dynamic_contribution_entry_point import _DynamicContributionEntryPoint_b3d2dfdeOrchestrator as DynamicContributionEntryPoint_b3d2dfdeWorkerbee
from .dependencies.dynamic_shade_contrib_entry_point import _DynamicShadeContribEntryPoint_b3d2dfdeOrchestrator as DynamicShadeContribEntryPoint_b3d2dfdeWorkerbee
from .dependencies.radiance_mapping_entry_point import _RadianceMappingEntryPoint_b3d2dfdeOrchestrator as RadianceMappingEntryPoint_b3d2dfdeWorkerbee


_default_inputs = {   'additional_idf': None,
    'air_speed': None,
    'comfort_parameters': '--standard ASHRAE-55',
    'cpu_count': 50,
    'ddy': None,
    'epw': None,
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'run_period': '',
    'simulation_folder': '.',
    'solarcal_parameters': '--posture seated --sharp 135 --absorptivity 0.7 '
                           '--emissivity 0.95'}


class CreateModelOccSchedules(QueenbeeTask):
    """Translate a Model's occupancy schedules into a JSON of 0/1 values.

    This JSON is useful in workflows that compute thermal comfort percent,
    daylight autonomy, etc."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

    threshold = luigi.Parameter(default='0.1')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_model_occ_schedules.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy translate model-occ-schedules model.json --threshold {threshold} --period "{period}" --output-file occ_schedules.json'.format(period=self.period, threshold=self.threshold)

    def output(self):
        return {
            'occ_schedule_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/occupancy_schedules.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.json', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'occ-schedule-json', 'from': 'occ_schedules.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/occupancy_schedules.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'period': self.period,
            'threshold': self.threshold}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.101.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateModelTransSchedules(QueenbeeTask):
    """Translate Model shade transmittance schedules into a JSON of fractional values."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_model_trans_schedules.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy translate model-transmittance-schedules model.json --period "{period}" --output-file trans_schedules.json'.format(period=self.period)

    def output(self):
        return {
            'trans_schedule_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/trans_schedules.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.json', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'trans-schedule-json', 'from': 'trans_schedules.json',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/trans_schedules.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'period': self.period}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.101.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateResultInfo(QueenbeeTask):
    """Get a JSON that specifies the data type and units for comfort map outputs."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def comfort_model(self):
        return 'adaptive'

    @property
    def run_period(self):
        return self._input_params['run_period']

    qualifier = luigi.Parameter(default='')

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_result_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'ladybug-comfort map map-result-info {comfort_model} --run-period "{run_period}" --qualifier "{qualifier}" --folder output --log-file results_info.json'.format(run_period=self.run_period, qualifier=self.qualifier, comfort_model=self.comfort_model)

    def output(self):
        return {
            'temperature_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature/results_info.json').resolve().as_posix()
            ),
            
            'condition_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition/results_info.json').resolve().as_posix()
            ),
            
            'condition_intensity_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity/results_info.json').resolve().as_posix()
            ),
            
            'tcp_vis_metadata': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP/vis_metadata.json').resolve().as_posix()
            ),
            
            'hsp_vis_metadata': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP/vis_metadata.json').resolve().as_posix()
            ),
            
            'csp_vis_metadata': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP/vis_metadata.json').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'temperature-info', 'from': 'output/temperature.json',
                'to': pathlib.Path(self.execution_folder, 'results/temperature/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'condition-info', 'from': 'output/condition.json',
                'to': pathlib.Path(self.execution_folder, 'results/condition/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'condition-intensity-info', 'from': 'output/condition_intensity.json',
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'tcp-vis-metadata', 'from': 'output/TCP.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP/vis_metadata.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'hsp-vis-metadata', 'from': 'output/HSP.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP/vis_metadata.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'csp-vis-metadata', 'from': 'output/CSP.json',
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP/vis_metadata.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'comfort_model': self.comfort_model,
            'run_period': self.run_period,
            'qualifier': self.qualifier}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/ladybug-comfort:0.16.47'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateSimPar(QueenbeeTask):
    """Get a SimulationParameter JSON with all outputs for thermal comfort mapping."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def north(self):
        return self._input_params['north']

    building_type = luigi.Parameter(default='')

    climate_zone = luigi.Parameter(default='')

    efficiency_standard = luigi.Parameter(default='')

    filter_des_days = luigi.Parameter(default='filter-des-days')

    reporting_frequency = luigi.Parameter(default='Hourly')

    @property
    def ddy(self):
        try:
            pathlib.Path(self._input_params['ddy'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['ddy'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_sim_par.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy settings comfort-sim-par input.ddy --run-period "{run_period}" --north {north} --{filter_des_days} --output-file sim_par.json'.format(run_period=self.run_period, north=self.north, filter_des_days=self.filter_des_days)

    def output(self):
        return {
            'sim_par_json': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/simulation_parameter.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'ddy', 'to': 'input.ddy', 'from': self.ddy, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sim-par-json', 'from': 'sim_par.json',
                'to': pathlib.Path(self.execution_folder, 'energy/simulation_parameter.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'run_period': self.run_period,
            'north': self.north,
            'building_type': self.building_type,
            'climate_zone': self.climate_zone,
            'efficiency_standard': self.efficiency_standard,
            'filter_des_days': self.filter_des_days,
            'reporting_frequency': self.reporting_frequency}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.101.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateSkyDome(QueenbeeTask):
    """Create a skydome for daylight coefficient studies."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    sky_density = luigi.Parameter(default='1')

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_sky_dome.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky --sky-density {sky_density}'.format(sky_density=self.sky_density)

    def output(self):
        return {
            'sky_dome': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.dome').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-dome', 'from': 'rflux_sky.sky',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.dome').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'sky_density': self.sky_density}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateViewFactorModifiers(QueenbeeTask):
    """Get a list of modifiers and a corresponding Octree for surface view factors."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def include_sky(self):
        return 'include'

    @property
    def include_ground(self):
        return 'include'

    @property
    def grouped_shades(self):
        return 'grouped'

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_view_factor_modifiers.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance view-factor modifiers model.hbjson --{include_sky}-sky --{include_ground}-ground --{grouped_shades}-shades --name scene'.format(grouped_shades=self.grouped_shades, include_ground=self.include_ground, include_sky=self.include_sky)

    def output(self):
        return {
            'modifiers_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.mod').resolve().as_posix()
            ),
            
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'modifiers-file', 'from': 'scene.mod',
                'to': pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.mod').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'radiance/longwave/resources/scene.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'include_sky': self.include_sky,
            'include_ground': self.include_ground,
            'grouped_shades': self.grouped_shades}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateWea(QueenbeeTask):
    """Translate an .epw file to a .wea file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def period(self):
        return self._input_params['run_period']

    timestep = luigi.Parameter(default='1')

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_wea.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'ladybug translate epw-to-wea weather.epw --analysis-period "{period}" --timestep {timestep} --output-file weather.wea'.format(timestep=self.timestep, period=self.period)

    def output(self):
        return {
            'wea': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/in.wea').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'wea', 'from': 'weather.wea',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/in.wea').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'period': self.period,
            'timestep': self.timestep}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/ladybug:0.42.3'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class DynamicConstructionOutputs(QueenbeeTask):
    """Get an IDF file that requests transmittance outputs for dynamic windows."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def base_idf(self):
        try:
            pathlib.Path(self._input_params['additional_idf'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['additional_idf'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'dynamic_construction_outputs.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy settings dynamic-window-outputs model.json --base-idf base.idf --output-file base.idf'

    def output(self):
        return {
            'dynamic_out_idf': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/additional.idf').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.json', 'from': self.model, 'optional': False},
            {'name': 'base_idf', 'to': 'base.idf', 'from': self.base_idf, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dynamic-out-idf', 'from': 'base.idf',
                'to': pathlib.Path(self.execution_folder, 'energy/additional.idf').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.101.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class GetPrevailingTemperature(QueenbeeTask):
    """Get Adaptive comfort Prevailing Outdoor Temperature from an EPW weather file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def comfort_par(self):
        return self._input_params['comfort_parameters']

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def output_format(self):
        return 'csv'

    @property
    def order_by(self):
        return 'columns'

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'get_prevailing_temperature.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'ladybug-comfort epw prevailing weather.epw --comfort-par "{comfort_par}" --run-period "{run_period}" --{output_format} --{order_by} --output-file prevailing.csv'.format(order_by=self.order_by, run_period=self.run_period, comfort_par=self.comfort_par, output_format=self.output_format)

    def output(self):
        return {
            'prevailing_temperature': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/prevailing.csv').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'prevailing-temperature', 'from': 'prevailing.csv',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/prevailing.csv').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'comfort_par': self.comfort_par,
            'run_period': self.run_period,
            'output_format': self.output_format,
            'order_by': self.order_by}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/ladybug-comfort:0.16.47'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class SetModifiersFromConstructions(QueenbeeTask):
    """Assign honeybee Radiance modifiers based on energy construction properties.

    This includes matching properties for reflectance, absorptance and transmission.
    Furthermore, any dynamic window constructions can be translated to dynamic
    Radiance groups and shade transmittance schedules will be translated to
    dynamic shade groups."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def use_visible(self):
        return 'solar'

    @property
    def exterior_offset(self):
        return '0.02'

    dynamic_behavior = luigi.Parameter(default='dynamic')

    dynamic_shade = luigi.Parameter(default='dynamic')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'set_modifiers_from_constructions.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy edit modifiers-from-constructions model.hbjson --{use_visible} --{dynamic_behavior}-groups --{dynamic_shade}-groups --exterior-offset {exterior_offset} --output-file new_model.hbjson'.format(use_visible=self.use_visible, dynamic_shade=self.dynamic_shade, dynamic_behavior=self.dynamic_behavior, exterior_offset=self.exterior_offset)

    def output(self):
        return {
            'new_model': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/model.hbjson').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'new-model', 'from': 'new_model.hbjson',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/model.hbjson').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'use_visible': self.use_visible,
            'exterior_offset': self.exterior_offset,
            'dynamic_behavior': self.dynamic_behavior,
            'dynamic_shade': self.dynamic_shade}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/lbt-honeybee:0.8.5'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CopyResultInfo(QueenbeeTask):
    """Copy a file or folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateResultInfo']['temperature_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_result_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateResultInfo': CreateResultInfo(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/results_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/results_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/python:3.7-slim'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateDirectSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sky_type(self):
        return 'sun-only'

    @property
    def output_type(self):
        return 'solar'

    @property
    def sun_up_hours(self):
        return 'sun-up-hours'

    cumulative = luigi.Parameter(default='hourly')

    output_format = luigi.Parameter(default='ASCII')

    sky_density = luigi.Parameter(default='1')

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateWea']['wea'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_direct_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sky mtx sky.wea --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(cumulative=self.cumulative, north=self.north, sky_density=self.sky_density, sun_up_hours=self.sun_up_hours, sky_type=self.sky_type, output_type=self.output_type, output_format=self.output_format)

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params)}

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky_direct.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky_direct.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'north': self.north,
            'sky_type': self.sky_type,
            'output_type': self.output_type,
            'sun_up_hours': self.sun_up_hours,
            'cumulative': self.cumulative,
            'output_format': self.output_format,
            'sky_density': self.sky_density}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateRadFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    grid_filter = luigi.Parameter(default='*')

    @property
    def input_model(self):
        value = pathlib.Path(self.input()['SetModifiersFromConstructions']['new_model'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_rad_folder.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid " {grid_filter} " --grid-check'.format(grid_filter=self.grid_filter)

    def requires(self):
        return {'SetModifiersFromConstructions': SetModifiersFromConstructions(_input_params=self._input_params)}

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/model').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature/grids_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'model/grid/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/model').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/temperature/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'grid_filter': self.grid_filter}

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'model/grid/_info.json').resolve().as_posix()}]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateTotalSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sky_type(self):
        return 'total'

    @property
    def output_type(self):
        return 'solar'

    @property
    def sun_up_hours(self):
        return 'sun-up-hours'

    cumulative = luigi.Parameter(default='hourly')

    output_format = luigi.Parameter(default='ASCII')

    sky_density = luigi.Parameter(default='1')

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateWea']['wea'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_total_sky.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sky mtx sky.wea --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(cumulative=self.cumulative, north=self.north, sky_density=self.sky_density, sun_up_hours=self.sun_up_hours, sky_type=self.sky_type, output_type=self.output_type, output_format=self.output_format)

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params)}

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sky.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'north': self.north,
            'sky_type': self.sky_type,
            'output_type': self.output_type,
            'sun_up_hours': self.sun_up_hours,
            'cumulative': self.cumulative,
            'output_format': self.output_format,
            'sky_density': self.sky_density}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class GenerateSunpath(QueenbeeTask):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def output_type(self):
        return '1'

    @property
    def wea(self):
        value = pathlib.Path(self.input()['CreateWea']['wea'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'generate_sunpath.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{output_type} -r {north} -v sky.wea'.format(output_type=self.output_type, north=self.north)

    def requires(self):
        return {'CreateWea': CreateWea(_input_params=self._input_params)}

    def output(self):
        return {
            'sunpath': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sunpath.mtx').resolve().as_posix()
            ),
            
            'sun_modifiers': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/suns.mod').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sunpath', 'from': 'sunpath.mtx',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/sunpath.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'sun-modifiers', 'from': 'suns.mod',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/suns.mod').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'north': self.north,
            'output_type': self.output_type}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RunEnergySimulation(QueenbeeTask):
    """Simulate a Model JSON file in EnergyPlus."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    additional_string = luigi.Parameter(default='')

    report_units = luigi.Parameter(default='none')

    viz_variables = luigi.Parameter(default='')

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sim_par(self):
        try:
            pathlib.Path(self.input()['CreateSimPar']['sim_par_json'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateSimPar']['sim_par_json'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def additional_idf(self):
        try:
            pathlib.Path(self.input()['DynamicConstructionOutputs']['dynamic_out_idf'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['DynamicConstructionOutputs']['dynamic_out_idf'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'run_energy_simulation.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-energy simulate model model.hbjson weather.epw --sim-par-json sim-par.json --measures measures --additional-string "{additional_string}" --additional-idf additional.idf --report-units {report_units} --folder output {viz_variables}'.format(report_units=self.report_units, additional_string=self.additional_string, viz_variables=self.viz_variables)

    def requires(self):
        return {'CreateSimPar': CreateSimPar(_input_params=self._input_params), 'DynamicConstructionOutputs': DynamicConstructionOutputs(_input_params=self._input_params)}

    def output(self):
        return {
            'sql': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/eplusout.sql').resolve().as_posix()
            ),
            
            'idf': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'energy/in.idf').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model.hbjson', 'from': self.model, 'optional': False},
            {'name': 'epw', 'to': 'weather.epw', 'from': self.epw, 'optional': False},
            {'name': 'sim_par', 'to': 'sim-par.json', 'from': self.sim_par, 'optional': True},
            {'name': 'additional_idf', 'to': 'additional.idf', 'from': self.additional_idf, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sql', 'from': 'output/run/eplusout.sql',
                'to': pathlib.Path(self.execution_folder, 'energy/eplusout.sql').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'idf', 'from': 'output/run/in.idf',
                'to': pathlib.Path(self.execution_folder, 'energy/in.idf').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'additional_string': self.additional_string,
            'report_units': self.report_units,
            'viz_variables': self.viz_variables}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-energy:1.101.19'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CopyGridInfo(QueenbeeTask):
    """Copy a file or folder to multiple destinations."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_grid_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst_1': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition/grids_info.json').resolve().as_posix()
            ),
            
            'dst_2': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity/grids_info.json').resolve().as_posix()
            ),
            
            'dst_3': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP/grids_info.json').resolve().as_posix()
            ),
            
            'dst_4': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP/grids_info.json').resolve().as_posix()
            ),
            
            'dst_5': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP/grids_info.json').resolve().as_posix()
            ),
            
            'dst_6': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/grids_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst-1', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'results/condition/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-2', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-3', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-4', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-5', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-6', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/python:3.7-slim'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateDynamicOctrees(QueenbeeTask):
    """Generate a set of octrees from a folder containing abstracted aperture groups."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sunpath(self):
        try:
            pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_dynamic_octrees.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-abstracted-groups model --sun-path sunpath.mtx --output-folder octree'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            
            'scene_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/dynamic_groups').resolve().as_posix()
            ),
            'scene_info': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'octree/group_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sunpath', 'to': 'sunpath.mtx', 'from': self.sunpath, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-folder', 'from': 'octree',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/dynamic_groups').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def output_parameters(self):
        return [{'name': 'scene-info', 'from': 'octree/group_info.json', 'to': pathlib.Path(self.params_folder, 'octree/group_info.json').resolve().as_posix()}]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_octree.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out}'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'black_out': self.black_out,
            'include_aperture': self.include_aperture}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateOctreeWithSuns(QueenbeeTask):
    """Generate an octree from a Radiance folder and a sky!"""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_octree_with_suns.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out} --add-before sky.sky'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene_with_suns.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sky', 'to': 'sky.sky', 'from': self.sky, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/scene_with_suns.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'black_out': self.black_out,
            'include_aperture': self.include_aperture}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CreateShadeTransOctrees(QueenbeeTask):
    """Generate a set of octrees from a folder containing shade transmittance groups."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sunpath(self):
        try:
            pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'create_shade_trans_octrees.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance octree from-shade-trans-groups model --sun-path sunpath.mtx --output-folder octree'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            
            'scene_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/dynamic_shades').resolve().as_posix()
            ),
            'scene_info': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'octree/trans_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False},
            {'name': 'sunpath', 'to': 'sunpath.mtx', 'from': self.sunpath, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-folder', 'from': 'octree',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/resources/dynamic_shades').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def output_parameters(self):
        return [{'name': 'scene-info', 'from': 'octree/trans_info.json', 'to': pathlib.Path(self.params_folder, 'octree/trans_info.json').resolve().as_posix()}]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class ParseSunUpHours(QueenbeeTask):
    """Parse sun up hours from sun modifiers file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'parse_sun_up_hours.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod --name sun-up-hours.txt'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params)}

    def output(self):
        return {
            'sun_up_hours': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/shortwave/sun-up-hours.txt').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sun_modifiers', 'to': 'suns.mod', 'from': self.sun_modifiers, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-up-hours', 'from': 'sun-up-hours.txt',
                'to': pathlib.Path(self.execution_folder, 'radiance/shortwave/sun-up-hours.txt').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class SplitGridFolder(QueenbeeTask):
    """Create new sensor grids folder with evenly distributed sensors.

    This function creates a new folder with evenly distributed sensor grids. The folder
    will include a ``_redist_info.json`` file which has the information to recreate the
    original input files from this folder and the results generated based on the grids
    in this folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def cpus_per_grid(self):
        return '3'

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def input_folder(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'grid')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'split_grid_folder.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder {cpu_count} --grid-divisor {cpus_per_grid} --min-sensor-count {min_sensor_count}'.format(cpu_count=self.cpu_count, min_sensor_count=self.min_sensor_count, cpus_per_grid=self.cpus_per_grid)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/grid').resolve().as_posix()
            ),
            
            'dist_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/results/temperature/_redist_info.json').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'radiance/grid/_split_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output_folder/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'radiance/grid').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dist-info', 'from': 'output_folder/_redist_info.json',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results/temperature/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'output_folder/_info.json',
                'to': pathlib.Path(self.execution_folder, 'radiance/grid/_split_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def input_parameters(self):
        return {
            'cpu_count': self.cpu_count,
            'cpus_per_grid': self.cpus_per_grid,
            'min_sensor_count': self.min_sensor_count}

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'output_folder/_info.json', 'to': pathlib.Path(self.params_folder, 'output_folder/_info.json').resolve().as_posix()}]

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class CopyRedistInfo(QueenbeeTask):
    """Copy a file or folder to multiple destinations."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['dist_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'copy_redist_info.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst_1': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/results/condition/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_2': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/results/condition_intensity/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_3': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/metrics/TCP/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_4': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/metrics/HSP/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_5': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/metrics/CSP/_redist_info.json').resolve().as_posix()
            ),
            
            'dst_6': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/conditions/_redist_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst-1', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results/condition/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-2', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/results/condition_intensity/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-3', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics/TCP/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-4', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics/HSP/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-5', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/metrics/CSP/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dst-6', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/conditions/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
}

    @property
    def task_image(self):
        return 'docker.io/python:3.7-slim'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RunRadianceSimulationLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['CreateOctreeWithSuns']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['CreateOctree']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_view_factor(self):
        value = pathlib.Path(self.input()['CreateViewFactorModifiers']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['output_folder'].path, '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['CreateSkyDome']['sky_dome'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['CreateTotalSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self.input()['CreateDirectSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view_factor_modifiers(self):
        value = pathlib.Path(self.input()['CreateViewFactorModifiers']['modifiers_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'radiance_parameters': self.radiance_parameters,
            'model': self.model,
            'octree_file_with_suns': self.octree_file_with_suns,
            'octree_file': self.octree_file,
            'octree_file_view_factor': self.octree_file_view_factor,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sensor_count': self.sensor_count,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers,
            'view_factor_modifiers': self.view_factor_modifiers
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [RadianceMappingEntryPoint_b3d2dfdeWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_simulation.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'CreateOctreeWithSuns': CreateOctreeWithSuns(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateDirectSky': CreateDirectSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'CreateViewFactorModifiers': CreateViewFactorModifiers(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_simulation.done').resolve().as_posix())
        }


class RunRadianceSimulation(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['SplitGridFolder']['sensor_grids'].path

    def run(self):
        yield [RunRadianceSimulationLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_simulation.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'CreateOctreeWithSuns': CreateOctreeWithSuns(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateDirectSky': CreateDirectSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'CreateViewFactorModifiers': CreateViewFactorModifiers(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_simulation.done').resolve().as_posix())
        }


class RunRadianceDynamicContributionLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def group_name(self):
        return self.item['identifier']

    @property
    def result_sql(self):
        value = pathlib.Path(self.input()['RunEnergySimulation']['sql'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_spec(self):
        value = pathlib.Path(self.input()['CreateDynamicOctrees']['scene_folder'].path, '{item_identifier}/{item_spec}'.format(item_spec=self.item['spec'], item_identifier=self.item['identifier']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_diff(self):
        value = pathlib.Path(self.input()['CreateDynamicOctrees']['scene_folder'].path, '{item_identifier}/{item_diff}'.format(item_diff=self.item['diff'], item_identifier=self.item['identifier']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['CreateDynamicOctrees']['scene_folder'].path, '{item_identifier}/{item_sun}'.format(item_identifier=self.item['identifier'], item_sun=self.item['sun']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid_folder(self):
        value = pathlib.Path('radiance/shortwave/grids')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['sensor_grids_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['CreateSkyDome']['sky_dome'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['CreateTotalSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self.input()['CreateDirectSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['ParseSunUpHours']['sun_up_hours'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'radiance_parameters': self.radiance_parameters,
            'result_sql': self.result_sql,
            'octree_file_spec': self.octree_file_spec,
            'octree_file_diff': self.octree_file_diff,
            'octree_file_with_suns': self.octree_file_with_suns,
            'group_name': self.group_name,
            'sensor_grid_folder': self.sensor_grid_folder,
            'sensor_grids': self.sensor_grids,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers,
            'sun_up_hours': self.sun_up_hours
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DynamicContributionEntryPoint_b3d2dfdeWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateDirectSky': CreateDirectSky(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'CreateDynamicOctrees': CreateDynamicOctrees(_input_params=self._input_params), 'RunEnergySimulation': RunEnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done').resolve().as_posix())
        }


class RunRadianceDynamicContribution(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def scene_info(self):
        value = pathlib.Path(self.input()['CreateDynamicOctrees']['scene_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.scene_info)
        except:
            # it is a parameter
            return self.input()['CreateDynamicOctrees']['scene_info'].path

    def run(self):
        yield [RunRadianceDynamicContributionLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateDirectSky': CreateDirectSky(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'CreateDynamicOctrees': CreateDynamicOctrees(_input_params=self._input_params), 'RunEnergySimulation': RunEnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_dynamic_contribution.done').resolve().as_posix())
        }


class RunRadianceShadeContributionLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def group_name(self):
        return self.item['identifier']

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['CreateShadeTransOctrees']['scene_folder'].path, self.item['default'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def octree_file_with_suns(self):
        value = pathlib.Path(self.input()['CreateShadeTransOctrees']['scene_folder'].path, self.item['sun'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid_folder(self):
        value = pathlib.Path('radiance/shortwave/grids')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['sensor_grids_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['CreateSkyDome']['sky_dome'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['CreateTotalSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix_direct(self):
        value = pathlib.Path(self.input()['CreateDirectSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['ParseSunUpHours']['sun_up_hours'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'radiance').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'radiance_parameters': self.radiance_parameters,
            'octree_file': self.octree_file,
            'octree_file_with_suns': self.octree_file_with_suns,
            'group_name': self.group_name,
            'sensor_grid_folder': self.sensor_grid_folder,
            'sensor_grids': self.sensor_grids,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'sky_matrix_direct': self.sky_matrix_direct,
            'sun_modifiers': self.sun_modifiers,
            'sun_up_hours': self.sun_up_hours
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [DynamicShadeContribEntryPoint_b3d2dfdeWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateDirectSky': CreateDirectSky(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'CreateShadeTransOctrees': CreateShadeTransOctrees(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done').resolve().as_posix())
        }


class RunRadianceShadeContribution(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def scene_info(self):
        value = pathlib.Path(self.input()['CreateShadeTransOctrees']['scene_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.scene_info)
        except:
            # it is a parameter
            return self.input()['CreateShadeTransOctrees']['scene_info'].path

    def run(self):
        yield [RunRadianceShadeContributionLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateDirectSky': CreateDirectSky(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'CreateShadeTransOctrees': CreateShadeTransOctrees(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_radiance_shade_contribution.done').resolve().as_posix())
        }


class RunComfortMapLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def run_period(self):
        return self._input_params['run_period']

    @property
    def solarcal_par(self):
        return self._input_params['solarcal_parameters']

    @property
    def comfort_parameters(self):
        return self._input_params['comfort_parameters']

    solarcal_parameters = luigi.Parameter(default='--posture seated --sharp 135 --absorptivity 0.7 --emissivity 0.95')

    @property
    def epw(self):
        value = pathlib.Path(self._input_params['epw'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def result_sql(self):
        value = pathlib.Path(self.input()['RunEnergySimulation']['sql'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def enclosure_info(self):
        value = pathlib.Path('radiance/enclosures', '{item_full_id}.json'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def view_factors(self):
        value = pathlib.Path('radiance/longwave/view_factors', '{item_full_id}.csv'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def modifiers(self):
        value = pathlib.Path(self.input()['CreateViewFactorModifiers']['modifiers_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def indirect_irradiance(self):
        value = pathlib.Path('radiance/shortwave/results/indirect', '{item_full_id}.ill'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def direct_irradiance(self):
        value = pathlib.Path('radiance/shortwave/results/direct', '{item_full_id}.ill'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def ref_irradiance(self):
        value = pathlib.Path('radiance/shortwave/results/reflected', '{item_full_id}.ill'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['ParseSunUpHours']['sun_up_hours'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def contributions(self):
        try:
            pathlib.Path('radiance/shortwave/dynamic/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path('radiance/shortwave/dynamic/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def transmittance_contribs(self):
        try:
            pathlib.Path('radiance/shortwave/shd_trans/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path('radiance/shortwave/shd_trans/final/{item_full_id}'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def trans_schedules(self):
        value = pathlib.Path(self.input()['CreateModelTransSchedules']['trans_schedule_json'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def occ_schedules(self):
        value = pathlib.Path(self.input()['CreateModelOccSchedules']['occ_schedule_json'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def air_speed(self):
        try:
            pathlib.Path(self._input_params['air_speed'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['air_speed'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def prevailing(self):
        value = pathlib.Path(self.input()['GetPrevailingTemperature']['prevailing_temperature'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'epw': self.epw,
            'result_sql': self.result_sql,
            'grid_name': self.grid_name,
            'enclosure_info': self.enclosure_info,
            'view_factors': self.view_factors,
            'modifiers': self.modifiers,
            'indirect_irradiance': self.indirect_irradiance,
            'direct_irradiance': self.direct_irradiance,
            'ref_irradiance': self.ref_irradiance,
            'sun_up_hours': self.sun_up_hours,
            'contributions': self.contributions,
            'transmittance_contribs': self.transmittance_contribs,
            'trans_schedules': self.trans_schedules,
            'occ_schedules': self.occ_schedules,
            'run_period': self.run_period,
            'air_speed': self.air_speed,
            'prevailing': self.prevailing,
            'solarcal_par': self.solarcal_par,
            'comfort_parameters': self.comfort_parameters
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [ComfortMappingEntryPoint_b3d2dfdeWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'run_comfort_map.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'GetPrevailingTemperature': GetPrevailingTemperature(_input_params=self._input_params), 'CreateViewFactorModifiers': CreateViewFactorModifiers(_input_params=self._input_params), 'CreateModelOccSchedules': CreateModelOccSchedules(_input_params=self._input_params), 'CreateModelTransSchedules': CreateModelTransSchedules(_input_params=self._input_params), 'RunEnergySimulation': RunEnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'RunRadianceDynamicContribution': RunRadianceDynamicContribution(_input_params=self._input_params), 'RunRadianceShadeContribution': RunRadianceShadeContribution(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_comfort_map.done').resolve().as_posix())
        }


class RunComfortMap(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['SplitGridFolder']['sensor_grids'].path

    def run(self):
        yield [RunComfortMapLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'run_comfort_map.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'GetPrevailingTemperature': GetPrevailingTemperature(_input_params=self._input_params), 'CreateViewFactorModifiers': CreateViewFactorModifiers(_input_params=self._input_params), 'CreateModelOccSchedules': CreateModelOccSchedules(_input_params=self._input_params), 'CreateModelTransSchedules': CreateModelTransSchedules(_input_params=self._input_params), 'RunEnergySimulation': RunEnergySimulation(_input_params=self._input_params), 'RunRadianceSimulation': RunRadianceSimulation(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params), 'RunRadianceDynamicContribution': RunRadianceDynamicContribution(_input_params=self._input_params), 'RunRadianceShadeContribution': RunRadianceShadeContribution(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'run_comfort_map.done').resolve().as_posix())
        }


class RestructureConditionIntensityResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/results/condition_intensity')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_condition_intensity_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition_intensity').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'results/condition_intensity').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureConditionResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/results/condition')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_condition_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/condition').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'results/condition').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureCspResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/metrics/CSP')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_csp_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/CSP').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'metrics/CSP').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureHspResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/metrics/HSP')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_hsp_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/HSP').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'metrics/HSP').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureTcpResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/metrics/TCP')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_tcp_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/TCP').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'metrics/TCP').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class RestructureTemperatureResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()
    _status_lock = _queenbee_status_lock_

    # Task inputs
    @property
    def extension(self):
        return 'csv'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/results/temperature')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def __script__(self):
        return pathlib.Path(__file__).parent.joinpath('scripts', 'restructure_temperature_results.py').resolve()

    @property
    def is_script(self):
        return False

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'RunComfortMap': RunComfortMap(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/temperature').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'results/temperature').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def input_parameters(self):
        return {
            'extension': self.extension}

    @property
    def task_image(self):
        return 'docker.io/ladybugtools/honeybee-radiance:1.65.36'

    @property
    def image_workdir(self):
        return '/home/ladybugbot/run'


class _Main_b3d2dfdeOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CopyResultInfo(_input_params=self.input_values), CopyGridInfo(_input_params=self.input_values), CopyRedistInfo(_input_params=self.input_values), RestructureConditionIntensityResults(_input_params=self.input_values), RestructureConditionResults(_input_params=self.input_values), RestructureCspResults(_input_params=self.input_values), RestructureHspResults(_input_params=self.input_values), RestructureTcpResults(_input_params=self.input_values), RestructureTemperatureResults(_input_params=self.input_values)]
