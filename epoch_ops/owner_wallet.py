"""Only the owning sanshos1 wallet may sign for this project."""
import re
from pathlib import Path
from genlayer_py import create_account
EXPECTED_WALLET = '0xad049e0edc298c97552ed60071a35bfc60181fd4'
def owner_account():
    env_path = Path(__file__).resolve().parents[5] / 'accounts.env'
    secret = None
    with env_path.open(encoding='utf-8') as stream:
        for line in stream:
            match = re.match(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*["\x27]?([^"\x27\r\n]+)', line)
            if match:
                secret = match.group(1).strip()
                break
    if not secret:
        raise RuntimeError('Owner wallet configuration missing')
    account = create_account(account_private_key=secret)
    if account.address.lower() != EXPECTED_WALLET:
        raise RuntimeError('Owner wallet mismatch; signing blocked')
    return account
