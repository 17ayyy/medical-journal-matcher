"""Interfaces for versioned external data-source adapters."""

from .base import ArticleSearchAdapter, JcrAdapter, JournalFactAdapter

__all__ = ["ArticleSearchAdapter", "JcrAdapter", "JournalFactAdapter"]
