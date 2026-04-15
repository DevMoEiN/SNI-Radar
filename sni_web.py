#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SNI Web UI with Advanced Dark Glassmorphism Design, Live Streaming, Concurrency, Live Sorting & TXT Export."""

import ipaddress
import json
import platform
import re
import socket
import ssl
import subprocess
import webbrowser
import threading
import concurrent.futures
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request, send_from_directory, Response, stream_with_context

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Persia Team Radar</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        @font-face {
            font-family: "AradWeb";
            src: url("/static/fonts/Arad-Regular.woff2") format("woff2");
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }

        @font-face {
            font-family: "AradWeb";
            src: url("/static/fonts/Arad-Medium.woff2") format("woff2");
            font-weight: 500;
            font-style: normal;
            font-display: swap;
        }

        @font-face {
            font-family: "AradWeb";
            src: url("/static/fonts/Arad-Bold.woff2") format("woff2");
            font-weight: 700;
            font-style: normal;
            font-display: swap;
        }

        :root {
            --c: #00e5ff;
            --c2: #7c3aed;
            --c3: #10b981;
            --red: #ef4444;
            --amber: #f59e0b;
            --bg: #060912;
            --surface: rgba(255,255,255,0.03);
            --border: rgba(255,255,255,0.07);
            --border-hi: rgba(255,255,255,0.13);
            --text: #e2e8f0;
            --muted: #64748b;
            --faint: rgba(255,255,255,0.04);
        }

        html { font-size: 16px; }
        @media (min-width: 768px) { html { font-size: 17px; } }
        @media (min-width: 1280px) { html { font-size: 18px; } }
        html, body { min-height: 100vh; background: var(--bg); color: var(--text); font-family: "AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; }

        /* ─── ANIMATED BACKGROUND ─────────────────────── */
        body::before {
            content:'';
            position:fixed; inset:0; pointer-events:none; z-index:0;
            background:
                radial-gradient(ellipse 60% 50% at 10% 0%, rgba(0,229,255,.10) 0%, transparent 70%),
                radial-gradient(ellipse 50% 40% at 90% 0%, rgba(124,58,237,.10) 0%, transparent 70%),
                radial-gradient(ellipse 40% 35% at 50% 100%, rgba(16,185,129,.06) 0%, transparent 70%);
        }

        body::after {
            content:'';
            position:fixed; inset:0; pointer-events:none; z-index:0;
            background-image:
                linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
            background-size: 80px 80px;
            mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, black 0%, transparent 100%);
        }

        .page { position:relative; z-index:1; max-width:1440px; margin:0 auto; padding:24px; display:flex; flex-direction:column; gap:20px; }

        /* ─── GLASS CARD ──────────────────────────────── */
        .card {
            background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.015) 100%);
            border: 1px solid var(--border);
            border-top-color: var(--border-hi);
            border-left-color: rgba(255,255,255,0.09);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 20px;
            box-shadow: 0 8px 40px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.05);
        }

        /* ─── HEADER ──────────────────────────────────── */
        .header {
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }

        .header-brand { display:flex; align-items:center; gap:14px; }

        .header-icon {
            width: 44px; height: 44px; border-radius: 14px; flex-shrink: 0;
            background: linear-gradient(135deg, rgba(0,229,255,.25), rgba(124,58,237,.2));
            border: 1px solid rgba(0,229,255,.3);
            display: flex; align-items:center; justify-content:center;
            box-shadow: 0 0 20px rgba(0,229,255,.15);
        }

        .header-icon svg { width:22px; height:22px; color: var(--c); }

        .brand-name {
            font-size: 1.2rem; font-weight: 800; letter-spacing: -.02em;
            background: linear-gradient(90deg, #fff 0%, rgba(255,255,255,.6) 100%);
            -webkit-background-clip: text; background-clip: text; color: transparent;
        }

        .brand-sub {
            font-family: "AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif;
            font-size: 0.62rem; color: var(--muted); letter-spacing: .25em; text-transform: uppercase; margin-top: 1px;
        }

        .header-pills { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }

        .pill {
            display:inline-flex; align-items:center; gap:6px;
            padding: 5px 12px; border-radius:999px;
            border: 1px solid var(--border-hi);
            background: var(--faint);
            font-family: "AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif;
            font-size: .65rem; letter-spacing:.12em; text-transform:uppercase; color: #94a3b8;
        }

        .pulse-dot {
            width:7px; height:7px; border-radius:50%; background:var(--c); position:relative; flex-shrink:0;
        }
        .pulse-dot::after {
            content:''; position:absolute; inset:-3px; border-radius:50%; background:var(--c);
            animation: pulse-ring 1.4s cubic-bezier(0,0,.2,1) infinite;
        }
        @keyframes pulse-ring { 0%{transform:scale(1);opacity:.7} 100%{transform:scale(2.2);opacity:0} }

        /* ─── HERO ────────────────────────────────────── */
        .hero {
            padding: 32px; position:relative; overflow:hidden;
            display:flex; flex-direction:column; gap:28px;
        }

        @media(min-width:900px){ .hero { flex-direction:row; align-items:center; justify-content:space-between; } }

        .hero-glow {
            position:absolute; right:-60px; bottom:-80px; width:340px; height:340px;
            background: radial-gradient(circle, rgba(0,229,255,.14) 0%, transparent 70%);
            pointer-events:none; filter:blur(2px);
        }

        .hero-content { position:relative; z-index:1; display:flex; gap:20px; align-items:flex-start; max-width:640px; }

        .hero-logo {
            width:76px; height:76px; border-radius:20px; flex-shrink:0;
            padding: 3px;
            background: linear-gradient(135deg, rgba(0,229,255,.4), rgba(124,58,237,.3));
            box-shadow: 0 12px 32px rgba(0,0,0,.4), 0 0 0 1px rgba(0,229,255,.2);
        }

        .hero-logo img { width:100%; height:100%; object-fit:cover; border-radius:17px; display:block; }

        .hero-text { flex:1; }

        .hero-tags { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px; }

        .tag {
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.62rem; letter-spacing:.1em; text-transform:uppercase;
            padding:3px 9px; border-radius:6px;
            background:rgba(255,255,255,.05); border:1px solid var(--border); color:#94a3b8;
        }

        .hero-title {
            font-size: clamp(1.4rem, 3vw, 2.2rem); font-weight: 800; line-height: 1.2; letter-spacing: -.03em;
            color: #fff; margin-bottom: 10px;
        }

        .hero-desc {
            font-size:.9rem; color:#94a3b8; line-height:1.7;
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.75rem;
        }

        /* ─── CHANNEL CARD ────────────────────────────── */
        .channel-card {
            flex-shrink:0; min-width:min(100%,300px);
            background: linear-gradient(160deg, rgba(10,15,30,.92), rgba(8,12,24,.88));
            border: 1px solid var(--border-hi);
            border-radius: 18px; padding:20px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
        }

        .tg-row { display:flex; align-items:center; gap:12px; margin-bottom:14px; }

        .tg-icon {
            width:44px; height:44px; border-radius:14px; flex-shrink:0;
            background: linear-gradient(135deg,#2eb8e6,#1a95c0);
            display:flex; align-items:center; justify-content:center;
            box-shadow: 0 8px 20px rgba(42,167,223,.25);
        }

        .tg-name { font-size:.9rem; font-weight:700; color:#fff; }
        .tg-handle { font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.68rem; color:var(--muted); margin-top:2px; }

        .tg-desc { font-size:.78rem; color:#94a3b8; line-height:1.6; margin-bottom:16px; }

        .tg-btn {
            display:flex; align-items:center; justify-content:center; gap:8px;
            padding:11px 16px; border-radius:12px; text-decoration:none;
            background:linear-gradient(135deg,#2eb8e6,#1aa34a);
            color:#021a10; font-weight:800; font-size:.82rem; letter-spacing:.02em;
            transition:transform .2s, box-shadow .2s;
            box-shadow: 0 8px 22px rgba(42,167,223,.28);
        }
        .tg-btn:hover { transform:translateY(-2px); box-shadow: 0 12px 28px rgba(42,167,223,.38); }

        /* ─── MAIN GRID ───────────────────────────────── */
        .main-grid {
            display:grid; grid-template-columns:1fr;
            gap:20px;
        }
        @media(min-width:1024px){ .main-grid { grid-template-columns:300px 1fr; } }
        @media(min-width:1280px){ .main-grid { grid-template-columns:320px 1fr; } }

        /* ─── SIDEBAR ─────────────────────────────────── */
        .sidebar { display:flex; flex-direction:column; gap:16px; }

        .panel { padding:22px; }

        .panel-title {
            display:flex; align-items:center; gap:8px;
            font-size:.7rem; font-weight:600; letter-spacing:.2em; text-transform:uppercase; color:#94a3b8;
            margin-bottom:18px;
        }
        .panel-title svg { width:14px; height:14px; opacity:.7; }

        label.field-label {
            display:flex; justify-content:space-between; align-items:center;
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif;
            font-size:.62rem; color:var(--muted); letter-spacing:.15em; text-transform:uppercase; margin-bottom:7px;
        }
        .val-badge { color:var(--c); font-weight:bold; }

        .glass-input {
            width:100%; padding:10px 14px;
            background:rgba(0,0,0,.28); border:1px solid var(--border);
            border-radius:12px; color:#f8fafc; font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.78rem; line-height:1.6;
            transition:border-color .25s, box-shadow .25s;
            box-shadow: inset 0 2px 4px rgba(0,0,0,.25);
            resize: vertical;
        }
        .glass-input:focus {
            outline:none; border-color:rgba(0,229,255,.5);
            box-shadow: inset 0 2px 4px rgba(0,0,0,.25), 0 0 0 3px rgba(0,229,255,.12);
        }

        /* Slider */
        .glass-slider {
            -webkit-appearance: none; appearance: none;
            width: 100%; height: 6px; border-radius: 4px;
            background: rgba(255,255,255,0.1); outline: none;
            margin-top: 6px; margin-bottom: 6px;
        }
        .glass-slider::-webkit-slider-thumb {
            -webkit-appearance: none; appearance: none;
            width: 16px; height: 16px; border-radius: 50%;
            background: var(--c); cursor: pointer;
            box-shadow: 0 0 10px rgba(0,229,255,0.5);
            transition: transform 0.1s;
        }
        .glass-slider::-webkit-slider-thumb:hover { transform: scale(1.2); }

        .field-gap { margin-bottom:14px; }

        /* Toggle */
        .toggle-row {
            display:flex; align-items:center; justify-content:space-between;
            padding:10px 14px; border-radius:12px;
            border:1px solid var(--border); background:rgba(0,0,0,.2);
        }
        .toggle-label-text { font-size:.82rem; color:#cbd5e1; font-weight:500; }
        .toggle-wrap { position:relative; width:46px; height:24px; }
        .toggle-input {
            position:absolute; inset:0; opacity:0; cursor:pointer; width:100%; height:100%; z-index:2; margin:0;
        }
        .toggle-track {
            position:absolute; inset:0; border-radius:999px;
            background:#334155; border:1px solid #475569;
            transition:background .25s, border-color .25s, box-shadow .25s;
        }
        .toggle-thumb {
            position:absolute; top:3px; left:3px; width:16px; height:16px;
            border-radius:50%; background:#fff;
            transition:transform .25s cubic-bezier(.4,0,.2,1); pointer-events:none; z-index:1;
        }
        .toggle-input:checked ~ .toggle-track {
            background:var(--c); border-color:var(--c);
            box-shadow:0 0 12px rgba(0,229,255,.4);
        }
        .toggle-input:checked ~ .toggle-thumb { transform:translateX(22px); }

        /* Buttons */
        .btn-group { display: flex; gap: 10px; margin-top: 18px; }
        
        .scan-btn {
            flex: 1; padding:13px 20px; border-radius:14px; border:none; cursor:pointer;
            background: linear-gradient(135deg, #4facfe 0%, #00e5ff 100%);
            color:#0f172a; font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-weight:800; font-size:.9rem; letter-spacing:.02em;
            display:flex; align-items:center; justify-content:center; gap:8px;
            position:relative; overflow:hidden; transition:all .3s cubic-bezier(.4,0,.2,1);
            box-shadow: 0 4px 16px rgba(0,229,255,.35);
        }
        .scan-btn::before {
            content:''; position:absolute; inset:0;
            background:linear-gradient(135deg,#00e5ff 0%,#4facfe 100%);
            opacity:0; transition:opacity .3s;
        }
        .scan-btn:hover:not(:disabled) { transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,229,255,.5); }
        .scan-btn:hover:not(:disabled)::before { opacity:1; }
        .scan-btn:disabled {
            background:rgba(255,255,255,.06); color:rgba(255,255,255,.25);
            box-shadow:none; cursor:not-allowed; border:1px solid rgba(255,255,255,.05);
        }

        .stop-btn {
            flex: 1; padding:13px 20px; border-radius:14px; border:none; cursor:pointer;
            background: linear-gradient(135deg, #f43f5e 0%, #ef4444 100%);
            color:#fff; font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-weight:800; font-size:.9rem; letter-spacing:.02em;
            display:flex; align-items:center; justify-content:center; gap:8px;
            position:relative; overflow:hidden; transition:all .3s cubic-bezier(.4,0,.2,1);
            box-shadow: 0 4px 16px rgba(239,68,68,.35);
        }
        .stop-btn:hover:not(:disabled) { transform:translateY(-2px); box-shadow:0 8px 24px rgba(239,68,68,.5); }

        .export-btn {
            padding:6px 12px; border-radius:8px; border:1px solid rgba(16,185,129,0.3); cursor:pointer;
            background: rgba(16,185,129,0.1);
            color:#34d399; font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-weight:600; font-size:.75rem; letter-spacing:.02em;
            display:flex; align-items:center; justify-content:center; gap:6px;
            transition:all .2s ease;
        }
        .export-btn:hover { background: rgba(16,185,129,0.2); box-shadow:0 2px 8px rgba(16,185,129,0.2); }

        .scan-btn span, .scan-btn svg, .stop-btn span, .stop-btn svg { position:relative; z-index:1; }
        .spin { animation:spin .8s linear infinite; }
        @keyframes spin { to { transform:rotate(360deg); } }
        .hidden { display:none !important; }

        /* ─── METRICS ─────────────────────────────────── */
        .metrics-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }

        .metric-card {
            border-radius:14px; padding:14px 12px;
            display:flex; flex-direction:column; align-items:center; justify-content:center;
            background:rgba(0,0,0,.25); border:1px solid var(--border);
        }
        .metric-card.emerald { background:rgba(16,185,129,.07); border-color:rgba(16,185,129,.2); box-shadow:inset 0 0 16px rgba(16,185,129,.04); }
        .metric-card.emerald .metric-num { color:var(--c3); }
        .metric-card.emerald .metric-label { color:rgba(16,185,129,.7); }

        .metric-card.blue { background:rgba(0,229,255,.07); border-color:rgba(0,229,255,.2); box-shadow:inset 0 0 16px rgba(0,229,255,.04); }
        .metric-card.blue .metric-num { color:var(--c); }
        .metric-card.blue .metric-label { color:rgba(0,229,255,.7); }

        .metric-card.purple { background:rgba(124,58,237,.07); border-color:rgba(124,58,237,.2); }
        .metric-card.purple .metric-num { color:var(--c2); }
        .metric-card.purple .metric-label { color:rgba(124,58,237,.7); }

        .metric-card.red { background:rgba(239,68,68,.07); border-color:rgba(239,68,68,.2); }
        .metric-card.red .metric-num { color:var(--red); }
        .metric-card.red .metric-label { color:rgba(239,68,68,.7); }

        .metric-num {
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:1.6rem; font-weight:700;
            line-height:1; margin-bottom:5px;
        }

        .metric-label {
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.58rem; letter-spacing:.18em; text-transform:uppercase;
        }

        /* ─── RESULTS PANEL ───────────────────────────── */
        .results-panel {
            display:flex; flex-direction:column; overflow:hidden; max-height:780px;
        }

        .results-header {
            padding:16px 22px;
            display:flex; align-items:center; justify-content:space-between;
            border-bottom:1px solid var(--border);
            background:rgba(255,255,255,.02);
        }

        .results-title {
            display:flex; align-items:center; gap:8px;
            font-size:.7rem; font-weight:600; letter-spacing:.2em; text-transform:uppercase; color:#94a3b8;
        }

        .header-actions {
            display: flex; align-items: center; gap: 12px;
        }

        .status-chip {
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.68rem;
            padding:4px 12px; border-radius:999px;
            background:rgba(0,229,255,.08); color:var(--c); border:1px solid rgba(0,229,255,.2);
            transition:all .3s;
        }
        .status-chip.done { background:rgba(16,185,129,.08); color:#34d399; border-color:rgba(16,185,129,.2); }
        .status-chip.error { background:rgba(239,68,68,.08); color:#f87171; border-color:rgba(239,68,68,.2); }
        .status-chip.stopped { background:rgba(245,158,11,.08); color:#fbbf24; border-color:rgba(245,158,11,.2); }

        .table-wrap {
            flex:1; overflow:auto;
            scrollbar-width:thin; scrollbar-color:rgba(255,255,255,.08) transparent;
        }
        .table-wrap::-webkit-scrollbar { width:6px; height:6px; }
        .table-wrap::-webkit-scrollbar-track { background:transparent; }
        .table-wrap::-webkit-scrollbar-thumb { background:rgba(255,255,255,.1); border-radius:4px; }
        .table-wrap::-webkit-scrollbar-thumb:hover { background:rgba(255,255,255,.2); }

        table { width:100%; border-collapse:collapse; }

        thead th {
            padding:10px 18px; text-align:left;
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.6rem; letter-spacing:.18em; text-transform:uppercase; color:var(--muted);
            background:rgba(10,15,25,.92); backdrop-filter:blur(12px);
            position:sticky; top:0; z-index:5; white-space:nowrap;
            border-bottom:1px solid var(--border);
        }
        thead th:last-child { text-align:right; }
        thead th.center { text-align:center; }

        tbody tr {
            border-bottom:1px solid rgba(255,255,255,.03);
            animation:fadeRow .25s ease;
            transition:background .2s;
        }
        tbody tr:hover { background:rgba(255,255,255,.025); }
        tbody tr:last-child { border-bottom:none; }

        @keyframes fadeRow {
            from { opacity:0; transform:translateY(-4px); }
            to { opacity:1; transform:translateY(0); }
        }

        td {
            padding:11px 18px; white-space:nowrap; font-size:.82rem;
        }

        .row-num { font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; color:var(--muted); font-size:0.75rem; text-align:center; }
        
        .copy-btn {
            display:inline-flex; align-items:center; justify-content:center;
            width:24px; height:24px; border-radius:6px; background:rgba(255,255,255,0.05); color:var(--muted);
            border:1px solid transparent; cursor:pointer; transition:all 0.2s; margin-left:8px;
        }
        .copy-btn:hover { background:rgba(0,229,255,0.1); color:var(--c); border-color:rgba(0,229,255,0.3); }
        .copy-btn svg { width:13px; height:13px; }

        .target-cell { font-weight:600; color:#e2e8f0; }
        .ip-cell { font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.72rem; color:var(--muted); }
        .ping-ok { font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.78rem; color:#34d399; }
        .ping-to { font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.78rem; color:#475569; }
        .check-ok { color:#34d399; font-size:.9rem; }
        .check-fail { color:#f87171; font-size:.9rem; }
        .td-center { text-align:center; }
        .td-right { text-align:right; }

        /* TCP/SNI combined cell */
        .checks-cell {
            display:flex; align-items:center; justify-content:center; gap:6px;
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.72rem;
        }
        .check-item { display:flex; align-items:center; gap:3px; }
        .check-sep { color:var(--border-hi); }

        /* ─── CDN BADGE ───────────────────────────────── */
        .cdn-badge {
            display:inline-flex; align-items:center; gap:6px;
            padding:4px 10px; border-radius:8px;
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.65rem; font-weight:600; letter-spacing:.05em; text-transform:uppercase;
            white-space:nowrap;
        }
        .cdn-icon { width:14px; height:14px; flex-shrink:0; }

        /* CDN colors */
        .cdn-cf   { background:rgba(249,115,22,.1); color:#fb923c; border:1px solid rgba(249,115,22,.25); }
        .cdn-vc   { background:rgba(255,255,255,.07); color:#e2e8f0; border:1px solid rgba(255,255,255,.15); }
        .cdn-aws  { background:rgba(255,153,0,.1); color:#fbbf24; border:1px solid rgba(255,153,0,.25); }
        .cdn-gcp  { background:rgba(66,133,244,.1); color:#60a5fa; border:1px solid rgba(66,133,244,.25); }
        .cdn-az   { background:rgba(0,120,212,.1); color:#38bdf8; border:1px solid rgba(0,120,212,.25); }
        .cdn-fly  { background:rgba(100,200,255,.1); color:#7dd3fc; border:1px solid rgba(100,200,255,.25); }
        .cdn-fst  { background:rgba(255,0,96,.1); color:#f87171; border:1px solid rgba(255,0,96,.2); }
        .cdn-ak   { background:rgba(0,160,140,.1); color:#2dd4bf; border:1px solid rgba(0,160,140,.2); }
        .cdn-gc   { background:rgba(148,163,184,.1); color:#94a3b8; border:1px solid rgba(148,163,184,.2); }
        .cdn-none { color:#475569; }

        /* ─── VERDICT BADGE ───────────────────────────── */
        .verdict {
            display:inline-flex; align-items:center; gap:5px;
            padding:4px 10px; border-radius:8px;
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.65rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase;
        }
        .v-sni     { background:rgba(16,185,129,.12); color:#34d399; border:1px solid rgba(16,185,129,.25); }
        .v-cdn     { background:rgba(14,165,233,.12); color:#38bdf8; border:1px solid rgba(14,165,233,.25); }
        .v-tcp-ping{ background:rgba(16,185,129,.12); color:#34d399; border:1px solid rgba(16,185,129,.25); }
        .v-ping    { background:rgba(0,229,255,.12); color:#00e5ff; border:1px solid rgba(0,229,255,.25); }
        .v-tcp     { background:rgba(124,58,237,.12); color:#a78bfa; border:1px solid rgba(124,58,237,.25); }
        .v-down    { background:rgba(239,68,68,.1); color:#f87171; border:1px solid rgba(239,68,68,.2); }

        /* ─── EMPTY STATE ─────────────────────────────── */
        .empty-state {
            display:flex; flex-direction:column; align-items:center; justify-content:center;
            padding:72px 24px; gap:16px; color:var(--muted);
        }
        .empty-icon {
            width:56px; height:56px; border-radius:18px;
            background:rgba(255,255,255,.04); border:1px solid var(--border);
            display:flex; align-items:center; justify-content:center;
        }
        .empty-text {
            font-family:"AradWeb", "Segoe UI", "Trebuchet MS", "Arial", sans-serif; font-size:.68rem; letter-spacing:.2em; text-transform:uppercase;
        }
    </style>
</head>
<body>
<div class="page">

    <header class="card header">
        <div class="header-brand">
            <div class="header-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            </div>
            <div>
                <div class="brand-name">SNI Radar</div>
                <div class="brand-sub">{{ channel_handle }} · Network Intelligence</div>
            </div>
        </div>
        <div class="header-pills">
            <span class="pill"><span class="pulse-dot"></span>Live Stream</span>
            <span class="pill">SNI · TCP · PING · CDN</span>
        </div>
    </header>

    <section class="card hero">
        <div class="hero-glow"></div>
        <div class="hero-content">
            <div class="hero-logo">
                <img src="{{ channel_logo_url }}" alt="{{ channel_name }}">
            </div>
            <div class="hero-text">
                <div class="hero-tags">
                    <span class="tag">{{ channel_name }}</span>
                    <span class="tag">Telegram</span>
                    <span class="tag">Network Probe</span>
                </div>
                <h1 class="hero-title">Intelligent SNI &amp; CDN Scanner</h1>
                <p class="hero-desc">پینگ، TCP، SNI و CDN را هم‌زمان بررسی کن<br>با ذخیره دستی و مرتب‌سازی هوشمند نتایج</p>
            </div>
        </div>

        <div class="channel-card">
            <div class="tg-row">
                <div class="tg-icon">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="white"><path d="M9.78 15.75 9.44 20.5c.49 0 .7-.21.95-.45l2.36-2.26 4.89 3.58c.89.49 1.52.23 1.74-.82l3.17-14.89c.28-1.31-.47-1.82-1.35-1.49L1.72 9.57C.45 10.06.47 10.77 1.5 11.09l4.47 1.4 10.38-6.54c.49-.31.94-.14.57.17Z"/></svg>
                </div>
                <div>
                    <div class="tg-name">{{ channel_name }}</div>
                    <div class="tg-handle">{{ channel_handle }}</div>
                </div>
            </div>
            <p class="tg-desc">برای خبرها، نسخه‌های جدید و نتایج تست شبکه کانال را دنبال کن.</p>
            <a class="tg-btn" href="{{ channel_url }}" target="_blank" rel="noopener">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M9.78 15.75 9.44 20.5c.49 0 .7-.21.95-.45l2.36-2.26 4.89 3.58c.89.49 1.52.23 1.74-.82l3.17-14.89c.28-1.31-.47-1.82-1.35-1.49L1.72 9.57C.45 10.06.47 10.77 1.5 11.09l4.47 1.4 10.38-6.54c.49-.31.94-.14.57.17Z"/></svg>
                Open in Telegram
                <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M9 7h8v8"/></svg>
            </a>
        </div>
    </section>

    <div class="main-grid">

        <div class="sidebar">
            <div class="card panel">
                <div class="panel-title">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
                    Configuration
                </div>

                <div class="field-gap">
                    <label class="field-label">Targets · Domains / IPs / CIDRs</label>
                    <textarea id="targets" rows="9" class="glass-input" spellcheck="false">{{ default_targets }}</textarea>
                </div>

                <div class="field-gap">
                    <label class="field-label">Max CIDR Hosts</label>
                    <input type="number" id="maxHosts" value="4096" class="glass-input" style="resize:none">
                </div>
                
                <div class="field-gap">
                    <label class="field-label">Speed (Threads) <span class="val-badge" id="threadVal">10</span></label>
                    <input type="range" id="threads" min="1" max="100" value="10" class="glass-slider">
                </div>

                <div class="field-gap">
                    <div class="toggle-row">
                        <span class="toggle-label-text">Strict Ping Mode</span>
                        <div class="toggle-wrap">
                            <input type="checkbox" class="toggle-input" id="strictPing" checked>
                            <div class="toggle-track"></div>
                            <div class="toggle-thumb"></div>
                        </div>
                    </div>
                </div>

                <div class="btn-group">
                    <button id="scanBtn" class="scan-btn">
                        <svg id="spinner" class="hidden spin" width="18" height="18" fill="none" viewBox="0 0 24 24">
                            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity=".25"/>
                            <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" opacity=".75"/>
                        </svg>
                        <span id="btnText">Start Scan</span>
                    </button>
                    <button id="stopBtn" class="stop-btn hidden">
                        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                            <rect x="6" y="6" width="12" height="12" rx="2"></rect>
                        </svg>
                        <span>Stop</span>
                    </button>
                </div>
            </div>

            <div class="card panel">
                <div class="panel-title" style="justify-content: space-between; width: 100%;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                        Live Metrics
                    </div>
                    <div style="color: #fff; font-size: 0.9rem;" id="stat-total-header">Checked: 0/0</div>
                </div>
                <div class="metrics-grid">
                    <div class="metric-card emerald">
                        <div class="metric-num" id="stat-tcp-ping">0</div>
                        <div class="metric-label">TCP &amp; PING</div>
                    </div>
                    <div class="metric-card blue">
                        <div class="metric-num" id="stat-ping">0</div>
                        <div class="metric-label">PING ONLY</div>
                    </div>
                    <div class="metric-card purple">
                        <div class="metric-num" id="stat-tcp">0</div>
                        <div class="metric-label">TCP ONLY</div>
                    </div>
                    <div class="metric-card red">
                        <div class="metric-num" id="stat-down">0</div>
                        <div class="metric-label">DOWN</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card results-panel">
            <div class="results-header">
                <div class="results-title">
                    <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg>
                    Scan Results
                </div>
                <div class="header-actions">
                    <button id="exportBtn" class="export-btn hidden" onclick="exportResults()">
                        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                        Export TXT
                    </button>
                    <span id="scan-time" class="status-chip">Ready</span>
                </div>
            </div>

            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 40px; text-align: center;">#</th>
                            <th>Target</th>
                            <th>IP Address</th>
                            <th>Ping</th>
                            <th class="center">TCP / SNI</th>
                            <th class="center">Provider</th>
                            <th style="text-align:right">Verdict</th>
                        </tr>
                    </thead>
                    <tbody id="resultsBody">
                        <tr>
                            <td colspan="7">
                                <div class="empty-state">
                                    <div class="empty-icon">
                                        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                                    </div>
                                    <div class="empty-text">Waiting for scan…</div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</div>

<script>
// ─── COPY TO CLIPBOARD ──────────────────────────────────────────────
window.copyText = function(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = btn.innerHTML;
        btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>`;
        setTimeout(() => { btn.innerHTML = originalHTML; }, 1500);
    });
};

// ─── UPDATE ROW NUMBERS ─────────────────────────────────────────────
function updateRowNumbers() {
    const rows = document.getElementById('resultsBody').children;
    for(let i=0; i<rows.length; i++) {
        const numCell = rows[i].querySelector('.row-num-cell');
        if(numCell) numCell.textContent = i + 1;
    }
}

// ─── CDN PROVIDER DATABASE ──────────────────────────────────────────
const CDN_PROVIDERS = {
    CLOUDFLARE: {
        label: 'Cloudflare',
        cls: 'cdn-cf',
        icon: `<svg class="cdn-icon" viewBox="0 0 128 128" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M113.2 72.4c-.5-1.5-2-2.5-3.6-2.5H33.9l-.6-1.8C30.9 60.7 23.9 55 15.8 55c-8.8 0-16 7.1-16 15.8C-.2 80.1 7.2 87.3 16.2 87h91c1.5 0 2.9-1 3.4-2.5l2.6-12.1z" fill="#F6821F"/><path d="M68.8 49.2l-.5-1.7C65.5 38.3 57.2 32 47.6 32c-11.4 0-20.7 9.2-20.7 20.5 0 1.1.1 2.2.2 3.2C19.8 57 14.3 63 14.3 70.3c0 8.3 6.8 15 15.1 15h60c7.2 0 13-5.8 13-12.9.1-6.8-5.2-12.3-11.9-13-.8 0-1.5-.1-2.3-.1-8.4 0-15.7 4.9-19.4 11.9" fill="#FBAD41"/></svg>`
    },
    AMAZON: {
        label: 'Amazon AWS',
        cls: 'cdn-aws',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="#FF9900"><path d="M6.763 10.036c0 .296.032.535.088.71.064.176.144.368.256.576.04.072.056.144.056.208 0 .088-.056.184-.168.272l-.552.368c-.08.056-.16.08-.232.08-.088 0-.176-.04-.264-.12-.12-.128-.224-.264-.312-.4-.088-.144-.176-.304-.272-.496C4.56 12.224 3.96 12.56 3.104 12.56c-.576 0-1.04-.16-1.376-.488-.336-.32-.512-.744-.512-1.28 0-.568.2-1.024.608-1.36.408-.336.952-.504 1.648-.504.224 0 .456.016.704.056.248.04.504.096.768.168v-.488c0-.504-.104-.856-.32-1.064-.216-.216-.584-.32-1.112-.32-.24 0-.488.024-.744.08-.256.056-.504.128-.744.224-.112.048-.192.072-.24.08-.048.008-.08.016-.104.016-.088 0-.136-.064-.136-.192V7.32c0-.104.016-.176.04-.224.032-.04.088-.08.176-.12.24-.12.528-.224.864-.312.336-.08.688-.128 1.064-.128.808 0 1.4.184 1.784.56.376.376.568.944.568 1.712v2.228zm-2.344.872c.216 0 .44-.04.672-.12.232-.08.44-.224.616-.424.104-.128.184-.264.224-.416.04-.16.064-.352.064-.576v-.28c-.192-.048-.4-.088-.616-.112-.216-.024-.424-.04-.624-.04-.448 0-.776.088-1 .264-.224.176-.336.432-.336.776 0 .312.08.544.24.704.16.168.4.224.76.224zm5.44.712c-.12 0-.2-.016-.256-.056-.056-.04-.104-.12-.144-.24l-1.608-5.296c-.04-.12-.064-.2-.064-.256 0-.104.048-.16.144-.16h.656c.128 0 .208.016.264.056.056.04.096.12.128.24l1.152 4.536 1.064-4.536c.032-.12.072-.2.128-.24.064-.04.144-.056.272-.056h.528c.128 0 .216.016.272.056.056.04.104.12.128.24l1.08 4.6 1.184-4.6c.032-.12.08-.2.128-.24.056-.04.136-.056.256-.056h.616c.104 0 .16.048.16.16 0 .032-.008.064-.016.104-.008.04-.016.08-.04.136l-1.64 5.296c-.04.12-.088.2-.144.24-.056.04-.136.056-.256.056h-.568c-.128 0-.216-.016-.272-.056-.056-.04-.104-.12-.128-.248l-1.064-4.44-1.056 4.432c-.032.128-.08.208-.128.248-.056.04-.144.056-.28.056h-.568zm8.72.152c-.352 0-.704-.04-1.04-.128-.344-.088-.608-.184-.784-.296-.104-.064-.176-.128-.2-.192-.024-.072-.04-.144-.04-.208V10.664c0-.128.056-.192.16-.192.04 0 .08.008.12.016.04.016.096.04.168.072.224.104.472.184.744.24.28.056.552.08.832.08.44 0 .776-.072 1.008-.224.232-.152.352-.36.352-.64 0-.192-.064-.344-.184-.48-.12-.128-.352-.248-.688-.352l-.984-.304c-.496-.152-.864-.384-1.104-.688-.24-.296-.36-.632-.36-1.008 0-.288.072-.544.2-.768.136-.224.32-.416.544-.576.224-.16.48-.28.768-.36.288-.08.592-.12.904-.12.16 0 .328.008.496.024.168.024.32.048.48.08.144.04.28.08.408.12.128.04.232.08.304.12.104.064.176.128.216.2.04.064.056.144.056.24v.344c0 .128-.056.2-.16.2-.056 0-.144-.024-.264-.08-.448-.2-.952-.296-1.52-.296-.4 0-.712.064-.936.2-.224.136-.336.336-.336.608 0 .192.072.352.216.488.144.136.408.264.776.384l.96.304c.488.152.84.368 1.064.648.224.28.336.6.336.968 0 .296-.072.568-.208.808-.136.24-.32.448-.56.616-.24.168-.52.296-.84.384-.32.096-.672.144-1.056.144zm5.6-.152a5.19 5.19 0 01-.592-.04 3.94 3.94 0 01-.536-.12c-.152-.048-.28-.104-.384-.168-.096-.064-.16-.128-.184-.2-.032-.064-.048-.136-.048-.216v-.36c0-.128.056-.192.168-.192.048 0 .088.008.12.016.048.016.104.04.168.072.232.096.48.168.744.216.272.048.544.08.824.08.44 0 .784-.072 1.016-.224.232-.152.352-.36.352-.64 0-.192-.064-.344-.184-.48-.12-.128-.352-.248-.688-.36l-.984-.296c-.496-.152-.864-.384-1.104-.688-.24-.296-.36-.632-.36-1.008 0-.288.072-.544.208-.768.136-.224.32-.416.544-.576.224-.16.48-.28.768-.36.288-.08.592-.12.904-.12.16 0 .328.008.496.024.168.024.32.048.48.08.144.04.28.08.408.12.128.04.232.08.304.12.104.064.176.128.216.2.04.064.056.144.056.24v.344c0 .128-.056.2-.16.2-.056 0-.144-.024-.264-.08-.448-.2-.952-.296-1.52-.296-.4 0-.712.064-.936.2-.224.136-.336.336-.336.608 0 .192.072.352.216.488.144.136.408.264.776.384l.96.296c.488.152.84.368 1.064.648.224.28.336.6.336.968 0 .296-.072.568-.208.808-.136.24-.32.448-.56.616-.24.168-.52.296-.84.384-.328.096-.688.144-1.072.144z"/></svg>`
    },
    VERCEL: {
        label: 'Vercel',
        cls: 'cdn-vc',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 19.778h20L12 2z"/></svg>`
    },
    FASTLY: {
        label: 'Fastly',
        cls: 'cdn-fst',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="#FF282D"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>`
    },
    AKAMAI: {
        label: 'Akamai',
        cls: 'cdn-ak',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#009BDE"/><path d="M7 12c0-2.76 2.24-5 5-5s5 2.24 5-5-2.24 5-5 5-5-2.24-5-5z" stroke="white" stroke-width="1.5"/><circle cx="12" cy="12" r="2" fill="white"/></svg>`
    },
    GOOGLE: {
        label: 'Google Cloud',
        cls: 'cdn-gcp',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="none"><path d="M12 6.5a5.5 5.5 0 015.5 5.5H20a8 8 0 00-8-8v2.5z" fill="#4285F4"/><path d="M6.5 12A5.5 5.5 0 0112 6.5V4a8 8 0 00-8 8h2.5z" fill="#34A853"/><path d="M12 17.5a5.5 5.5 0 01-5.5-5.5H4a8 8 0 008 8v-2.5z" fill="#FBBC05"/><path d="M17.5 12a5.5 5.5 0 01-5.5 5.5V20a8 8 0 008-8h-2.5z" fill="#EA4335"/></svg>`
    },
    MICROSOFT: {
        label: 'Azure / MS',
        cls: 'cdn-az',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="none"><path d="M5 12.5L10.5 4l5 8.5H5z" fill="#0078D4"/><path d="M10.5 4l5 8.5L19 20H5l5.5-7.5" fill="#50E6FF" opacity=".8"/></svg>`
    },
    GCORE: {
        label: 'Gcore',
        cls: 'cdn-gc',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="#94a3b8"><circle cx="12" cy="12" r="10" stroke="#94a3b8" stroke-width="1.5" fill="none"/><path d="M12 7v5l3 3" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/></svg>`
    }
};

function getCDNInfo(cdnKey) {
    if (!cdnKey || cdnKey === 'NONE') return null;
    return CDN_PROVIDERS[cdnKey.toUpperCase()] || {
        label: cdnKey,
        cls: 'cdn-gc',
        icon: `<svg class="cdn-icon" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20"/></svg>`
    };
}

function renderCDN(cdnKey) {
    const info = getCDNInfo(cdnKey);
    if (!info) return `<span class="cdn-none">—</span>`;
    return `<span class="cdn-badge ${info.cls}">${info.icon}${info.label}</span>`;
}

function renderVerdict(status) {
    const map = {
        'SNI-USABLE': ['v-sni', '✦ SNI Usable'],
        'CDN-USABLE': ['v-cdn', '◈ CDN Usable'],
        'TCP+PING':   ['v-tcp-ping', '✓ TCP + Ping'],
        'PING-ONLY':  ['v-ping', '◐ Ping Only'],
        'TCP-ONLY':   ['v-tcp', '◐ TCP Only'],
        'DOWN':       ['v-down', '✕ Down'],
    };
    const [cls, label] = map[status] || ['', status];
    return `<span class="verdict ${cls}">${label}</span>`;
}

// Live Update Threads Counter
document.getElementById('threads').addEventListener('input', (e) => {
    document.getElementById('threadVal').textContent = e.target.value;
});

let isScanning = false;
let successfulResultsTxt = ""; 

const copyIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;

async function runScan() {
    if (isScanning) return;
    
    const btn        = document.getElementById('scanBtn');
    const stopBtn    = document.getElementById('stopBtn');
    const exportBtn  = document.getElementById('exportBtn');
    const btnText    = document.getElementById('btnText');
    const spinner    = document.getElementById('spinner');
    const tbody      = document.getElementById('resultsBody');
    const statusChip = document.getElementById('scan-time');

    const rawTargets = document.getElementById('targets').value;
    const lines      = rawTargets.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
    const strictPing = document.getElementById('strictPing').checked;
    const maxHosts   = parseInt(document.getElementById('maxHosts').value, 10) || 4096;
    const threads    = parseInt(document.getElementById('threads').value, 10) || 10;

    if (lines.length === 0) return;

    isScanning = true;
    successfulResultsTxt = "";
    btn.classList.add('hidden');
    exportBtn.classList.add('hidden');
    stopBtn.classList.remove('hidden');
    
    tbody.innerHTML = '';
    statusChip.className = 'status-chip';
    statusChip.textContent = 'Initializing…';

    document.getElementById('stat-total-header').textContent = 'Checked: 0';
    document.getElementById('stat-tcp-ping').textContent   = '0';
    document.getElementById('stat-ping').textContent       = '0';
    document.getElementById('stat-tcp').textContent        = '0';
    document.getElementById('stat-down').textContent       = '0';

    try {
        const resp = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ targets: lines, strict_ping: strictPing, max_hosts: maxHosts, threads: threads })
        });

        if (!resp.body) throw new Error('Streaming not supported.');

        const reader  = resp.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const parts = buffer.split(/\\r?\\n/);
            buffer = parts.pop();

            for (const part of parts) {
                if (!part.trim()) continue;
                const data = JSON.parse(part);

                if (data.type === 'init') {
                    statusChip.textContent = `0 / ${data.total}`;

                } else if (data.type === 'progress') {
                    const r = data.result, s = data.stats;

                    if (s.checked === 1) {
                        tbody.innerHTML = '';
                    }

                    statusChip.textContent = `${s.checked} / ${s.total}`;
                    document.getElementById('stat-total-header').textContent = `Checked: ${s.checked} / ${s.total}`;
                    document.getElementById('stat-tcp-ping').textContent   = s.tcp_ping;
                    document.getElementById('stat-ping').textContent       = s.ping_only;
                    document.getElementById('stat-tcp').textContent        = s.tcp_only;
                    document.getElementById('stat-down').textContent       = s.down;

                    const pingHTML = r.ping_ms !== null
                        ? `<span class="ping-ok">${Math.round(r.ping_ms)} ms</span>`
                        : `<span class="ping-to">T/O</span>`;

                    const ok   = v => `<span class="check-ok">✓</span><span style="font-family:'AradWeb','Segoe UI','Trebuchet MS','Arial',sans-serif;font-size:.7rem;color:#94a3b8">${v}</span>`;
                    const fail = v => `<span class="check-fail">✗</span><span style="font-family:'AradWeb','Segoe UI','Trebuchet MS','Arial',sans-serif;font-size:.7rem;color:#475569">${v}</span>`;

                    // Smart Live Sorting Score (Float calculation)
                    let baseScore = 0;
                    if (r.tcp_ok && r.ping_ok) baseScore = 30000;
                    else if (!r.tcp_ok && r.ping_ok) baseScore = 20000;
                    else if (r.tcp_ok && !r.ping_ok) baseScore = 10000;
                    else baseScore = 0;

                    let pingVal = (r.ping_ms !== null && r.ping_ms !== undefined) ? parseFloat(r.ping_ms) : 5000;
                    if (isNaN(pingVal)) pingVal = 5000;

                    let score = baseScore - pingVal;

                    const tr = document.createElement('tr');
                    tr.dataset.score = score;
                    tr.innerHTML = `
                        <td class="row-num-cell row-num"></td>
                        <td class="target-cell">
                            <div style="display:flex; align-items:center;">
                                ${r.target}
                                <button class="copy-btn" onclick="copyText('${r.target}', this)" title="Copy Target">${copyIcon}</button>
                            </div>
                        </td>
                        <td class="ip-cell">
                            <div style="display:flex; align-items:center;">
                                ${r.ip}
                                <button class="copy-btn" onclick="copyText('${r.ip}', this)" title="Copy IP">${copyIcon}</button>
                            </div>
                        </td>
                        <td>${pingHTML}</td>
                        <td class="td-center">
                            <div class="checks-cell">
                                <div class="check-item">${r.tcp_ok ? ok('TCP') : fail('TCP')}</div>
                                <span class="check-sep">|</span>
                                <div class="check-item">${r.sni_ok ? ok('SNI') : fail('SNI')}</div>
                            </div>
                        </td>
                        <td class="td-center">${renderCDN(r.cdn)}</td>
                        <td class="td-right">${renderVerdict(r.overall)}</td>
                    `;

                    // Live Insertion logic
                    let inserted = false;
                    const rows = tbody.children;
                    for (let i = 0; i < rows.length; i++) {
                        const rowScore = parseFloat(rows[i].dataset.score);
                        if (!isNaN(rowScore) && score > rowScore) {
                            tbody.insertBefore(tr, rows[i]);
                            inserted = true;
                            break;
                        }
                    }
                    if (!inserted) {
                        tbody.appendChild(tr);
                    }
                    
                    updateRowNumbers();

                    // Accumulate successful results for export
                    if (r.tcp_ok || r.ping_ok) {
                        let p = r.ping_ms !== null ? Math.round(r.ping_ms) + "ms" : "Timeout";
                        let t = r.tcp_ok ? "OK" : "Failed";
                        successfulResultsTxt += `${r.target} (${r.ip}) - Ping: ${p}, TCP: ${t}\n`;
                    }

                } else if (data.type === 'done') {
                    if (data.metadata.status === 'Stopped') {
                        statusChip.className = 'status-chip stopped';
                        statusChip.textContent = `Stopped · ${data.metadata.elapsed_seconds}s`;
                    } else {
                        statusChip.className = 'status-chip done';
                        statusChip.textContent = `Done · ${data.metadata.elapsed_seconds}s`;
                    }
                    
                    if (successfulResultsTxt.length > 0) {
                        exportBtn.classList.remove('hidden');
                    }
                }
            }
        }
    } catch (err) {
        statusChip.className = 'status-chip error';
        statusChip.textContent = 'Error';
        console.error(err);
    } finally {
        isScanning = false;
        stopBtn.classList.add('hidden');
        btn.classList.remove('hidden');
    }
}

async function stopScan() {
    if (!isScanning) return;
    try {
        await fetch('/api/stop', { method: 'POST' });
        document.getElementById('scan-time').textContent = 'Stopping...';
    } catch (e) {
        console.error(e);
    }
}

function exportResults() {
    if (!successfulResultsTxt) return;
    const blob = new Blob([successfulResultsTxt], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Successful_Targets_${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

document.getElementById('scanBtn').addEventListener('click', runScan);
document.getElementById('stopBtn').addEventListener('click', stopScan);
</script>
</body>
</html>
"""

# Global registry for managing active scans and stop events
ACTIVE_SCANS = {}

class SNIChecker:
    """Scanner that reports ping, TCP, SNI, CDN and usability for domain/IP/CIDR."""

    FALLBACK_IPS = {
        "nextjs.org": ["216.230.86.65", "216.230.84.129"],
        "react.dev": ["66.33.60.193", "66.33.60.66"],
        "vitejs.dev": ["3.33.186.135"],
        "cloudflare.com": ["104.16.132.229"],
        "vercel.com": ["198.169.2.193", "76.76.21.21"],
        "npmjs.com": ["104.17.134.117", "104.17.135.117"],
        "pypi.org": ["151.101.192.223", "151.101.0.223"],
        "e7.c.lencr.org": ["104.18.21.213"],
        "r10.c.lencr.org": ["104.18.20.213"],
    }

    CDN_PREFIXES = {
        "CLOUDFLARE": [
            "104.16.", "104.17.", "104.18.", "104.19.", "104.20.", "104.21.",
            "172.64.", "172.65.", "172.66.", "172.67.", "172.68.", "172.69.",
        ],
        "VERCEL": ["76.76.", "66.33.", "216.230.", "198.169."],
        "FASTLY": ["151.101."],
        "AKAMAI": ["23.", "96.", "124.", "125.", "184.", "203.", "205.", "212."],
        "GCORE": ["195.5."],
    }

    def __init__(self):
        self.platform_system = platform.system().lower()

    @staticmethod
    def get_pretty_os():
        system = platform.system() or "Unknown"
        release = platform.release() or "Unknown"
        version = platform.version() or "Unknown"
        machine = platform.machine() or "Unknown"
        return f"{system} {release} ({version}) [{machine}]"

    @staticmethod
    def check_dns_available():
        try:
            socket.gethostbyname("one.one.one.one")
            return True
        except Exception:
            return False

    @staticmethod
    def is_ip(value):
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_cidr(value):
        try:
            ipaddress.ip_network(value, strict=False)
            return "/" in value
        except ValueError:
            return False

    def expand_targets(self, raw_targets, max_hosts=4096):
        expanded = []
        for item in raw_targets:
            target = item.strip()
            if not target:
                continue

            if self.is_cidr(target):
                network = ipaddress.ip_network(target, strict=False)
                hosts = list(network.hosts())
                if len(hosts) > max_hosts:
                    hosts = hosts[:max_hosts]
                for host in hosts:
                    expanded.append(str(host))
                continue

            expanded.append(target)

        unique = []
        for item in expanded:
            if item not in unique:
                unique.append(item)
        return unique

    def resolve_ips(self, target):
        if self.is_ip(target):
            return [target]

        ips = []
        try:
            resolved = socket.gethostbyname_ex(target)[2]
            ips.extend(resolved)
        except Exception:
            pass

        if target in self.FALLBACK_IPS:
            ips.extend(self.FALLBACK_IPS[target])

        unique = []
        for ip in ips:
            if ip not in unique:
                unique.append(ip)
        return unique

    def check_ping(self, host, timeout_ms=1200):
        if self.platform_system == "windows":
            command = ["ping", "-n", "1", "-w", str(timeout_ms), host]
        else:
            command = ["ping", "-c", "1", "-W", str(max(1, int(timeout_ms / 1000))), host]

        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=(timeout_ms / 1000) + 2,
            )
            output = (proc.stdout or "") + "\n" + (proc.stderr or "")
            ok = proc.returncode == 0

            latency = None
            match_int = re.search(r"time[=<]\s*(\d+)\s*ms", output, flags=re.IGNORECASE)
            match_float = re.search(r"time[=<]\s*(\d+(?:\.\d+)?)", output, flags=re.IGNORECASE)
            if match_int:
                latency = float(match_int.group(1))
            elif match_float:
                latency = float(match_float.group(1))

            return ok, latency
        except Exception:
            return False, None

    @staticmethod
    def check_tcp(ip, port=443, timeout=2.0):
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except Exception:
            return False

    @staticmethod
    def check_tls_sni(domain, ip, timeout=3.0):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((ip, 443), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain):
                    return True
        except Exception:
            return False

    def detect_cdn(self, domain, ip):
        domain_low = domain.lower() if domain else ""
        if "cloudflare" in domain_low:
            return "CLOUDFLARE"
        if "vercel" in domain_low:
            return "VERCEL"
        if "fastly" in domain_low:
            return "FASTLY"

        for cdn_name, prefixes in self.CDN_PREFIXES.items():
            for prefix in prefixes:
                if ip.startswith(prefix):
                    return cdn_name
        return "NONE"

    def evaluate_wrapper(self, target, strict_ping, stop_event):
        if stop_event and stop_event.is_set():
            return None
        return self.evaluate_target(target, strict_ping)

    def evaluate_target(self, target, strict_ping=True):
        target_type = "IP" if self.is_ip(target) else "DOMAIN"
        ips = self.resolve_ips(target)

        if not ips:
            return {
                "target": target, "type": target_type, "ip": "N/A", "ping_ok": False,
                "ping_ms": None, "tcp_ok": False, "sni_ok": False, "cdn": "NONE",
                "sni_usable": False, "cdn_usable": False, "overall": "DOWN",
            }

        best = None
        best_score = -1

        for ip in ips:
            ping_ok, ping_ms = self.check_ping(ip)
            tcp_ok = self.check_tcp(ip)

            if target_type == "DOMAIN" and tcp_ok:
                sni_ok = self.check_tls_sni(target, ip)
            else:
                sni_ok = False

            cdn = self.detect_cdn(target if target_type == "DOMAIN" else "", ip)

            ping_required = strict_ping
            sni_usable = sni_ok and ((ping_ok and ping_required) or (not ping_required and tcp_ok))
            cdn_usable = (cdn != "NONE") and tcp_ok and (ping_ok if ping_required else True)

            if sni_usable: overall = "SNI-USABLE"
            elif cdn_usable: overall = "CDN-USABLE"
            elif tcp_ok and ping_ok: overall = "TCP+PING"
            elif ping_ok: overall = "PING-ONLY"
            elif tcp_ok: overall = "TCP-ONLY"
            else: overall = "DOWN"

            score = (
                (100 if sni_usable else 0) + (70 if cdn_usable else 0) +
                (20 if ping_ok else 0) + (10 if tcp_ok else 0) + (10 if sni_ok else 0)
            )

            row = {
                "target": target, "type": target_type, "ip": ip, "ping_ok": ping_ok,
                "ping_ms": ping_ms, "tcp_ok": tcp_ok, "sni_ok": sni_ok, "cdn": cdn,
                "sni_usable": sni_usable, "cdn_usable": cdn_usable, "overall": overall,
            }

            if score > best_score:
                best_score = score
                best = row

        return best

    @staticmethod
    def load_targets_from_file(path="targets.txt"):
        target_file = Path(path)
        if not target_file.exists(): return []
        items = []
        for raw in target_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"): continue
            items.append(line)
        return items

    def scan_stream(self, raw_targets, strict_ping=True, max_hosts=4096, threads=10, stop_event=None):
        """Generator function that yields live JSON progress strings concurrently."""
        started = datetime.now()
        targets = self.expand_targets(raw_targets, max_hosts=max_hosts)
        total = len(targets)
        
        yield json.dumps({"type": "init", "total": total}) + "\n"

        rows = []
        stats = {"tcp_ping": 0, "ping_only": 0, "tcp_only": 0, "down": 0, "total": total, "checked": 0}
        was_stopped = False

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.evaluate_wrapper, t, strict_ping, stop_event) for t in targets]
            
            for future in concurrent.futures.as_completed(futures):
                if stop_event and stop_event.is_set():
                    was_stopped = True
                    break
                try:
                    row = future.result()
                    if row is None: continue
                    rows.append(row)
                    stats["checked"] += 1

                    if row["tcp_ok"] and row["ping_ok"]: stats["tcp_ping"] += 1
                    elif row["ping_ok"]: stats["ping_only"] += 1
                    elif row["tcp_ok"]: stats["tcp_only"] += 1
                    else: stats["down"] += 1

                    yield json.dumps({"type": "progress", "result": row, "stats": stats}) + "\n"
                except Exception:
                    pass

        elapsed = (datetime.now() - started).total_seconds()
        metadata = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "os": self.get_pretty_os(),
            "dns_available": self.check_dns_available(),
            "strict_ping": strict_ping,
            "elapsed_seconds": round(elapsed, 3),
            "total": total,
            "tcp_ping": stats["tcp_ping"],
            "ping_only": stats["ping_only"],
            "tcp_only": stats["tcp_only"],
            "down": stats["down"],
            "status": "Stopped" if was_stopped else "Completed"
        }

        # Send completion status
        yield json.dumps({"type": "done", "metadata": metadata, "all_results": rows}) + "\n"


DEFAULT_TARGETS = [
    "cloudflare.com",
    "vercel.com",
    "nextjs.org",
    "react.dev",
    "vitejs.dev",
    "npmjs.com",
    "pypi.org",
    "e7.c.lencr.org",
    "1.1.1.1",
    "8.8.8.8",
    "127.0.0.1/30",
]

CHANNEL_NAME = "Persia Team"
CHANNEL_HANDLE = "@PersiaTmChannel"
CHANNEL_URL = "https://t.me/PersiaTmChannel"
CHANNEL_LOGO_URL = "/logo.jpg"


def create_app():
    app = Flask(__name__, static_folder="static")
    checker = SNIChecker()

    @app.get("/")
    def index():
        file_targets = checker.load_targets_from_file("targets.txt")
        merged = DEFAULT_TARGETS + file_targets
        text = "\n".join(merged)
        return render_template_string(
            HTML_TEMPLATE,
            default_targets=text,
            channel_name=CHANNEL_NAME,
            channel_handle=CHANNEL_HANDLE,
            channel_url=CHANNEL_URL,
            channel_logo_url=CHANNEL_LOGO_URL,
        )

    @app.route("/static/<path:filename>")
    def serve_static(filename):
        return send_from_directory("static", filename)

    @app.get("/logo.jpg")
    def serve_logo():
        return send_from_directory(".", "logo.jpg")

    @app.post("/api/scan")
    def scan():
        payload = request.get_json(force=True, silent=False) or {}
        targets = payload.get("targets") or []
        strict_ping = bool(payload.get("strict_ping", True))
        max_hosts = int(payload.get("max_hosts", 4096))
        threads = int(payload.get("threads", 10))

        if not isinstance(targets, list):
            targets = [targets] if targets else []

        targets = [t.strip() for t in targets if t and t.strip()]
        file_targets = checker.load_targets_from_file("targets.txt")
        merged_targets = targets + file_targets

        # Register Stop Event
        job_id = "default_job"
        stop_event = threading.Event()
        ACTIVE_SCANS[job_id] = stop_event

        def generate():
            try:
                for chunk in checker.scan_stream(merged_targets, strict_ping=strict_ping, max_hosts=max_hosts, threads=threads, stop_event=stop_event):
                    data = json.loads(chunk)
                    if data["type"] == "done":
                        
                        file_name = f"sni_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        save_data = {"metadata": data["metadata"], "results": data["all_results"]}
                        try:
                            with open(file_name, "w", encoding="utf-8") as fh:
                                json.dump(save_data, fh, ensure_ascii=False, indent=2)
                            data["metadata"]["saved_json"] = file_name
                        except Exception:
                            pass
                        
                        del data["all_results"] 
                        yield json.dumps(data) + "\n"
                    else:
                        yield chunk
            finally:
                ACTIVE_SCANS.pop(job_id, None)
                
        return Response(stream_with_context(generate()), mimetype="application/x-ndjson")

    @app.post("/api/stop")
    def stop():
        job_id = "default_job"
        if job_id in ACTIVE_SCANS:
            ACTIVE_SCANS[job_id].set()
        return jsonify({"status": "stopping"})

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "time": datetime.now().isoformat()})

    return app

def main():
    app = create_app()
    port = 10808
    url = f"http://0.0.0.0:{port}"
    print(f"🌐 Web UI is starting on {url}")
    try:
        webbrowser.open(f"http://127.0.0.1:{port}")
    except Exception:
        pass
    
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
