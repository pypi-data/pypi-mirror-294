from fetchfox.constants.charles import (
    CHARLES_TOKEN_ASSET_ID,
    CHARLES_TOKEN_ASSET_NAME,
    CHARLES_TOKEN_POLICY_ID,
    CHARLES_TOKEN_FINGERPRINT,
    CHARLES_TOKEN_SYMBOL,
)

from .base import CardanoToken


class CharlesToken(CardanoToken):
    def __init__(self, dexhunterio_partner_code: str = None):
        super().__init__(
            asset_id=CHARLES_TOKEN_ASSET_ID,
            asset_name=CHARLES_TOKEN_ASSET_NAME,
            fingerprint=CHARLES_TOKEN_FINGERPRINT,
            policy_id=CHARLES_TOKEN_POLICY_ID,
            symbol=CHARLES_TOKEN_SYMBOL,
            decimals=0,
            dexhunterio_partner_code=dexhunterio_partner_code,
        )
