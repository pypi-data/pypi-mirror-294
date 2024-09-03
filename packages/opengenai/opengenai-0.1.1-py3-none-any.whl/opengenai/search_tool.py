from gixo_search import GoogleSearcher
from gixo_html_parser import FastHTMLParser, FastHTMLParserV2, FastHTMLParserV3
from gixo_embed_search import fast_embedding_search


class WebFetcher:
    @staticmethod
    async def google_fetch(query, top_k=3, fast_response=False):
        searcher = GoogleSearcher()
        res = searcher.search(query=query)
        parser = FastHTMLParserV3(urls=res.urls, fast_response=fast_response)
        contents = await parser.fetch_content()
        text_corpus: str = "\n".join(contents)
        results = fast_embedding_search(text_corpus, query, top_k=top_k)
        response_str = "\n".join([s for s, _ in results])
        return response_str
