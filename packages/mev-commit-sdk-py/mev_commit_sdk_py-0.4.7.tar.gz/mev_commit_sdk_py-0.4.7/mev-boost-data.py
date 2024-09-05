import marimo

__generated_with = "0.8.9"
app = marimo.App(width="medium")


@app.cell
def __():
    import polars as pl
    from mev_boost_py.proposer_payload import ProposerPayloadFetcher
    from mev_boost_py.proposer_payload import Network, Relay

    # expand polars df output
    pl.Config.set_fmt_str_lengths(200)
    pl.Config.set_fmt_float("full")
    return Network, ProposerPayloadFetcher, Relay, pl


@app.cell
def __(Network, ProposerPayloadFetcher):
    fetcher = ProposerPayloadFetcher(
        network=Network.HOLESKY,
        # relay=Relay.TITANRELAY
    )

    # Run the fetcher to fetch data
    df = fetcher.run()
    return df, fetcher


@app.cell
def __(df):
    df.head(5)
    return


@app.cell
def __(df):
    # get latest 300 block numbers
    block_numbers = (
        df.sort(by="block_number")["block_number"].unique().to_list()[-300:]
    )
    return block_numbers,


@app.cell
def __():
    # hypersync client to get blocks
    return


@app.cell
def __(pl):
    import asyncio
    import nest_asyncio
    from mev_commit_sdk_py.hypersync_client import Hypersync

    # expand polars df output
    pl.Config.set_fmt_str_lengths(200)
    pl.Config.set_fmt_float("full")

    nest_asyncio.apply()
    return Hypersync, asyncio, nest_asyncio


@app.cell
def __(Hypersync, asyncio, block_numbers):
    mev_commit: str = 'https://mev-commit.hypersync.xyz'
    holesky: str = 'https://holesky.hypersync.xyz'
    client = Hypersync(holesky)

    blocks_query_hc = asyncio.run(client.get_blocks(from_block=min(block_numbers), to_block=max(block_numbers)+1))

    return blocks_query_hc, client, holesky, mev_commit


@app.cell
def __(blocks_query_hc):
    blocks_query_hc
    return


@app.cell
def __():
    # use hypersync to fetch the block data.
    return


@app.cell
def __():
    # import nest_asyncio
    # import hypersync

    # from hypersync import (
    #     ColumnMapping,
    #     DataType,
    #     TransactionField,
    #     BlockField,
    #     BlockSelection,
    #     TransactionSelection,
    # )

    # nest_asyncio.apply()
    return


@app.cell
def __():
    # async def get_blocks():
    #     """
    #     Use hypersync to query blocks and transactions and write to a LanceDB table. Assumes existence of a previous LanceDB table to
    #     query for the latest block number to resume querying.
    #     """
    #     # hypersync client
    #     client = hypersync.HypersyncClient(
    #         hypersync.ClientConfig(url="http://holesky.hypersync.xyz")
    #     )
    #     query = hypersync.Query(
    #         # search block range by individual blocks
    #         from_block=min(block_numbers),
    #         to_block=max(block_numbers)+1,
    #         # include_all_blocks=True,
    #         # transactions=[TransactionSelection()],
    #         # blocks=[BlockSelection(hash=["0x136f19bae9fd98a31cbfee0ccc81b55306f447ba9b9691944ccead5f21fb08b0"])],
    #         blocks=[BlockSelection()],
    #         field_selection=hypersync.FieldSelection(
    #             block=[e.value for e in BlockField],
    #         ),
    #     )

    #     config = hypersync.StreamConfig(
    #         hex_output=hypersync.HexOutput.PREFIXED,
    #         column_mapping=ColumnMapping(
    #             block={
    #                 BlockField.GAS_LIMIT: DataType.FLOAT64,
    #                 BlockField.GAS_USED: DataType.FLOAT64,
    #                 BlockField.SIZE: DataType.FLOAT64,
    #                 BlockField.BLOB_GAS_USED: DataType.FLOAT64,
    #                 BlockField.EXCESS_BLOB_GAS: DataType.FLOAT64,
    #                 BlockField.BASE_FEE_PER_GAS: DataType.FLOAT64,
    #                 BlockField.TIMESTAMP: DataType.INT64,
    #             }
    #         ),
    #     )

    #     return await client.collect_arrow(query, config)


    # block_query = asyncio.run(get_blocks())

    # block_query_df = pl.from_arrow(block_query.data.blocks)
    return


@app.cell
def __(block_query_df):
    block_query_df
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
