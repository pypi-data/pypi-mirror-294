import re
import sys
import typer
import simplesam

app = typer.Typer()

@app.command()
def main(infile: str):
  with simplesam.Reader(open(infile)) as in_bam:
    with simplesam.Writer(sys.stdout, in_bam.header) as out_sam:
      for read in in_bam:
        # Get header name and split by "_"
        header = read.qname.split("#")
        # Remove '?_' from first element of header
        umi = header[0].replace("?_", "")
        bc = header[1].replace("_", "")
        # Set new header and new tags
        new_header = umi + "_" + bc + "#" + header[2]
        # Set tags and new header
        read.tags['CB'] = bc
        read.tags['UR'] = umi
        read.qname = new_header

        # Write new reads to stdout
        out_sam.write(read)
