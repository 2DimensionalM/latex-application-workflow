# Ensure LaTeX tools resolve shared files under src/ when compiling from repo root
ensure_path('TEXINPUTS', './src//');
$pdf_mode = 1;
$pdflatex = 'pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error %O %S';
