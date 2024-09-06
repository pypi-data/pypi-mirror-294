from .fast_api_client import AuthenticatedClient
from .fast_api_client.models import Document, DocumentMetadata, Source, UpsertRequest, UpsertResponse
from .fast_api_client.api.default import upsert_upsert_post
from paper2vec.abc import RetrieverDestination, Content
from argparse import ArgumentParser
import dbm
import os
import hashlib


def compute_hash(content):
    text = content.text.encode("utf8")
    return (f"MD5:{hashlib.md5(text).hexdigest()}|"
            f"SHA1:{hashlib.sha1(text).hexdigest()}|"
            f"SHA256:{hashlib.sha256(text).hexdigest()}|"
            f"HEAD:{content.text[:256]}|")


class ChatGPTRetrievalPlugin(RetrieverDestination):
    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument("--base_url", type=str, required=True, help="URL to your ChatGPT Plugin instance.")
        parser.add_argument("--token", type=str, required=True, help="Bearer of your ChatGPT Plugin.")
        parser.add_argument("--cache", type=str, default="chatgptplugin_cache", help="Your cache file for existing contents.")

    def __init__(self, args):
        self.base_url = args.base_url
        self.token = args.token
        self.cache = args.cache
        if os.path.dirname(args.cache):
            os.makedirs(os.path.dirname(args.cache), exist_ok=True)
        with dbm.open(self.cache, 'c'):
            pass

    async def get_cache(self, sentences):
        with dbm.open(self.cache, 'r') as db:
            return [True if compute_hash(content) in db else False for content in sentences]

    async def put_cache(self, sentences):
        with dbm.open(self.cache, 'w') as db:
            for sentence in sentences:
                db[compute_hash(sentence)] = ""

    async def upsert(self, *contents: Content) -> None:
        ok_cache = await self.get_cache(contents)
        if not False in ok_cache:
            print("Skip", len(ok_cache), "Documents")
            return
        async with AuthenticatedClient(base_url=self.base_url, token=self.token) as client:
            for content in contents:
                if "source" in content.metadata:
                    content.metadata["source"] = Source(content.metadata["source"])
            response: UpsertResponse = await upsert_upsert_post.asyncio(
                client=client,
                body=UpsertRequest([
                    Document(id=content.id, text=content.text, metadata=DocumentMetadata(**content.metadata))
                    for content, ok in zip(contents, ok_cache) if not ok
                ])
            )
            print("Done", f"{len(response.ids)}/{len(ok_cache)}", "Documents", "Skip", f"{len(ok_cache) - len(response.ids)}/{len(ok_cache)}")
            await self.put_cache(contents)
