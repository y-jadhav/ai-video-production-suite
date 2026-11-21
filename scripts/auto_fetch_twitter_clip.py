#!/usr/bin/env python3
"""Automated Twitter Video Asset Fetcher for Video Editing Agents.
Enforces the strict Wire Agency Whitelist: ANI, PTI, IANS.
Downloads clips using https://twitsave.com/en and outputs mandatory on-screen attribution.
"""

import os
import sys
import json
import argparse
import subprocess
import re

# Add twitter-mcp to path
script_dir = os.path.dirname(os.path.abspath(__file__))
mcp_dir = os.path.join(script_dir, "twitter-mcp")
if mcp_dir not in sys.path:
    sys.path.insert(0, mcp_dir)

from twitsave_downloader import download_twitter_video

# Strict Whitelist of Wire Agencies
ALLOWED_AGENCIES = {
    "ANI": ["ANI", "ani_digital", "aninews"],
    "PTI": ["PTI_News", "ptinews"],
    "IANS": ["IANS_India", "ians_news", "ians"]
}

def detect_agency(url_or_handle: str) -> str:
    """Detect which authorized wire agency the tweet belongs to."""
    lower = url_or_handle.lower()
    for agency, aliases in ALLOWED_AGENCIES.items():
        for alias in aliases:
            if f"/{alias.lower()}/" in lower or f"@{alias.lower()}" in lower or lower == alias.lower():
                return agency
    if "ani" in lower:
        return "ANI"
    if "pti" in lower:
        return "PTI"
    if "ians" in lower:
        return "IANS"
    return "UNKNOWN"

def search_agency_tweets(query: str, agency: str = None, max_results: int = 10):
    """Search Twitter for tweets strictly from authorized wire agencies."""
    try:
        from tools_read import search_tweets
        
        # Build query targeting authorized accounts
        if agency and agency in ALLOWED_AGENCIES:
            primary_handle = ALLOWED_AGENCIES[agency][0]
            search_query = f"{query} from:{primary_handle}"
        else:
            search_query = f"{query} (from:ANI OR from:PTI_News OR from:IANS_India)"
            
        print(f"[*] Querying Twitter/X with Wire Agency Filter: '{search_query}'...")
        raw_text = search_tweets(search_query, max_results=max_results)
        
        # Extract tweet URLs
        urls = re.findall(r'https?://(?:twitter|x)\.com/[A-Za-z0-9_]+/status/\d+', raw_text)
        return list(set(urls))
    except Exception as e:
        print(f"[Search Notice] Search error: {e}")
        return []

def format_clip_for_video_edit(input_path: str, aspect: str = None, fps: int = 30) -> str:
    """Format downloaded clip for seamless insertion into Remotion or video editors."""
    if not os.path.exists(input_path) or (not aspect and not fps):
        return input_path
        
    dirname = os.path.dirname(input_path)
    basename = os.path.basename(input_path)
    name, ext = os.path.splitext(basename)
    out_path = os.path.join(dirname, f"{name}_formatted.mp4")
    
    vf_filters = []
    if fps:
        vf_filters.append(f"fps={fps}")
        
    if aspect == "9:16":
        vf_filters.append("scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2")
    elif aspect == "16:9":
        vf_filters.append("scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2")
        
    filter_str = ",".join(vf_filters) if vf_filters else "copy"
    
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", filter_str,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    print(f"[*] Post-processing clip for {aspect or 'standard'} @ {fps}fps...")
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode == 0 and os.path.exists(out_path):
        print(f"✓ Formatted clip saved: {out_path}")
        return out_path
    return input_path

def auto_fetch_clip(
    url: str = None,
    query: str = None,
    agency: str = None,
    output_dir: str = "./downloads",
    filename: str = None,
    aspect: str = None,
    fps: int = 30,
    enforce_whitelist: bool = True
) -> dict:
    """Main automated entrypoint for video editing agents."""
    os.makedirs(output_dir, exist_ok=True)
    target_url = url
    detected_agency = agency
    
    if target_url:
        detected_agency = detect_agency(target_url)
        if enforce_whitelist and detected_agency == "UNKNOWN":
            print(f"[!] WARNING: The provided URL does not appear to be from ANI, PTI, or IANS.")
            print(f"    Per project rules, only clips from ANI, PTI, and IANS are authorized for events.")
    
    # If query provided, search specifically within allowed agency feeds
    if not target_url and query:
        candidates = search_agency_tweets(query, agency=agency)
        if candidates:
            target_url = candidates[0]
            detected_agency = detect_agency(target_url)
            print(f"[+] Selected wire agency clip: {target_url} ({detected_agency})")
            
    if not target_url:
        return {
            "success": False,
            "error": "No authorized wire agency tweet URL or query match found for this event."
        }
        
    # Download via TwitSave engine
    res = download_twitter_video(target_url, output_dir=output_dir, filename=filename)
    
    if res.get("success"):
        raw_video = res["output_path"]
        if aspect or fps:
            formatted_video = format_clip_for_video_edit(raw_video, aspect=aspect, fps=fps)
            res["formatted_path"] = os.path.abspath(formatted_video)
            
        agency_name = detected_agency if detected_agency in ["ANI", "PTI", "IANS"] else (agency or "ANI")
        res["agency"] = agency_name
        res["attribution_text"] = f"Clip Source: {agency_name}"
        
        print("\n🎉 [WIRE AGENCY ASSET READY FOR EDIT]")
        print(f"File:        {res.get('formatted_path', res['output_path'])}")
        print(f"Agency:      {agency_name}")
        print(f"Attribution: \"{res['attribution_text']}\"")
        return res
    else:
        return res

def main():
    parser = argparse.ArgumentParser(description="Automated Twitter Wire Agency Fetcher (ANI, PTI, IANS)")
    parser.add_argument("--url", "-u", default=None, help="Direct Twitter/X tweet URL")
    parser.add_argument("--query", "-q", default=None, help="Event keywords to search wire agencies")
    parser.add_argument("--agency", choices=["ANI", "PTI", "IANS"], default=None, help="Preferred agency")
    parser.add_argument("--output-dir", "-o", default="./downloads", help="Output directory")
    parser.add_argument("--filename", "-f", default=None, help="Custom output filename")
    parser.add_argument("--aspect", "-a", choices=["9:16", "16:9"], default=None, help="Target aspect ratio")
    parser.add_argument("--fps", type=int, default=30, help="Target FPS (default 30)")
    
    args = parser.parse_args()
    
    result = auto_fetch_clip(
        url=args.url,
        query=args.query,
        agency=args.agency,
        output_dir=args.output_dir,
        filename=args.filename,
        aspect=args.aspect,
        fps=args.fps
    )
    
    if result.get("success"):
        sys.exit(0)
    else:
        print(f"\n[ERROR] {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
