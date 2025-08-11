#!/usr/bin/env python3
# mosaico_batch.py
from pathlib import Path
from PIL import Image
import argparse
import sys

ROWS = COLS = 4                         # 4 × 4 grade → 16 pedaços

def split_image(img):
    """Divide a imagem em tiles linha‑major e devolve (lista_tiles, (tw, th))."""
    w, h = img.size
    tw, th = w // COLS, h // ROWS
    tiles = []
    for r in range(ROWS):
        for c in range(COLS):
            box = (c * tw, r * th, (c + 1) * tw, (r + 1) * th)
            tiles.append(img.crop(box))
    return tiles, (tw, th)

def recombine_transpose(tiles, tile_size):
    """Remonta aplicando transposição da grade."""
    tw, th = tile_size
    canvas = Image.new("RGB", (tw * COLS, th * ROWS))
    for r in range(ROWS):
        for c in range(COLS):
            src_idx = c * COLS + r      # (coluna, linha) → índice origem
            canvas.paste(tiles[src_idx], (c * tw, r * th))
    return canvas

def process_file(in_path: Path, out_path: Path):
    try:
        img = Image.open(in_path)
    except FileNotFoundError:
        print(f"[!] Arquivo não encontrado: {in_path.name}", file=sys.stderr)
        return
    tiles, tile_sz = split_image(img)
    result = recombine_transpose(tiles, tile_sz)
    result.save(out_path)

def main():
    p = argparse.ArgumentParser(
        description="Recombina em lote X páginas 4×4 já embaralhadas (1…X).")
    p.add_argument("folder", help="pasta contendo as páginas embaralhadas")
    p.add_argument("x", type=int, help="quantidade de páginas (X)")
    p.add_argument("--ext", default=".jpg", help="extensão dos arquivos (padrão: .jpg)")
    p.add_argument("--prefix", default="", help="prefixo do nome‑base na saída")
    p.add_argument("--outdir", default="saida", help="subpasta de saída (default: saida)")
    args = p.parse_args()

    base_dir = Path(args.folder).expanduser()
    if not base_dir.is_dir():
        sys.exit(f"Pasta não encontrada: {base_dir}")

    out_dir = base_dir / args.outdir
    out_dir.mkdir(exist_ok=True)

    print(f"Processando {args.x} arquivo(s) em: {base_dir}")
    for i in range(1, args.x + 1):
        fname = f"{i}{args.ext}"
        in_path = base_dir / fname
        out_name = f"{args.prefix}{i:02d}{args.ext}"
        out_path = out_dir / out_name
        process_file(in_path, out_path)
        print(f"  • {fname} → {out_name}")

    print(f"Concluído! Arquivos prontos em: {out_dir.resolve()}")

if __name__ == "__main__":
    main()
