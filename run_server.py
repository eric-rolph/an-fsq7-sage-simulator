#!/usr/bin/env python3
"""
Custom server runner to work around Windows hot-reload issues.
"""
import asyncio
import sys
from reflex import constants
from reflex.utils import exec as reflex_exec

async def main():
    """Run the backend server."""
    print("Starting backend server...")
    await reflex_exec.run_backend(
        host="0.0.0.0",
        port=8000,
        loglevel=constants.LogLevel.INFO
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
