"""Adapter pattern.

Reference: https://refactoring.guru/design-patterns/adapter

Also known as: Wrapper

Intent
------
Allow objects with incompatible interfaces to collaborate by wrapping one of
them in an adapter that translates calls at runtime.

Example
-------
A stock-market app fetches data from a feed and receives it as raw XML.
A third-party analytics library only accepts data as JSON — its interface
cannot be changed. An XmlToJsonAdapter wraps the XML feed and converts the
data on the fly so the analytics library can consume it without modification.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET


# --- Our existing data source (produces XML) ---------------------------------

class StockXmlFeed:
    """Simulates a market data feed that returns stock prices as XML."""

    def get_xml(self) -> str:
        return (
            "<stocks>"
            "  <stock ticker='AAPL' price='189.50' change='+1.2'/>"
            "  <stock ticker='GOOG' price='175.30' change='-0.5'/>"
            "  <stock ticker='MSFT' price='420.10' change='+2.8'/>"
            "</stocks>"
        )


# --- Third-party analytics library (expects JSON) ----------------------------
# Imagine this is an external library we cannot modify.

class AnalyticsLibrary:
    """Third-party analytics library. Only understands JSON input."""

    def analyse(self, json_data: str) -> None:
        records = json.loads(json_data)
        print("Analytics report:")
        for record in records:
            direction = "▲" if float(record["change"]) >= 0 else "▼"
            print(
                f"  {record['ticker']:6s}  ${float(record['price']):.2f}"
                f"  {direction} {record['change']}"
            )


# --- Adapter -----------------------------------------------------------------
# Implements the interface the analytics library expects (accepts_json_data)
# while internally fetching XML from the feed and converting it to JSON.

class XmlToJsonAdapter:
    """Adapts StockXmlFeed (XML) to the interface expected by AnalyticsLibrary (JSON)."""

    def __init__(self, xml_feed: StockXmlFeed) -> None:
        self._feed = xml_feed

    def get_json(self) -> str:
        """Fetch XML from the feed and convert it to a JSON string."""
        raw_xml = self._feed.get_xml()
        root = ET.fromstring(raw_xml)
        records = [
            {
                "ticker": stock.attrib["ticker"],
                "price": stock.attrib["price"],
                "change": stock.attrib["change"],
            }
            for stock in root.findall("stock")
        ]
        return json.dumps(records, indent=2)


# --- Client code -------------------------------------------------------------
# Works only with the analytics library interface. The XML feed detail is
# hidden behind the adapter — client code never sees XML at all.

def client_code(adapter: XmlToJsonAdapter, library: AnalyticsLibrary) -> None:
    json_data = adapter.get_json()
    library.analyse(json_data)


if __name__ == "__main__":
    feed = StockXmlFeed()
    library = AnalyticsLibrary()

    print("Without adapter — raw XML (library cannot consume this):")
    print(feed.get_xml())

    print("\nWith adapter — XML converted to JSON transparently:")
    adapter = XmlToJsonAdapter(feed)
    client_code(adapter, library)
