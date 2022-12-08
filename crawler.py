from icrawler.builtin import GoogleImageCrawler


def google_crawler_standart():
    crawler = GoogleImageCrawler(storage={"root_dir": "test"})
    crawler.crawl(keyword="Chainsaw Man", max_num=10)


def google_crawler_ext():
    filters = dict(
        size="large",
        color="orange",
        license="noncommercial,modify",
        date=((2020, 1, 1), (2022, 11, 30)),
    )
    crawler = GoogleImageCrawler(storage={"root_dir": "test"})
    crawler.crawl(
        keyword="Maine coon",
        max_num=15,
        min_size=(1000, 1000),
        overwrite=True,
        filters=filters,
        file_idx_offset="auto",
    )


google_crawler_ext()
