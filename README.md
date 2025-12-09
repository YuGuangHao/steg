# steg

A simple tool that generates stegged pictures that can be analysed by StegSolve.jar.

## Usage

`python .\steg.py --help`

## Examples

`python .\steg.py -i 0.png -s test.7z --plane_order BGR`

`python .\steg.py -i 0.png -s test.7z --method column`

`python .\steg.py -i 0.png -s 1.png --qrcode --plane_order G`
