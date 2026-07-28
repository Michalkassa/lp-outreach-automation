#!/usr/bin/env python3
"""
Diagnostic for scripts/make_draft.py. Run this when make_draft says it cannot
find the To, Subject or body field — Outlook on the web renames these between
releases, and this prints what they are called today.

  .venv/bin/python scripts/inspect_compose.py

It opens a new message, writes every candidate field to compose_dom.json next
to this script, and closes. It is read-only: it types nothing into any field
and never sends. Paste the output back to Claude to get the selectors fixed.
"""
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_draft import first_visible, SEL_NEW_MAIL

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "compose_dom.json"

DUMP_JS = """
() => {
  const sel = 'input, textarea, [contenteditable="true"], [role="textbox"], [role="combobox"]';
  return Array.from(document.querySelectorAll(sel)).map(e => {
    const r = e.getBoundingClientRect();
    return {
      tag: e.tagName.toLowerCase(),
      type: e.getAttribute('type'),
      role: e.getAttribute('role'),
      aria: e.getAttribute('aria-label'),
      ariaPlaceholder: e.getAttribute('aria-placeholder'),
      placeholder: e.getAttribute('placeholder'),
      id: e.id || null,
      testid: e.getAttribute('data-testid'),
      autoid: e.getAttribute('data-automationid') || e.getAttribute('automationid'),
      editable: e.getAttribute('contenteditable'),
      cls: (e.className && e.className.toString().slice(0, 90)) || null,
      visible: r.width > 0 && r.height > 0,
      box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]
    };
  });
}
"""

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        str(ROOT / ".browser-profile"), headless=False,
        viewport={"width": 1440, "height": 900},
        args=["--disable-blink-features=AutomationControlled"],
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_default_navigation_timeout(120000)
    try:
        page.goto("https://outlook.office.com/mail/", wait_until="commit", timeout=120000)
    except Exception as e:
        print(f"goto warning (continuing anyway): {type(e).__name__}")
    page.wait_for_timeout(8000)
    print("landed on:", page.url[:100])

    nm = first_visible(page, SEL_NEW_MAIL, timeout=45000)
    if not nm:
        print("could not find New mail"); ctx.close(); sys.exit(1)
    nm.click()
    print("clicked New mail, waiting for the compose form to settle...")
    page.wait_for_timeout(5000)

    frames = [page.main_frame] + list(page.main_frame.child_frames)
    all_rows = []
    for i, fr in enumerate(frames):
        try:
            rows = fr.evaluate(DUMP_JS)
        except Exception as e:
            print(f"frame {i}: {e}"); continue
        for r in rows:
            r["frame"] = i
            r["frame_url"] = (fr.url or "")[:70]
        all_rows.extend(rows)

    vis = [r for r in all_rows if r["visible"]]
    OUT.write_text(json.dumps(all_rows, indent=2))

    print(f"\n{len(all_rows)} candidates, {len(vis)} visible. full dump -> {OUT}\n")
    for r in vis:
        print(f"  f{r['frame']} <{r['tag']}> role={r['role']!r} aria={r['aria']!r} "
              f"ph={r['placeholder'] or r['ariaPlaceholder']!r} testid={r['testid']!r} "
              f"autoid={r['autoid']!r} editable={r['editable']!r} box={r['box']}")

    page.screenshot(path=str(Path(__file__).resolve().parent / "owa_compose.png"))
    print("\nscreenshot -> owa_compose.png")
    ctx.close()
