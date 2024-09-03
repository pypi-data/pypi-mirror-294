import marimo

__generated_with = "0.8.7"
app = marimo.App(width="medium")


@app.cell
def __():
    import polars as pl
    return pl,


@app.cell
def __(pl):
    df = pl.read_json("block_payloads.json").drop_nulls()
    return df,


@app.cell
def __(df):
    df.head(5)
    return


@app.cell
def __(df, pl):
    df.group_by('builder_pubkey').agg(pl.len().alias('count')).sort(by='count', descending=True)
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
