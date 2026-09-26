# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request

app = Flask(__name__)

# ─────────────────────────────────────────────
#  All HTML / CSS / JS lives right here in code
# ─────────────────────────────────────────────

HOME_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Chai &mdash; The Soul of India</title>
  <meta name="description" content="Explore the rich, aromatic world of Chai — India's beloved spiced tea. Discover recipes, varieties, and the culture behind every cup." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />

  <style>
    /* ── RESET & BASE ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --chai-brown:   #6B3A2A;
      --chai-gold:    #D4A853;
      --chai-amber:   #C67C3A;
      --chai-cream:   #FDF6EC;
      --chai-dark:    #1C0F0A;
      --chai-spice:   #8B2500;
      --chai-milk:    #F5E6D3;
      --chai-steam:   rgba(212, 168, 83, 0.15);
      --text-light:   #F5E6D3;
      --text-muted:   #C9A98A;
      --transition:   0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', sans-serif;
      background: var(--chai-dark);
      color: var(--text-light);
      overflow-x: hidden;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--chai-dark); }
    ::-webkit-scrollbar-thumb { background: var(--chai-gold); border-radius: 3px; }

    /* ── CURSOR GLOW ── */
    #cursor-glow {
      width: 300px; height: 300px;
      background: radial-gradient(circle, rgba(212,168,83,0.08) 0%, transparent 70%);
      border-radius: 50%;
      position: fixed; pointer-events: none; z-index: 0;
      transform: translate(-50%, -50%);
      transition: opacity 0.3s;
    }

    /* ── PARTICLES ── */
    #particles { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
    .particle {
      position: absolute; border-radius: 50%;
      background: var(--chai-gold); opacity: 0;
      animation: floatUp linear infinite;
    }

    @keyframes floatUp {
      0%   { transform: translateY(0) rotate(0deg);   opacity: 0; }
      10%  { opacity: 0.6; }
      90%  { opacity: 0.2; }
      100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }

    /* ── NAV ── */
    nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 1.2rem 5%;
      background: rgba(28, 15, 10, 0.7);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(212, 168, 83, 0.15);
      transition: var(--transition);
    }
    .nav-logo {
      font-family: 'Playfair Display', serif;
      font-size: 1.8rem; font-weight: 900;
      background: linear-gradient(135deg, var(--chai-gold), var(--chai-amber));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text; letter-spacing: 2px;
    }
    .nav-links { display: flex; gap: 2rem; list-style: none; }
    .nav-links a {
      color: var(--text-muted); text-decoration: none;
      font-size: 0.9rem; font-weight: 500; letter-spacing: 0.05em;
      position: relative; transition: color 0.3s;
    }
    .nav-links a::after {
      content: ''; position: absolute; bottom: -4px; left: 0; right: 0;
      height: 1px; background: var(--chai-gold);
      transform: scaleX(0); transform-origin: left; transition: transform 0.3s;
    }
    .nav-links a:hover { color: var(--chai-gold); }
    .nav-links a:hover::after { transform: scaleX(1); }
    .nav-cta {
      padding: 0.55rem 1.4rem; border-radius: 50px;
      background: linear-gradient(135deg, var(--chai-gold), var(--chai-amber));
      color: var(--chai-dark) !important; font-weight: 600 !important;
      -webkit-text-fill-color: var(--chai-dark) !important;
    }
    .nav-cta::after { display: none !important; }
    .nav-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(212,168,83,0.4); }

    /* ── HERO ── */
    #hero {
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
      text-align: center; padding: 8rem 5% 4rem;
      position: relative;
      background: radial-gradient(ellipse at 50% 0%, rgba(107,58,42,0.4) 0%, transparent 60%),
                  radial-gradient(ellipse at 80% 80%, rgba(212,168,83,0.1) 0%, transparent 50%);
    }
    .hero-content { position: relative; z-index: 1; max-width: 800px; }
    .hero-badge {
      display: inline-block; padding: 0.4rem 1.2rem; border-radius: 50px;
      border: 1px solid rgba(212,168,83,0.5);
      font-size: 0.78rem; letter-spacing: 0.2em; text-transform: uppercase;
      color: var(--chai-gold); margin-bottom: 2rem;
      animation: fadeInDown 0.8s ease both;
    }
    .hero-title {
      font-family: 'Playfair Display', serif;
      font-size: clamp(3.5rem, 10vw, 7rem);
      font-weight: 900; line-height: 1;
      background: linear-gradient(135deg, #FFF8F0 30%, var(--chai-gold) 60%, var(--chai-amber) 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text; margin-bottom: 1.5rem;
      animation: fadeInUp 0.9s 0.2s ease both;
    }
    .hero-subtitle {
      font-size: clamp(1rem, 2.5vw, 1.25rem); color: var(--text-muted);
      line-height: 1.7; max-width: 560px; margin: 0 auto 3rem;
      animation: fadeInUp 0.9s 0.4s ease both;
    }
    .hero-buttons { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;
      animation: fadeInUp 0.9s 0.6s ease both; }
    .btn-primary {
      padding: 0.9rem 2.4rem; border-radius: 50px; border: none; cursor: pointer;
      background: linear-gradient(135deg, var(--chai-gold), var(--chai-amber));
      color: var(--chai-dark); font-size: 1rem; font-weight: 700;
      letter-spacing: 0.03em; transition: var(--transition);
      box-shadow: 0 4px 20px rgba(212,168,83,0.3);
    }
    .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(212,168,83,0.5); }
    .btn-secondary {
      padding: 0.9rem 2.4rem; border-radius: 50px; cursor: pointer;
      background: transparent; border: 1px solid rgba(212,168,83,0.4);
      color: var(--chai-gold); font-size: 1rem; font-weight: 500;
      transition: var(--transition); letter-spacing: 0.03em;
    }
    .btn-secondary:hover { background: rgba(212,168,83,0.1); border-color: var(--chai-gold); transform: translateY(-3px); }

    /* Steaming cup SVG animation */
    .hero-cup { margin-top: 4rem; animation: fadeInUp 1s 0.8s ease both; }
    .steam-line { animation: steam 2s ease-in-out infinite; transform-origin: bottom; }
    .steam-line:nth-child(2) { animation-delay: 0.4s; }
    .steam-line:nth-child(3) { animation-delay: 0.8s; }
    @keyframes steam {
      0%, 100% { transform: scaleY(0.8) translateY(0); opacity: 0.3; }
      50%       { transform: scaleY(1.2) translateY(-6px); opacity: 0.9; }
    }

    /* ── SECTION BASE ── */
    section { padding: 7rem 5%; position: relative; z-index: 1; }
    .section-label {
      font-size: 0.75rem; letter-spacing: 0.25em; text-transform: uppercase;
      color: var(--chai-gold); margin-bottom: 0.8rem;
    }
    .section-title {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 900;
      line-height: 1.15; margin-bottom: 1.2rem;
    }
    .section-desc { color: var(--text-muted); font-size: 1.05rem; line-height: 1.8; max-width: 560px; }

    /* ── DIVIDER ── */
    .divider {
      height: 1px; margin: 0 5%;
      background: linear-gradient(to right, transparent, rgba(212,168,83,0.3), transparent);
    }

    /* ── ABOUT (SPLIT) ── */
    #about {
      display: grid; grid-template-columns: 1fr 1fr; gap: 5rem;
      align-items: center;
    }
    .about-visual {
      position: relative; display: flex; align-items: center; justify-content: center;
    }
    .about-ring {
      width: 320px; height: 320px; border-radius: 50%;
      border: 2px solid rgba(212,168,83,0.25);
      display: flex; align-items: center; justify-content: center;
      position: relative; animation: rotateSlow 20s linear infinite;
    }
    .about-ring::before {
      content: ''; position: absolute; inset: 16px; border-radius: 50%;
      border: 1px dashed rgba(212,168,83,0.15);
    }
    .about-emoji {
      font-size: 6rem; animation: rotateSlow 20s linear infinite reverse;
      filter: drop-shadow(0 0 30px rgba(212,168,83,0.4));
    }
    .orbit-dot {
      position: absolute; width: 10px; height: 10px;
      background: var(--chai-gold); border-radius: 50%;
      box-shadow: 0 0 10px var(--chai-gold);
    }
    .orbit-dot:nth-child(2) { top: 0; left: 50%; transform: translate(-50%, -50%); }
    .orbit-dot:nth-child(3) { bottom: 0; left: 50%; transform: translate(-50%, 50%); }
    .orbit-dot:nth-child(4) { left: 0; top: 50%; transform: translate(-50%, -50%); }
    .orbit-dot:nth-child(5) { right: 0; top: 50%; transform: translate(50%, -50%); }
    @keyframes rotateSlow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    .about-stats {
      display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 3rem;
    }
    .stat-box {
      padding: 1.5rem; border-radius: 16px;
      background: rgba(212,168,83,0.06);
      border: 1px solid rgba(212,168,83,0.15);
      transition: var(--transition);
    }
    .stat-box:hover { background: rgba(212,168,83,0.12); transform: translateY(-4px); }
    .stat-num {
      font-family: 'Playfair Display', serif;
      font-size: 2.4rem; font-weight: 900;
      background: linear-gradient(135deg, var(--chai-gold), var(--chai-amber));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .stat-label { font-size: 0.82rem; color: var(--text-muted); margin-top: 0.3rem; }

    /* ── VARIETIES CARDS ── */
    #varieties { text-align: center; }
    #varieties .section-desc { margin: 0 auto 4rem; }
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 1.5rem; text-align: left; margin-top: 2rem;
    }
    .chai-card {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(212,168,83,0.12);
      border-radius: 24px; padding: 2rem;
      cursor: pointer; transition: var(--transition);
      position: relative; overflow: hidden;
    }
    .chai-card::before {
      content: ''; position: absolute; inset: 0; opacity: 0;
      background: radial-gradient(circle at 50% 0%, rgba(212,168,83,0.12) 0%, transparent 70%);
      transition: opacity 0.4s;
    }
    .chai-card:hover { transform: translateY(-8px); border-color: rgba(212,168,83,0.4);
      box-shadow: 0 24px 48px rgba(0,0,0,0.4); }
    .chai-card:hover::before { opacity: 1; }
    .card-icon { font-size: 2.8rem; margin-bottom: 1.2rem; display: block; }
    .card-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.3rem; font-weight: 700; margin-bottom: 0.6rem; color: #FFF8F0;
    }
    .card-desc { font-size: 0.9rem; color: var(--text-muted); line-height: 1.7; }
    .card-tag {
      display: inline-block; margin-top: 1.2rem;
      padding: 0.3rem 0.9rem; border-radius: 50px;
      background: rgba(212,168,83,0.12); color: var(--chai-gold);
      font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em;
    }

    /* ── RECIPE SECTION ── */
    #recipe {
      display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: start;
    }
    .recipe-steps { list-style: none; margin-top: 2.5rem; }
    .recipe-steps li {
      display: flex; gap: 1.2rem; align-items: flex-start;
      padding: 1.2rem 0; border-bottom: 1px solid rgba(212,168,83,0.08);
      transition: var(--transition);
    }
    .recipe-steps li:hover { padding-left: 0.5rem; }
    .step-num {
      flex-shrink: 0; width: 36px; height: 36px; border-radius: 50%;
      background: linear-gradient(135deg, var(--chai-gold), var(--chai-amber));
      display: flex; align-items: center; justify-content: center;
      font-size: 0.8rem; font-weight: 700; color: var(--chai-dark);
    }
    .step-text { font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; padding-top: 0.4rem; }

    .ingredients-box {
      background: rgba(212,168,83,0.05);
      border: 1px solid rgba(212,168,83,0.15);
      border-radius: 24px; padding: 2.5rem; margin-top: 2.5rem;
    }
    .ingredients-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.4rem; margin-bottom: 1.5rem; color: var(--chai-gold);
    }
    .ingredient {
      display: flex; justify-content: space-between; align-items: center;
      padding: 0.8rem 0; border-bottom: 1px solid rgba(212,168,83,0.08);
    }
    .ingredient:last-child { border: none; }
    .ing-name { font-size: 0.92rem; }
    .ing-qty {
      font-size: 0.82rem; color: var(--chai-gold); font-weight: 600;
      background: rgba(212,168,83,0.1); padding: 0.25rem 0.7rem; border-radius: 50px;
    }

    /* ── TESTIMONIALS ── */
    #testimonials { text-align: center; }
    .testimonials-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem; margin-top: 4rem; text-align: left;
    }
    .testimonial-card {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(212,168,83,0.12);
      border-radius: 20px; padding: 2rem;
      transition: var(--transition);
    }
    .testimonial-card:hover { transform: translateY(-6px); border-color: rgba(212,168,83,0.3); }
    .stars { color: var(--chai-gold); font-size: 1.1rem; margin-bottom: 1rem; letter-spacing: 2px; }
    .testimonial-text { font-size: 0.95rem; line-height: 1.8; color: var(--text-muted); font-style: italic; }
    .testimonial-author { margin-top: 1.5rem; display: flex; align-items: center; gap: 0.8rem; }
    .author-avatar {
      width: 40px; height: 40px; border-radius: 50%;
      background: linear-gradient(135deg, var(--chai-brown), var(--chai-gold));
      display: flex; align-items: center; justify-content: center;
      font-weight: 700; font-size: 0.85rem; color: var(--chai-cream);
    }
    .author-name { font-size: 0.88rem; font-weight: 600; }
    .author-city { font-size: 0.78rem; color: var(--text-muted); }

    /* ── FEEDBACK / VOTING ── */
    #feedback {
      text-align: center;
      background: radial-gradient(ellipse at 50% 50%, rgba(107,58,42,0.3) 0%, transparent 70%);
      border-top: 1px solid rgba(212,168,83,0.1);
      border-bottom: 1px solid rgba(212,168,83,0.1);
    }
    .vote-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem; margin: 3rem auto 0; max-width: 900px;
    }
    .vote-btn {
      position: relative;
      padding: 1.2rem 1rem; border-radius: 18px; border: none; cursor: pointer;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(212,168,83,0.15);
      color: var(--text-light); font-size: 0.9rem; font-weight: 500;
      transition: var(--transition); display: flex; flex-direction: column;
      align-items: center; gap: 0.5rem;
    }
    .vote-btn:hover {
      background: rgba(212,168,83,0.1);
      border-color: rgba(212,168,83,0.5);
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(0,0,0,0.35);
    }
    .vote-btn.voted {
      background: rgba(212,168,83,0.15);
      border-color: var(--chai-gold);
      box-shadow: 0 0 0 2px rgba(212,168,83,0.3);
    }
    .vote-btn .v-icon { font-size: 2rem; }
    .vote-btn .v-name { font-family: 'Playfair Display', serif; font-size: 0.95rem; font-weight: 700; }
    .vote-btn .v-count {
      font-size: 0.78rem; color: var(--chai-gold); font-weight: 600;
      background: rgba(212,168,83,0.12); padding: 0.15rem 0.6rem;
      border-radius: 50px; min-width: 48px;
    }
    .crown-badge {
      position: absolute; top: -10px; right: -10px;
      font-size: 1.3rem; display: none;
      filter: drop-shadow(0 2px 6px rgba(212,168,83,0.7));
      animation: popIn 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
    }
    @keyframes popIn {
      from { transform: scale(0) rotate(-20deg); opacity: 0; }
      to   { transform: scale(1) rotate(0deg);   opacity: 1; }
    }

    /* Live bar chart */
    .chart-wrap {
      max-width: 700px; margin: 3.5rem auto 0; text-align: left;
    }
    .chart-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.15rem; color: var(--chai-gold); margin-bottom: 1.5rem;
      text-align: center;
    }
    .bar-row {
      display: flex; align-items: center; gap: 0.8rem;
      margin-bottom: 0.85rem;
    }
    .bar-label {
      min-width: 160px; font-size: 0.82rem; color: var(--text-muted);
      text-align: right; white-space: nowrap; overflow: hidden;
      text-overflow: ellipsis;
    }
    .bar-track {
      flex: 1; height: 26px; background: rgba(255,255,255,0.05);
      border-radius: 50px; overflow: hidden;
      border: 1px solid rgba(212,168,83,0.1);
    }
    .bar-fill {
      height: 100%; border-radius: 50px;
      background: linear-gradient(90deg, var(--chai-brown), var(--chai-gold));
      width: 0%; transition: width 0.7s cubic-bezier(0.25,0.8,0.25,1);
      display: flex; align-items: center; justify-content: flex-end;
      padding-right: 8px;
    }
    .bar-fill.leader {
      background: linear-gradient(90deg, var(--chai-spice), var(--chai-gold), #FFD580);
      box-shadow: 0 0 12px rgba(212,168,83,0.4);
    }
    .bar-pct {
      font-size: 0.7rem; font-weight: 700; color: var(--chai-dark);
      opacity: 0; transition: opacity 0.4s 0.5s;
    }
    .bar-pct.show { opacity: 1; }
    .total-votes {
      text-align: center; margin-top: 1.5rem;
      font-size: 0.82rem; color: var(--text-muted);
    }
    .total-votes span { color: var(--chai-gold); font-weight: 700; }
    .voted-msg {
      display: none; margin-top: 1rem;
      color: var(--chai-gold); font-size: 0.92rem;
      animation: fadeInUp 0.5s ease;
    }

    /* ── FOOTER ── */
    footer {
      padding: 3rem 5%; display: flex; justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(212,168,83,0.1);
    }
    .footer-logo {
      font-family: 'Playfair Display', serif;
      font-size: 1.4rem; font-weight: 900;
      background: linear-gradient(135deg, var(--chai-gold), var(--chai-amber));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .footer-text { font-size: 0.82rem; color: var(--text-muted); margin-top: 0.3rem; }
    .footer-right { font-size: 0.8rem; color: var(--text-muted); }

    /* ── ANIMATIONS ── */
    @keyframes fadeInDown {
      from { opacity: 0; transform: translateY(-20px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(30px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .reveal { opacity: 0; transform: translateY(40px); transition: opacity 0.7s ease, transform 0.7s ease; }
    .reveal.visible { opacity: 1; transform: translateY(0); }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
      #about, #recipe { grid-template-columns: 1fr; gap: 3rem; }
      .about-visual { order: -1; }
      .about-ring { width: 200px; height: 200px; }
      .about-emoji { font-size: 4rem; }
      nav { padding: 1rem 4%; }
      .nav-links { gap: 1.2rem; }
    }
    @media (max-width: 500px) {
      .nav-links { display: none; }
    }
  </style>
</head>
<body>

<!-- Cursor glow -->
<div id="cursor-glow"></div>

<!-- Floating particles -->
<div id="particles"></div>

<!-- NAV -->
<nav id="navbar">
  <div class="nav-logo">&#9749; CHAI</div>
  <ul class="nav-links">
    <li><a href="#about">About</a></li>
    <li><a href="#varieties">Varieties</a></li>
    <li><a href="#recipe">Recipe</a></li>
    <li><a href="#testimonials">Stories</a></li>
    <li><a href="#feedback" class="nav-cta">Vote Now</a></li>
  </ul>
</nav>

<!-- HERO -->
<section id="hero">
  <div class="hero-content">
    <span class="hero-badge">&#10022; The Soul of India &#10022;</span>
    <h1 class="hero-title">Chai</h1>
    <p class="hero-subtitle">
      More than a drink &mdash; it's a ritual, a comfort, a culture.
      One sip and the whole world slows down.
    </p>
    <div class="hero-buttons">
      <button class="btn-primary" onclick="document.getElementById('varieties').scrollIntoView({behavior:'smooth'})">
        Explore Varieties
      </button>
      <button class="btn-secondary" onclick="document.getElementById('recipe').scrollIntoView({behavior:'smooth'})">
        See Recipe &#8595;
      </button>
    </div>

    <!-- Animated steaming cup SVG -->
    <div class="hero-cup">
      <svg width="200" height="180" viewBox="0 0 200 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path class="steam-line" d="M75 60 Q80 40 75 20" stroke="#D4A853" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
        <path class="steam-line" d="M100 55 Q105 35 100 15" stroke="#D4A853" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
        <path class="steam-line" d="M125 60 Q130 40 125 20" stroke="#D4A853" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
        <ellipse cx="100" cy="158" rx="70" ry="10" fill="#5A3020" opacity="0.8"/>
        <path d="M45 80 Q48 155 100 155 Q152 155 155 80 Z" fill="url(#cupGrad)"/>
        <path d="M155 95 Q185 95 185 120 Q185 145 155 145" stroke="#8B4A30" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M48 95 Q50 145 100 147 Q150 145 152 95 Z" fill="url(#chaiGrad)" opacity="0.9"/>
        <ellipse cx="100" cy="80" rx="55" ry="8" fill="#7A4030"/>
        <ellipse cx="80" cy="110" rx="10" ry="20" fill="white" opacity="0.05" transform="rotate(-15 80 110)"/>
        <defs>
          <linearGradient id="cupGrad" x1="45" y1="80" x2="155" y2="155" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#8B4A30"/>
            <stop offset="100%" stop-color="#5A2810"/>
          </linearGradient>
          <linearGradient id="chaiGrad" x1="48" y1="95" x2="152" y2="147" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#C67C3A"/>
            <stop offset="100%" stop-color="#8B3A1A"/>
          </linearGradient>
        </defs>
      </svg>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- ABOUT -->
<section id="about">
  <div class="about-visual reveal">
    <div class="about-ring">
      <span class="about-emoji">&#127861;</span>
      <span class="orbit-dot"></span>
      <span class="orbit-dot"></span>
      <span class="orbit-dot"></span>
      <span class="orbit-dot"></span>
    </div>
  </div>
  <div class="about-text reveal">
    <p class="section-label">About Chai</p>
    <h2 class="section-title">A Cup That Tells<br/>a Thousand Stories</h2>
    <p class="section-desc">
      Chai (&#2330;&#2366;&#2351;) is India's heartbeat &mdash; a blend of black tea, milk, sugar,
      and a symphony of spices like cardamom, ginger, cinnamon and cloves.
      Shared across roadside tapris, corporate offices, and family gatherings alike,
      chai is the universal language of warmth.
    </p>
    <div class="about-stats">
      <div class="stat-box">
        <div class="stat-num" id="stat-0">1.2B</div>
        <div class="stat-label">Cups consumed in India daily</div>
      </div>
      <div class="stat-box">
        <div class="stat-num" id="stat-1">5000+</div>
        <div class="stat-label">Years of tea history in Asia</div>
      </div>
      <div class="stat-box">
        <div class="stat-num" id="stat-2">40+</div>
        <div class="stat-label">Regional varieties of chai</div>
      </div>
      <div class="stat-box">
        <div class="stat-num" id="stat-3">#2</div>
        <div class="stat-label">Most consumed drink after water</div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- VARIETIES -->
<section id="varieties">
  <p class="section-label reveal">Explore the Range</p>
  <h2 class="section-title reveal">Popular Chai Varieties</h2>
  <p class="section-desc reveal">From the fragrant streets of Kolkata to the misty hills of Darjeeling &mdash; every region brews its own magic.</p>

  <div class="cards-grid">
    <div class="chai-card reveal">
      <span class="card-icon">&#127807;</span>
      <div class="card-title">Masala Chai</div>
      <div class="card-desc">The classic. A bold brew with ginger, cardamom, cloves, and cinnamon that warms you from the inside out. The undisputed king of Indian chai.</div>
      <span class="card-tag">&#128293; Most Popular</span>
    </div>
    <div class="chai-card reveal">
      <span class="card-icon">&#127800;</span>
      <div class="card-title">Kashmiri Noon Chai</div>
      <div class="card-desc">A pink salted tea made with gunpowder green tea, milk, and nuts. From the beautiful Kashmir valley &mdash; utterly unique in flavor and colour.</div>
      <span class="card-tag">&#128142; Exotic</span>
    </div>
    <div class="chai-card reveal">
      <span class="card-icon">&#9749;</span>
      <div class="card-title">Kadak Cutting Chai</div>
      <div class="card-desc">Mumbai's signature street-style chai. Strong, milky, served in half-glasses. Fuels the city's relentless energy every single morning.</div>
      <span class="card-tag">&#9889; Street Style</span>
    </div>
    <div class="chai-card reveal">
      <span class="card-icon">&#127809;</span>
      <div class="card-title">Tulsi Adrak Chai</div>
      <div class="card-desc">Holy basil and ginger come together in this immunity-boosting, soothing brew. Perfect during monsoon season or a cold evening at home.</div>
      <span class="card-tag">&#127807; Wellness</span>
    </div>
    <div class="chai-card reveal">
      <span class="card-icon">&#127861;</span>
      <div class="card-title">Darjeeling First Flush</div>
      <div class="card-desc">The "Champagne of teas." Light, floral, and exquisitely delicate. Grown in the Himalayan foothills at elevations above 6,000 feet.</div>
      <span class="card-tag">&#127942; Premium</span>
    </div>
    <div class="chai-card reveal">
      <span class="card-icon">&#129482;</span>
      <div class="card-title">Iced Masala Chai</div>
      <div class="card-desc">The modern refreshing twist. Freshly brewed masala chai chilled over ice &mdash; perfect for sweltering Indian summers.</div>
      <span class="card-tag">&#10052; Summer Special</span>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- RECIPE -->
<section id="recipe">
  <div class="reveal">
    <p class="section-label">How To Make It</p>
    <h2 class="section-title">Perfect Masala<br/>Chai Recipe</h2>
    <p class="section-desc">Follow these steps for an authentic, aromatic cup that tastes just like your favourite tapri.</p>

    <ol class="recipe-steps">
      <li>
        <div class="step-num">1</div>
        <div class="step-text">Crush fresh ginger and cardamom pods lightly with the back of a knife to release their oils.</div>
      </li>
      <li>
        <div class="step-num">2</div>
        <div class="step-text">Bring 1 cup of water to a boil in a saucepan. Add crushed ginger, cardamom, a cinnamon stick, and 2 cloves.</div>
      </li>
      <li>
        <div class="step-num">3</div>
        <div class="step-text">Add 2 teaspoons of strong Assam or CTC tea leaves. Let it simmer for 2-3 minutes until the water turns a deep amber.</div>
      </li>
      <li>
        <div class="step-num">4</div>
        <div class="step-text">Pour in 1 cup of full-fat milk and sugar to taste. Bring to a rolling boil, then reduce to medium heat.</div>
      </li>
      <li>
        <div class="step-num">5</div>
        <div class="step-text">Let the chai froth and rise slightly &mdash; this is called "ubalna." Strain into cups and serve immediately.</div>
      </li>
    </ol>
  </div>

  <div class="reveal">
    <div class="ingredients-box">
      <div class="ingredients-title">&#129474; Ingredients (Serves 2)</div>
      <div class="ingredient"><span class="ing-name">Full-fat milk</span><span class="ing-qty">1 cup</span></div>
      <div class="ingredient"><span class="ing-name">Water</span><span class="ing-qty">1 cup</span></div>
      <div class="ingredient"><span class="ing-name">CTC / Assam tea leaves</span><span class="ing-qty">2 tsp</span></div>
      <div class="ingredient"><span class="ing-name">Fresh ginger</span><span class="ing-qty">1 inch</span></div>
      <div class="ingredient"><span class="ing-name">Green cardamom pods</span><span class="ing-qty">3-4</span></div>
      <div class="ingredient"><span class="ing-name">Cinnamon stick</span><span class="ing-qty">1 small</span></div>
      <div class="ingredient"><span class="ing-name">Cloves</span><span class="ing-qty">2</span></div>
      <div class="ingredient"><span class="ing-name">Sugar</span><span class="ing-qty">to taste</span></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- TESTIMONIALS -->
<section id="testimonials">
  <p class="section-label reveal">Chai Lovers Say</p>
  <h2 class="section-title reveal">Stories Over a Cup</h2>

  <div class="testimonials-grid">
    <div class="testimonial-card reveal">
      <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <div class="testimonial-text">"My day doesn't start without chai. It's not just a drink &mdash; it's a moment of peace before the storm of the day begins."</div>
      <div class="testimonial-author">
        <div class="author-avatar">P</div>
        <div><div class="author-name">Priya Sharma</div><div class="author-city">Mumbai, India</div></div>
      </div>
    </div>
    <div class="testimonial-card reveal">
      <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <div class="testimonial-text">"Chai is the reason I survived my engineering degree. Three cups a day, every deadline, every exam &mdash; it never let me down."</div>
      <div class="testimonial-author">
        <div class="author-avatar">A</div>
        <div><div class="author-name">Arjun Mehta</div><div class="author-city">Bangalore, India</div></div>
      </div>
    </div>
    <div class="testimonial-card reveal">
      <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <div class="testimonial-text">"I traveled all the way from London to Kolkata just to taste the famous roadside chai. Worth every mile. Nothing compares."</div>
      <div class="testimonial-author">
        <div class="author-avatar">S</div>
        <div><div class="author-name">Sophie Turner</div><div class="author-city">London, UK</div></div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- FEEDBACK / VOTING -->
<section id="feedback">
  <p class="section-label reveal">Community Feedback</p>
  <h2 class="section-title reveal">Which Chai Is<br/>Loved the Most?</h2>
  <p class="section-desc reveal" style="margin:0 auto;">
    Cast your vote for your all-time favourite chai and see live results from the community. One vote per session!
  </p>

  <!-- Vote buttons -->
  <div class="vote-grid reveal" id="vote-grid">
    <button class="vote-btn" id="vbtn-0" onclick="castVote('Masala Chai',0)">
      <span class="crown-badge" id="crown-0">&#128081;</span>
      <span class="v-icon">&#127807;</span>
      <span class="v-name">Masala Chai</span>
      <span class="v-count" id="vc-0">0 votes</span>
    </button>
    <button class="vote-btn" id="vbtn-1" onclick="castVote('Kashmiri Noon Chai',1)">
      <span class="crown-badge" id="crown-1">&#128081;</span>
      <span class="v-icon">&#127800;</span>
      <span class="v-name">Kashmiri Noon Chai</span>
      <span class="v-count" id="vc-1">0 votes</span>
    </button>
    <button class="vote-btn" id="vbtn-2" onclick="castVote('Kadak Cutting Chai',2)">
      <span class="crown-badge" id="crown-2">&#128081;</span>
      <span class="v-icon">&#9749;</span>
      <span class="v-name">Kadak Cutting Chai</span>
      <span class="v-count" id="vc-2">0 votes</span>
    </button>
    <button class="vote-btn" id="vbtn-3" onclick="castVote('Tulsi Adrak Chai',3)">
      <span class="crown-badge" id="crown-3">&#128081;</span>
      <span class="v-icon">&#127809;</span>
      <span class="v-name">Tulsi Adrak Chai</span>
      <span class="v-count" id="vc-3">0 votes</span>
    </button>
    <button class="vote-btn" id="vbtn-4" onclick="castVote('Darjeeling First Flush',4)">
      <span class="crown-badge" id="crown-4">&#128081;</span>
      <span class="v-icon">&#127861;</span>
      <span class="v-name">Darjeeling First Flush</span>
      <span class="v-count" id="vc-4">0 votes</span>
    </button>
    <button class="vote-btn" id="vbtn-5" onclick="castVote('Iced Masala Chai',5)">
      <span class="crown-badge" id="crown-5">&#128081;</span>
      <span class="v-icon">&#129482;</span>
      <span class="v-name">Iced Masala Chai</span>
      <span class="v-count" id="vc-5">0 votes</span>
    </button>
  </div>

  <p class="voted-msg" id="voted-msg">&#10003; Thanks for voting! Live results below.</p>

  <!-- Live bar chart -->
  <div class="chart-wrap reveal">
    <div class="chart-title">&#128202; Live Community Results</div>
    <div id="bar-chart"></div>
    <p class="total-votes" id="total-votes-label">Total votes: <span id="total-votes-num">0</span></p>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div>
    <div class="footer-logo">&#9749; CHAI</div>
    <div class="footer-text">Made with love &amp; ginger &#10022; Flask Edition</div>
  </div>
  <div class="footer-right">&copy; 2026 Chai &mdash; The Soul of India</div>
</footer>

<script>
  // CURSOR GLOW
  const glow = document.getElementById('cursor-glow');
  document.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top  = e.clientY + 'px';
  });

  // PARTICLES
  const pContainer = document.getElementById('particles');
  for (let i = 0; i < 40; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 4 + 2;
    p.style.cssText = [
      'width:' + size + 'px',
      'height:' + size + 'px',
      'left:' + (Math.random() * 100) + '%',
      'bottom:' + (Math.random() * 20) + '%',
      'animation-duration:' + (Math.random() * 12 + 8) + 's',
      'animation-delay:' + (Math.random() * 10) + 's',
      'opacity:' + (Math.random() * 0.5)
    ].join(';');
    pContainer.appendChild(p);
  }

  // NAV SCROLL
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.style.background = window.scrollY > 50
      ? 'rgba(28,15,10,0.95)' : 'rgba(28,15,10,0.7)';
  });

  // REVEAL ON SCROLL
  const reveals = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
  reveals.forEach(el => observer.observe(el));

  // ── VOTING ──
  const VARIETIES = [
    'Masala Chai', 'Kashmiri Noon Chai', 'Kadak Cutting Chai',
    'Tulsi Adrak Chai', 'Darjeeling First Flush', 'Iced Masala Chai'
  ];
  let hasVoted = false;

  function castVote(name, idx) {
    if (hasVoted) return;
    hasVoted = true;
    // Mark chosen button
    document.getElementById('vbtn-' + idx).classList.add('voted');
    // Disable all
    VARIETIES.forEach((_, i) => {
      const b = document.getElementById('vbtn-' + i);
      b.disabled = true;
      b.style.opacity = i === idx ? '1' : '0.5';
      b.style.cursor = 'default';
    });
    document.getElementById('voted-msg').style.display = 'block';
    // POST vote to Flask
    fetch('/api/vote', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ variety: name })
    }).then(() => fetchResults());
  }

  function fetchResults() {
    fetch('/api/votes')
      .then(r => r.json())
      .then(data => renderChart(data));
  }

  function renderChart(data) {
    const chart = document.getElementById('bar-chart');
    const total = data.total || 0;
    document.getElementById('total-votes-num').textContent = total;

    // Find leader
    let maxVotes = 0, leaderId = -1;
    VARIETIES.forEach((name, i) => {
      const v = data.votes[name] || 0;
      if (v > maxVotes) { maxVotes = v; leaderId = i; }
    });

    // Update vote count badges
    VARIETIES.forEach((name, i) => {
      const v = data.votes[name] || 0;
      const el = document.getElementById('vc-' + i);
      if (el) el.textContent = v + (v === 1 ? ' vote' : ' votes');
      // Crown the leader
      const crown = document.getElementById('crown-' + i);
      if (crown) crown.style.display = (i === leaderId && maxVotes > 0) ? 'block' : 'none';
    });

    // Build bars
    chart.innerHTML = '';
    VARIETIES.forEach((name, i) => {
      const v = data.votes[name] || 0;
      const pct = total > 0 ? Math.round((v / total) * 100) : 0;
      const isLeader = i === leaderId && maxVotes > 0;
      const row = document.createElement('div');
      row.className = 'bar-row';
      row.innerHTML = `
        <span class="bar-label">${name}</span>
        <div class="bar-track">
          <div class="bar-fill${isLeader ? ' leader' : ''}" id="bf-${i}" style="width:0%">
            <span class="bar-pct" id="bp-${i}">${pct}%</span>
          </div>
        </div>
      `;
      chart.appendChild(row);
      // Animate width after paint
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          const fill = document.getElementById('bf-' + i);
          const pctEl = document.getElementById('bp-' + i);
          if (fill) fill.style.width = Math.max(pct, pct > 0 ? 4 : 0) + '%';
          if (pctEl) pctEl.classList.add('show');
        });
      });
    });
  }

  // Load results on page open
  fetchResults();
  // Poll every 5s for live updates
  setInterval(fetchResults, 5000);
