from enum import auto
from strenum import StrEnum

class LogLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERR = auto()
    EXCEPTION = auto()
    SUCCESS = auto()
    FAILURE = auto()

class AssetClass(StrEnum):
    SHARE = auto()
    FUND = auto()
    INDEX = auto()
    EXCHANGE_RATE = auto()
    ZERO_COUPON_BOND = auto()
    DEPOSIT_RATE = auto()
    SWAP_RATE = auto()

class AssetKind(StrEnum):
    EQUITY = auto()
    FOREIGN_EXCHANGE = auto()
    INTEREST_RATE = auto()

class EventKind(StrEnum):
    BARRIER = auto()
    CHOICE = auto()
    FIXING = auto()
    NOTHING = auto()
    PAYMENT = auto()
    PURCHASE = auto()
    RECEIPT = auto()
    SALE = auto()
    SETTING = auto()

class ContractKind(StrEnum):
    CONSOLE = auto()
    FILE = auto()
    AIRGBAG_CERTIFICATE_EXAMPLE = auto()
    AMERICAN_OPTION_EXAMPLE = auto()
    ASIAN_OPTION_EXAMPLE = auto()
    BARRIER_OPTION_EXAMPLE = auto()
    BARRIER_REVERSE_CONVERTIBLE_EXAMPLE = auto()
    BONUS_CERTIFICATE_EXAMPLE = auto()
    BUTTERFLY_SPREAD_EXAMPLE = auto()
    CAPPED_BONUS_CERTIFICATE_EXAMPLE = auto()
    CONDOR_SPREAD_EXAMPLE = auto()
    DIGITAL_OPTION_EXAMPLE = auto()
    DISCOUNT_CERTIFICATE_EXAMPLE = auto()
    DOUBLE_BARRIER_OPTION_EXAMPLE = auto()
    EUROPEAN_OPTION_EXAMPLE = auto()
    MULTI_ASSET_OPTION_EXAMPLE = auto()
    OUT_PERFORMANCE_BONUS_CERTIFICATE_EXAMPLE = auto()
    REVERSE_CONVERTIBLE_EXAMPLE = auto()
    RISK_REVERSAL_EXAMPLE = auto()
    SPREAD_OPTION_EXAMPLE = auto()
    STRADDLE_EXAMPLE = auto()
    STRANGLE_EXAMPLE = auto()
    TWIN_WIN_CERTIFICATE_EXAMPLE = auto()
    AUTOCALL = auto()
    VANILLA = auto()

class BasketKind(StrEnum):
    BASKET = auto()
    BEST_OF = auto()
    RAINBOW = auto()
    WORST_OF = auto()

class StrikeKind(StrEnum):
    ASIAN = auto()
    LOOKBACK_MIN = auto()
    LOOKBACK_MAX = auto()

class BarrierKind(StrEnum):
    KNOCK_OUT = auto()
    KNOCK_IN = auto()