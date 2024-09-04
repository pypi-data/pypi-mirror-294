import logging
import os
import re
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import EmptyDataError, ParserError
from tqdm import tqdm

cuda_devices: List[int] = [0, 1, 2, 3]

network_interfaces: List[str] = ['lo', 'enp195s0', 'bond0', 'hsn0', 'hsn1']

plot_col: List[str] = [
    'cpu_percent (%)/mean',
    'memory_used (GiB)/mean',
    'memory_percent (%)/mean'
] + [
    f'cuda:{i} (gpu:{i})/{metric}/mean'
    for i in cuda_devices
    for metric in ['memory_used (MiB)', 'gpu_utilization (%)']
] + [
    f'network_{interface}/{direction} (Mbps)'
    for interface in network_interfaces
    for direction in ['sent', 'recv']
]

# Define constant colors for specific tags
tag_colors_map: Dict[str, str] = {
    'load_model': 'blue',
    'load_token': 'green',
    'load_data': 'orange',
    'load_trainer': 'purple',
    'train': 'red',
    'save_model': 'brown'
}

# Define line styles for each GPU
line_styles: List[str] = ['-', '--', '-.', ':']

# Define a fallback colormap for any tags not explicitly listed
fallback_colors = plt.get_cmap("Paired").colors  # type: ignore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PerformancePlotter:
    """Performance plotter class."""

    def __init__(self, base_dir: str, log_node: str):
        self.log_node: str = log_node
        self.metric_dir: str = f"{base_dir}/metric"
        self.graph_dir: str = f"{base_dir}/graph"

        os.makedirs(self.graph_dir, exist_ok=True)

    def get_tag_colors(self, df: pd.DataFrame) -> Dict[str, str]:
        """Returns the tag colors."""

        tags = df['tag'].unique()

        # Use the predefined tag colors, and assign remaining tags to fallback colors
        return {
            tag: tag_colors_map.get(tag, fallback_colors[i % len(fallback_colors)])
            for i, tag in enumerate(tags)
        }

    def graph(self, df: pd.DataFrame, node_plot_dir: str) -> None:
        """Graphs the performance metrics."""

        os.makedirs(node_plot_dir, exist_ok=True)

        tag_colors = self.get_tag_colors(df)

        for col in tqdm(plot_col, desc=f"Plotting metrics for node-{self.log_node}: "):
            if col not in df.columns:
                logging.warning("Column %s not found in DataFrame, skipping.", col)
                continue

            _, ax = plt.subplots(figsize=(10, 6))

            for tag, segment in df.groupby('tag'):
                # Drop rows where 'duration (s)' is NaN
                segment = segment.dropna(subset=['duration (s)'])

                # Convert 'duration (s)' and 'segment[col]' to numeric if possible
                segment['duration (s)'] = pd.to_numeric(segment['duration (s)'], errors='coerce')
                segment[col] = pd.to_numeric(segment[col], errors='coerce')

                # Drop any rows where either 'duration (s)' or 'segment[col]' has NaN values
                segment = segment.dropna(subset=['duration (s)', col])

                # Ensure there is data left to plot after handling NaNs
                if not segment.empty:
                    ax.plot(segment['duration (s)'], segment[col], label=tag, color=tag_colors[tag])

            if 'memory_used (MiB)' in col:
                gpu_memory_col = col.replace('memory_used (MiB)', 'memory_total (MiB)')
                if gpu_memory_col in df.columns:
                    # Ensure the column contains numeric data
                    df[gpu_memory_col] = pd.to_numeric(df[gpu_memory_col], errors='coerce')
                    max_y = df[gpu_memory_col].mean()
                    if not pd.isna(max_y):
                        ax.axhline(y=max_y, color='red', linestyle='-', label="Max Memory")

            ax.legend(title='Tag')

            name = re.sub(r"[ /]", "_", col)
            name = re.sub(r"_mean", "", name)
            name = re.sub(r"\(gpu:\d+\)", "", name)

            ax.set_xlabel('Duration (s)')
            ax.set_ylabel(name)

            # Add GPU label only at the end of the line
            if 'cuda:' in col:
                gpu_num = re.search(r'cuda:(\d+)', col).group(1)
                last_point = segment['duration (s)'].iloc[-1]
                last_value = segment[col].iloc[-1]
                ax.text(last_point, last_value, f'GPU {gpu_num}', fontsize=9,
                        color=tag_colors[df['tag'].iloc[-1]],
                        ha='left', va='bottom', rotation=45)

            plt.tight_layout()
            plt.savefig(f"{node_plot_dir}/{name}.jpg", format='jpeg', dpi=100, bbox_inches='tight')
            plt.close()

    def plot_cuda_memory(self, df: pd.DataFrame, node_plot_dir: str) -> None:
        """Plots memory used by each CUDA device with different line styles and individual max memory lines."""

        _, ax = plt.subplots(figsize=(14, 8))  # Increase figure size for better readability
        tag_colors = self.get_tag_colors(df)

        # Plot the actual memory usage lines
        for i, cuda_device in enumerate(cuda_devices):
            col = f'cuda:{cuda_device} (gpu:{cuda_device})/memory_used (MiB)/mean'
            max_col = f'cuda:{cuda_device} (gpu:{cuda_device})/memory_total (MiB)/mean'

            if col in df.columns:
                for tag in df['tag'].unique():
                    segment = df[df['tag'] == tag]
                    if segment.empty:
                        continue  # Skip empty segments
                    ax.plot(segment['duration (s)'], segment[col], label=tag if i == 0 else "",
                            color=tag_colors[tag], linestyle=line_styles[i])

                    # Adding GPU label only at the end of each line with a bit of offset to prevent overlap
                    last_point = segment['duration (s)'].iloc[-1]
                    last_value = segment[col].iloc[-1]
                    ax.text(last_point, last_value, f'GPU {cuda_device}', fontsize=9, color=tag_colors[tag],
                            ha='left', va='bottom', rotation=45)

                # Plot max memory line for each GPU
                if max_col in df.columns:
                    max_memory = df[max_col].max()
                    ax.axhline(y=max_memory, color=tag_colors[list(tag_colors.keys())[i % len(tag_colors)]],
                               linestyle=':', label=f'Max GPU {cuda_device}')
                    ax.text(df['duration (s)'].max(), max_memory, f'Max GPU {cuda_device}: {max_memory:.0f} MiB',
                            fontsize=9, color=tag_colors[list(tag_colors.keys())[i % len(tag_colors)]],
                            ha='right', va='bottom')

        ax.set_xlabel('Duration (s)')
        ax.set_ylabel('Memory Used (MiB)')

        # Legend only once per tag and max memory line
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = dict(zip(labels, handles))
        ax.legend(unique_labels.values(), unique_labels.keys(), title='Tag', loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()
        plt.savefig(f"{node_plot_dir}/cuda_memory_used_all.jpg", format='jpeg', dpi=100, bbox_inches='tight')
        plt.close()

    def plot(self) -> None:
        """Plots the performance metrics."""

        filepath = f"{self.metric_dir}/node-{self.log_node}.csv"

        try:
            df = pd.read_csv(filepath)

            if df.empty:
                logging.warning("File %s is empty, skipping.", filepath)

            df['duration (s)'] = pd.to_numeric(df['duration (s)'], errors='coerce')

            df.sort_values(by=['duration (s)'], inplace=True)

            df = df[df['tag'].notna()]
            node_plot_dir = f"{self.graph_dir}/node-{self.log_node}"
            self.graph(df, node_plot_dir)
            self.plot_cuda_memory(df, node_plot_dir)
        except EmptyDataError:
            logging.warning("File %s is empty, skipping.", filepath)
        except ParserError:
            logging.error("File %s is improperly formatted, skipping.", filepath)
        except OSError as e:
            logging.error("Error reading file %s: %s", filepath, e)

        logging.info("Graphs saved in %s", self.graph_dir)