</script>

</body>
</html>"""


@app.route("/")
def home():
    """Main chai homepage - all HTML/CSS/JS is coded inline above, zero template files."""
    return HOME_PAGE


# ── In-memory vote store ──
CHAI_VARIETIES = [
    "Masala Chai", "Kashmiri Noon Chai", "Kadak Cutting Chai",
    "Tulsi Adrak Chai", "Darjeeling First Flush", "Iced Masala Chai",
]
vote_counts = {v: 0 for v in CHAI_VARIETIES}


@app.route("/api/vote", methods=["POST"])
def cast_vote():
    """Accept a vote for a chai variety and update the in-memory tally."""
    data = request.get_json(silent=True) or {}
    variety = data.get("variety", "").strip()
    if variety not in vote_counts:
        return jsonify({"status": "error", "message": "Unknown variety"}), 400
    vote_counts[variety] += 1
    return jsonify({"status": "ok", "variety": variety, "votes": vote_counts[variety]})


@app.route("/api/votes")
def get_votes():
    """Return current vote tallies for all chai varieties."""
    total = sum(vote_counts.values())
    leader = max(vote_counts, key=vote_counts.get) if total > 0 else None
    return jsonify({
        "status": "ok",
        "total": total,
        "leader": leader,
        "votes": vote_counts,
    })


@app.route("/api/varieties")
def varieties():
    """JSON API endpoint returning chai varieties data."""
    data = [
        {"name": "Masala Chai",            "spice_level": "High",   "origin": "Pan-India",   "emoji": "leaf"},
        {"name": "Kashmiri Noon Chai",     "spice_level": "Medium", "origin": "Kashmir",     "emoji": "flower"},
        {"name": "Kadak Cutting Chai",     "spice_level": "High",   "origin": "Mumbai",      "emoji": "coffee"},
        {"name": "Tulsi Adrak Chai",       "spice_level": "Medium", "origin": "North India", "emoji": "herb"},
        {"name": "Darjeeling First Flush", "spice_level": "Low",    "origin": "West Bengal", "emoji": "tea"},
        {"name": "Iced Masala Chai",       "spice_level": "Medium", "origin": "Modern",      "emoji": "ice"},
    ]
    return jsonify({"status": "ok", "count": len(data), "varieties": data})


@app.route("/api/recipe")
def recipe():
    """JSON API endpoint for the classic masala chai recipe."""
    return jsonify({
        "name": "Classic Masala Chai",
        "serves": 2,
        "prep_time_min": 2,
        "cook_time_min": 8,
        "ingredients": [
            {"item": "Full-fat milk",      "quantity": "1 cup"},
            {"item": "Water",              "quantity": "1 cup"},
            {"item": "CTC / Assam tea",    "quantity": "2 tsp"},
            {"item": "Fresh ginger",       "quantity": "1 inch"},
            {"item": "Cardamom pods",      "quantity": "3-4"},
            {"item": "Cinnamon stick",     "quantity": "1 small"},
            {"item": "Cloves",             "quantity": "2"},
            {"item": "Sugar",              "quantity": "to taste"},
        ],
        "steps": [
            "Crush ginger and cardamom to release oils.",
            "Boil water, add crushed spices, cinnamon, cloves.",
            "Add tea leaves, simmer 2-3 min until deep amber.",
            "Pour in milk and sugar, bring to rolling boil.",
            "Let it rise once (ubalna), strain and serve.",
        ]
    })


if __name__ == "__main__":
    print("\n  [CHAI] Chai Flask App is brewing...")
    print("  [WEB]  Visit  ->  http://127.0.0.1:5000")
    print("  [API]  API    ->  http://127.0.0.1:5000/api/varieties")
    print("  [API]  API    ->  http://127.0.0.1:5000/api/recipe\n")
    app.run(debug=True, port=5000)
