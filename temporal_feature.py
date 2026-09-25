from src.util import load_pcap
from src.detection import detect_website_keystrokes, detect_keystrokes


def get_temporal_feature(pcap, website=None):
    # Load the pcap
    pcap = load_pcap(pcap)

    if website is None:
        website, keystrokes = detect_website_keystrokes(pcap)
    else:
        keystrokes = detect_keystrokes(pcap, website)
    return website, keystrokes, pcap