import os
import glob

from datetime import datetime, timedelta
from obspy import Stream, read, UTCDateTime
from typing import List
from .utilities import (
    validate_directory_structure,
    trimming_trace,
    directory_structures_group,
)


class Search:
    def __init__(self,
                 input_dir: str,
                 directory_structure: str,
                 network: str = '*',
                 station: str = '*',
                 channel: str = '*',
                 location: str = '*',
                 check_file_integrity: bool = False,):
        """Search sesimic files and return as daily seismic Stream

        Args:
            input_dir (str): input directory path
            directory_structure (str): input directory structure
            network (str): input network name
            station (str): input station name
            channel (str): input channel name
            location (str): input location name
            check_file_integrity (bool, optional): check file integrity. Defaults to False.
        """
        self.input_dir = input_dir
        self.directory_structure = validate_directory_structure(directory_structure)
        self.network = network
        self.station = station
        self.channel = channel
        self.location = location
        self.select = {
            'network': network,
            'station': station,
            'location': location,
            'component': channel,
        }
        self.check_file_integrity = check_file_integrity

    def check_integrity(self,
                        seismic_dir: str,
                        prefix: str = 'ERROR',
                        input_dir: str = None,
                        channel: str = None) -> None:
        """Check file integrity

        Args:
            seismic_dir: Seismic directory
            prefix (str): prefix. Default 'ERROR'
            input_dir (str): input directory path
            channel (str): input channel name. For SAC

        Returns:
            None
        """
        seismic_files: List[str] = glob.glob(seismic_dir)
        error_list: List[str] = []

        if len(seismic_files) > 0:
            for seismic_file in seismic_files:
                try:
                    read(seismic_file, headonly=True)
                except Exception as e:
                    if len(str(e)) > 0:
                        error_list.append(seismic_file)

        if len(error_list) > 0:
            for error_file in error_list:
                _basedir: str = os.path.dirname(error_file)
                _basename: str = os.path.basename(error_file)

                _file_error = f"{prefix}_{_basename}"
                if channel is not None:
                    _file_error = _file_error.replace('.', '__')

                if input_dir is not None:
                    _basedir: str = self.input_dir

                _fix_file: str = os.path.join(_basedir, _file_error)

                os.rename(
                    error_file,
                    _fix_file
                )
                print(f"⚠️➡️ {error_file} -> {_fix_file}")

        return None

    @staticmethod
    def merged(stream: Stream, date_str: str) -> Stream:
        """Merging seismic data into daily seismic data.

        Args:
            stream (Stream): Stream object
            date_str (str): Date in yyyy-mm-dd format

        Returns:
            Stream: Stream object
        """
        start_time: UTCDateTime = UTCDateTime(date_str)
        end_time: UTCDateTime = UTCDateTime(f"{date_str}T23:59:59")
        return trimming_trace(stream, start_time, end_time)

    def sac(self, date_str: str) -> Stream:
        """Read SAC data structure.

        <earthworm_dir>/ContinuousSAC/YYYYMM/YYYYMMDD_HHMM00_MAN/<per_channel>

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        import warnings
        warnings.filterwarnings("error")

        channels: List[str] = [self.channel]
        if (self.channel == '*') or (self.channel is None):
            channels: List[str] = ['H', 'EH']

        _date_str: str = date_str.replace('-', '')
        _date_str = f"{_date_str}*"
        yyyy_mm: str = _date_str[0:6]

        stream: Stream = Stream()

        for channel in channels:
            seismic_dir: str = os.path.join(self.input_dir, yyyy_mm, _date_str, f"*.{channel}*")

            while True:
                try:
                    temp_stream: Stream = read(seismic_dir)
                    stream = stream + temp_stream
                    stream = stream.select(**self.select)
                except Exception as e:
                    print(f'⛔ {date_str} - self.sac() :: {e}')
                    if self.check_file_integrity is True:
                        print(f"⚠️ {date_str} - Checking integrity :: {e}")
                        self.check_integrity(seismic_dir=seismic_dir, channel=channel)
                    break
                else:
                    break

        return stream

    def seisan(self, date_str: str) -> Stream:
        """Read seisan data structure.

        <earthworm_dir>/Continuous/YYYY-MM-DD-hhmm-00S.MAN__<nunber_of_channels>

        Example data per 10 minutes:
            <earthworm_dir>/Continuous/2021-12-04-1620-00S.MAN___003
            <earthworm_dir>/Continuous/2021-12-04-1630-00S.MAN___003

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        import warnings
        warnings.filterwarnings("error")

        wildcard: str = "{}*".format(date_str)
        seismic_dir: str = os.path.join(self.input_dir, wildcard)

        stream : Stream = Stream()

        while True:
            try:
                stream: Stream = read(seismic_dir)
                stream = stream.select(**self.select)
            except Exception as e:
                print(f'⛔ {date_str} - self.seisan() :: {e}')
                if self.check_file_integrity is True:
                    print(f"⚠️ {date_str} - Checking integrity :: {e}")
                    self.check_integrity(seismic_dir=seismic_dir)
                break
            else:
                break

        return stream

    def ijen(self, date_str: str) -> Stream:
        """Read Ijen seismic directory

        <seismic_dir>/YYYY/YYYYMMDD/Set00/<per_channel>

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        input_dir = self.input_dir
        stream = Stream()

        current_day_obj = datetime.strptime(date_str, '%Y-%m-%d')
        current_year: str = current_day_obj.strftime('%Y')
        current_yyyymmdd: str = current_day_obj.strftime('%Y%m%d')

        _seismic_dir: str = os.path.join(input_dir, current_year, current_yyyymmdd)

        if os.path.exists(_seismic_dir):
            try:
                seismic_dir: str = os.path.join(_seismic_dir, '*', '{}*'.format(date_str))
                stream: Stream = read(seismic_dir)
                stream = stream.select(**self.select)
            except Exception as e:
                print(f'⛔ {date_str} - self.ijen():: {e}')
                return stream

        if stream.count() > 0:
            next_day_obj = current_day_obj + timedelta(days=1)
            next_day_year: str = next_day_obj.strftime('%Y')
            next_day_yyyymmdd: str = next_day_obj.strftime('%Y%m%d')

            try:
                next_dir: str = os.path.join(input_dir, next_day_year, next_day_yyyymmdd,
                                             '*', '{}-2350-*'.format(date_str))
                next_stream = read(next_dir)
                stream: Stream = stream + next_stream
            except:
                return stream

        return stream

    def idds(self, date_str: str) -> Stream:
        """Search seismic data based on IDDS format.

        <seismic_dir>/YEAR/NET/STA/CHAN.TYPE/DAY/NET.STA.LOC.CHAN.TYPE.YEAR.DAY.HOUR

        Args:
            date_str (str): Date format in yyyy-mm-dd

        Returns:
            Stream: Stream object
        """
        input_dir = self.input_dir

        date_obj: datetime = datetime.strptime(date_str, '%Y-%m-%d')
        year: str = date_obj.strftime('%Y')
        julian_day: str = date_obj.strftime('%j')

        seismic_dir: str = os.path.join(input_dir, year, '*', self.station, '*', julian_day, '*')

        try:
            stream: Stream = read(seismic_dir)
            stream = stream.select(**self.select)
        except Exception as e:
            print(f'⛔ {date_str} - self.idds():: {e}')
            return Stream()

        return stream

    def search(self, date_str: str) -> Stream:
        """Search seismic data structure.

        Args:
            date_str (str): Date format in yyyy-mm-d

        Returns:
            Stream: Stream object
        """
        stream: Stream = Stream()
        directory_structure: str = self.directory_structure

        if directory_structure in ['ijen']:
            stream = self.ijen(date_str)

        if directory_structure in ['idds']:
            stream = self.idds(date_str)

        if directory_structure in directory_structures_group['seisan']:
            stream = self.seisan(date_str)

        if directory_structure in directory_structures_group['sac']:
            stream = self.sac(date_str)

        print(f"👍 {date_str} :: Total {stream.count()} traces found.")

        return self.merged(stream, date_str)
