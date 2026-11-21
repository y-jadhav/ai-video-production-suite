#!/usr/bin/env python3
"""CLI Script to download Twitter/X video clips using https://twitsave.com/en.

Usage:
    python download_twitter_clip.py <tweet_url> [--output-dir DIR] [--filename NAME]

Examples:
    python download_twitter_clip.py https://x.com/NASA/status/123456789
    python download_twitter_clip.py https://twitter.com/SpaceX/status/123456789 --output-dir ./clips
"""

import os
import sys
import argparse

# Add twitter-mcp directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
mcp_dir = os.path.join(script_dir, "twitter-mcp")
if mcp_dir not in sys.path:
    sys.path.insert(0, mcp_dir)

from twitsave_downloader import download_twitter_video

def main():
    parser = argparse.ArgumentParser(
        description="Download Twitter/X video clips using https://twitsave.com/en"
    )
    parser.add_argument("tweet_url", help="Twitter or X.com status post URL")
    parser.add_argument(
        "--output-dir",
        "-o",
        default="./downloads",
        help="Destination directory for downloaded video (default: ./downloads)",
    )
    parser.add_argument(
        "--filename",
        "-f",
        default=None,
        help="Custom output filename (e.g. clip.mp4)",
    )

    args = parser.parse_args()

    result = download_twitter_video(
        tweet_url=args.tweet_url,
        output_dir=args.output_dir,
        filename=args.filename,
    )

    if result.get("success"):
        print(f"\n[DONE] Video successfully saved to:")
        print(f"       -> {result['output_path']}")
        print(f"       File size: {result.get('filesize_mb', '?')} MB")
        print(f"       Source:    {result.get('source')}")
        sys.exit(0)
    else:
        print(f"\n[FAILED] {result.get('error', 'Download failed')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
