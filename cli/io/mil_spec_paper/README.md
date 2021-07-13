# Production Figures

Following are notes for production-ready figures.

## Acceleration

```bash
> cd ~/sibl/cli/io/mil_spec_paper
> vim h1-master-acc.json  # edit as necessary
> cd ~/sibl
> conda activate siblenv
> python cli/src/xyfigure/client.py cli/io/mil_spec_paper/h1-master-acc.json
# print to .pdf format at 600 dpi, .png and .tiff formats as well
```

## Strain and Strain Rate Point Cloud
