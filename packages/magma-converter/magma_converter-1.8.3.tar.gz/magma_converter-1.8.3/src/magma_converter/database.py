from typing import Any, List, Self
from .model import db, database, Station, Sds
from obspy import read, Trace
from obspy.clients.filesystem.sds import Client

import os
import datetime
import pandas as pd
import numpy as np


def reset() -> bool | None:
    """Reset database.

    Returns:
        True | None
    """
    database_location = database()
    if os.path.exists(database_location):
        if not db.is_closed():
            db.close()

        os.remove(database_location)
        db.connect(reuse_if_open=True)
        db.create_tables([Station, Sds])
        db.close()
        print(f"⌛ Reset database: {database_location}")
        return True
    return None


def recreate_tables() -> None:
    """Drop and create tables."""
    models = (Sds, Station)
    db.drop_tables(models)
    db.create_tables(models)


class DatabaseConverter:
    def __init__(self, sds_results: List[dict[str, Any]]):
        """
        sds_results: SDS success results
            examples:
            {'nslc': 'VG.INFR.00.EHZ',
              'date': '2018-01-01',
              'start_time': '2018-01-01 00:00:00',
              'end_time': '2018-01-01 23:59:59',
              'sampling_rate': 100.0,
              'completeness': 99.99770833333334,
              'file_location': 'L:\\converted\\SDS\\2018\\VG\\INFR\\EHZ.D\\VG.INFR.00.EHZ.D.2018.001',
              'file_size': 1024, # In byte
              }

        Args:
            sds_results: SDS success results. Can be accessed through SDS `results` property
        """
        self.sds_results = sds_results
        self.station_ids: List[int] = []
        self.sds_ids: List[int] = []

    @staticmethod
    def rescan_all_stations(sds_directory: str,
                            start_date: str,
                            end_date: str,) -> None:
        """Rescan all stations and update database.

        Args:
            sds_directory (str): SDS root directory
            start_date: Start date.
            end_date: End date.

        Returns:
            None
        """
        client = Client(sds_root=sds_directory)
        nslc_list = client.get_all_nslc()

        for nslc in nslc_list:
            network, station, location, channel = nslc
            print(network, station, location, channel)
            results = DatabaseConverter.rescan(
                sds_directory=sds_directory,
                station=station,
                channel=channel,
                start_date=start_date,
                end_date=end_date,
            )

    @staticmethod
    def rescan(sds_directory: str,
               station: str,
               channel: str,
               start_date: str,
               end_date: str,
               network: str = 'VG',
               location: str = '00', ) -> List[dict[str, Any]]:
        """Rescan SDS directory an update database.

        Args:
            sds_directory: SDS directory.
            station: Station name.
            channel: Channel name.
            start_date: Start date.
            end_date: End date.
            network: Network name.
            location: Location name.

        Returns:
            List[dict[str, Any]]

            Examples list of:
            -----------------
            {'nslc': 'VG.INFR.00.EHZ',
              'date': '2018-01-01',
              'start_time': '2018-01-01 00:00:00',
              'end_time': '2018-01-01 23:59:59',
              'sampling_rate': 100.0,
              'completeness': 99.99770833333334,
              'file_location': 'L:\\converted\\SDS\\2018\\VG\\INFR\\EHZ.D\\VG.INFR.00.EHZ.D.2018.001',
              'file_size': 1024, # In byte
              }
        """

        sds_results: List[dict[str, Any]] = []

        dates: pd.DatetimeIndex = pd.date_range(start_date, end_date, freq='D')

        nslc: str = f"{network}.{station}.{location}.{channel}"

        __station: dict[str, Any] = {'nslc': nslc,
                                     'network': network,
                                     'station': station,
                                     'channel': channel,
                                     'location': location}

        db.connect(reuse_if_open=True)
        db.create_tables([Station, Sds])
        db.close()

        station_id = DatabaseConverter.update_station(station=__station)
        print(f"📌 Station {nslc} updated : id={station_id}")

        for date_obj in dates:
            year = date_obj.strftime('%Y')
            julian_day = date_obj.strftime('%j')
            date_str = date_obj.strftime('%Y-%m-%d')

            filename: str = f"{network}.{station}.{location}.{channel}.D.{year}.{julian_day}"
            file_location: str = os.path.join(sds_directory, year, network, station, f"{channel}.D", filename)

            if os.path.exists(file_location):
                trace: Trace = read(file_location)[0]
                completeness: float = (np.count_nonzero(trace.data) / 8640000) * 100

                __sds: dict[str, Any] = {'nslc': trace.id,
                                         'date': date_str,
                                         'start_time': trace.stats.starttime.strftime('%Y-%m-%d %H:%M:%S'),
                                         'end_time': trace.stats.endtime.strftime('%Y-%m-%d %H:%M:%S'),
                                         'completeness': completeness,
                                         'sampling_rate': trace.stats.sampling_rate,
                                         'file_location': file_location,
                                         'file_size': os.stat(file_location).st_size}

                __sds['id'] = DatabaseConverter.update_sds(sds=__sds)
                sds_results.append(__sds)
                print(f"✅ {date_str} :: {nslc} {completeness}% ➡️ {file_location}")
            else:
                print(f"⛔ {date_str} :: {nslc} Not exists ➡️ {file_location}")

        return sds_results

    @property
    def stations(self) -> List[dict[str, Any]]:
        _nslc: List[str] = []
        _stations: List[dict[str, Any]] = []

        for result in self.sds_results:
            nslc = result['nslc']

            if nslc not in _nslc:
                network, station, channel, location = nslc.split('.')
                __stations: dict[str, Any] = {'nslc': result['nslc'], 'network': network, 'station': station,
                                              'channel': channel, 'location': location}
                _nslc.append(nslc)
                _stations.append(__stations)

        return _stations

    @property
    def sds(self) -> List[dict[str, Any]]:
        """Map sds results to list of dict (collection)

        Returns:
            List[dict[str, Any]]
        """
        _sds: List[dict[str, Any]] = []

        for result in self.sds_results:
            __sds: dict[str, Any] = {'nslc': result['nslc'], 'date': result['date'],
                                     'start_time': result['start_time'], 'end_time': result['end_time'],
                                     'completeness': result['completeness'], 'sampling_rate': result['sampling_rate'],
                                     'file_location': result['file_location'], 'file_size': result['file_size']}
            _sds.append(__sds)

        return _sds

    @staticmethod
    def update_station(station: dict[str, Any]) -> int:
        """Update stations table

        Args:
            station (dict[str, Any]): Station data

        Returns:
            int: id of the updated station
        """
        _station, created = Station.get_or_create(
            nslc=station['nslc'],
            defaults={
                'network': station['network'],
                'station': station['station'],
                'channel': station['channel'],
                'location': station['location']
            }
        )

        station_id = _station.get_id()

        if created is True:
            return station_id

        _station.nslc = station['nslc']
        _station.network = station['network']
        _station.station = station['station']
        _station.location = station['location']
        _station.channel = station['channel']
        _station.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        _station.save()

        return station_id

    @staticmethod
    def update_sds(sds: dict[str, Any]) -> int:
        """Update sds table.

        Args:
            sds: SDS success results. Can be accessed through SDS `results` property

        Returns:
            int: id of sds model
        """
        _sds, created = Sds.get_or_create(
            nslc=sds['nslc'],
            date=sds['date'],
            defaults={
                'start_time': sds['start_time'],
                'end_time': sds['end_time'],
                'sampling_rate': sds['sampling_rate'],
                'completeness': sds['completeness'],
                'file_location': sds['file_location'],
                'file_size': sds['file_size'],
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc),
            }
        )

        sds_id = _sds.get_id()

        if created is True:
            return sds_id

        _sds.nslc = sds['nslc']
        _sds.date = sds['date']
        _sds.start_time = sds['start_time']
        _sds.end_time = sds['end_time']
        _sds.completeness = sds['completeness']
        _sds.sampling_rate = sds['sampling_rate']
        _sds.file_location = sds['file_location']
        _sds.file_size = sds['file_size']
        _sds.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        _sds.save()

        return sds_id

    def update(self) -> Self:
        """
        Bulk update:
        https://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts

        Upsert:
        https://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert

        Returns:
            Self
        """
        for station in self.stations:
            station_id: int = self.update_station(station)
            if station_id not in self.station_ids:
                self.station_ids.append(station_id)

        for sds in self.sds:
            sds_id: int = self.update_sds(sds)
            if sds_id not in self.sds_ids:
                self.sds_ids.append(sds_id)

        return self
