meta:
  id: strf_spectrum
  file-extension: bin
  endian: le
seq:
  - id: spectra
    type: spectrum
    repeat: expr
    repeat-expr: 60
types:
  spectrum:
    seq:
      - id: header
        type: str
        size: 256
        encoding: ascii
      - id: data
        type: f4
        repeat: expr
        repeat-expr: 400
