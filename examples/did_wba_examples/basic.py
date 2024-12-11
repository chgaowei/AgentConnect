# AgentConnect: https://github.com/chgaowei/AgentConnect
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: https://agent-network-protocol.com/
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.

# This is a basic example of how to use DID WBA authentication.
# It first creates a DID document and private keys.
# Then it uploads the DID document to the server.
# Then it generates an authentication header and tests the DID authentication.

import os
import sys
import json
import secrets
import asyncio
import aiohttp
import logging
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from canonicaljson import encode_canonical_json

from agent_connect.authentication.did_wba import (
    create_did_wba_document,
    resolve_did_wba_document,
    generate_auth_header
)
from agent_connect.utils.log_base import set_log_color_level

_is_local_testing = False

# TODO: Change to your own server domain. 
# Or use the test domain we provide (currently using pi-unlimited.com, will later change to agent-network-protocol.com)
# SERVER_DOMAIN = "agent-network-protocol.com"
SERVER_DOMAIN = "pi-unlimited.com"

def convert_url_for_local_testing(url: str) -> str:
    if _is_local_testing:
        url = url.replace('https://', 'http://')
        url = url.replace(SERVER_DOMAIN, '127.0.0.1:9000')
    return url

async def upload_did_document(url: str, did_document: dict) -> bool:
    """Upload DID document to server"""
    try:
        local_url = convert_url_for_local_testing(url)
        logging.info("Converting URL from %s to %s", url, local_url)
        
        async with aiohttp.ClientSession() as session:
            async with session.put(
                local_url,
                json=did_document,
                headers={'Content-Type': 'application/json'}
            ) as response:
                return response.status == 200
    except Exception as e:
        logging.error("Failed to upload DID document: %s", e)
        return False

async def download_did_document(url: str) -> dict:
    """Download DID document from server"""
    try:
        local_url = convert_url_for_local_testing(url)
        logging.info("Converting URL from %s to %s", url, local_url)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(local_url) as response:
                if response.status == 200:
                    return await response.json()
                logging.warning("Failed to download DID document, status: %d", response.status)
                return None
    except Exception as e:
        logging.error("Failed to download DID document: %s", e)
        return None

async def test_did_auth(url: str, auth_header: str) -> tuple[bool, str]:
    """Test DID authentication and get token"""
    try:
        local_url = convert_url_for_local_testing(url)
        logging.info("Converting URL from %s to %s", url, local_url)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                local_url,
                headers={'Authorization': auth_header}
            ) as response:
                token = response.headers.get('Authorization', '')
                if token.startswith('Bearer '):
                    token = token[7:]  # Remove 'Bearer ' prefix
                return response.status == 200, token
    except Exception as e:
        logging.error("DID authentication test failed: %s", e)
        return False, ''

def save_private_key(unique_id: str, keys: dict, did_document: dict) -> str:
    """Save private keys and DID document to user directory and return the user directory path"""
    current_dir = Path(__file__).parent.absolute()
    user_dir = current_dir / "did_keys" / f"user_{unique_id}"
    # Create parent directories if they don't exist
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # Save private keys
    for method_fragment, (private_key_bytes, _) in keys.items():
        private_key_path = user_dir / f"{method_fragment}_private.pem"
        with open(private_key_path, 'wb') as f:
            f.write(private_key_bytes)
        logging.info("Saved private key '%s' to %s", method_fragment, private_key_path)
    
    # Save DID document
    did_path = user_dir / "did.json"
    with open(did_path, 'w', encoding='utf-8') as f:
        json.dump(did_document, f, indent=2)
    logging.info("Saved DID document to %s", did_path)
    
    return str(user_dir)

def load_private_key(private_key_dir: str, method_fragment: str) -> ec.EllipticCurvePrivateKey:
    """Load private key from file"""
    key_dir = Path(private_key_dir)
    key_path = key_dir / f"{method_fragment}_private.pem"
    
    logging.info("Loading private key from %s", key_path)
    with open(key_path, 'rb') as f:
        private_key_bytes = f.read()
    return serialization.load_pem_private_key(
        private_key_bytes,
        password=None
    )

def sign_callback(content: bytes, method_fragment: str) -> bytes:
    """Sign content using private key"""
    # Load private key using the global variable
    private_key = load_private_key(sign_callback.private_key_dir, method_fragment)
    
    # Sign the content
    signature = private_key.sign(
        content,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

async def main():
    # 1. Generate unique identifier (8 bytes = 16 hex characters)
    unique_id = secrets.token_hex(8)
    
    # 2. Set server information
    server_domain = SERVER_DOMAIN
    base_path = f"/wba/user/{unique_id}"
    did_path = f"{base_path}/did.json"
    
    # 3. Create DID document
    logging.info("Creating DID document...")
    did_document, keys = create_did_wba_document(
        hostname=server_domain,
        path_segments=["wba", "user", unique_id]
    )
    
    # 4. Save private keys, DID document and set path for sign_callback
    user_dir = save_private_key(unique_id, keys, did_document)
    sign_callback.private_key_dir = user_dir
    
    # 5. Upload DID document (This should be stored on your server)
    document_url = f"https://{server_domain}{did_path}"
    logging.info("Uploading DID document to %s", document_url)
    success = await upload_did_document(document_url, did_document)
    if not success:
        logging.error("Failed to upload DID document")
        return
    logging.info("DID document uploaded successfully")
    
    # 7. Generate authentication header
    logging.info("Generating authentication header...")
    auth_header = generate_auth_header(
        did_document,
        server_domain,
        sign_callback
    )
    
    # 8. Test DID authentication and get token
    test_url = f"https://{server_domain}/wba/test"
    logging.info("Testing DID authentication at %s", test_url)
    auth_success, token = await test_did_auth(test_url, auth_header)
    
    if not auth_success or not token:
        logging.error(f"DID authentication test failed. auth_success: {auth_success}, token: {token}")
        return
        
    logging.info("DID authentication test successful")

if __name__ == "__main__":
    set_log_color_level(logging.INFO)
    asyncio.run(main())






