"""Export four unaltered BOJ chart panels as visually faithful image quotations.
Source: https://www.boj.or.jp/about/press/koen_2026/data/ko260527a1.pdf
Only crop page whitespace/other figures, do not change the chart axes/labels/content.
Each quoted figure is accompanied by source attribution and critical commentary.
"""
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen
import fitz

URL="https://www.boj.or.jp/about/press/koen_2026/data/ko260527a1.pdf"
ROOT=Path(__file__).resolve().parents[2]
IMAGES=ROOT/"images"
IMAGES.mkdir(exist_ok=True)
# PDF zero-based pages: 7 lower=fig2; 8 upper=fig3, lower=fig4; 9 upper=fig5.
# normalized clip: left, top, right, bottom; includes original panel title/legend/note
CHARTS={
    2:(7,(.04,.505,.95,.998)),
    3:(8,(.04,.01,.95,.50)),
    4:(8,(.04,.505,.95,.998)),
    5:(9,(.04,.01,.95,.50)),
}
with tempfile.TemporaryDirectory() as temp:
    target=Path(temp)/"official.pdf"
    request=Request(URL,headers={"User-Agent":"Mozilla/5.0 economic education charts"})
    with urlopen(request,timeout=60) as response:
        target.write_bytes(response.read())
    pdf=fitz.open(target)
    assert len(pdf)==10, f"BOJ PDF page count changed: {len(pdf)}"
    for number,(pageno,frac) in CHARTS.items():
        page=pdf[pageno]
        r=page.rect
        x0,y0,x1,y1=frac
        clip=fitz.Rect(r.x0+r.width*x0,r.y0+r.height*y0,
                       r.x0+r.width*x1,r.y0+r.height*y1)
        pix=page.get_pixmap(matrix=fitz.Matrix(2.6,2.6),clip=clip,alpha=False)
        image=IMAGES/f"boj-ueda-2026-chart-{number}-quoted.webp"
        # render via Pillow (format conversion only)
        from PIL import Image
        from io import BytesIO
        pic=Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")
        pic.save(image,"WEBP",quality=93,method=6)
        print(number, pageno+1, image.name, pic.size)
