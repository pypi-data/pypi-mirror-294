import seaborn as sns
import os
import numpy as np
import pandas as pd

from .model import Sds
from .plotly_calplot import calplot
import plotly.express as px
from matplotlib import pyplot as plt
from PIL import Image
from obspy import Trace, Stream
from typing import Any, Dict, List, Self, Tuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sds import SDS

sns.set_style("whitegrid")


class Plot:
    types: List[str] = ['normal', 'dayplot', 'relative', 'section']

    def __init__(self,
                 sds: "SDS",
                 plot_type: str = 'dayplot'):
        """Plot daily seismogram

        Args:
            sds: SDS object
            plot_type: Plot type must be between 'normal', 'dayplot', 'relative', 'section'.
        """
        assert type not in self.types, f"Plot type must be between 'normal', 'dayplot', 'relative', 'section'."

        self.sds = sds
        self.completeness = sds.results['completeness']
        self.trace: Trace = sds.trace
        self.sampling_rate = sds.results['sampling_rate']
        self.date = sds.results['date']
        self.filename: str = f"{sds.filename}.jpg"
        self.plot_type = plot_type
        self.plot_gaps: bool = False

        output_dir: str = os.path.dirname(sds.path).replace('Converted\\SDS', 'Seismogram')
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir: str = output_dir

        thumbnail_dir: str = os.path.join(output_dir, 'thumbnail')
        os.makedirs(thumbnail_dir, exist_ok=True)
        self.thumbnail_dir: str = thumbnail_dir

    def plot_with_gaps(self, plot_gaps: bool = False) -> Self:
        """Plot with gaps.

        Args:
            plot_gaps: Plot gaps between traces.

        Returns:
            Self: Plot with gaps.
        """
        self.plot_gaps = plot_gaps
        return self

    @property
    def title(self):
        """Plot title

        Returns:
            title (str)
        """
        return (f"{self.date} | {self.trace.id} | {self.sampling_rate} Hz | "
                f"{self.trace.stats.npts} samples ({self.completeness:.2f})%")

    def thumbnail(self, seismogram: str) -> str:
        """Generate thumbnail of seismogram.

        Args:
            seismogram (str): Seismogram image path
        """
        outfile = os.path.join(self.thumbnail_dir, self.filename)

        image = Image.open(seismogram)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.thumbnail((320, 180))
        image.save(outfile)

        return outfile

    def replace_zeros_with_gaps(self, trace: Trace) -> Stream | Trace:
        """Replace zeros with gaps.

        Args:
            trace (Trace): Trace to replace zeros with gaps.

        Returns:
            Stream | Trace: Stream or trace with zeros replaced with gaps.
        """
        if self.plot_gaps is True:
            trace.data = np.ma.masked_equal(trace.data, 0)
            stream: Stream = trace.split()
            return stream

        return trace.split()

    def replot_from_sds(self):
        pass

    def save(self) -> Tuple[str, str]:
        """Save plot to file.

        Returns:
            seismogram, thumbnail (str, str): seismogram_image_path (str), thumbnail_image_path (str)
        """
        seismogram = os.path.join(self.output_dir, self.filename)

        stream = self.replace_zeros_with_gaps(self.trace.copy())

        stream.plot(
            type='dayplot',
            interval=60,
            one_tick_per_line=True,
            color=['k'],
            outfile=seismogram,
            number_of_ticks=13,
            size=(1600, 900),
            title=self.title
        )

        plt.close('all')

        thumbnail = self.thumbnail(seismogram)

        print(f"🏞️ {self.date} :: Seismogram saved to : {seismogram}")

        return seismogram, thumbnail


class PlotAvailability:
    def __init__(self,
                 station: str,
                 channel: str,
                 network: str = 'VG',
                 location: str = '00', ):
        self.station: str = station
        self.channel: str = channel
        self.network: str = network
        self.location: str = location
        self.nslc: str = f"{network}.{station}.{location}.{channel}"
        self._df: pd.DataFrame = pd.DataFrame.from_records(self.sds_list, index='id')

    @property
    def df(self) -> pd.DataFrame:
        self._df.sort_values(by=['date'], inplace=True)
        return self._df

    @property
    def output_dir(self) -> str:
        output_dir: str = os.path.join(os.getcwd(), 'output', 'figures')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    @property
    def sds_list(self) -> List[Dict[str, Any]]:
        sds_list = []

        sds_dicts = Sds.select().where(Sds.nslc == self.nslc)
        _sds_list = [dict(sds_dict) for sds_dict in sds_dicts.dicts()]

        for sds in _sds_list:
            _sds = {
                'id': sds['id'],
                'nslc': sds['nslc'],
                'date': str(sds['date']),
                'start_time': str(sds['start_time']),
                'end_time': str(sds['end_time']),
                'completeness': float(sds['completeness']),
                'sampling_rate': float(sds['sampling_rate']),
                'file_location': sds['file_location'],
                'file_size': sds['file_size'],
                'created_at': str(sds['created_at']),
                'updated_at': str(sds['updated_at']),
            }
            sds_list.append(_sds)

        return sds_list

    def filter(self, start_date: str, end_date: str) -> Self:
        """Filter data by start and end dates.

        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            Self
        """
        df = self.df
        self._df = df[(df['date'] > start_date) & (df['date'] < end_date)]
        return self

    def save(self):
        pass
