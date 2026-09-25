import dpkt
import socket
import numpy as np
from scipy.fft import rfft, rfftfreq
from get_ip import getIp
from src.util import load_pcap, get_outgoing_packets
import matplotlib.pyplot as plt

def get_outgoing(pcap_file, server_ip=None):
    if server_ip is None:
        candidate_ips, _ = getIp(pcap_file)
        df = load_pcap(pcap_file)
        actual_dst_ips = set(df['dst'].unique())
        matched = [ip for ip in candidate_ips if ip in actual_dst_ips]
        if not matched:
            print("No matching server IP found!")
            return
    df = load_pcap(pcap_file)
    outgoing = get_outgoing_packets(df, matched)
    return outgoing

def detect_event_model_from_df(outgoing_df):
    if len(outgoing_df) < 3:
        return "unknown", "unknown", "N/A", "N/A"

    ts = outgoing_df['frame_time'].values.astype(float)
    sizes = outgoing_df['frame_length'].values.astype(float)

    intervals = np.diff(ts)
    deltas = np.diff(sizes)

    mean_int = np.mean(intervals)
    std_int = np.std(intervals)
    cv = std_int / mean_int if mean_int > 1e-6 else np.inf
    multi_char_ratio = np.mean(deltas > 1.5)

    def is_multiple_of_100(x, tol=15):
        remainder = x % 100
        return min(remainder, 100 - remainder) <= tol

    polling_like = np.mean([is_multiple_of_100(iv) for iv in intervals])
    print(f"[DBG] 100-ms-like ratio = {polling_like:.2%}, cv = {cv:.2f}, multi-char = {multi_char_ratio:.2%}")
    polling_like = np.mean([is_multiple_of_100(iv) for iv in intervals]) > 0.45
    if polling_like and cv < 2.0:
        model = "polling"
    else:
        model = "callback"
